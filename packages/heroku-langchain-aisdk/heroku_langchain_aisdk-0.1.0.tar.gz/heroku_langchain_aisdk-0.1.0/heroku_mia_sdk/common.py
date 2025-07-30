import os
import json
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional, AsyncIterator, Generator, Union

# Attempt to import LangChain types
try:
    from langchain_core.messages import (
        BaseMessage,
        HumanMessage,
        AIMessage,
        SystemMessage,
        ToolMessage,
        ChatMessage,
    )
    from langchain_core.tools import StructuredTool
    from langchain_core.pydantic_v1 import BaseModel as LangChainBaseModel
except ImportError:
    # Define dummy types if LangChain is not available for basic type checking
    BaseMessage = Any
    HumanMessage = Any
    AIMessage = Any
    SystemMessage = Any
    ToolMessage = Any
    ChatMessage = Any
    StructuredTool = Any
    LangChainBaseModel = Any

# Also try to import regular Pydantic BaseModel for v2 compatibility
try:
    from pydantic import BaseModel as PydanticBaseModel
except ImportError:
    PydanticBaseModel = Any

# Import the dataclasses from types.py
from .types import (
    HerokuChatMessage,
    HerokuToolCall, # This is the actual tool call object in an AIMessage from Heroku
    HerokuFunction, # This is the 'function' field within HerokuToolCall
    HerokuToolMessageContent,
    HerokuChatMessageRole,
    HerokuFunctionTool, # Correct nested type for tools definition in requests
    HerokuFunctionDetails, # The nested 'function' part of HerokuFunctionTool
    HerokuFunctionToolParameters,
)

DEFAULT_HEROKU_API_URL = "https://inference.heroku.com"

class HerokuApiError(Exception):
    """Custom exception for Heroku API errors."""
    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        error_payload: Optional[Any] = None,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.error_payload = error_payload
        self.message = message

    def __str__(self) -> str:
        return f"HerokuApiError(status_code={self.status_code}, message='{self.message}', payload={self.error_payload})"

@dataclass
class HerokuConfig:
    api_key: str
    api_url: str

def get_heroku_config_options(
    heroku_api_key: Optional[str] = None,
    heroku_api_url: Optional[str] = None,
    endpoint_path: str = "",
) -> HerokuConfig:
    """
    Resolves Heroku API key and URL from direct arguments or environment variables.
    Constructs the full API endpoint URL.
    """
    key = heroku_api_key or os.environ.get("HEROKU_API_KEY") or os.environ.get("INFERENCE_KEY")
    if not key:
        raise ValueError(
            "Heroku API key not found. Please set it in the constructor, "
            "or set the HEROKU_API_KEY or INFERENCE_KEY environment variable."
        )

    base_url = heroku_api_url or os.environ.get("HEROKU_API_URL") or os.environ.get("INFERENCE_URL") or DEFAULT_HEROKU_API_URL

    # Ensure no double slashes and correct single slash
    if not base_url.endswith("/"):
        base_url += "/"
    if endpoint_path.startswith("/"):
        endpoint_path = endpoint_path[1:]
    
    full_url = base_url + endpoint_path # base_url now always ends with /
        
    return HerokuConfig(api_key=key, api_url=full_url)


def langchain_messages_to_heroku_messages(
    messages: List[BaseMessage],
) -> List[HerokuChatMessage]:
    """Converts a list of LangChain messages to Heroku API message format."""
    heroku_messages: List[HerokuChatMessage] = []
    for msg in messages:
        role: HerokuChatMessageRole
        content_str_or_list: Union[str, List[HerokuToolMessageContent]]
        tool_calls_converted: Optional[List[HerokuToolCall]] = None
        
        if isinstance(msg, HumanMessage):
            role = "user"
            content_str_or_list = str(msg.content)
        elif isinstance(msg, AIMessage):
            role = "assistant"
            content_str_or_list = str(msg.content)
            if msg.tool_calls and len(msg.tool_calls) > 0:
                tool_calls_converted = []
                for tc in msg.tool_calls:
                    # LangChain ToolCall (dict in AIMessage.tool_calls) has 'name', 'args' (dict), 'id'
                    # HerokuToolCall expects 'function' to be a HerokuFunction object (or dict matching it)
                    tool_calls_converted.append(
                        HerokuToolCall(
                            id=tc["id"],
                            type="function",
                            function=HerokuFunction( # Create HerokuFunction object
                                name=tc["name"],
                                arguments=json.dumps(tc["args"]),
                            ),
                        )
                    )
                if not content_str_or_list: # If content is empty string and there are tool_calls.
                    content_str_or_list = "" # Or None, Heroku spec implies content can be empty string.

        elif isinstance(msg, SystemMessage):
            role = "system"
            content_str_or_list = str(msg.content)
        elif isinstance(msg, ToolMessage):
            role = "tool"
            content_str_or_list = str(msg.content)
            # For tool messages, we need to set the tool_call_id separately
            heroku_msg = HerokuChatMessage(
                role=role, 
                content=content_str_or_list,
                tool_call_id=msg.tool_call_id
            )
            heroku_messages.append(heroku_msg)
            continue
        elif isinstance(msg, ChatMessage):
            role = msg.role # type: ignore 
            content_str_or_list = str(msg.content)
        else:
            raise ValueError(f"Unsupported LangChain message type: {type(msg)}")

        heroku_msg = HerokuChatMessage(role=role, content=content_str_or_list)
        if tool_calls_converted:
            heroku_msg.tool_calls = tool_calls_converted
        
        heroku_messages.append(heroku_msg)
    return heroku_messages

def langchain_tools_to_heroku_tools(
    tools: List[StructuredTool],
) -> List[HerokuFunctionTool]: 
    """Converts a list of LangChain StructuredTools to Heroku API tool format (HerokuFunctionTool)."""
    heroku_tools_list: List[HerokuFunctionTool] = []
    for tool in tools:
        if not isinstance(tool, StructuredTool):
            raise ValueError(f"Unsupported tool type: {type(tool)}. Expected StructuredTool.")

        schema_properties = {}
        schema_required = []
        
        if tool.args_schema:
            # Check if it's a Pydantic v1 or v2 model
            is_pydantic_v1 = hasattr(tool.args_schema, '__pydantic_model__') or (
                LangChainBaseModel != Any and issubclass(tool.args_schema, LangChainBaseModel)
            )
            is_pydantic_v2 = hasattr(tool.args_schema, 'model_json_schema') or (
                PydanticBaseModel != Any and issubclass(tool.args_schema, PydanticBaseModel)
            )
            
            if is_pydantic_v2:
                # Pydantic v2
                try:
                    schema = tool.args_schema.model_json_schema()
                except AttributeError:
                    # Fallback to v1 method
                    schema = tool.args_schema.schema()
            elif is_pydantic_v1:
                # Pydantic v1
                schema = tool.args_schema.schema()
            else:
                # Unknown schema type, try both methods
                try:
                    schema = tool.args_schema.model_json_schema()
                except AttributeError:
                    try:
                        schema = tool.args_schema.schema()
                    except AttributeError:
                        schema = {}
            
            schema_properties = schema.get("properties", {})
            schema_required = schema.get("required", [])
            
            # Validate required field
            if "required" in schema and not (
                isinstance(schema["required"], list) and
                all(isinstance(item, str) for item in schema["required"])
            ):
                schema_required = []

        heroku_tools_list.append(
            HerokuFunctionTool( 
                type="function",
                function=HerokuFunctionDetails(
                    name=tool.name,
                    description=tool.description or "", 
                    parameters=HerokuFunctionToolParameters(
                        type="object",
                        properties=schema_properties,
                        required=schema_required,
                    ),
                )
            )
        )
    return heroku_tools_list


@dataclass
class ParsedSSEEvent:
    event: Optional[str] = None
    data: Optional[str] = None
    id: Optional[str] = None
    retry: Optional[str] = None


async def parse_heroku_sse(
    response_iterator: AsyncIterator[bytes],
) -> AsyncIterator[ParsedSSEEvent]:
    """
    Parses Server-Sent Events (SSE) from an async byte iterator.
    Yields ParsedSSEEvent objects.
    """
    current_event_dict = {"event": None, "data_lines": [], "id": None, "retry": None}

    async for line_bytes in response_iterator:
        line = line_bytes.decode("utf-8").rstrip("\n\r")

        if not line:
            # Dispatch event if any field was populated
            if current_event_dict["event"] or current_event_dict["data_lines"] or current_event_dict["id"] or current_event_dict["retry"]:
                data_str = "\n".join(current_event_dict["data_lines"]) if current_event_dict["data_lines"] else None
                yield ParsedSSEEvent(
                    event=current_event_dict["event"],
                    data=data_str,
                    id=current_event_dict["id"],
                    retry=current_event_dict["retry"],
                )
            current_event_dict = {"event": None, "data_lines": [], "id": None, "retry": None}
            continue

        if line.startswith(":"):
            continue

        field, _, value = line.partition(":")
        value = value.lstrip(" ")

        if field == "event":
            current_event_dict["event"] = value
        elif field == "data":
            current_event_dict["data_lines"].append(value)
        elif field == "id":
            current_event_dict["id"] = value
        elif field == "retry":
            current_event_dict["retry"] = value
        # else: ignore unknown fields as per spec

    # After the loop, yield any remaining event
    if current_event_dict["event"] or current_event_dict["data_lines"] or current_event_dict["id"] or current_event_dict["retry"]:
        data_str = "\n".join(current_event_dict["data_lines"]) if current_event_dict["data_lines"] else None
        yield ParsedSSEEvent(
            event=current_event_dict["event"],
            data=data_str,
            id=current_event_dict["id"],
            retry=current_event_dict["retry"],
        )

def heroku_message_to_dict(msg: HerokuChatMessage) -> Dict[str, Any]:
    """Convert HerokuChatMessage to dictionary, properly handling nested objects."""
    result = {
        "role": msg.role,
        "content": msg.content,
    }
    
    # Add optional fields only if they're not None
    if msg.name is not None:
        result["name"] = msg.name
    if msg.tool_calls is not None:
        result["tool_calls"] = [asdict(tc) for tc in msg.tool_calls]
    if msg.tool_call_id is not None:
        result["tool_call_id"] = msg.tool_call_id
    
    return result

if __name__ == "__main__":
    # Basic test for get_heroku_config_options
    os.environ["HEROKU_API_KEY"] = "test_key_from_env"
    os.environ["INFERENCE_URL"] = "https://test.heroku.com/api/" 

    config1 = get_heroku_config_options(endpoint_path="/v1/chat/completions")
    print(f"Config 1: {config1}")
    assert config1.api_key == "test_key_from_env"
    assert config1.api_url == "https://test.heroku.com/api/v1/chat/completions"

    config3 = get_heroku_config_options(endpoint_path="v1/chat/completions") 
    print(f"Config 3: {config3}")
    assert config3.api_url == "https://test.heroku.com/api/v1/chat/completions"
    
    del os.environ["HEROKU_API_KEY"]
    del os.environ["INFERENCE_URL"]
    print("Common utilities module loaded and get_heroku_config_options tests passed.")

    try:
        from langchain_core.messages import HumanMessage as TestHuman, AIMessage as TestAI, ToolMessage as TestTool
        from langchain_core.tools import tool as test_tool_decorator
        from langchain_core.pydantic_v1 import BaseModel as TestBaseModel, Field as TestField

        @test_tool_decorator
        class GetWeatherTool(TestBaseModel):
            """Gets the weather in a city."""
            city: str = TestField(description="The city to get weather for")
            unit: Optional[str] = TestField("celsius", description="Unit for temperature")

        sample_lc_messages = [
            TestHuman(content="Hello"),
            TestAI(content="Hi there", tool_calls=[{"name": "GetWeatherTool", "args": {"city": "London"}, "id": "call_123"}]),
            TestTool(content="Weather is sunny", tool_call_id="call_123")
        ]
        heroku_api_messages = langchain_messages_to_heroku_messages(sample_lc_messages)
        print("\nConverted Heroku Messages:")
        for m in heroku_api_messages:
            print(m)
            if m.role == "assistant" and m.tool_calls:
                assert isinstance(m.tool_calls[0].function, HerokuFunction)
        
        sample_lc_tools = [GetWeatherTool()]
        heroku_api_tools = langchain_tools_to_heroku_tools(sample_lc_tools)
        print("\nConverted Heroku Tools:")
        for t in heroku_api_tools:
            print(t)
            assert t.type == "function"
            assert isinstance(t.function, HerokuFunctionDetails)
            assert t.function.name == "GetWeatherTool"
            assert t.function.parameters.properties["city"]["type"] == "string"

        print("\nLangChain conversion tests passed.")

    except ImportError:
        print("\nSkipping LangChain conversion tests as LangChain is not fully available.")
    except Exception as e:
        print(f"\nError during LangChain conversion tests: {e}")

