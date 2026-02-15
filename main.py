import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None:
    raise RuntimeError("api key not found")

client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Gemini Powered Chatbot")
parser.add_argument("user_input", type=str, help="Enter your prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [types.Content(role="user", parts=[types.Part(text=args.user_input)])]

response = client.models.generate_content(
    model="gemini-2.5-flash", contents=messages
)

user_prompt = args.user_input
prompt_token = response.usage_metadata.prompt_token_count
response_token = response.usage_metadata.candidates_token_count

if args.verbose:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {prompt_token}")
    print(f"Response tokens: {response_token}")


print(f"Response: {response.text}")