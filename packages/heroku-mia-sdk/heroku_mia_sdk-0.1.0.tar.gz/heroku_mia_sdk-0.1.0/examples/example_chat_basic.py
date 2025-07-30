import os
import asyncio
from heroku_mia_sdk import HerokuMia
from langchain_core.messages import HumanMessage

# Ensure you have HEROKU_API_KEY and INFERENCE_MODEL_ID set in your environment variables
# or provide them directly to the HerokuMia constructor.

def run_basic_chat():
    print("Running basic chat example...")
    try:
        # Initialize the client. It will try to pick up API key and model ID from env vars.
        # You can also pass them directly:
        # client = HerokuMia(
        #     model="your-model-id-here", 
        #     heroku_api_key="your-api-key-here"
        # )
        client = HerokuMia()

        messages = [HumanMessage(content="Hello, what is the capital of France?")]
        
        print(f"Sending messages: {messages}")
        response = client.invoke(messages)
        
        print("\nResponse from HerokuMia:")
        print(f"Content: {response.content}")
        if response.tool_calls:
            print(f"Tool Calls: {response.tool_calls}")
        if response.additional_kwargs:
            print(f"Additional Kwargs: {response.additional_kwargs}")

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure your HEROKU_API_KEY and INFERENCE_MODEL_ID are correctly set.")
        print("If your model requires specific parameters (e.g. for tools), ensure they are configured.")

if __name__ == "__main__":
    # Check for environment variables (optional, for user guidance)
    if not os.getenv("HEROKU_API_KEY") or not os.getenv("INFERENCE_MODEL_ID"):
        print("Warning: HEROKU_API_KEY or INFERENCE_MODEL_ID environment variables are not set.")
        print("The example might fail unless these are configured or passed directly to HerokuMia.")
        # Example of how to set them if you were running this script directly with hardcoded values (NOT RECOMMENDED for real use)
        # os.environ["HEROKU_API_KEY"] = "YOUR_KEY_HERE" 
        # os.environ["INFERENCE_MODEL_ID"] = "YOUR_MODEL_ID_HERE"


    run_basic_chat()

