# StudyMate AI 📚

An AI-powered learning assistant that converts study material (lecture notes, textbooks, and handouts) into custom summaries, interactive quizzes, flashcards, and Q&A bots to accelerate learning.

## Features
- **📄 PDF Understanding**: Extract text seamlessly from uploaded PDF notes.
- **📖 AI Summaries**: Condense complex materials into organized key concepts, definitions, and exam tips.
- **📝 Smart Quizzes**: Auto-generate multiple-choice quizzes with feedback, answer justifications, and final score calculations.
- **🎴 AI Flashcards**: Generate interactive study cards with terms on the front and definitions on the back to test recall.
- **🤖 Study Chat (Ask AI)**: Chat with an AI assistant that answers questions *exclusively* based on the uploaded notes.

## Tech Stack
- **Python**: Core programming language.
- **Streamlit**: Modern UI frontend.
- **Google Gemini API** (`gemini-2.5-flash`): Generative AI model powering the summary, quiz, flashcard, and Q&A systems.
- **PyPDF**: PDF parsing and text extraction.
- **Python-Dotenv**: Environment variable configuration.

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd StudyMateAI
   ```

2. **Set up a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add your API Key:**
   Create a `.env` file in the root directory and add your Google Gemini API Key:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

5. **Run the Streamlit application:**
   ```bash
   streamlit run app.py
   ```

## Future Improvements
- **📅 Study Planner**: Enter your exam date and syllabus to generate an AI-powered study schedule.
- **📈 Progress Tracking**: Track quiz scores and flashcard completion history over time.
- **🎙️ Voice Explanation**: Have the AI read notes aloud or explain concepts like a teacher using audio generation.
