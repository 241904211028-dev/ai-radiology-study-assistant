"""
AI-Powered Radiology Study Assistant Using Generative AI
A Streamlit Web Application for Medical Students and Examination Revision.
"""

import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

# 1. Page Configuration (Blue & White Medical Theme)
st.set_page_config(
    page_title="AI Radiology Study Assistant",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Professional Blue-and-White Medical Aesthetics
st.markdown("""
<style>
    .main-header {
        color: #0c4a6e;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 700;
        margin-bottom: 0px;
    }
    .sub-header {
        color: #0284c7;
        font-size: 1.1rem;
        margin-bottom: 15px;
    }
    .disclaimer-box {
        background-color: #f0f9ff;
        border-left: 4px solid #0284c7;
        padding: 12px;
        border-radius: 6px;
        margin-bottom: 20px;
        font-size: 0.9rem;
        color: #0369a1;
    }
    .stButton>button {
        background-color: #0284c7;
        color: white;
        border-radius: 6px;
        border: none;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #0369a1;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# 2. Load Environment Variables (.env file)
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Gemini Client using the official google-genai SDK
@st.cache_resource
def get_gemini_client():
    if not API_KEY:
        return None
    try:
        return genai.Client(api_key=API_KEY)
    except Exception as e:
        st.error(f"Error initializing Gemini Client: {e}")
        return None

client = get_gemini_client()

# System Instruction for Academic Radiology Tutor
SYSTEM_INSTRUCTION = """
You are the "AI-Powered Radiology Study Assistant", an expert academic medical imaging tutor.
Your role is to guide medical students, radiology residents, and radiographers preparing for exams.

Instructions:
1. Explain concepts in clear, simple English with bullet points and bold technical terms.
2. Provide concrete clinical imaging examples (e.g. T1 vs T2 MRI signal, Hounsfield units on CT).
3. Focus on high-yield college examination points, classic signs, and viva tips.
4. STRICT SAFETY DISCLAIMER: This tool is exclusively for academic education. NEVER provide a patient-specific diagnosis or individualized medical advice.
5. In radiation physics, always emphasize radiation safety (ALARA: As Low As Reasonably Achievable).
"""

# 3. Sidebar Configuration
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1516549655169-df83a0774514?auto=format&fit=crop&w=300&q=80", use_container_width=True)
    st.title("🩺 RadAI Navigation")
    st.markdown("**Academic Exam Edition**")
    
    app_mode = st.radio(
        "Choose Feature:",
        [
            "💬 AI Radiology Tutor",
            "📝 Short Notes Generator",
            "🎯 10 MCQ Exam Quiz",
            "📑 Topic Summarizer"
        ]
    )
    
    st.markdown("---")
    selected_subject = st.selectbox(
        "Select Radiology Modality:",
        [
            "MRI (Magnetic Resonance Imaging)",
            "CT Scan (Computed Tomography)",
            "X-Ray & Fluoroscopy",
            "Ultrasound & Doppler",
            "Radiation Physics & Safety",
            "Nuclear Medicine & PET-CT"
        ]
    )
    
    st.markdown("---")
    if app_mode == "💬 AI Radiology Tutor":
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    st.markdown("### 🎓 Exam Tips")
    st.info("Tip: In exams, always describe the imaging modality, projection/sequence, primary finding, and differential diagnosis!")

# 4. Header Banner & Disclaimer
col1, col2 = st.columns([4, 1])
with col1:
    st.markdown("<h1 class='main-header'>AI-Powered Radiology Study Assistant</h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='sub-header'>Current Subject: <strong>{selected_subject}</strong> | Powered by Google Gemini Generative AI</p>", unsafe_allow_html=True)

with col2:
    if client:
        st.success("🟢 Gemini AI Active")
    else:
        st.warning("⚠️ API Key Needed in .env")

st.markdown("""
<div class='disclaimer-box'>
    <strong>⚠️ Educational & Academic Disclaimer:</strong> This application is designed solely for college examination preparation and academic medical education. It does NOT provide patient diagnosis or medical treatment advice.
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# FEATURE 1: AI RADIOLOGY TUTOR (CHATBOT)
# -------------------------------------------------------------
if app_mode == "💬 AI Radiology Tutor":
    st.subheader(f"💬 Interactive Radiology Tutor - {selected_subject}")
    st.caption("Ask any conceptual, anatomical, or technical question about this modality.")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": f"Hello! I am your AI Radiology Study Assistant. Ask me anything about **{selected_subject}**, such as imaging physics, image weighting, normal anatomy, or common pathologies!"
            }
        ]

    # Render previous conversation
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User Input
    if user_prompt := st.chat_input(f"Ask a question about {selected_subject}..."):
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        with st.chat_message("assistant"):
            if client:
                with st.spinner("AI Tutor is preparing your exam-oriented response..."):
                    try:
                        full_prompt = f"Subject: {selected_subject}\nStudent Query: {user_prompt}\nProvide a detailed, bulleted, exam-oriented response with examples and viva tips."
                        response = client.models.generate_content(
                            model="gemini-2.5-flash",
                            contents=full_prompt,
                            config=types.GenerateContentConfig(
                                system_instruction=SYSTEM_INSTRUCTION
                            )
                        )
                        bot_reply = response.text
                        st.markdown(bot_reply)
                        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                    except Exception as e:
                        err_msg = f"Error communicating with Gemini API: {str(e)}"
                        st.error(err_msg)
            else:
                demo_reply = f"**[Offline Demo Mode]** You asked: '{user_prompt}' regarding **{selected_subject}**.\n\nTo enable live generative AI tutoring, add your free GEMINI_API_KEY in the '.env' file!\n\n**Key Concept:** Focus on modality physics, diagnostic indications, and classic exam signs."
                st.markdown(demo_reply)
                st.session_state.messages.append({"role": "assistant", "content": demo_reply})

# -------------------------------------------------------------
# FEATURE 2: SHORT NOTES GENERATOR
# -------------------------------------------------------------
elif app_mode == "📝 Short Notes Generator":
    st.subheader("📝 High-Yield Revision Notes Generator")
    st.caption("Generate concise, structured study notes tailored for quick exam revision.")

    topic = st.text_input("Enter Topic or Concept:", placeholder="e.g. Diffusion-Weighted MRI, CT Radiation Dose, Silhouette Sign")
    
    col_a, col_b = st.columns([1, 4])
    with col_a:
        generate_btn = st.button("Generate Notes", use_container_width=True)

    if generate_btn:
        if not topic:
            st.warning("Please enter a topic name first.")
        elif not client:
            st.info("Please set GEMINI_API_KEY in .env for live generation.")
        else:
            with st.spinner(f"Synthesizing revision notes for '{topic}'..."):
                try:
                    notes_prompt = f"""
                    Create high-yield revision short notes for a radiology student on:
                    Subject: {selected_subject}
                    Topic: {topic}

                    Format required:
                    1. Definition & Core Principle
                    2. Indications & Technique
                    3. Characteristic Imaging Findings / Signs
                    4. Exam High-Yield Points & Viva Pearls
                    5. Safety / Contraindications
                    """
                    resp = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=notes_prompt,
                        config=types.GenerateContentConfig(
                            system_instruction=SYSTEM_INSTRUCTION
                        )
                    )
                    st.success("Notes Generated Successfully!")
                    st.markdown(resp.text)
                    st.download_button(
                        label="📥 Download Notes as Text",
                        data=resp.text,
                        file_name=f"{topic.replace(' ', '_')}_notes.txt",
                        mime="text/plain"
                    )
                except Exception as e:
                    st.error(f"Error: {e}")

# -------------------------------------------------------------
# FEATURE 3: 10 MCQ EXAM QUIZ GENERATOR
# -------------------------------------------------------------
elif app_mode == "🎯 10 MCQ Exam Quiz":
    st.subheader(f"🎯 10 Multiple-Choice Questions (MCQ) Generator - {selected_subject}")
    st.caption("Generate exam-standard MCQs with 4 options, correct answers, and thorough rationales.")

    quiz_topic = st.text_input("Focus Area / Topic (Optional):", placeholder="e.g. Brain MRI, Contrast media, ALARA principle")
    difficulty = st.select_slider("Select Examination Difficulty:", options=["Undergraduate / Beginner", "Standard College Exam", "Postgraduate / Advanced"])

    if st.button("Generate 10 MCQs", use_container_width=False):
        if not client:
            st.info("Showing pre-loaded examination MCQs. Set GEMINI_API_KEY for infinite dynamic questions.")
        else:
            with st.spinner("Generating 10 exam-level questions with Gemini AI..."):
                try:
                    mcq_prompt = f"""
                    Generate exactly 10 multiple-choice questions (MCQs) for an academic radiology examination.
                    Subject: {selected_subject}
                    Topic: {quiz_topic or 'Comprehensive'}
                    Difficulty: {difficulty}

                    Format each question clearly as:
                    ### Question X: [Question text]
                    A) [Option]
                    B) [Option]
                    C) [Option]
                    D) [Option]

                    **Correct Answer:** [Letter]
                    **Explanation:** [Detailed academic reason why the answer is correct and distractors are wrong]
                    """
                    resp = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=mcq_prompt,
                        config=types.GenerateContentConfig(
                            system_instruction=SYSTEM_INSTRUCTION
                        )
                    )
                    st.markdown(resp.text)
                    st.download_button(
                        label="📥 Download MCQs & Solutions",
                        data=resp.text,
                        file_name=f"{selected_subject}_10_MCQs.txt",
                        mime="text/plain"
                    )
                except Exception as e:
                    st.error(f"Error generating MCQs: {e}")

# -------------------------------------------------------------
# FEATURE 4: TOPIC SUMMARIZER
# -------------------------------------------------------------
elif app_mode == "📑 Topic Summarizer":
    st.subheader("📑 Long Concept & Textbook Summarizer")
    st.caption("Paste lengthy radiology textbook excerpts, case discussions, or lecture notes to extract core high-yield points.")

    text_to_summarize = st.text_area("Paste Content Here:", height=200, placeholder="Paste your lengthy radiology chapter or notes here...")
    
    if st.button("Summarize Concept"):
        if not text_to_summarize.strip():
            st.warning("Please paste some text to summarize.")
        elif not client:
            st.info("GEMINI_API_KEY required in .env for live AI summarization.")
        else:
            with st.spinner("Analyzing and condensing medical imaging text..."):
                try:
                    sum_prompt = f"""
                    Summarize this radiology text for examination revision:
                    Modality: {selected_subject}
                    Content:
                    {text_to_summarize}

                    Output format:
                    - **One-Sentence Core Takeaway**
                    - **Top 5 Bulleted Key Points**
                    - **Crucial Diagnostic Findings**
                    - **Quick Memory Anchor / Mnemonic**
                    """
                    resp = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=sum_prompt,
                        config=types.GenerateContentConfig(
                            system_instruction=SYSTEM_INSTRUCTION
                        )
                    )
                    st.subheader("📋 Academic Summary")
                    st.markdown(resp.text)
                except Exception as e:
                    st.error(f"Error during summarization: {e}")
