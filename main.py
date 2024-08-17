import streamlit as st
import json
import re
import  fitz

import logging
import CrewAgent.Chemistry_agent as Chemistry_agent
import CrewAgent.Physics_agent as Physics_agent
import CrewAgent.Biology_agent as Biology_agent
from content_relevent import is_content_relevant, subject_keywords
import numpy as np


# Set page configuration
st.set_page_config(page_title="NEET Descriptor With Agent", layout="wide")

def display_welcome_message():
    st.markdown(
        """
        <div class="header">
            <h2>Welcome to the NEET Descriptor With Agent!</h2>
            <p>This tool is designed to help NEET exam aspirants by generating multiple choice questions (MCQs) based on relevant study materials. Students can upload PDFs, take mock tests, and receive detailed feedback on their performance. The system ensures a comprehensive preparation experience by covering various topics, providing a mix of easy, moderate, and difficult questions, and offering explanations and targeted feedback to help students improve their understanding and performance.</p>
        </div>
        """, unsafe_allow_html=True
    )

# Add custom CSS for styling
st.markdown("""
    <style>
        .stApp {
            background-color: #FAF0E6;
        }
        .css-1d391kg {
            background-color: #F5E6E8;
        }
        .header {
            background-color: #D6A5A5;
            padding: 5px;
            text-align: center;
            margin-bottom: 10px;
            border-radius: 10px;
            color: #ffffff;
        }
        .header h1 {
            margin: 0;
            font-size: 2em;
        }
        .question-card {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
            border: 2px solid #D6A5A5;
        }
        .question-card h3 {
            font-size: 1.2em;
        }
        .question-card .stRadio > div {
            padding-left: 10px;
        }
        .stButton>button {
            background-color: #D6A5A5;
            color: #ffffff;
            padding: 10px 20px;
            border-radius: 10px;
        }
        .stButton>button:hover {
            background-color: #c59393;
        }
        .quiz-title {
            text-align: center;
            color: #333333;
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# Page title
st.markdown(
    """
    <div class="header">
        <h1>NEET Descriptor With Agent</h1>
    </div>
    """, unsafe_allow_html=True
)

# Initialize session state
if 'mcqs' not in st.session_state:
    st.session_state['mcqs'] = []

if 'student_answers' not in st.session_state:
    st.session_state['student_answers'] = {}

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_text_from_pdf(uploaded_pdfs):
    all_text = ""
    for pdf in uploaded_pdfs:
        try:
            doc = fitz.open(stream=pdf.read(), filetype="pdf")
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                all_text += page.get_text()
        except Exception as e:
            logging.error(f"Error reading PDF: {e}")
            st.error(f"An error occurred while reading the PDF: {e}")
    return all_text

def parse_agent_output(raw_output):
    questions = []
    try:
        # Remove irrelevant text before "Final Answer:"
        cleaned_output = re.sub(r'Thought:.*?Final Answer:', '', raw_output, flags=re.DOTALL).strip()

        # Split the output by the numbered questions (e.g., 1., 2., 3.)
        question_blocks = re.split(r'\d+\.\s', cleaned_output)[1:]

        for block in question_blocks:
            lines = block.strip().split('\n')
            question_text = lines[0].strip()

            options = []
            correct_answer = None
            explanation = "No explanation available."
            focus_area = "General Review"  # Default value

            for line in lines[1:]:
                # Match for options
                option_match = re.match(r'^[A-D]\.\s(.+)', line)
                # Match for correct answer
                correct_answer_match = re.match(r'Correct Answer:\s([A-D])', line)
                # Match for explanation
                explanation_match = re.match(r'Explanation of question:\s(.+)', line)
                # Match for focus area
                focus_area_match = re.match(r'focus area of question:\s(.+)', line, re.IGNORECASE)

                if option_match:
                    options.append(option_match.group(1).strip())
                elif correct_answer_match:
                    correct_answer = correct_answer_match.group(1).strip()
                elif explanation_match:
                    explanation = explanation_match.group(1).strip()
                elif focus_area_match:
                    focus_area = focus_area_match.group(1).strip()

            if question_text and options and correct_answer:
                questions.append({
                    'question_text': question_text,
                    'options': options,
                    'answer': correct_answer,
                    'explanation': explanation,
                    'focus_area': focus_area  # Ensuring the focus area is added
                })

    except Exception as e:
        logging.error("Unexpected error occurred: %s", e)
    return questions


# Function to save output to JSON
def save_output_to_json(questions, filename="output.json", to_session_state=False):
    if to_session_state:
        st.session_state['mcqs'] = questions
    with open(filename, "w") as json_file:
        json.dump(questions, json_file, indent=4)

# Function to calculate results
def calculate_results(student_answers, correct_answers):
    correct_count = 0
    result_summary = {'results': {}}

    for q_num, student_answer in student_answers.items():
        student_answer = student_answer.strip().upper()
        correct_answer = correct_answers.get(q_num, '').strip().upper()

        logging.debug(f"Comparing Question {q_num}: Student: '{student_answer}', Correct: '{correct_answer}'")

        if student_answer == correct_answer:
            correct_count += 1
            result_summary['results'][q_num] = "Correct"
        else:
            result_summary['results'][q_num] = f"Incorrect (Correct: {correct_answer})"
            logging.debug(f"Incorrect Answer: Question {q_num}, Student: {student_answer}, Correct: {correct_answer}")

    result_summary['score'] = correct_count
    result_summary['total'] = len(student_answers)
    logging.debug(f"Results Summary: {result_summary}")

    return result_summary

# Function to display MCQs in Streamlit
def display_mcqs(questions):
    student_answers = {}
    correct_answers = {}

    for i, question in enumerate(questions):
        st.markdown(
            f"""
            <div class="question-card">
                <h5>Question {i + 1}: {question['question_text']}</h5>
            """, unsafe_allow_html=True
        )

        if 'http' in question['question_text']:  # Check if it's a graph-based question
            st.image(question['question_text'], caption=f'Graph for Question {i + 1}')
        else:
            options = question['options']
            
            option_mapping = {f"{chr(65+j)}": option for j, option in enumerate(options)}
            answer = st.radio(
                f"Select your answer for Question {i + 1}", 
                [f"{key}: {value}" for key, value in option_mapping.items()], 
                key=f"q{i}"
            )
            
            selected_letter = answer.split(':')[0]
            
            student_answers[f"Question {i + 1}"] = selected_letter
            correct_answers[f"Question {i + 1}"] = question['answer']
            
            logging.debug(f"Displayed Options for Question {i + 1}: {options}")
            logging.debug(f"Selected Answer for Question {i + 1}: {selected_letter}")
            logging.debug(f"Correct Answer for Question {i + 1}: {question['answer']}")
        
        st.markdown("</div>", unsafe_allow_html=True)

    return student_answers, correct_answers

# Function to generate detailed feedback
def generate_detailed_feedback(student_answers, correct_answers, questions):
    detailed_feedback = ""
    focus_areas = {}

    for q_num, student_answer in student_answers.items():
        correct_answer = correct_answers.get(q_num, '').strip().upper()
        student_answer = student_answer.strip().upper()

        if student_answer != correct_answer:
            question_idx = int(q_num.split(' ')[1]) - 1
            question = questions[question_idx]
            explanation = question.get('explanation', 'No explanation available.')
            focus_area = question.get('focus_area', 'General Review')

            # Formatting the detailed feedback
            detailed_feedback += f"Question {q_num.split(' ')[1]}: {question['question_text']}\n"
            detailed_feedback += f"Your Answer: {student_answer}\n"
            detailed_feedback += f"Correct Answer: {correct_answer}\n"
            detailed_feedback += f"Explanation: {explanation}\n\n"

            if focus_area in focus_areas:
                focus_areas[focus_area] += 1
            else:
                focus_areas[focus_area] = 1
        else:
            # Append correct answer feedback
            detailed_feedback += f"Question {q_num.split(' ')[1]}: Correct\n"

    # Adding the summary of focus areas
    if focus_areas:
        detailed_feedback += "Summary of Focus Areas:\n"
        for area, count in focus_areas.items():
            detailed_feedback += f"- {area}: {count} question(s)\n"
    else:
        detailed_feedback += "Great job! All your answers are correct."

    return detailed_feedback


# Sidebar for quiz parameters
if 'quiz_generated' not in st.session_state:
    st.session_state['quiz_generated'] = False

# Sidebar for quiz parameters
with st.sidebar:
    st.header("Mock Test Settings")
    
    subject = st.selectbox("Select Subject", ["Chemistry", "Physics", "Biology"])
    
    uploaded_pdf = st.file_uploader("Upload PDF Content", type=["pdf"], accept_multiple_files=True)
    num_questions = st.number_input("Number of Questions", min_value=1, max_value=50, value=5, step=1)

    if st.button("Generate Quiz"):
        if uploaded_pdf:
            try:
                text_content = extract_text_from_pdf(uploaded_pdf)

                if not is_content_relevant(text_content, subject_keywords[subject]):
                    st.error("Please upload topic related content.")
                else:
                    if subject == "Chemistry":
                        result = Chemistry_agent.generate_chemistry_questions(text_content, num_questions)
                    elif subject == "Physics":
                        result = Physics_agent.generate_physics_questions(text_content, num_questions)
                    elif subject == "Biology":
                        result = Biology_agent.generate_biology_questions(text_content, num_questions)
                    result_str = str(result)
                    logging.debug(f"Generated result string: {result_str}")
                    
                    if result_str:
                        structured_questions = parse_agent_output(result_str)
                        save_output_to_json(structured_questions, to_session_state=True)
                        st.session_state['quiz_generated'] = True
                    else:
                        st.error("No result string returned. Please check the agent functions.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
                logging.error(f"Error generating quiz: {e}")
        else:
            st.error("Please upload a PDF file to generate a quiz.")

# Display welcome message or quiz based on session state
if not st.session_state['quiz_generated']:
    display_welcome_message()
else:
    st.markdown(
    f"""
    <div class="quiz-title">
        <h2>Generated Quiz for {subject}</h2>
        <p>Based on the content of the '{subject}' document, here are the questions:</p>
    </div>
    """, unsafe_allow_html=True
    )

    if st.session_state['mcqs']:
        student_answers, correct_answers = display_mcqs(st.session_state['mcqs'])

        if st.button("Submit Quiz", key="submit_quiz_button"):
            results = calculate_results(student_answers, correct_answers)
            st.write(f"Your Score: {results['score']} / {results['total']}")
            for q, result in results['results'].items():
                st.write(f"{q}: {result}")
            feedback = generate_detailed_feedback(student_answers, correct_answers, st.session_state['mcqs'])
            st.write(feedback)
    else:   
        st.write("No questions available.")
