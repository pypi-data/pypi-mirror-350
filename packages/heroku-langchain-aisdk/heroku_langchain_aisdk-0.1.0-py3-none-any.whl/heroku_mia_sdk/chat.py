import httpx
import json
import os
import time # For retries
from dataclasses import asdict # For converting dataclasses to dicts
from typing import (
    Any, List, Optional, Dict, Iterator, AsyncIterator, Union, cast, Tuple
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
    ToolCall, # LangChain's representation of a completed tool call
    ToolCallChunk, # LangChain's representation of a streaming tool call chunk
)
from langchain_core.outputs import ChatGeneration, ChatGenerationChunk, ChatResult
from langchain_core.tools import StructuredTool
from pydantic import Field

# SDK specific imports
from .common import (
    get_heroku_config_options,
    langchain_messages_to_heroku_messages,
    langchain_tools_to_heroku_tools,
    parse_heroku_sse,
    heroku_message_to_dict,
    HerokuApiError,
    HerokuConfig,
    ParsedSSEEvent,
)
from .types import (
    HerokuMiaConstructorFields,
    HerokuMiaRuntimeOptions,
    HerokuChatCompletionRequest,
    HerokuChatCompletionResponse,
    HerokuChatCompletionStreamResponse,
    HerokuChatMessage, # For constructing request message list
    HerokuToolCall as HerokuApiToolCall, # API version of ToolCall
    PartialHerokuToolCall, # For streaming tool call chunks
    PartialHerokuToolCallFunction,
    HerokuFunctionTool, # For defining tools in requests
    HerokuToolChoiceOption,
    # LocalToolCallChunk, # Langchain's ToolCallChunk should be sufficient
    # HerokuChatCompletionStreamChoiceDelta, # Not used in this version's _stream
    HerokuChatCompletionUsage,
    HerokuChatCompletionChoice,
)

# Default timeout for HTTP requests
DEFAULT_TIMEOUT = 60.0 # seconds


class HerokuMia(BaseChatModel):
    model: str
    temperature: float = 1.0
    max_tokens: Optional[int] = None
    stop: Optional[List[str]] = None
    streaming: bool = False # Default for invoke, stream() sets it true
    top_p: float = 0.999
    
    heroku_api_key: Optional[str] = None
    heroku_api_url: Optional[str] = None # Base URL, endpoint path added later
    
    max_retries: int = 2
    timeout: float = DEFAULT_TIMEOUT
    additional_kwargs: Dict[str, Any] = {} # Field(default_factory=dict) for pydantic

    # LangChain specific fields if needed, e.g. for binding tools
    # bound_tools: Optional[List[HerokuFunctionTool]] = None 
    # bound_tool_choice: Optional[Union[str, Dict]] = None


    def __init__(self, **kwargs: Any):
        # Initialize HerokuMiaConstructorFields from kwargs
        _constructor_fields = HerokuMiaConstructorFields(**kwargs)
        
        # Auto-detect model from environment variable if not provided (matching JS behavior)
        model_from_env = os.environ.get("INFERENCE_MODEL_ID")
        resolved_model = _constructor_fields.model or model_from_env or ""
        
        # Set default timeout if not provided (matching JS behavior)
        resolved_timeout = _constructor_fields.timeout or DEFAULT_TIMEOUT
        
        # Filter out parameters we're explicitly setting to avoid conflicts
        explicit_params = {
            'model', 'temperature', 'max_tokens', 'stop', 'streaming', 'top_p',
            'heroku_api_key', 'heroku_api_url', 'max_retries', 'timeout', 'additional_kwargs'
        }
        filtered_kwargs = {k: v for k, v in kwargs.items() if k not in explicit_params}
        
        super().__init__(
            model=resolved_model,
            temperature=_constructor_fields.temperature,
            max_tokens=_constructor_fields.max_tokens,
            stop=_constructor_fields.stop,
            streaming=_constructor_fields.streaming,
            top_p=_constructor_fields.top_p,
            heroku_api_key=_constructor_fields.heroku_api_key,
            heroku_api_url=_constructor_fields.heroku_api_url,
            max_retries=_constructor_fields.max_retries,
            timeout=resolved_timeout,
            additional_kwargs=_constructor_fields.additional_kwargs,
            **filtered_kwargs # Pass only remaining kwargs
        )
        
        # Validate that model is set (matching JS behavior)
        if not self.model:
            raise ValueError(
                "Heroku model ID not found. Please set it in the constructor, "
                "or set the INFERENCE_MODEL_ID environment variable."
            )


    @property
    def _llm_type(self) -> str:
        return "heroku-mia"

    def _get_config(self) -> HerokuConfig:
        return get_heroku_config_options(
            self.heroku_api_key, self.heroku_api_url, "/v1/chat/completions"
        )

    def _invocation_params( # Renamed from invocation_params to _invocation_params to match BaseChatModel
        self, stop_sequences: Optional[List[str]] = None, runtime_options: Optional[Dict[str, Any]] = None # runtime_options was HerokuMiaRuntimeOptions before
    ) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "stream": self.streaming, # Default, might be overridden for _stream
            **(self.additional_kwargs or {}),
        }
        
        # Runtime options from HerokuMiaRuntimeOptions (passed via **kwargs to _generate/_stream)
        # These can override constructor defaults.
        # LangChain's BaseChatModel passes `stop` and other kwargs.
        # `runtime_options` here is a conceptual merge of those kwargs that are specific to Heroku.

        _runtime_opts_obj = HerokuMiaRuntimeOptions(**(runtime_options or {}))

        if _runtime_opts_obj.temperature is not None:
            params["temperature"] = _runtime_opts_obj.temperature
        if _runtime_opts_obj.max_tokens is not None:
            params["max_tokens"] = _runtime_opts_obj.max_tokens
        if _runtime_opts_obj.top_p is not None:
            params["top_p"] = _runtime_opts_obj.top_p
        
        # Stop sequences: priority to method arg, then runtime_options, then constructor
        effective_stop = stop_sequences or _runtime_opts_obj.stop or self.stop
        if effective_stop is not None:
            params["stop"] = effective_stop

        if _runtime_opts_obj.tools: # These should be already in Heroku format
            params["tools"] = _runtime_opts_obj.tools
        
        if _runtime_opts_obj.tool_choice:
            tool_choice = _runtime_opts_obj.tool_choice
            if isinstance(tool_choice, str) and tool_choice not in ["none", "auto", "required"]:
                params["tool_choice"] = HerokuToolChoiceOption(type="function", function={"name": tool_choice})
            else:
                params["tool_choice"] = tool_choice
        
        if _runtime_opts_obj.additional_kwargs:
            params.update(_runtime_opts_obj.additional_kwargs)

        # Remove None values to keep payload clean, unless API expects them
        return {k: v for k, v in params.items() if v is not None}

    # bind_tools is complex with current BaseChatModel.
    # A common way is to use .bind(tools=[...], tool_choice=...) which returns a new Runnable.
    # This method is more about creating a new pre-configured instance.
    def bind_tools(self, tools: List[StructuredTool], tool_choice: Optional[Union[str, Dict[str, Any], HerokuToolChoiceOption]] = None) -> 'HerokuMia':
        """ Returns a new instance of HerokuMia with tools bound."""
        heroku_formatted_tools = langchain_tools_to_heroku_tools(tools)
        
        # Create a new dictionary of parameters for the new instance
        # Only include fields that are part of HerokuMiaConstructorFields
        new_kwargs = {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stop": self.stop,
            "streaming": self.streaming,
            "top_p": self.top_p,
            "heroku_api_key": self.heroku_api_key,
            "heroku_api_url": self.heroku_api_url,
            "max_retries": self.max_retries,
            "timeout": self.timeout,
            "additional_kwargs": (self.additional_kwargs or {}).copy(),
        }
        
        # Update additional_kwargs for the new instance to hold bound tools
        updated_additional_kwargs = new_kwargs["additional_kwargs"]
        updated_additional_kwargs["tools"] = heroku_formatted_tools
        if tool_choice:
            updated_additional_kwargs["tool_choice"] = tool_choice
        else: # Default tool_choice when tools are provided
            updated_additional_kwargs["tool_choice"] = "auto"

        new_kwargs["additional_kwargs"] = updated_additional_kwargs
        
        return self.__class__(**new_kwargs)


    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        
        # `kwargs` here will receive `tools`, `tool_choice` etc. if passed to `invoke`
        # These should be passed to `_invocation_params` via `runtime_options`
        # We need to ensure `streaming` is False for _generate
        self.streaming = False 
        
        all_params = self._invocation_params(stop_sequences=stop, runtime_options=kwargs) # Pass kwargs as runtime_options
        all_params["stream"] = False # Ensure stream is false for _generate

        heroku_messages = langchain_messages_to_heroku_messages(messages)
        
        # Construct payload ensuring correct types and structure
        # Model is part of all_params if not overridden, or from self.model
        # Messages are converted HerokuChatMessage
        # Tools should be list of HerokuFunctionTool dicts
        
        # Start with all_params which includes model, temp, etc.
        # Pop model as it's a top-level key in HerokuChatCompletionRequest
        # model_id = all_params.pop("model", self.model) # Ensure we have a model_id

        final_payload_dict = {
            "model": self.model, # Use model from instance, _invocation_params already includes it
            "messages": [heroku_message_to_dict(msg) for msg in heroku_messages], # Convert HerokuChatMessage to dict
            **all_params # Spread remaining validated params
        }
        # Remove stream from all_params before spreading as it's already set
        if "stream" in final_payload_dict: del final_payload_dict["stream"] 
        if "model" in all_params: del all_params["model"] # remove model from all_params to avoid duplicate key

        # Re-create final_payload_dict to ensure correct structure and order
        final_payload_dict = {
            "model": self.model,
            "messages": [heroku_message_to_dict(msg) for msg in heroku_messages],
            **all_params
        }
        
        # Convert tools if they are HerokuFunctionTool objects to dicts
        if "tools" in final_payload_dict and final_payload_dict["tools"]:
             final_payload_dict["tools"] = [
                 asdict(t, dict_factory=lambda x: {k: v for (k, v) in x if v is not None}) 
                 for t in final_payload_dict["tools"]
            ]
        if "tool_choice" in final_payload_dict and isinstance(final_payload_dict["tool_choice"], HerokuToolChoiceOption):
            final_payload_dict["tool_choice"] = asdict(final_payload_dict["tool_choice"], dict_factory=lambda x: {k: v for (k, v) in x if v is not None})


        api_config = self._get_config()
        
        response_json: Optional[Dict[str, Any]] = None
        last_error: Optional[Exception] = None

        with httpx.Client(timeout=self.timeout) as client:
            for attempt in range(self.max_retries + 1):
                try:
                    response = client.post(
                        api_config.api_url,
                        headers={
                            "Authorization": f"Bearer {api_config.api_key}",
                            "Content-Type": "application/json",
                        },
                        json=final_payload_dict,
                    )
                    response.raise_for_status() 
                    response_json = response.json()
                    break
                except httpx.TimeoutException as e:
                    last_error = e
                    if run_manager: 
                        run_manager.on_llm_error(e)
                    if attempt >= self.max_retries:
                        raise HerokuApiError(f"Request timed out after {self.max_retries + 1} attempts: {e}", error_payload=e) from e
                    time.sleep(1 * (attempt + 1)) 
                except httpx.HTTPStatusError as e:
                    last_error = e
                    if run_manager: 
                        run_manager.on_llm_error(e)
                    response_data = {}
                    try: 
                        response_data = e.response.json()
                    except: 
                        # If JSON parsing fails, try to get text response
                        try:
                            response_data = e.response.text
                        except:
                            response_data = {}
                    
                    # Handle both dict and string response_data
                    if isinstance(response_data, dict):
                        error_message = response_data.get("error", {}).get("message") or response_data.get("message") or str(e)
                    else:
                        error_message = str(response_data) if response_data else str(e)
                    
                    if e.response.status_code >= 400 and e.response.status_code < 500:
                         raise HerokuApiError(
                            f"Heroku API request failed with status {e.response.status_code}: {error_message}",
                            status_code=e.response.status_code, error_payload=response_data) from e
                    if attempt >= self.max_retries:
                        raise HerokuApiError(
                            f"Heroku API request failed after {self.max_retries + 1} attempts with status {e.response.status_code}: {error_message}",
                            status_code=e.response.status_code, error_payload=response_data) from e
                    time.sleep(1 * (attempt + 1))
                except Exception as e: 
                    last_error = e
                    if run_manager: 
                        run_manager.on_llm_error(e)
                    if attempt >= self.max_retries:
                        raise HerokuApiError(f"An unexpected error occurred after {self.max_retries + 1} attempts: {e}", error_payload=e) from e
                    time.sleep(1 * (attempt + 1))
            
        if response_json is None:
            raise HerokuApiError("Failed to get a response from Heroku API after all retries.", error_payload=last_error)

        # Manually convert nested dictionaries to dataclass objects
        from .types import HerokuChatCompletionUsage, HerokuChatCompletionChoice
        
        # Convert choices
        converted_choices = []
        for choice_dict in response_json.get("choices", []):
            message_dict = choice_dict.get("message", {})
            
            # Convert tool_calls if present
            tool_calls = None
            if message_dict.get("tool_calls"):
                from .types import HerokuToolCall, HerokuFunction
                tool_calls = []
                for tc_dict in message_dict["tool_calls"]:
                    function_dict = tc_dict.get("function", {})
                    tool_calls.append(HerokuToolCall(
                        id=tc_dict.get("id"),
                        type=tc_dict.get("type", "function"),
                        function=HerokuFunction(
                            name=function_dict.get("name"),
                            arguments=function_dict.get("arguments", "{}")
                        )
                    ))
            
            # Create HerokuChatMessage
            heroku_message = HerokuChatMessage(
                role=message_dict.get("role"),
                content=message_dict.get("content"),
                name=message_dict.get("name"),
                tool_calls=tool_calls,
                tool_call_id=message_dict.get("tool_call_id")
            )
            
            # Create HerokuChatCompletionChoice
            choice = HerokuChatCompletionChoice(
                index=choice_dict.get("index"),
                message=heroku_message,
                finish_reason=choice_dict.get("finish_reason")
            )
            converted_choices.append(choice)
        
        # Convert usage
        usage_dict = response_json.get("usage", {})
        usage = HerokuChatCompletionUsage(
            prompt_tokens=usage_dict.get("prompt_tokens", 0),
            completion_tokens=usage_dict.get("completion_tokens", 0),
            total_tokens=usage_dict.get("total_tokens", 0)
        )
        
        # Create the response object with converted nested objects
        heroku_response = HerokuChatCompletionResponse(
            id=response_json.get("id"),
            object=response_json.get("object"),
            created=response_json.get("created"),
            model=response_json.get("model"),
            choices=converted_choices,
            usage=usage,
            system_fingerprint=response_json.get("system_fingerprint")
        )
        
        generations: List[ChatGeneration] = []
        for choice in heroku_response.choices:
            message_data = choice.message 
            
            tool_calls_list: List[ToolCall] = []
            invalid_tool_calls_list: List[Any] = []

            if message_data.tool_calls:
                for api_tc in message_data.tool_calls:
                    try:
                        tool_args = json.loads(api_tc.function.arguments)
                        tool_calls_list.append(ToolCall(name=api_tc.function.name, args=tool_args, id=api_tc.id))
                    except json.JSONDecodeError:
                        invalid_tool_calls_list.append(ToolCall(name=api_tc.function.name, args=api_tc.function.arguments, id=api_tc.id, type="tool_call"))

            gen_message_content = ""
            if isinstance(message_data.content, str):
                gen_message_content = message_data.content
            elif message_data.content is None and message_data.tool_calls:
                 gen_message_content = ""


            gen_message = AIMessage(
                content=gen_message_content,
                tool_calls=tool_calls_list,
                invalid_tool_calls=invalid_tool_calls_list,
            )
            generation_info = {"finish_reason": choice.finish_reason, "index": choice.index}
            # Add raw message data if needed for debugging or extended info
            # generation_info["raw_choice_message"] = asdict(message_data) 
            generations.append(ChatGeneration(message=gen_message, generation_info=generation_info))
        
        llm_output = {"token_usage": asdict(heroku_response.usage) if heroku_response.usage else None, "model_name": self.model, "system_fingerprint": heroku_response.system_fingerprint}
        
        result = ChatResult(generations=generations, llm_output=llm_output)
        if run_manager:
            run_manager.on_llm_end(result)
        return result


    def _stream(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> Iterator[ChatGenerationChunk]:
        """Stream the output of the model synchronously."""
        # For sync streaming, we'll use the async method in a sync context
        import asyncio
        
        # Create a new event loop if one doesn't exist
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                raise RuntimeError("Event loop is closed")
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        # Convert async generator to sync generator
        async def _async_generator():
            async for chunk in self._astream(messages, stop, run_manager, **kwargs):
                yield chunk
        
        async_gen = _async_generator()
        
        try:
            while True:
                try:
                    chunk = loop.run_until_complete(async_gen.__anext__())
                    yield chunk
                except StopAsyncIteration:
                    break
        finally:
            loop.run_until_complete(async_gen.aclose())

    async def _astream(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> AsyncIterator[ChatGenerationChunk]:
        """Stream the output of the model asynchronously."""
        try:
            # Convert messages to the format expected by the API
            heroku_messages = langchain_messages_to_heroku_messages(messages)
            
            # Prepare the request payload
            payload = {
                "model": self.model,
                "messages": [heroku_message_to_dict(msg) for msg in heroku_messages],
                "stream": True,
                **kwargs
            }
            
            if stop:
                payload["stop"] = stop
            
            # Get API configuration
            api_config = self._get_config()
            
            # Make the streaming request
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                async with client.stream(
                    "POST",
                    api_config.api_url,
                    headers={"Authorization": f"Bearer {api_config.api_key}", "Content-Type": "application/json", "Accept": "text/event-stream"},
                    json=payload
                ) as response:
                    if response.status_code != 200:
                        error_content = await response.aread()
                        error_data = {}
                        try: 
                            error_data = json.loads(error_content.decode())
                        except: 
                            error_data = {"raw_content": error_content.decode()}
                        
                        err = HerokuApiError(f"Heroku API stream request failed with status {response.status_code}",
                            status_code=response.status_code, error_payload=error_data)
                        if run_manager: 
                            await run_manager.on_llm_error(err)
                        raise err
                    
                    async for line in response.aiter_lines():
                        if line.strip() == "":
                            continue
                            
                        if line.startswith("event:"):
                            # We can track event type if needed, but for now we just process data lines
                            continue
                            
                        if line.startswith("data:"):
                            data = line[5:].strip()
                            
                            if data == "[DONE]":
                                break
                                
                            try:
                                chunk_data = json.loads(data)
                                
                                if "choices" in chunk_data and chunk_data["choices"]:
                                    choice = chunk_data["choices"][0]
                                    
                                    if "delta" in choice:
                                        delta = choice["delta"]
                                        
                                        if "content" in delta and delta["content"]:
                                            content = delta["content"]
                                            
                                            chunk = ChatGenerationChunk(
                                                message=AIMessageChunk(content=content)
                                            )
                                            
                                            if run_manager:
                                                await run_manager.on_llm_new_token(content, chunk=chunk)
                                            
                                            yield chunk
                                
                            except json.JSONDecodeError:
                                # Skip malformed JSON
                                continue
                            
        except Exception as e:
            if run_manager:
                await run_manager.on_llm_error(e)
            raise e

