import openai
import re

# Set up the OpenAI API client
openai.api_key = ""

# Set the model engine
model_engine = "text-davinci-003"
def generatetc(text):

    # Set the prompt (the one-line requirement)
    text = "Login with username and password"
    prompt = re.sub(r'\n+', ' ', text)
    # print(prompt)
    # Generate test cases using the OpenAI API
    response = openai.Completion.create(
        engine=model_engine,
        prompt=f"generate maximum number test cases with summary,testing type,test category,testcasetype, priority, multiple steps with input data and expected outcome,expected outcome for the following requirement in json format: {prompt} \n\n",
        n=1,
        max_tokens=4000,
        temperature=0
    )
    # Extract the test cases from the response
    test_cases = response["choices"][0]["text"].strip()

    # Print the test cases
    # print(test_cases)
    return test_cases
