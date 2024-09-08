from openai import OpenAI
from coderag.config import OPENAI_API_KEY, OPENAI_CHAT_MODEL
from coderag.search import search_code

# Initialize the OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Keep the conversational history in a list
conversation_history = []

def get_intent_and_variations(user_input):
    """
    Derive intent and prompt variations from user input.
    """
    prompt = f"""
    Analyze this input:
    User Input: "{user_input}"

    Provide:
    1. Intent
    2. Three prompt variations (max 20 words each)
    """
    try:
        response = client.chat.completions.create(
            model=OPENAI_CHAT_MODEL,
            messages=[{"role": "system", "content": prompt}],
            temperature=0.7,
            max_tokens=200
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error in getting intent and variations: {e}"

def extract_keywords(intent, prompt_variations):
    """
    Extract keywords from intent and prompt variations.
    """
    prompt = f"""
    Extract 5-7 keywords from:
    Intent: {intent}
    Prompt Variations:
    {prompt_variations}
    """
    try:
        response = client.chat.completions.create(
            model=OPENAI_CHAT_MODEL,
            messages=[{"role": "system", "content": prompt}],
            temperature=0.5,
            max_tokens=100
        )
        return [kw.strip() for kw in response.choices[0].message.content.split(',')]
    except Exception as e:
        return f"Error in extracting keywords: {e}"

def construct_code_improvement_prompt(intent, search_results, user_input):
    """
    Construct the prompt asking OpenAI to improve the code based on the search results.
    This will send the relevant code files and ask OpenAI to suggest improvements.
    """
    # Get full content of all relevant files (not excerpts)
    full_code = "\n\n".join([
        f"File: {result['filename']}\nContent:\n{result['content']}"
        for result in search_results  # Include all results or limit if needed
    ])

    return f"""
    The following code files are related to the user's query. Please review the code and suggest improvements, fix any issues, and merge the files if necessary.

    User's Intent: {intent}
    User's Question: "{user_input}"

    Here are the relevant code files:

    {full_code}

    Provide a full, fixed, and improved version of the code with detailed comments where necessary. Merge the files if relevant, and apply best coding practices.
    """

def update_conversation_history(user_input, assistant_response):
    """
    Update the conversation history by appending the user input and assistant's response.
    """
    conversation_history.append({"role": "user", "content": user_input})
    conversation_history.append({"role": "assistant", "content": assistant_response})

    # To prevent exceeding token limits, limit the history to the last N exchanges
    if len(conversation_history) > 10:  # Keep the last 5 user-assistant pairs (10 entries)
        conversation_history.pop(0)  # Remove the oldest conversation entries

def execute_prompt_flow(user_input, project_path=None):
    """
    Execute the complete prompt flow using vector database for code search, with conversational history.
    """
    try:
        # Step 1: Get the intent and variations from the user input
        intent_and_variations = get_intent_and_variations(user_input)
        if "Error" in intent_and_variations:
            return intent_and_variations

        # Split the response into lines
        lines = intent_and_variations.split('\n')

        # Step 2: Check if there are enough lines to process
        if len(lines) < 4:
            return "Error: Unexpected response format from OpenAI. The response does not have enough lines."

        # Step 3: Extract intent and variations
        intent_line = lines[1] if len(lines) > 1 else "Intent: Unable to determine intent"
        intent = intent_line.split(': ', 1)[-1] if ': ' in intent_line else "Unable to determine intent"

        variations = '\n'.join(lines[2:]) if len(lines) > 2 else "No variations provided"

        # Step 4: Extract keywords from intent and variations
        keywords = extract_keywords(intent, variations)
        if "Error" in keywords:
            return keywords

        # Step 5: Perform code search using the vector database
        search_results = search_code(','.join(keywords))
        if not search_results:
            return "No relevant code found."

        # Step 6: Construct the code improvement prompt based on search results
        improvement_prompt = construct_code_improvement_prompt(intent, search_results, user_input)

        # Step 7: Add conversational history to the prompt
        messages_with_history = conversation_history + [{"role": "system", "content": improvement_prompt}]

        # Step 8: Get the code improvements from OpenAI with history
        response = client.chat.completions.create(
            model=OPENAI_CHAT_MODEL,
            messages=messages_with_history,  # Include history in the API call
            temperature=0.7,
            max_tokens=2000  # Increase max tokens to accommodate full code responses
        )

        assistant_response = response.choices[0].message.content.strip()

        # Step 9: Update the conversation history
        update_conversation_history(user_input, assistant_response)

        return assistant_response

    except Exception as e:
        return f"Error in prompt flow execution: {e}"
