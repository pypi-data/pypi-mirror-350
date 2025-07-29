import json
import logging
import os
import pickle
import uuid
from contextlib import suppress
from typing import Any, Optional

from llama_index.core.workflow import (
    Context,
    HumanResponseEvent,
    InputRequiredEvent,
    JsonPickleSerializer,
)
from llama_index.core.workflow.handler import WorkflowHandler
from openinference.instrumentation.llama_index import LlamaIndexInstrumentor
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from uipath import UiPath
from uipath._cli._runtime._contracts import (
    UiPathApiTrigger,
    UiPathBaseRuntime,
    UiPathErrorCategory,
    UiPathResumeTrigger,
    UiPathRuntimeResult,
    UiPathRuntimeStatus,
)

from .._tracing._oteladapter import LlamaIndexExporter
from ._context import UiPathLlamaIndexRuntimeContext
from ._exception import UiPathLlamaIndexRuntimeError

logger = logging.getLogger(__name__)


class UiPathLlamaIndexRuntime(UiPathBaseRuntime):
    """
    A runtime class for hosting UiPath LlamaIndex agents.
    """

    def __init__(self, context: UiPathLlamaIndexRuntimeContext):
        super().__init__(context)
        self.context: UiPathLlamaIndexRuntimeContext = context
        self._uipath = UiPath()

    async def execute(self) -> Optional[UiPathRuntimeResult]:
        """
        Start the LlamaIndex agent runtime.

        Returns:
            Dictionary with execution results

        Raises:
            UiPathLlamaIndexRuntimeError: If execution fails
        """
        await self.validate()

        self.trace_provider = TracerProvider()

        with suppress(Exception):
            trace.set_tracer_provider(self.trace_provider)
            self.trace_provider.add_span_processor(
                BatchSpanProcessor(LlamaIndexExporter())
            )  # type: ignore

            LlamaIndexInstrumentor().instrument(tracer_provider=self.trace_provider)

        try:
            start_event_class = self.context.workflow._start_event_class
            ev = start_event_class(**self.context.input_json)

            ctx: Context = await self._get_context()

            handler: WorkflowHandler = self.context.workflow.run(start_event=ev, ctx=ctx, **self.context.input_json)

            resume_trigger: UiPathResumeTrigger = None

            async for event in handler.stream_events():
                if isinstance(event, InputRequiredEvent):
                    resume_trigger = UiPathResumeTrigger(
                        api_resume=UiPathApiTrigger(
                            inbox_id=str(uuid.uuid4()), request=event.prefix
                        )
                    )
                    break
                print(event)

            if resume_trigger is None:
                output = await handler
                self.context.result = UiPathRuntimeResult(
                    output=self._serialize_object(output),
                    status=UiPathRuntimeStatus.SUCCESSFUL,
                )
            else:
                self.context.result = UiPathRuntimeResult(
                    output=self._serialize_object(output),
                    status=UiPathRuntimeStatus.SUSPENDED,
                    resume=resume_trigger,
                )

            if self.context.state_file:
                serializer = JsonPickleSerializer()
                ctx_dict = ctx.to_dict(serializer=serializer)
                ctx_dict["uipath_resume_trigger"] = (
                    serializer.serialize(resume_trigger) if resume_trigger else None
                )
                with open(self.context.state_file, "wb") as f:
                    pickle.dump(ctx_dict, f)

            return self.context.result

        except Exception as e:
            if isinstance(e, UiPathLlamaIndexRuntimeError):
                raise
            detail = f"Error: {str(e)}"
            raise UiPathLlamaIndexRuntimeError(
                "EXECUTION_ERROR",
                "LlamaIndex Runtime execution failed",
                detail,
                UiPathErrorCategory.USER,
            ) from e
        finally:
            self.trace_provider.shutdown()

    async def validate(self) -> None:
        """Validate runtime inputs and load Llama agent configuration."""
        try:
            if self.context.input:
                self.context.input_json = json.loads(self.context.input)
        except json.JSONDecodeError as e:
            raise UiPathLlamaIndexRuntimeError(
                "INPUT_INVALID_JSON",
                "Invalid JSON input",
                "The input data is not valid JSON.",
                UiPathErrorCategory.USER,
            ) from e

        if self.context.config is None:
            raise UiPathLlamaIndexRuntimeError(
                "CONFIG_MISSING",
                "Invalid configuration",
                "Failed to load configuration",
                UiPathErrorCategory.DEPLOYMENT,
            )

        try:
            self.context.config.load_config()
        except Exception as e:
            raise UiPathLlamaIndexRuntimeError(
                "CONFIG_INVALID",
                "Invalid configuration",
                f"Failed to load configuration: {str(e)}",
                UiPathErrorCategory.DEPLOYMENT,
            ) from e

        # Determine entrypoint if not provided
        workflows = self.context.config.workflows
        if not self.context.entrypoint and len(workflows) == 1:
            self.context.entrypoint = workflows[0].name
        elif not self.context.entrypoint:
            workflow_names = ", ".join(w.name for w in workflows)
            raise UiPathLlamaIndexRuntimeError(
                "ENTRYPOINT_MISSING",
                "Entrypoint required",
                f"Multiple workflows available. Please specify one of: {workflow_names}.",
                UiPathErrorCategory.DEPLOYMENT,
            )

        # Get the specified workflow configuration
        self.workflow_config = self.context.config.get_workflow(self.context.entrypoint)
        if not self.workflow_config:
            raise UiPathLlamaIndexRuntimeError(
                "WORKFLOW_NOT_FOUND",
                "Workflow not found",
                f"Workflow '{self.context.entrypoint}' not found.",
                UiPathErrorCategory.DEPLOYMENT,
            )
        try:
            self.context.workflow = await self.workflow_config.load_workflow()
        except ImportError as e:
            raise UiPathLlamaIndexRuntimeError(
                "WORKFLOW_IMPORT_ERROR",
                "Workflow import failed",
                f"Failed to import workflow '{self.context.entrypoint}': {str(e)}",
                UiPathErrorCategory.USER,
            ) from e
        except TypeError as e:
            raise UiPathLlamaIndexRuntimeError(
                "WORKFLOW_TYPE_ERROR",
                "Invalid workflow type",
                f"Workflow '{self.context.entrypoint}' is not a valid `Workflow`: {str(e)}",
                UiPathErrorCategory.USER,
            ) from e
        except ValueError as e:
            raise UiPathLlamaIndexRuntimeError(
                "WORKFLOW_VALUE_ERROR",
                "Invalid workflow value",
                f"Invalid value in workflow '{self.context.entrypoint}': {str(e)}",
                UiPathErrorCategory.USER,
            ) from e
        except Exception as e:
            raise UiPathLlamaIndexRuntimeError(
                "WORKFLOW_LOAD_ERROR",
                "Failed to load workflow",
                f"Unexpected error loading workflow '{self.context.entrypoint}': {str(e)}",
                UiPathErrorCategory.USER,
            ) from e

    async def cleanup(self) -> None:
        """Clean up all resources."""
        pass

    async def _get_context(self) -> Context:
        """
        Get the context for the LlamaIndex agent.

        Returns:
            The context object for the LlamaIndex agent.
        """
        logger.debug(f"Resumed: {self.context.resume} Input: {self.context.input_json}")

        if not self.context.resume:
            return Context(self.context.workflow)

        if not self.context.state_file or not os.path.exists(self.context.state_file):
            return Context(self.context.workflow)

        serializer = JsonPickleSerializer()
        ctx: Context = None

        with open(self.context.state_file, "rb") as f:
            loaded_ctx_dict = pickle.load(f)
            ctx = Context.from_dict(
                self.context.workflow,
                loaded_ctx_dict,
                serializer=serializer,
            )

        if self.context.input_json:
            ctx.send_event(HumanResponseEvent(response=self.context.input_json))

        resumed_trigger_data = loaded_ctx_dict["uipath_resume_trigger"]
        if resumed_trigger_data:
            resumed_trigger: UiPathResumeTrigger = serializer.deserialize(
                resumed_trigger_data, UiPathResumeTrigger
            )
            inbox_id = resumed_trigger.api_resume.inbox_id
            payload = await self._get_api_payload(inbox_id)
            ctx.send_event(HumanResponseEvent(response=payload))

        return ctx

    async def _get_api_payload(self, inbox_id: str) -> Any:
        """
        Fetch payload data for API triggers.

        Args:
            inbox_id: The Id of the inbox to fetch the payload for.

        Returns:
            The value field from the API response payload, or None if an error occurs.
        """
        try:
            response = self._uipath.api_client.request(
                "GET",
                f"/orchestrator_/api/JobTriggers/GetPayload/{inbox_id}",
                include_folder_headers=True,
            )
            data = response.json()
            return data.get("payload")
        except Exception as e:
            raise UiPathLlamaIndexRuntimeError(
                "API_CONNECTION_ERROR",
                "Failed to get trigger payload",
                f"Error fetching API trigger payload for inbox {inbox_id}: {str(e)}",
                UiPathErrorCategory.SYSTEM,
                response.status_code,
            ) from e

    def _serialize_object(self, obj):
        """Recursively serializes an object and all its nested components."""
        # Handle Pydantic models
        if hasattr(obj, "model_dump"):
            return self._serialize_object(obj.model_dump(by_alias=True))
        elif hasattr(obj, "dict"):
            return self._serialize_object(obj.dict())
        elif hasattr(obj, "to_dict"):
            return self._serialize_object(obj.to_dict())
        # Handle dictionaries
        elif isinstance(obj, dict):
            return {k: self._serialize_object(v) for k, v in obj.items()}
        # Handle lists
        elif isinstance(obj, list):
            return [self._serialize_object(item) for item in obj]
        # Handle other iterable objects (convert to dict first)
        elif hasattr(obj, "__iter__") and not isinstance(obj, (str, bytes)):
            try:
                return self._serialize_object(dict(obj))
            except (TypeError, ValueError):
                return obj
        # Return primitive types as is
        else:
            return obj
