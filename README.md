# Quiz_Generation

This project generates multiple-choice question (MCQ) quizzes from uploaded text documents.  It uses the Langchain framework with the Google Gemini language model to create quizzes, offering control over the number of questions, subject, and complexity level. The generated quizzes are presented via a Streamlit interface.


## Features

* **Input Flexibility:** Accepts both PDF and TXT files.
* **Customizable Quizzes:** Control the number of questions, subject matter, and difficulty level.
* **Langchain & Gemini Integration:** Leverages Langchain for workflow management and Google Gemini for question generation.
* **Streamlit User Interface:** Provides a user-friendly web application for quiz creation.
* **Robust Error Handling:** Includes error checks for file processing and API interactions.
* **Clear Output:** Presents the generated MCQ quiz in a well-formatted table.


## Setup

1. **Clone the Repository:**  `git clone https://github.com/pdobariya1/Quiz_Generation.git`
2. **Install Dependencies:**  `pip install -r requirements.txt`
3. **Google Cloud Setup:**
   * Create a Google Cloud project and enable the Generative AI API.
   * Create a service account, download the JSON key file, rename it to `.credential.json`, and place it in the project's root directory.  Ensure sufficient permissions for Gemini API access.
4. **Run the Application:** `streamlit run streamlitApp.py`  This will open the Streamlit app in your browser.

## Usage

1. Upload a PDF or TXT file.
2. Input the desired number of questions, subject, and complexity level.
3. Click "Generate MCQs" to create your quiz.

## Data

Sample data for testing is provided in `data.txt`.  The `experiment/Deep Learning_Quiz.csv` file shows an example of the output format.  `response.json` provides a template for the JSON structure of the generated quiz.
