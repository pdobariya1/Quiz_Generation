from google.oauth2 import service_account
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains.sequential import SequentialChain
from langchain_google_genai import ChatGoogleGenerativeAI


# Access credentials for model
credentials_path = "./.credential.json"
CREDENTIALS = service_account.Credentials.from_service_account_file(credentials_path)


# LLM Model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-001", credentials=CREDENTIALS, temperature=0.5)



# Template 1
TEMPLATE = """
Text: {text}
You are an expert MCQ Maker. Given the above text, it is your job to \
Create a quiz of {number} multiple choice questions for {subject} students in {tone} tone.
Make sure the the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format you response like RESPONSE_JSON below and use it as a guide. \
### RESPONSE_JSON
{response_json}
"""

# Template 2
TEMPLATE2 = """
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""



# Quiz generation Prompt
quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "response_json"],
    template=TEMPLATE,
)

# Quiz review Prompt
quiz_evaluation_prompt = PromptTemplate(
    input_variables=["subject", "quiz"],
    template=TEMPLATE2,
)



# Quiz chain
quiz_chain = LLMChain(llm=llm, prompt=quiz_generation_prompt, output_key="quiz", verbose=True)

# Review chain
review_chain = LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key="review", verbose=True)



# Combine both chain using SequentialChain
generate_evaluation_chain = SequentialChain(
    chains=[quiz_chain, review_chain],
    input_variables=["text", "number", "subject", "tone", "response_json"],
    output_variables=["quiz", "review"],
    verbose=True,
)
