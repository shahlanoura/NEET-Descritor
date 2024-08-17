from crewai import Task

def create_research_task(tools, researcher):
    return Task(
        description="Analyze the provided documents to identify key content related to {topic}. Extract relevant information to create exam-oriented multiple choice questions.",
        expected_output="""Generate {num_questions} multiple choice questions and answers based on the content of the documents for {topic}. Each question should have four options labeled A, B, C, and D, with one correct answer. formate is like 
1. [Question]
A. [Option A]
B. [Option B]
C. [Option C]
D. [Option D]
Correct Answer: [Correct Answer]
Explanation of question:[explanation of question]
focus area of question:[Focus Area of question]""",
        tools=[tools],
        agent=researcher,
    )
