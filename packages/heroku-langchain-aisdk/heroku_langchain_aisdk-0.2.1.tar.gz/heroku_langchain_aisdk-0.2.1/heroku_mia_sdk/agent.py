import httpx
import json
import os
import time # For retries
import asyncio
from dataclasses import asdict, is_dataclass # For converting dataclasses to dicts
from typing import (
    Any, List, Optional, Dict, AsyncIterator, Union, cast, Tuple
)

from langchain_core.callbacks.manager import (
    AsyncCallbackManagerForLLMRun,
    CallbackManagerForLLMRun,
)
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import (
    AIMessage,
    AIMessageChunk,
    BaseMessage,
    ToolCall, 
    ToolCallChunk,
    HumanMessage, # For _generate aggregation if needed
)
from langchain_core.outputs import ChatGeneration, ChatGenerationChunk, ChatResult
# from langchain_core.pydantic_v1 import Field # If needed

# SDK specific imports
from .common import (
    get_heroku_config_options,
    langchain_messages_to_heroku_messages,
    # Agent tools are HerokuAgentToolDefinition, not FunctionToolDefinition
    # We might need a specific converter or assume they are passed correctly.
    parse_heroku_sse,
    HerokuApiError,
    HerokuConfig,
    ParsedSSEEvent,
)
from .types import (
    HerokuMiaAgentConstructorFields,
    HerokuMiaAgentRuntimeOptions,
    HerokuAgentStreamRequest,
    HerokuAgentToolDefinition, # For tools in constructor
    # SSE Data Types
    HerokuAgentSSEData,
    HerokuAgentMessageDeltaEventData,
    HerokuAgentToolCallEventData,
    HerokuAgentToolCompletionEventData,
    HerokuAgentToolErrorEventData,
    HerokuAgentAgentErrorEventData,
    HerokuAgentStreamEndEventData,
    # Other supporting types if needed from types.py
    HerokuChatMessage,
)

DEFAULT_TIMEOUT = 60.0

class HerokuMiaAgent(BaseChatModel):
    model: str # Optional in constructor fields, but practically required.
    temperature: float = 1.0
    # max_tokens_per_request: Optional[int] = None # From HerokuMiaAgentConstructorFields
    stop: Optional[List[str]] = None
    top_p: float = 0.999
    tools: Optional[List[HerokuAgentToolDefinition]] = None # Agent-specific tool format

    heroku_api_key: Optional[str] = None
    heroku_api_url: Optional[str] = None
    
    max_retries: int = 2 # For initial connection attempts, stream itself is long-lived
    timeout: float = DEFAULT_TIMEOUT # For individual read timeouts on the stream, or initial connect
    additional_kwargs: Dict[str, Any] = {}

    # stream_usage: bool = True # Langchain internal to indicate _stream should be used by default by .invoke()
    # This is typically set in Pydantic model config or by BaseChatModel if it sees _stream
    max_tokens_per_request: Optional[int] = None # Added this line based on prompt's __init__

    def __init__(self, **kwargs: Any):
        # Similar to HerokuMia, using HerokuMiaAgentConstructorFields
        _constructor_fields = HerokuMiaAgentConstructorFields(**kwargs)
        
        # Ensure all fields from _constructor_fields are passed to super or handled
        # BaseChatModel uses Pydantic. Declare fields at class level for Pydantic to pick them up.
        super().__init__(
            model=_constructor_fields.model,
            temperature=_constructor_fields.temperature,
            # max_tokens_per_request=_constructor_fields.max_tokens_per_request, # Not a BaseChatModel field
            stop=_constructor_fields.stop,
            top_p=_constructor_fields.top_p,
            tools=_constructor_fields.tools,
            heroku_api_key=_constructor_fields.heroku_api_key,
            heroku_api_url=_constructor_fields.heroku_api_url,
            max_retries=_constructor_fields.max_retries,
            timeout=_constructor_fields.timeout,
            additional_kwargs=_constructor_fields.additional_kwargs,
            **kwargs # Pass all kwargs
        )
        if not self.model: # model is optional in constructor fields, but should be checked
            # Based on JS, model can be optional for agent, so no error if None/empty
            pass
        
        # Store fields not in BaseChatModel if any, e.g. max_tokens_per_request
        # If declared at class level, Pydantic handles this.
        self.max_tokens_per_request = _constructor_fields.max_tokens_per_request


    @property
    def _llm_type(self) -> str:
        return "heroku-mia-agent"

    @property # Overriding this from BaseChatModel to signal that this model prefers streaming
    def _should_use_stream(self) -> bool:
        return True

    def _get_config(self) -> HerokuConfig:
        # Agent endpoint might be different, e.g., "/v1/agents/heroku"
        return get_heroku_config_options(
            self.heroku_api_key, self.heroku_api_url, "/v1/agents/heroku" # Verify endpoint
        )

    def _invocation_params( # Name changed from prompt's invocation_params to match BaseChatModel if needed
        self, stop_sequences: Optional[List[str]] = None, runtime_options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        # Based on HerokuAgentStreamRequest and HerokuMiaAgentRuntimeOptions
        params: Dict[str, Any] = {
            "model": self.model, # Must be present
            "temperature": self.temperature,
            "max_tokens_per_inference_request": self.max_tokens_per_request,
            "top_p": self.top_p,
            "tools": self.tools, # Tools from constructor
            **(self.additional_kwargs or {}),
        }

        _runtime_opts_obj = HerokuMiaAgentRuntimeOptions(**(runtime_options or {}))

        # Override with runtime options if provided
        if _runtime_opts_obj.metadata is not None:
            params["metadata"] = _runtime_opts_obj.metadata
        if _runtime_opts_obj.session_id is not None:
            params["session_id"] = _runtime_opts_obj.session_id
        
        effective_stop = stop_sequences or self.stop # Runtime stop from LLM call, then constructor
        if effective_stop is not None:
            params["stop"] = effective_stop
        
        if _runtime_opts_obj.additional_kwargs:
            params.update(_runtime_opts_obj.additional_kwargs)
            
        # Tools can also be passed at runtime, potentially overriding constructor tools
        # This part is not explicitly in HerokuMiaAgentRuntimeOptions, but could be in additional_kwargs
        # For now, assume tools are primarily set at construction for agents.

        return {k: v for k, v in params.items() if v is not None}

    async def _stream(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None, # stop is passed to _invocation_params
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
        **kwargs: Any, # For runtime options like metadata, session_id
    ) -> AsyncIterator[ChatGenerationChunk]:
        
        all_params = self._invocation_params(stop_sequences=stop, runtime_options=kwargs) # Use runtime_options=kwargs
        heroku_api_messages = langchain_messages_to_heroku_messages(messages)

        request_payload_dict = {
            "messages": [msg.dict(exclude_none=True) for msg in heroku_api_messages], # if HerokuChatMessage is pydantic
            **all_params
        }
        # Ensure messages are dicts (if not pydantic)
        request_payload_dict["messages"] = [
             {k:v for k,v in msg.__dict__.items() if v is not None} for msg in heroku_api_messages
        ]
        # Agent tools might be structured differently if they are not just functions.
        # HerokuAgentToolDefinition is used.
        if "tools" in request_payload_dict and request_payload_dict["tools"]:
             request_payload_dict["tools"] = [
                 tool_def.dict(exclude_none=True) if hasattr(tool_def, 'dict') else tool_def.__dict__
                 for tool_def in request_payload_dict["tools"]
            ]


        api_config = self._get_config()

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            async with client.stream(
                "POST",
                api_config.api_url, # Should point to the agent streaming endpoint
                headers={
                    "Authorization": f"Bearer {api_config.api_key}",
                    "Content-Type": "application/json",
                    "Accept": "text/event-stream",
                },
                json=request_payload_dict,
            ) as response:
                if response.status_code != 200:
                    error_content = await response.aread()
                    try:
                        error_data = json.loads(error_content.decode())
                    except json.JSONDecodeError:
                        error_data = error_content.decode()
                    raise HerokuApiError(
                        f"Heroku Agent API stream request failed with status {response.status_code}",
                        status_code=response.status_code,
                        error_payload=error_data
                    )
                
                # Tool call chunk aggregation logic might be needed if args are streamed piece by piece
                # For now, assume ToolCallChunk from AIMessageChunk handles this if we provide full arg strings.
                
                async for event in parse_heroku_sse(response.aiter_bytes()):
                    if not event.data or event.data == "[DONE]": # Standard DONE signal
                        if run_manager: run_manager.on_llm_end(response) # Pass raw response or aggregated info
                        break

                    # The 'event' field from SSE determines how to parse 'data'
                    # Heroku Agent SSE spec has event names like 'message.delta', 'tool.call', etc.
                    # These names are used to structure additional_kwargs or content.
                    
                    try:
                        event_data_json = json.loads(event.data)
                        # Determine event type based on Heroku's spec (e.g. a field in event_data_json or event.event)
                        # The JS SDK uses event_data_json.object or event.event.
                        # Let's assume event.event is the primary distinguisher from our SSE parser.
                        
                        heroku_event_type = event.event # From ParsedSSEEvent
                        # Or, if Heroku nests type info: heroku_event_type = event_data_json.get("object") or event.event

                        content_chunk_str: Optional[str] = None
                        tool_call_chunks_list: Optional[List[ToolCallChunk]] = None
                        additional_event_kwargs: Dict[str, Any] = {"heroku_agent_event_type": heroku_event_type, "raw_event_data": event_data_json}
                        finish_reason: Optional[str] = None

                        if heroku_event_type == "message.delta":
                            # data should be HerokuAgentMessageDeltaEventData
                            delta_data = HerokuAgentMessageDeltaEventData(**event_data_json)
                            content_chunk_str = delta_data.delta
                            if run_manager: run_manager.on_llm_new_token(content_chunk_str)
                        
                        elif heroku_event_type == "tool.call":
                            # data should be HerokuAgentToolCallEventData
                            tool_call_data = HerokuAgentToolCallEventData(**event_data_json)
                            tool_call_chunks_list = [
                                ToolCallChunk(
                                    name=tool_call_data.name,
                                    args=tool_call_data.input, # Input is JSON string of args
                                    id=tool_call_data.id,
                                    # index might be needed if multiple tool calls can be streamed with same ID but diff parts
                                )
                            ]
                            additional_event_kwargs.update(tool_call_data.__dict__)
                            finish_reason = "tool_calls" # A tool call implies the LLM part of turn might be done

                        elif heroku_event_type == "tool.completion":
                            # data should be HerokuAgentToolCompletionEventData
                            # This event usually comes from the *client* to the server.
                            # If the server echoes it or sends a related event, handle here.
                            # For now, just pass it through additional_kwargs.
                            completion_data = HerokuAgentToolCompletionEventData(**event_data_json)
                            additional_event_kwargs.update(completion_data.__dict__)
                            # This might not directly yield an AIMessageChunk, or it's metadata for a later message.

                        elif heroku_event_type == "tool.error":
                            tool_error_data = HerokuAgentToolErrorEventData(**event_data_json)
                            additional_event_kwargs.update(tool_error_data.__dict__)
                            # This could be a separate error signal or part of a message.
                            if run_manager: run_manager.on_llm_error(HerokuApiError("Tool error in agent stream", error_payload=tool_error_data))
                        
                        elif heroku_event_type == "agent.error":
                            agent_error_data = HerokuAgentAgentErrorEventData(**event_data_json)
                            additional_event_kwargs.update(agent_error_data.__dict__)
                            if run_manager: run_manager.on_llm_error(HerokuApiError("Agent error in stream", error_payload=agent_error_data))
                            # This might be a terminal error for the stream.
                            raise HerokuApiError("Agent error in stream", error_payload=agent_error_data)

                        elif heroku_event_type == "stream.end": # Or "done" if that's what Heroku sends
                            # data could be HerokuAgentStreamEndEventData
                            end_data = HerokuAgentStreamEndEventData(**event_data_json)
                            additional_event_kwargs.update(end_data.__dict__)
                            if end_data.final_message and end_data.final_message.content:
                                content_chunk_str = end_data.final_message.content # if final message has content
                            finish_reason = "stop" # Stream ended
                            if run_manager: run_manager.on_llm_end(response) # Or pass specific end data
                            break # End stream processing

                        else: # Unknown event type, or generic message event
                            # Fallback: if data field contains typical LLM delta (e.g. from a 'message' event)
                            if isinstance(event_data_json.get("choices"), list) and event_data_json["choices"]:
                                choice = event_data_json["choices"][0]
                                if "delta" in choice and "content" in choice["delta"]:
                                     content_chunk_str = choice["delta"]["content"]
                                     if run_manager: run_manager.on_llm_new_token(content_chunk_str or "")
                                if choice.get("finish_reason"):
                                    finish_reason = choice.get("finish_reason")


                        # Yield a chunk, even if it's just metadata from an event
                        chunk_msg = AIMessageChunk(
                            content=content_chunk_str or "",
                            tool_call_chunks=tool_call_chunks_list if tool_call_chunks_list else None,
                            additional_kwargs=additional_event_kwargs,
                        )
                        yield ChatGenerationChunk(message=chunk_msg, generation_info={"finish_reason": finish_reason} if finish_reason else None)
                        
                        if finish_reason == "stop": # If explicitly stopped by an event
                            if run_manager: run_manager.on_llm_end(response)
                            break


                    except json.JSONDecodeError:
                        if run_manager: run_manager.on_llm_error(HerokuApiError("Failed to parse agent SSE JSON", error_payload=event.data))
                        # Decide whether to continue or raise based on severity
                        continue 
                    except Exception as e:
                        if run_manager: run_manager.on_llm_error(e)
                        raise e

    async def _agenerate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        # This is the primary async entry point used by .ainvoke()
        # It should aggregate from _stream()
        
        final_content = []
        aggregated_tool_call_chunks: List[ToolCallChunk] = []
        generation_info_agg: Dict[str, Any] = {}

        async for chunk in self._stream(messages, stop, run_manager, **kwargs):
            final_content.append(chunk.message.content)
            if chunk.message.tool_call_chunks:
                aggregated_tool_call_chunks.extend(chunk.message.tool_call_chunks)
            if chunk.generation_info:
                generation_info_agg.update(chunk.generation_info)
        
        # Consolidate tool_call_chunks into full ToolCall objects
        # LangChain AIMessage can do this if tool_call_chunks are passed to its constructor.
        final_ai_message = AIMessage(
            content="".join(final_content),
            tool_call_chunks=aggregated_tool_call_chunks if aggregated_tool_call_chunks else None,
            # additional_kwargs could be aggregated too, if needed
        )

        return ChatResult(
            generations=[ChatGeneration(message=final_ai_message, generation_info=generation_info_agg or None)],
            # llm_output can be populated if agent provides usage at the end, etc.
        )

    # _generate is the sync version, used by .invoke()
    # BaseChatModel will typically call _agenerate if _generate is not overridden
    # or if _generate calls an async helper.
    # For an async-native model like this agent, it's common for _generate to be a sync wrapper around _agenerate.
    # However, the prompt asks to implement _generate by calling _stream and aggregating.
    # This means _stream needs to be callable synchronously or _generate needs an event loop.
    # The JS SDK did this by making _generate effectively async and then having a sync wrapper if needed.
    # For LangChain Python, if _agenerate is defined, .invoke() can use it via an event loop.
    # Let's stick to the plan: _generate calls _stream and aggregates. This is tricky if _stream is async.
    # A simpler _generate for an async-preferred model:
    # raise NotImplementedError("Sync generation not directly supported for this streaming-first agent. Use .ainvoke() or .astream().")
    # Or, use an async_to_sync helper if required.
    # The prompt asked for _generate to call _stream and aggregate:

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        # This is a simplified synchronous wrapper.
        # In a real LangChain model, you'd use `arun_in_main_thread(self._agenerate(...))`
        # or BaseChatModel might handle this if only _agenerate is provided.
        # For now, directly implementing the aggregation from _stream (which is async).
        # This requires _stream to be callable from sync code, or this needs to run an event loop.
        
        # Let's assume BaseChatModel handles the async->sync if _agenerate is present and preferred.
        # If we must implement _generate by calling _stream:
        # This is a conceptual representation; actual sync aggregation of async stream is complex.
        
        # Re-evaluating: The prompt for _generate says "call self._stream() and aggregate".
        # This implies _stream might need to be adaptable or we run an ad-hoc loop.
        # Given _stream is async, _generate cannot directly iterate it without an event loop.

        # Simplest compliant approach: If BaseChatModel doesn't auto-wrap _agenerate for .invoke(),
        # then this sync _generate needs to manage an event loop.
        # Or, we acknowledge that the JS pattern of _generate calling _stream and aggregating
        # translates to Python's _agenerate, and _generate might be unsupported or an async-to-sync wrapper.

        # Forcing _generate to work by running _agenerate (if no better sync path):
        import asyncio
        try:
            loop = asyncio.get_event_loop() # Changed from get_event_loop_policy().get_event_loop()
            if loop.is_running():
                # This is a more complex case, e.g. already in Jupyter aysnc event loop
                # For simplicity, we won't handle this nested loop case here.
                # In such env, ainvoke should be used.
                raise NotImplementedError("Sync .generate() cannot be reliably called from a running asyncio event loop. Use .ainvoke() instead.")
            return loop.run_until_complete(self._agenerate(messages, stop, cast(Optional[AsyncCallbackManagerForLLMRun], run_manager), **kwargs))
        except RuntimeError as e: 
            if "no current event loop" in str(e) or "Event loop is closed" in str(e):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                # Ensure the result is returned and the loop is managed correctly
                try:
                    result = loop.run_until_complete(self._agenerate(messages, stop, cast(Optional[AsyncCallbackManagerForLLMRun], run_manager), **kwargs))
                finally:
                    asyncio.set_event_loop(None) # Reset the event loop for the current thread
                    loop.close()
                return result
            else:
                raise e
