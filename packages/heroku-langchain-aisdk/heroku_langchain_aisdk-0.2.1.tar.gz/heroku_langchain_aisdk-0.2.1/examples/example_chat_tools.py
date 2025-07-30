import os
import asyncio
from heroku_mia_sdk import HerokuMia
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage # <--- Ensure AIMessage is imported
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from typing import Optional, List, Union # Union might be needed for Python < 3.10 for | operator in type hints

# Ensure you have HEROKU_API_KEY and INFERENCE_MODEL_ID (for a tool-enabled model)
# set in your environment variables or provide them directly.

# 1. Define your tool's argument schema
class GetWeatherArgs(BaseModel):
    city: str = Field(description="The city to get the weather for")
    unit: Optional[str] = Field("celsius", description="The unit of temperature (celsius or fahrenheit)")

# 2. Create the tool function
def get_weather_tool_function(city: str, unit: str = "celsius") -> str:
    # In a real scenario, this would call a weather API or perform a real lookup
    print(f"--- Tool 'get_weather_tool_function' called with city={city}, unit={unit} ---")
    if city.lower() == "london":
        return f"The weather in London is currently 15 degrees {unit} and mostly cloudy."
    elif city.lower() == "san francisco":
        return f"The weather in San Francisco is currently 18 degrees {unit} and sunny."
    else:
        return f"Sorry, I don't have weather information for {city}."

# 3. Create the StructuredTool
weather_tool = StructuredTool.from_function(
    func=get_weather_tool_function,
    name="get_weather",
    description="Gets the current weather in a given city. Use it to answer questions about weather.",
    args_schema=GetWeatherArgs
)

def run_chat_with_tools():
    print("Running chat with tools example...")
    try:
        # Ensure your Heroku model supports tools/function calling
        # client = HerokuMia(model="your-tool-enabled-model-id", heroku_api_key="your-api-key")
        client = HerokuMia() # Assumes env vars are set

        # 4. Bind tools to the client
        client_with_tools = client.bind_tools([weather_tool])

        # 5. Invoke with a prompt that might trigger the tool
        # Use Union for Python < 3.10 compatibility if needed, otherwise | is fine for 3.10+
        messages: List[Union[HumanMessage, ToolMessage, AIMessage]] = [HumanMessage(content="What's the weather like in London?")]
        print(f"Initial prompt: {messages[0].content}")

        response = client_with_tools.invoke(messages)

        print("\nFirst response from HerokuMia:")
        if response.tool_calls:
            print(f"  Tool Calls: {response.tool_calls}")
            # Add the AIMessage with tool calls to messages history
            messages.append(response) 
            
            # 6. Execute tool calls and prepare ToolMessage responses
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                tool_call_id = tool_call["id"]
                
                if tool_name == "get_weather":
                    tool_output = get_weather_tool_function(city=tool_args["city"], unit=tool_args.get("unit", "celsius"))
                    print(f"  Output of '{tool_name}' (ID: {tool_call_id}): {tool_output}")
                    messages.append(ToolMessage(content=tool_output, tool_call_id=tool_call_id))
                else:
                    # Handle unknown tool or pass error back
                    print(f"  Unknown tool called: {tool_name}")
                    messages.append(ToolMessage(content=f"Error: Unknown tool '{tool_name}'", tool_call_id=tool_call_id))
            
            # 7. Send tool responses back to the model
            print(f"\nSending tool responses back to the model: {messages[-len(response.tool_calls):]}")
            second_response = client_with_tools.invoke(messages)
            
            print("\nSecond response from HerokuMia (after tool execution):")
            print(f"  Content: {second_response.content}")

        else:
            print(f"  Content: {response.content}") # Model responded directly without tool use

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure your HEROKU_API_KEY and a tool-enabled INFERENCE_MODEL_ID are correctly set.")


if __name__ == "__main__":
    if not os.getenv("HEROKU_API_KEY") or not os.getenv("INFERENCE_MODEL_ID"):
        print("Warning: HEROKU_API_KEY or INFERENCE_MODEL_ID environment variables are not set.")
        print("The example might fail unless these are configured for a tool-enabled model.")
    
    run_chat_with_tools()

