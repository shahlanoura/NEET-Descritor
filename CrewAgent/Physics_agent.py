import logging
from pdf import merge_text_files
from CrewAgent.tool import txt_upload
from CrewAgent.agent import create_researcher
from CrewAgent.task import create_research_task
from CrewAgent.crew import create_crew

def generate_physics_questions(text_content, num_questions):
    try:
        previous_year_file = 'C:/Users/user/Desktop/test2/physics_previousyear_questns.txt'
        
        # Combine uploaded files with the previous year question paper
        input_file = [text_content] + [previous_year_file]
        output = "merged.pdf"
        logging.debug(f"Merging Txt files: {input_file}")

        merged_files = merge_text_files(input_file, output)
        logging.debug(f"Merged Txt: {merged_files}")

        tools = txt_upload(merged_files)
        logging.debug(f"Tools created: {tools}")

        researcher = create_researcher(tools)
        logging.debug(f"Researcher created: {researcher}")

        research_task = create_research_task(tools, researcher)
        logging.debug(f"Research task created: {research_task}")

        crew_instance = create_crew(researcher, research_task)
        logging.debug(f"Crew instance created: {crew_instance}")

        prompt = f"""
You are an AI tasked with creating multiple choice questions (MCQs) for higher secondary school physics students. The goal is to generate questions that help students prepare for their exams effectively.

*Source Material*:
1. physics textbook units (provided).
2. Previous year question papers (provided).

*Task Description*:
- Read and understand the content from the provided textbook units and previous year question papers.
- Generate {num_questions} multiple choice questions based on the previous year question papers.
- Ensure that the questions are relevant to the syllabus and exam patterns.

*Output Format*:
For each question, provide:
1. The question itself.
2. Four answer options labeled as A, B, C, and D.
3. The correct answer.
4. An explanation for the correct answer.
5.Provide a focused area of question to give feedback
6. Questions is based on the content / topic

*Additional Instructions*:
- Ensure the questions cover a variety of topics from the units and previous year question papers.
- Maintain a balance between easy, moderate, and difficult questions.
- Avoid repetition of questions.
- Provide clear and concise questions and answers.
- For graph-type questions, ensure the graph is well-labeled and the question clearly asks students to interpret it.
"""


        logging.debug(f"Prompt: {prompt}")

        result_str = crew_instance.kickoff(inputs={'prompt': prompt, 'topic': 'Physics', 'num_questions': num_questions})
        logging.debug("Generated result string: %s", result_str)
        return result_str
    except Exception as e:
        logging.error("Error in generate_physics_questions: %s", e)
        return None
