from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Union, Literal

# --- Heroku API Specific Types ---
HerokuChatMessageRole = Literal["system", "user", "assistant", "tool"]

@dataclass
class HerokuFunction:
    name: str
    arguments: str  # JSON string of arguments

@dataclass
class HerokuToolCall:
    id: str
    type: Literal["function"]
    function: HerokuFunction

@dataclass
class HerokuToolMessageContent:
    tool_call_id: str
    content: str
    name: Optional[str] = None

@dataclass
class HerokuChatMessage:
    role: HerokuChatMessageRole
    content: Union[str, List[HerokuToolMessageContent]]
    name: Optional[str] = None
    tool_calls: Optional[List[HerokuToolCall]] = None
    tool_call_id: Optional[str] = None

@dataclass
class HerokuFunctionToolParameters:
    type: Literal["object"]
    properties: Dict[str, Any]
    required: Optional[List[str]] = field(default_factory=list)

@dataclass
class HerokuFunctionToolDefinition: # Corresponds to HerokuFunctionTool in TS
    type: Literal["function"] # Added this field based on TS HerokuFunctionTool
    function: "HerokuFunctionToolDefinition" # Use forward reference to avoid NameError
    # Correcting the above based on TS:
    # function: HerokuFunctionToolDefinition -> function: HerokuFunctionDetails (new dataclass)

@dataclass # New dataclass to match TS structure for HerokuFunctionTool.function
class HerokuFunctionDetails:
    name: str
    description: str
    parameters: HerokuFunctionToolParameters

@dataclass # Corrected HerokuFunctionToolDefinition
class HerokuFunctionTool: # Renamed from HerokuFunctionToolDefinition to HerokuFunctionTool
    type: Literal["function"]
    function: HerokuFunctionDetails


@dataclass
class HerokuToolChoiceFunction:
    name: str

@dataclass
class HerokuToolChoiceOption:
    type: Literal["function"]
    function: HerokuToolChoiceFunction

# --- Request/Response Payloads for Chat Completions ---
@dataclass
class HerokuChatCompletionRequest:
    model: str
    messages: List[HerokuChatMessage]
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None # maxTokens in TS, max_tokens in Heroku API
    stop: Optional[List[str]] = None
    stream: Optional[bool] = None
    top_p: Optional[float] = None # topP in TS, top_p in Heroku API
    tools: Optional[List[HerokuFunctionTool]] = None # Corrected type
    tool_choice: Optional[Union[Literal["none", "auto", "required"], HerokuToolChoiceOption]] = None
    # additional_kwargs: Optional[Dict[str, Any]] = field(default_factory=dict) # This field is handled by **kwargs in Python usually, or by directly adding known fields like extended_thinking
    extended_thinking: Optional[bool] = None # Example from TS, should be captured by a more general additional_kwargs or similar

    # To handle arbitrary additional arguments as in TS [key: string]: any
    # This is not directly translatable to a dataclass field in the same way.
    # It's usually handled by passing **kwargs to a function or by having a specific
    # field like `additional_kwargs: Optional[Dict[str, Any]] = field(default_factory=dict)`
    # The prompt's python has `additional_kwargs` at the end of HerokuMiaConstructorFields,
    # implying it should be here for API consistency as well.
    additional_kwargs: Optional[Dict[str, Any]] = field(default_factory=dict)


@dataclass
class HerokuChatCompletionChoice:
    index: int
    message: HerokuChatMessage
    finish_reason: str

@dataclass
class HerokuChatCompletionUsage:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

@dataclass
class HerokuChatCompletionResponse:
    id: str
    object: str
    created: int
    model: str
    choices: List[HerokuChatCompletionChoice]
    usage: HerokuChatCompletionUsage
    system_fingerprint: Optional[str] = None

# --- Streaming Specific Types for /v1/chat/completions ---
@dataclass
class HerokuChatCompletionStreamChoiceDelta:
    role: Optional[HerokuChatMessageRole] = None
    content: Optional[str] = None
    tool_calls: Optional[List["PartialHerokuToolCall"]] = None # TS uses Partial<HerokuToolCall>[]

@dataclass # New dataclass for PartialHerokuToolCall based on TS Partial<HerokuToolCall>
class PartialHerokuToolCallFunction:
    name: Optional[str] = None
    arguments: Optional[str] = None

@dataclass # New dataclass for PartialHerokuToolCall
class PartialHerokuToolCall:
    id: Optional[str] = None # id is not optional in HerokuToolCall, but can be in chunks
    type: Optional[Literal["function"]] = None
    function: Optional[PartialHerokuToolCallFunction] = None
    index: Optional[int] = None # Added index for tool_calls chunk, similar to LocalToolCallChunk

@dataclass
class HerokuChatCompletionStreamChoice:
    index: int
    delta: HerokuChatCompletionStreamChoiceDelta
    finish_reason: Optional[str] = None

@dataclass
class HerokuChatCompletionStreamResponse:
    id: str
    object: str
    created: int
    model: str
    choices: List[HerokuChatCompletionStreamChoice]
    usage: Optional[HerokuChatCompletionUsage] = None # As per TS: usage might appear in the last chunk

# --- LangChain Compatibility Types ---
@dataclass
class LocalToolCallChunk: # As per prompt
    name: Optional[str] = None
    args: Optional[str] = None
    id: Optional[str] = None
    index: Optional[int] = None
    # type: "tool_call_chunk" # TS has this, Python equivalent would be a Literal or just implied by class name

# --- Heroku Agent API Specific Types ---
@dataclass
class HerokuAgentToolRuntimeParams: # As per prompt
    target_app_name: str
    dyno_size: Optional[str] = None
    ttl_seconds: Optional[int] = None
    max_calls: Optional[int] = None
    tool_params: Optional[Dict[str, Any]] = field(default_factory=dict)

@dataclass
class HerokuAgentToolDefinition: # As per prompt
    type: Literal["heroku_tool", "mcp"]
    name: str
    runtime_params: HerokuAgentToolRuntimeParams
    description: Optional[str] = None

@dataclass # HerokuAgentBaseRequest from prompt, with added additional_kwargs for consistency
class HerokuAgentBaseRequest:
    messages: List[HerokuChatMessage]
    model: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens_per_inference_request: Optional[int] = None # Renamed from maxTokensPerRequest from TS
    stop: Optional[List[str]] = None
    top_p: Optional[float] = None
    tools: Optional[List[HerokuAgentToolDefinition]] = None
    metadata: Optional[Dict[str, Any]] = field(default_factory=dict) # As per prompt
    session_id: Optional[str] = None # As per prompt
    # additionalKwargs from TS not in prompt's Python for this class, adding for consistency
    additional_kwargs: Optional[Dict[str, Any]] = field(default_factory=dict)


@dataclass
class HerokuAgentInvokeRequest(HerokuAgentBaseRequest): # As per TS
    pass

@dataclass
class HerokuAgentStreamRequest(HerokuAgentBaseRequest): # As per prompt
    pass


@dataclass
class HerokuAgentInvokeResponse: # As per prompt
    message: Optional[HerokuChatMessage] = None
    tool_results: Optional[List[Any]] = field(default_factory=list)
    session_id: Optional[str] = None
    error: Optional[Any] = None

# --- Agent SSE Event Data Payloads ---
# These correspond to the `data` field of various SSE events
# Based on SPECS.md 3.2.2 and TS types

@dataclass
class HerokuAgentMessageDeltaEventData: # As per prompt
    delta: str
    # Any other fields Heroku sends with message.delta (Not specified in prompt)

@dataclass
class HerokuAgentToolCallEventData: # As per prompt
    id: str
    name: str
    input: str # JSON string
    # Any other fields Heroku sends with tool.call (Not specified in prompt)

@dataclass
class HerokuAgentToolCompletionEventData: # As per prompt
    id: str
    name: str
    output: str # JSON string or plain text
    # Any other fields Heroku sends with tool.completion (Not specified in prompt)

@dataclass
class HerokuAgentToolErrorEventData: # As per prompt
    error: str
    id: Optional[str] = None
    name: Optional[str] = None
    # Any other fields Heroku sends with tool.error (Not specified in prompt)

@dataclass
class HerokuAgentAgentErrorEventData: # As per prompt
    message: str
    # Any other fields Heroku sends with agent.error (Not specified in prompt)

@dataclass
class HerokuAgentStreamEndEventData: # As per prompt
    final_message: Optional[HerokuChatMessage] = None
    # Any other fields Heroku sends with stream.end (Not specified in prompt)


HerokuAgentSSEData = Union[ # As per prompt
    HerokuAgentMessageDeltaEventData,
    HerokuAgentToolCallEventData,
    HerokuAgentToolCompletionEventData,
    HerokuAgentToolErrorEventData,
    HerokuAgentAgentErrorEventData,
    HerokuAgentStreamEndEventData,
]

# --- SDK Class Constructor Parameter Types ---
# These are for configuring the SDK classes themselves, not direct API payloads.
# They correspond to HerokuMiaFields and HerokuMiaAgentFields in TypeScript.

@dataclass
class HerokuMiaConstructorFields: # As per prompt's Python example (HerokuMiaFields in TS)
    model: Optional[str] = None
    temperature: Optional[float] = 1.0
    max_tokens: Optional[int] = None # maxTokens in TS
    stop: Optional[List[str]] = None
    # stream from TS (HerokuMiaFields) is named streaming here
    streaming: Optional[bool] = False # stream in TS, streaming in prompt's Python
    top_p: Optional[float] = 0.999 # topP in TS
    heroku_api_key: Optional[str] = None # herokuApiKey in TS
    heroku_api_url: Optional[str] = None # herokuApiUrl in TS
    max_retries: Optional[int] = 2 # maxRetries in TS
    timeout: Optional[int] = None
    additional_kwargs: Optional[Dict[str, Any]] = field(default_factory=dict) # additionalKwargs in TS

@dataclass
class HerokuMiaRuntimeOptions: # As per prompt's Python example (HerokuMiaCallOptions in TS)
    # tools: Optional[List[Any]] = None # Placeholder for LangChain StructuredTool.
    # The prompt's TS says: tools?: StructuredTool[];
    # The prompt's Python says: tools: Optional[List[Any]] = None
    # This 'Any' should ideally be a more specific type if we know what StructuredTool translates to,
    # or a forward reference if StructuredTool is defined elsewhere in this SDK.
    # For now, List[Any] is a placeholder.
    tools: Optional[List[Any]] = None # Placeholder for LangChain StructuredTool / HerokuFunctionTool
    tool_choice: Optional[Union[Literal["none", "auto", "required"], HerokuToolChoiceOption]] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None # maxTokens in TS
    top_p: Optional[float] = None # topP in TS
    stop: Optional[List[str]] = None
    additional_kwargs: Optional[Dict[str, Any]] = field(default_factory=dict) # additionalKwargs in TS

@dataclass
class HerokuMiaAgentConstructorFields: # As per prompt's Python example (HerokuMiaAgentFields in TS)
    model: Optional[str] = None
    temperature: Optional[float] = 1.0
    max_tokens_per_request: Optional[int] = None # maxTokensPerRequest in TS
    stop: Optional[List[str]] = None
    top_p: Optional[float] = 0.999 # topP in TS
    tools: Optional[List[HerokuAgentToolDefinition]] = None
    heroku_api_key: Optional[str] = None # herokuApiKey in TS
    heroku_api_url: Optional[str] = None # herokuApiUrl in TS
    max_retries: Optional[int] = 2 # maxRetries in TS
    timeout: Optional[int] = None
    additional_kwargs: Optional[Dict[str, Any]] = field(default_factory=dict) # additionalKwargs in TS

@dataclass
class HerokuMiaAgentRuntimeOptions: # As per prompt's Python example (HerokuMiaAgentCallOptions in TS)
    metadata: Optional[Dict[str, Any]] = field(default_factory=dict)
    session_id: Optional[str] = None # sessionId in TS
    additional_kwargs: Optional[Dict[str, Any]] = field(default_factory=dict) # additionalKwargs in TS
