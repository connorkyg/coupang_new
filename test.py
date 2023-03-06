import openai
import os

# Set up the OpenAI API credentials
openai.api_key = os.environ["OPENAI_API_KEY"]


# Define a function to generate text based on a prompt
def generate_text(prompt):
    # Set the OpenAI API parameters
    completions = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )

    # Get the generated text
    message = completions.choices[0].text.strip()

    return message


# Ask for user input
prompt = input("Enter a prompt: ")

# Generate text based on the prompt
generated_text = generate_text(prompt)

# Print the generated text
print(generated_text)
