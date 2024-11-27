import re
import json
import traceback
import pandas as pd
import streamlit as st

from langchain_community.callbacks.manager import get_openai_callback

from src.mcqgenerator.logger import logging
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.MCQGenerator import generate_evaluation_chain


# Loading json file
response_json = r"/home/petpooja-739/Learning/Quiz_Generation/response.json"
with open(response_json, 'r') as file:
    RESPONSE_JSON = json.load(file)


# App title
st.title("Quiz Generation Application with LangChain 🦜⛓️")

# Streamlit Form
with st.form("user_input"):
    # File Upload
    uploaded_file = st.file_uploader("Upload a PDF or txt file")
    
    # Input Fields
    mcq_counts = st.number_input("No. of MCQs", min_value=3, max_value=50)
    
    # Subject
    subject = st.text_input("Insert Subject", max_chars=30)
    
    # Quiz Tone
    tone = st.text_input("Complexity level of Questions", max_chars=20, placeholder="simple")
    
    # Add Button
    button = st.form_submit_button("Generate MCQs")
    
    # Check if the button is clicked and all fields have input
    if button and uploaded_file is not None and mcq_counts and subject and tone:
        with st.spinner("Loading..."):
            try:
                text = read_file(uploaded_file)
                
                # Count tokens and the cost of API call
                with get_openai_callback() as cb:
                    response = generate_evaluation_chain(
                        {
                            "text": text,
                            "number": mcq_counts,
                            "subject": subject,
                            "tone": tone,
                            "response_json": json.dumps(RESPONSE_JSON)
                        }
                    )
            
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error")
            
            else:
                print(f"Total Tokens: {cb.total_tokens}")
                print(f"Prompt Tokens: {cb.prompt_tokens}")
                print(f"Completion Tokens: {cb.completion_tokens}")
                print(f"Total Cost: {cb.total_cost}")
                
                if isinstance(response, dict):
                    # Extract the quiz data from the response
                    quiz = response.get("quiz", None)
                    quiz = re.search(r'\{.*\}', quiz, re.DOTALL).group(0)
                    # logging.info(quiz)
                    print(quiz)
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        if table_data is not None:
                            df = pd.DataFrame(table_data)
                            df.index = df.index + 1
                            st.table(df)
                            
                            # Display the review in a text box as well
                            st.text_area(label="review", value=response["review"], height=300)
                        
                        else:
                            st.error("Error in the table data")
                
                else:
                    st.write(response)



