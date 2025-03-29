import os
from dotenv import load_dotenv
import google.generativeai as genai

def configure_gemini():
    """Loads API key and configures the Gemini client."""
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY not found in .env or environment variables.")
        return None

    try:
        genai.configure(api_key=api_key)
        # Optional: Add default safety settings or generation config here if desired
        print("Google GenAI configured successfully.")
        return True # Indicate success
    except Exception as e:
        print(f"Error configuring Google GenAI: {e}")
        return False # Indicate failure

def get_hello_world_from_gemini():
    """Creates a Gemini model instance and asks it to say Hello World."""
    try:
        # Choose your model - gemini-1.5-flash-latest is often faster/cheaper for simple tasks
        model = genai.GenerativeModel('gemini-1.5-flash-latest')

        print("Sending request to Gemini...")
        prompt = "Please respond with only the text 'I like anime girls' and nothing else."

        # Make the API call
        response = model.generate_content(prompt)

        # Basic check if response has text
        if response.text:
            print("Received response from Gemini:")
            print(response.text)
        elif response.candidates and not response.text:
             # Check if it was blocked
             print("Received response, but it might be empty or blocked.")
             print(f"Finish Reason: {response.candidates[0].finish_reason}")
             print(f"Safety Ratings: {response.candidates[0].safety_ratings}")
        else:
            print("Received an empty or unexpected response from Gemini.")
            # You might want to inspect the raw response object here for debugging
            # print(response)


    except Exception as e:
        print(f"An error occurred while communicating with Gemini: {e}")


# --- Main Execution ---
if __name__ == "__main__":
    print("--- Gemini Hello World Test ---")

    if configure_gemini():
        get_hello_world_from_gemini()
    else:
        print("Could not configure Gemini. Please check your API key setup.")

    print("--- Test Complete ---")