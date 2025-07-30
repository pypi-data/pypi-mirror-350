import os
import asyncio
from heroku_mia_sdk import HerokuMia
from langchain_core.messages import HumanMessage

# Ensure you have HEROKU_API_KEY and INFERENCE_MODEL_ID set in your environment variables
# or provide them directly to the HerokuMia constructor.

async def run_streaming_chat():
    print("Running streaming chat example...")
    try:
        # Initialize the client. It will try to pick up API key and model ID from env vars.
        # client = HerokuMia(
        #     model="your-model-id-here", 
        #     heroku_api_key="your-api-key-here"
        # )
        client = HerokuMia() 

        messages = [HumanMessage(content="Tell me a short story about a friendly robot who explores a new planet.")]
        
        print(f"Sending messages: {messages}")
        print("\nStreaming response from HerokuMia:")
        
        async for chunk in client.astream(messages):
            if chunk.content:
                print(chunk.content, end="", flush=True)
        
        print("\n--- Stream finished ---")

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure your HEROKU_API_KEY and INFERENCE_MODEL_ID are correctly set.")

if __name__ == "__main__":
    if not os.getenv("HEROKU_API_KEY") or not os.getenv("INFERENCE_MODEL_ID"):
        print("Warning: HEROKU_API_KEY or INFERENCE_MODEL_ID environment variables are not set.")
        print("The example might fail unless these are configured or passed directly to HerokuMia.")

    asyncio.run(run_streaming_chat())
