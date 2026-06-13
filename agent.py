import os
import google.generativeai as genai
from dotenv import load_dotenv
import json

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")

def summarize_notes(text):

    prompt = f"""
    Summarize these study notes.

    Format your response as:

    ## Key Concepts
    ## Important Definitions
    ## Exam Tips

    Notes:
    {text[:15000]}
    """

    response = model.generate_content(prompt)

    return response.text

def generate_quiz(text):

    prompt = f"""

Create exactly 5 multiple choice questions from these notes.

Rules:
- Return ONLY valid JSON.
- No markdown.
- No explanation outside JSON.
- Each question must have 4 options.
- Include correct answer and explanation.

Format:

[
{{
"question":"",
"options":["","","",""],
"answer":"",
"explanation":""
}}
]


Notes:

{text[:12000]}

"""

    response = model.generate_content(prompt)

    return response.text


def ask_notes(notes, question):

    prompt = f"""
    You are a study assistant.

    Answer ONLY using the uploaded notes.

    If the answer is not present in the notes, say:
    "I could not find that information in the uploaded notes."

    Notes:
    {notes[:15000]}

    Question:
    {question}
    """

    response = model.generate_content(prompt)

    return response.text

def generate_flashcards(text):
    prompt = f"""
    Create exactly 8 flashcards from the uploaded study notes.
    Each flashcard must have a 'front' (concept, question, or term) and a 'back' (definition, answer, or explanation).

    Return ONLY valid JSON.
    Do not add markdown or extra text.

    Format:
    [
      {{
        "front": "Front of card",
        "back": "Back of card"
      }}
    ]

    Notes:
    {text[:15000]}
    """

    response = model.generate_content(
        prompt,
        generation_config={"response_mime_type": "application/json"}
    )

    return response.text


