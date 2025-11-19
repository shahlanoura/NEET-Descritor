# NEET Descriptor 🤖📚

A smart, AI-powered chatbot designed to revolutionize NEET (National Eligibility cum Entrance Test) preparation. This application leverages CrewAI agents and RAG (Retrieval-Augmented Generation) to provide a personalized learning experience, including generating custom question papers, conducting mock tests, and delivering detailed performance analytics.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![CrewAI](https://img.shields.io/badge/CrewAI-0A0A0A?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## ✨ Features

- **📄 Smart PDF Processing**: Upload chapter PDFs; the RAG agent reads and understands the content.
- **🧠 AI Question Paper Generation**: CrewAI agents generate new, context-aware question papers based on uploaded content and previous year patterns.
- **📝 Conduct Mock Tests**: Take the generated tests in an interactive, chatbot-led environment.
- **📊 Performance Analytics**: Get immediate results with a detailed breakdown of strengths and weaknesses.
- **🎯 Focus Area Recommendations**: Receive AI-curated insights on which topics and areas need more focus.

## 🏗️ Architecture & Workflow

1.  **Student Onboarding**: The student enters the chatbot and uploads a chapter PDF.
2.  **RAG Processing**: The RAG agent processes the PDF, chunks the text, and creates a searchable knowledge base.
3.  **CrewAI Orchestration**: A CrewAI crew, consisting of specialized agents (like `QuestionPaperGeneratorAgent` and `EvaluationAgent`), is formed.
4.  **Question Paper Generation**: The crew uses the RAG context and a database of previous year questions to create a new, unique question paper.
5.  **Mock Test & Evaluation**: The chatbot administers the test, collects answers, and evaluates them.
6.  **Result & Feedback**: The student receives a score and a detailed report highlighting areas for improvement.

## 🛠️ Tech Stack

- **Framework**: `Streamlit`
- **AI/ML**: `OpenAI GPT API`, `CrewAI`, `LangChain` (for RAG)
- **Language**: `Python`
- **Vector Store**: `ChromaDB` / `FAISS`
- **PDF Processing**: `PyPDF2` or `pdfplumber`

## 📦 Installation & Setup

Follow these steps to set up the project locally.

### Prerequisites

- Python 3.10 or higher
- An OpenAI API key

### Steps

1.  **Clone the repository**
    ```bash
    git clone https://github.com/shahlanoura/NEET-Descritor.git
    cd NEET-Descritor
    ```

2.  **Create a virtual environment (Recommended)**
    ```bash
    python -m venv neet_env
    # On Windows
    neet_env\Scripts\activate
    # On macOS/Linux
    source neet_env/bin/activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up Environment Variables**
    Create a `.env` file in the root directory and add your OpenAI API key.
    ```env
    OPENAI_API_KEY="your-openai-api-key-here"
    ```

5.  **Run the Streamlit Application**
    ```bash
    streamlit run app/main.py
    ```
    The application will open in your default browser.

## 🚀 Usage

1.  **Start the App**: Run the Streamlit command as above.
2.  **Enter Chat**: You will be greeted by the NEET Descriptor chatbot.
3.  **Upload PDF**: Use the file uploader to provide a chapter PDF you want to be tested on.
4.  **Generate Test**: The AI will process the PDF and generate a custom question paper.
5.  **Take the Test**: Answer the questions presented by the chatbot one by one.
6.  **View Results**: After completing the test, you will instantly receive your score and a personalized study plan.

## 🤖 CrewAI Agents

This project utilizes a multi-agent crew:

- **RAG Agent**: Specializes in retrieving relevant information from the uploaded PDFs and the knowledge base of previous year questions.
- **Question Paper Generator Agent**: An expert in NEET patterns, responsible for creating balanced and challenging question papers.
- **Evaluation Agent**: Assesses the student's answers, provides scores, and generates analytical feedback.


## 🤝 Contributing

We welcome contributions! Please feel free to submit issues, fork the repository, and create pull requests.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [CrewAI](https://www.crewai.com/) for the powerful multi-agent framework.
- [OpenAI](https://openai.com/) for the GPT API.
- [Streamlit](https://streamlit.io/) for making web app development so simple.
