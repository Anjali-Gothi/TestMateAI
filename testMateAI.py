import openai,os,re,tiktoken

# Set up the OpenAI API client
openai.api_key = "Use your own key"

# Set the model engine
model_engine = "text-davinci-003"

text = """ Description

Use case : As a Tester, I need an ability to link an Issue (bug/defect) directly to the Test case in the Issue Tab, without executing the Test case in a Test suite. In many instances I am aware that the bug corresponds to a Test case and I don’t want to create an execution for it to link it to test case and direct link is easier to track. 

Implementation Approach - 

Add a button to “link issue” to the Test case, the window should open list of all the issues available in the Issue Module.  (Similar feature is available in Requirement Module).  

Issue link ability is needed only at Test case level, the scope to add it for specific step is not part of this feature. 

Show Unique Entry for Linked Issue/Bug. Currently the product shows duplicate entries for a single bug if linked multiple times, that should be fixed.

Add 2 columns new columns 

Direct Linkage - Introduce a column “Direct Linkage” - Yes when direct link, No when linked from execution. (Similar feature is available in Requirement Module).  

Yes - When Issue is linked from Test case Module. 

No - When Issue is linked from Test Execution Screen. 

If the same defect is linked on Execution and linked on Test case the Direct Linkage should be Yes.

Unlinking of defects directly linked on Test case should be possible. If the same defect is linked on Execution and linked on Test case the Direct Linkage. After Unlinking of issue the Direct Linkage should be No. But the Execution count will still persist. (Similar feature is available in Requirement Module).

# Execution Linkages 

This should show total number of times the issue is linked on the execution screen.(Similar feature is available in Requirement Module).

 The count shall be clickable. After clicking the count a pop-up should open than will display the execution details where the bug was linked. 


If the issue is not linked from execution screen then count is 0.

The bugs which are linked directly to test case should be auto linked to associated requirements in QMetry and Jira (linked issue section)like it happens for bug linked from execution screen (This is needed we already cross confirmed from Peter over the call)

In Requirement module >> Issue Tab the issue shall be displayed - With Direct Linkage as No and Execution Count as 0.

On the Test case List Grid, the count of issues shown be should unique. 

Ensure to display bug fields accordingly as per the external tracker or internal tracker.  """

prompt = re.sub(r'\n+', ' ', text)

#Count No of Tokens in text words
def count_tokens(text):
    encoding = tiktoken.get_encoding("p50k_base")
    input_ids = encoding.encode(text)
    num_tokens = len(input_ids)
    return num_tokens
num_tokens = count_tokens(text=text)
print("Number of tokens:  ", num_tokens)


def split_text_into_chunks(text, chunk_size):
    tt_encoding = tiktoken.get_encoding("p50k_base")
    tokens = tt_encoding.encode(text) #can also include prompt here
    total_tokens = len(tokens)
    chunks = []
    for i in range(0,total_tokens,chunk_size):
        chunk=tokens[i:i+chunk_size]
        chunks.append(chunk)
    return chunks

# Specify the desired chunk size (in number of tokens)
chunk_size = 900

# Split the text into chunks
text_chunks = split_text_into_chunks(text, chunk_size)
for i, chunk in enumerate(text_chunks):
    print(f"Chunk {i}: {len(chunk)} tokens")

prompt_response = []
tt_encoding = tiktoken.get_encoding("p50k_base")

# Generate test cases using the OpenAI API
for index,chunk in enumerate(text_chunks):
    prompt_request = f"generate maximum number of test cases with summary, multiple steps with input data and expected outcome for the following requirement, All in json format: {tt_encoding.decode(text_chunks[i])} \n\n"
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt_request,
        max_tokens=500,
        temperature=0,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # Extract the test cases from the response
    test_cases = response["choices"][0]["text"].strip()
    print(test_cases)
    prompt_response.append(test_cases)

#Not Needed Code---------------------------------------------
prompt_request = "The Final Result are: " + str(prompt_response)
response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt_request,
        temperature=0,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
final_TestCases_Result = response["choices"][0]["text"].strip()
# print(final_TestCases_Result)
