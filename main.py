import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_functions import available_functions
from call_functions import call_function

model_name = "gemini-2.5-flash"

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

num_iteration = 20
for i in range(num_iteration):
    response = client.models.generate_content(
        model=model_name, 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
            ),
        )
    
    candidates = response.candidates
    if candidates:
        for candidate in candidates:
            messages.append(candidate.content)

    if not response.function_calls:
        break
    
    if i == num_iteration - 1:
        sys.exit("Max number of iterations reached. No final response from model.")
        
    
    function_responses = []
    if response.function_calls:
        for the_function in response.function_calls:
            function_call_result = call_function(the_function, args.verbose)
            if function_call_result.parts is None:
                raise Exception("types.Content object should have a non-empty .parts list")
            if function_call_result.parts[0].function_response is None:
                raise Exception("function response should be a FunctionResponse object")
                
            function_responses.append(function_call_result.parts[0])
            
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
    
    
    messages.append(types.Content(role="user", parts=function_responses))


user_prompt = args.user_input
prompt_token = response.usage_metadata.prompt_token_count
response_token = response.usage_metadata.candidates_token_count

if args.verbose:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {prompt_token}")
    print(f"Response tokens: {response_token}")


print(f"Response: {response.text}")


            
        
