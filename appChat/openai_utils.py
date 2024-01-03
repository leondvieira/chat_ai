from openai import OpenAI
from decouple import config


API_KEY = config("OPENAI_KEY")
client = OpenAI(api_key=API_KEY)


def send_to_openai(prompt):
    """Send the prompt to OpenAI

    Args:
        prompt (string): Prompt to send to OpenAI

    Returns:
        string: Response from OpenAI
    """
    response = client.completions.create(
    model="text-davinci-003",
    prompt=prompt,
    temperature=0,
    max_tokens=150,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    stop=["#", ";"])
    return response
