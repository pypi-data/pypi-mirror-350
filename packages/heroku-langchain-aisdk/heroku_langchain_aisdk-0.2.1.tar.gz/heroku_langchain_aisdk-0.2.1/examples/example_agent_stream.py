import os
import asyncio
from heroku_mia_sdk import HerokuMiaAgent
from langchain_core.messages import HumanMessage
# from heroku_mia_sdk import HerokuAgentToolDefinition # Uncomment if defining tools client-side

# Ensure you have HEROKU_API_KEY and an appropriate INFERENCE_MODEL_ID for an agent
# set in your environment variables or provide them directly.

async def run_agent_streaming_interaction():
    print("Running agent streaming example...")
    try:
        # Initialize the agent client. 
        # It will try to pick up API key and model ID from env vars.
        # agent_client = HerokuMiaAgent(
        #     model="your-agent-model-id-here", 
        #     heroku_api_key="your-api-key-here"
        # )
        #
        # If your agent tools are defined on the client side (check Heroku API for how this is supported):
        # example_agent_tools = [
        #     HerokuAgentToolDefinition(
        #         type="heroku_tool", 
        #         name="my_custom_app_tool",
        #         description="A tool that interacts with a custom Heroku application.",
        #         runtime_params={"target_app_name": "your-heroku-app-name"}
        #     )
        # ]
        # agent_client = HerokuMiaAgent(model="your-agent-model-id", tools=example_agent_tools)
        
        agent_client = HerokuMiaAgent() # Assumes env vars are set & agent model is pre-configured if tools are used

        messages = [HumanMessage(content="What are my open support tickets related to billing?")]
        
        print(f"Sending messages to agent: {messages}")
        print("\nStreaming response from HerokuMiaAgent:")
        
        async for chunk in agent_client.astream(messages):
            if chunk.message.content: # content is already a string in AIMessageChunk
                print(f"{chunk.message.content}", end="", flush=True)
            
            if chunk.message.tool_call_chunks:
                for tc_chunk in chunk.message.tool_call_chunks:
                    # ToolCallChunk is a TypedDict: {'name': Optional[str], 'args': Optional[str], 'id': Optional[str], 'index': Optional[int]}
                    chunk_id = tc_chunk.get('id', 'N/A')
                    chunk_name = tc_chunk.get('name', 'N/A')
                    chunk_args = tc_chunk.get('args', '')
                    print(f"\n--- Tool Call Chunk (ID: {chunk_id}, Name: {chunk_name}) ---")
                    print(f"    Args part: {chunk_args}")
                    print(f"--- End Tool Call Chunk ---")
            
            if chunk.message.additional_kwargs:
                event_type = chunk.message.additional_kwargs.get('heroku_agent_event_type')
                if event_type:
                    print(f"\n--- Agent Event Received ---")
                    print(f"    Type: {event_type}")
                    # raw_data = chunk.message.additional_kwargs.get('raw_event_data')
                    # print(f"    Data: {raw_data}") # Can be verbose
                    
                    # Example of accessing specific event data
                    if event_type == "tool.call":
                        print(f"    Tool Call Details: ID={chunk.message.additional_kwargs.get('id')}, Name={chunk.message.additional_kwargs.get('name')}, Input={chunk.message.additional_kwargs.get('input')}")
                    elif event_type == "tool.error":
                         print(f"    Tool Error: ID={chunk.message.additional_kwargs.get('id')}, Name={chunk.message.additional_kwargs.get('name')}, Error={chunk.message.additional_kwargs.get('error')}")
                    print(f"--- End Agent Event ---")

        print("\n--- Agent stream finished ---")

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure your HEROKU_API_KEY and an agent-compatible INFERENCE_MODEL_ID are correctly set.")

if __name__ == "__main__":
    if not os.getenv("HEROKU_API_KEY") or not os.getenv("INFERENCE_MODEL_ID"):
        print("Warning: HEROKU_API_KEY or INFERENCE_MODEL_ID environment variables are not set.")
        print("The example might fail unless these are configured for an agent model.")

    asyncio.run(run_agent_streaming_interaction())

