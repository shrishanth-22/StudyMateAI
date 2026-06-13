import streamlit as st
from pdf_reader import extract_text
from agent import summarize_notes, generate_quiz, ask_notes, generate_flashcards
import json

st.set_page_config(
    page_title="StudyMate AI",
    page_icon="📚"
)

st.title("📚 StudyMate AI")
st.markdown(
    """
    ### Your Personal AI Study Assistant

    Upload your notes and let AI help you:
    - 📖 Summarize concepts
    - 📝 Generate quizzes
    - 🤖 Answer questions from your notes
    """
)


with st.sidebar:

    st.header("📂 Upload Notes")

    uploaded_file = st.file_uploader(
        "Choose PDF",
        type=["pdf"]
    )

    st.info(
        "Upload your lecture notes, textbooks, or study material."
    )

    if uploaded_file and "num_pages" in st.session_state:
        st.write("---")
        with st.container(border=True):
            st.markdown(f"""
            ### 📄 PDF Info
            **File:**  
            `{uploaded_file.name}`
            
            **Pages:** `{st.session_state.num_pages}`
            
            **Characters:** `{len(st.session_state.extracted_text):,}`
            
            **AI Status:** AI Ready ✅
            """)

if uploaded_file:
    if "current_file" not in st.session_state or st.session_state.current_file != uploaded_file.name:
        st.session_state.current_file = uploaded_file.name
        for key in ["quiz", "summary", "chat_answer", "chat_question", "quiz_submitted", "flashcards", "card_index", "card_flipped", "extracted_text", "num_pages"]:
            if key in st.session_state:
                del st.session_state[key]

    if "extracted_text" not in st.session_state:
        with st.spinner("📚 Reading PDF and extracting text..."):
            text, num_pages = extract_text(uploaded_file)
            st.session_state.extracted_text = text
            st.session_state.num_pages = num_pages
            st.rerun()
    else:
        text = st.session_state.extracted_text
        num_pages = st.session_state.num_pages

    st.success("PDF processed successfully!")

    with st.expander("📄 View Extracted Text"):
        st.text_area(
            "Content",
            text,
            height=300
        )
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📖 AI Summary", "📝 Smart Quiz", "🎴 Flashcards", "🤖 Study Chat"]
    )

    with tab1:
        if st.button("Generate AI Summary"):
            with st.spinner("🧠 AI is understanding your notes and summarizing..."):
                try:
                    st.session_state.summary = summarize_notes(text)
                except Exception as e:
                    st.error(f"⚠️ AI Service error: {e}")
                    print(f"Summary error: {e}")

        if "summary" in st.session_state:
            st.subheader("AI Summary")
            st.markdown(st.session_state.summary)
            
            st.download_button(
                label="📥 Download Summary (.md)",
                data=st.session_state.summary,
                file_name=f"{uploaded_file.name.replace('.pdf', '')}_summary.md",
                mime="text/markdown"
            )

    with tab2:
        st.subheader("📝 Smart Quiz")
        if "quiz" not in st.session_state:
            if st.button("Generate Quiz"):
                with st.spinner("Creating quiz..."):
                    try:
                        quiz_text = generate_quiz(text)

                        quiz_text = quiz_text.replace("```json", "")
                        quiz_text = quiz_text.replace("```", "")
                        quiz_text = quiz_text.strip()

                        st.session_state.quiz = json.loads(quiz_text)

                        st.session_state.quiz_submitted = {}

                        st.rerun()

                    except json.JSONDecodeError:
                        st.error(
                            "⚠️ AI returned invalid quiz format. Try again."
                        )

                    except Exception as e:
                        if "429" in str(e):
                            st.error(
                                """
                                ⚠️ Gemini API quota reached.

                                Please wait for quota reset or use another API key.
                                """
                            )
                        else:
                            st.error(f"AI Error: {e}")

        if "quiz" in st.session_state:

            if "quiz_submitted" not in st.session_state:
                st.session_state.quiz_submitted = {}
            score = 0
            for i, q in enumerate(st.session_state.quiz):
                st.markdown(
                    f"### Question {i+1}"
                )

                st.write(q["question"])
                answered = i in st.session_state.quiz_submitted
                selected = st.radio(
                    "Select option:",
                    q["options"],
                    key=f"question_{i}",
                    index=None,
                    disabled=answered
                )
                if answered:
                    user_answer = st.session_state.quiz_submitted[i]
                    if user_answer == q["answer"]:
                        st.success("✅ Correct!")
                        score += 1
                    else:
                        st.error(
                            f"❌ Wrong! Correct answer: {q['answer']}"
                        )

                    st.info(
                        f"💡 Explanation: {q['explanation']}"
                    )

                else:
                    if st.button(
                        f"Submit Question {i+1}",
                        key=f"submit_{i}"
                    ):
                        if selected is None:
                            st.warning(
                                "Please select an option first."
                            )

                        else:
                            st.session_state.quiz_submitted[i] = selected
                            st.rerun()
                st.divider()

            if len(st.session_state.quiz_submitted) == len(st.session_state.quiz):
                st.success(
                    f"🏆 Quiz Completed! Score: {score}/{len(st.session_state.quiz)}"
                )
                if st.button("Restart Quiz"):
                    del st.session_state.quiz_submitted
                    st.rerun()
    with tab3:
        st.subheader("🎴 Study Flashcards")

        if "flashcards" not in st.session_state:
            if st.button("Generate Flashcards"):
                with st.spinner("🎴 AI is generating interactive flashcards..."):
                    try:
                        fc_text = generate_flashcards(text)
                        fc_text = fc_text.replace("```json", "").replace("```", "").strip()
                        st.session_state.flashcards = json.loads(fc_text)
                        st.session_state.card_index = 0
                        st.session_state.card_flipped = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"⚠️ AI Service error: {e}")
                        print(f"Flashcard generation error: {e}")

        if "flashcards" in st.session_state:
            card = st.session_state.flashcards[st.session_state.card_index]

            st.write(f"Card {st.session_state.card_index + 1} of {len(st.session_state.flashcards)}")
            st.progress((st.session_state.card_index + 1) / len(st.session_state.flashcards))

            st.markdown(
                f"""
                <div style="
                    width: 320px;
                    height: 320px;
                    margin: 20px auto;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    text-align: center;
                    background-color: var(--secondary-background-color, #f0f2f6);
                    border: 1px solid rgba(128, 128, 128, 0.2);
                    border-radius: 16px;
                    padding: 24px;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
                ">
                    <h5 style="color: var(--text-color, #000000); opacity: 0.6; margin: 0; font-size: 13px; text-transform: uppercase; letter-spacing: 2px;">
                        {"FRONT" if not st.session_state.card_flipped else "BACK"}
                    </h5>
                    <h3 style="color: var(--text-color, #000000); margin: 20px 0 0 0; font-size: 22px; font-weight: 500; line-height: 1.4;">
                        {"🤔 " + card["front"] if not st.session_state.card_flipped else "💡 " + card["back"]}
                    </h3>
                </div>
                """,
                unsafe_allow_html=True
            )

            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                if st.button("⬅️ Previous", disabled=st.session_state.card_index == 0, use_container_width=True):
                    st.session_state.card_index -= 1
                    st.session_state.card_flipped = False
                    st.rerun()
            with col2:
                if st.button("🔄 Flip Card", use_container_width=True):
                    st.session_state.card_flipped = not st.session_state.card_flipped
                    st.rerun()
            with col3:
                if st.button("Next ➡️", disabled=st.session_state.card_index == len(st.session_state.flashcards) - 1, use_container_width=True):
                    st.session_state.card_index += 1
                    st.session_state.card_flipped = False
                    st.rerun()

            st.write("---")
            if st.button("Reset Flashcards"):
                del st.session_state.flashcards
                if "card_index" in st.session_state:
                    del st.session_state.card_index
                if "card_flipped" in st.session_state:
                    del st.session_state.card_flipped
                st.rerun()

    with tab4:

        question = st.text_input(
            "Ask a question about your notes"
        )

        if st.button("Ask AI"):

            if question:
                with st.spinner("🤖 AI is reading your notes for an answer..."):
                    try:
                        st.session_state.chat_answer = ask_notes(text, question)
                        st.session_state.chat_question = question
                    except Exception as e:
                        st.error(f"⚠️ AI Service error: {e}")
                        print(f"Chat error: {e}")

        if "chat_answer" in st.session_state:
            st.write(f"**Q:** {st.session_state.chat_question}")
            with st.chat_message("assistant"):
                st.markdown(st.session_state.chat_answer)
    st.divider()

    st.caption(
        "Built with ❤️ using Generative AI | StudyMate AI"
    )