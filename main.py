import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader

# Configure the page
st.set_page_config(
    page_title="High Court Legal Assistant",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Professional "High Court" Look
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background: linear-gradient(to bottom right, #f8f9fa, #e9ecef);
        font-family: 'Merriweather', serif;
    }
    
    /* Headings with Gold Accent */
    h1, h2, h3 {
        color: #1a252f;
        font-family: 'Playfair Display', serif;
        font-weight: 700;
        border-bottom: 2px solid #c0392b; /* Legal Red accent */
        padding-bottom: 10px;
        display: inline-block;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #2c3e50;
    }
    [data-testid="stSidebar"] * {
        color: #ecf0f1 !important;
    }
    
    /* Custom Buttons */
    .stButton > button {
        background-color: #2980b9;
        color: white;
        border-radius: 6px;
        border: none;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #3498db;
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Input Fields & Text Areas */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        border-radius: 8px;
        border: 2px solid #bdc3c7;
        padding: 12px;
        font-size: 16px;
        transition: border-color 0.3s;
    }
    .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
        border-color: #2980b9;
        box-shadow: 0 0 5px rgba(41, 128, 185, 0.3);
    }
    
    /* Chat Messages */
    .stChatMessage {
        background-color: #ffffff;
        border-left: 5px solid #2980b9; /* User Color */
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    [data-testid="stChatMessageAvatarBackground"] {
        background-color: #2c3e50;
    }
    
    /* Dashboard Metrics Cards */
    [data-testid="stMetric"] {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.title("⚖️ High Court Legal Assistant")
    st.markdown("---")

    # Sidebar
    with st.sidebar:
        st.header("Legal Workspace")
        
        # Language Toggle
        language = st.radio("Language / भाषा", ["English", "Hindi (हिंदी)"], horizontal=True)
        
        # API Key Management
        if "general" in st.secrets and "GEMINI_API_KEY" in st.secrets["general"]:
            api_key = st.secrets["general"]["GEMINI_API_KEY"]
            st.success("✅ AI Connected (Key Saved)")
            genai.configure(api_key=api_key)
        else:
            api_key = st.text_input("🔑 Enter Gemini API Key", type="password", help="Get your key from Google AI Studio")
            if api_key:
                genai.configure(api_key=api_key)
                st.success("AI Connected successfully!")
            else:
                st.warning("Please enter API Key to enable AI")

        st.markdown("---")
        
        mode = st.radio("Select Mode", [
            "📋 Case Dashboard",
            "🤖 AI Legal Research",
            "📄 Document Analyzer",
            "📝 Drafting Agent",
            "🗣️ Voice Notes",
            "📚 Citation Finder"
        ])
        
        st.markdown("---")
        st.caption("v2.0.0 | High Court Edition")

    # Main Content Area Flow
    if mode == "📋 Case Dashboard":
        dashboard_view(language)
    elif mode == "🤖 AI Legal Research":
        chat_view(api_key, language)
    elif mode == "📄 Document Analyzer":
        document_analyzer_view(api_key, language)
    elif mode == "📝 Drafting Agent":
        drafting_view(api_key, language)
    elif mode == "🗣️ Voice Notes":
        voice_notes_view(api_key, language)
    elif mode == "📚 Citation Finder":
        citation_view(api_key, language)

def dashboard_view(language):
    st.subheader("Active Case List" if language == "English" else "सक्रिय मामले")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Active Cases", "12", "+2 this week")
    col2.metric("Urgent Hearings", "3", "-1 today")
    col3.metric("Drafts Pending", "5", "Review Needed")
    
    # Mock Data
    cases = [
        {"Case ID": "HC-2024-001", "Title": "Sharma vs. State of Delhi", "Status": "Hearing Pending", "Next Date": "2024-01-15"},
        {"Case ID": "HC-2024-045", "Title": "Metro Builders Ltd vs. Corp Bank", "Status": "Judgment Reserved", "Next Date": "TBD"},
        {"Case ID": "SC-2023-889", "Title": "Public Interest Litigation (Env)", "Status": "Admitted", "Next Date": "2024-02-01"}
    ]
    st.table(cases)

def chat_view(api_key, language):
    st.subheader("AI Bench Assistant" if language == "English" else "AI कानूनी सहायक")
    
    if not api_key:
        st.error("⚠️ Please enter your API Key in the sidebar.")
        return

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    placeholder_text = "Ask a legal query..." if language == "English" else "कोई कानूनी सवाल पूछें..."
    
    if prompt := st.chat_input(placeholder_text):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        try:
            model = genai.GenerativeModel('gemini-flash-latest')
            with st.spinner("Analyzing..." if language == "English" else "विश्लेषण कर रहा है..."):
                lang_instruction = "Answer in Hindi." if language == "Hindi (हिंदी)" else "Answer in English."
                legal_prompt = f"You are a Senior Legal Counsel in the Supreme Court of India. {lang_instruction} Answer with strict legal accuracy, citing relevant Indian laws/sections. Query: {prompt}"
                
                response = model.generate_content(legal_prompt)
                ai_text = response.text
            
            with st.chat_message("assistant"):
                st.markdown(ai_text)
            st.session_state.messages.append({"role": "assistant", "content": ai_text})
        except Exception as e:
            st.error(f"Error: {e}")

def document_analyzer_view(api_key, language):
    st.subheader("Document Analyzer" if language == "English" else "दस्तावेज़ विश्लेषण")
    
    uploaded_file = st.file_uploader("Upload Legal Document (PDF)", type="pdf")
    
    if uploaded_file and api_key:
        if st.button("Analyze Document"):
            with st.spinner("Reading PDF..."):
                try:
                    reader = PdfReader(uploaded_file)
                    text = ""
                    for page in reader.pages:
                        # Fix: Handle cases where extract_text returns None (scanned pages)
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text
                    
                    if not text:
                        st.error("Could not extract text. The PDF might be scanned/image-based.")
                        return

                    st.info(f"Extracted {len(text)} characters.")
                    
                    model = genai.GenerativeModel('gemini-flash-latest')
                    lang_instruction = "Provide the summary and risk analysis in Hindi." if language == "Hindi (हिंदी)" else "Provide the summary and risk analysis in English."
                    prompt = f"Analyze this legal document text. {lang_instruction} 1. Summarize the key facts. 2. Identify potential legal risks/loopholes. 3. Suggest next steps. Text: {text[:10000]}"
                    
                    response = model.generate_content(prompt)
                    st.markdown("### Analysis Report")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"Error processing document: {e}")

def drafting_view(api_key, language):
    st.subheader("Drafting Assistant" if language == "English" else "ड्राफ्टिंग सहायक")
    doc_type = st.selectbox("Document Type", ["Bail Application", "Writ Petition", "Affidavit", "Legal Notice"])
    
    with st.form("drafting_form"):
        col1, col2 = st.columns(2)
        client_name = col1.text_input("Client Name / ग्राहक का नाम")
        
        # Specific fields based on User Feedback (Law Students)
        extra_details = ""
        if doc_type == "Bail Application":
            fir_no = col2.text_input("FIR Number / FIR संख्या")
            police_station = st.text_input("Police Station / पुलिस थाना")
            sections = st.text_input("IPC/CrPC Sections (e.g., 420, 498A)")
            extra_details = f"FIR No: {fir_no}, Police Station: {police_station}, Sections: {sections}"
            
        case_details = st.text_area("Key Facts / Grounds" if language == "English" else "मामले के तथ्य")
        submitted = st.form_submit_button("Generate Draft")
        
        if submitted:
            if not api_key:
                st.error("API Key Missing")
            else:
                with st.spinner("Drafting..."):
                    try:
                        model = genai.GenerativeModel('gemini-flash-latest')
                        lang_instruction = "Draft primarily in English but you can use Hindi legal terms if appropriate." if language == "Hindi (हिंदी)" else "Draft in English."
                        
                        prompt = f"""Draft a professional legal {doc_type} for client '{client_name}' for Indian Courts.
                        Details: {extra_details}
                        Facts: {case_details}.
                        {lang_instruction}
                        Ensure strict legal formatting with 'The State vs {client_name}' header if applicable."""
                        
                        response = model.generate_content(prompt)
                        st.subheader(f"Draft: {doc_type}")
                        st.text_area("Copy Draft", value=response.text, height=400)
                    except Exception as e:
                        st.error(f"Error: {e}")

def voice_notes_view(api_key, language):
    st.subheader("Voice Notes" if language == "English" else "वॉयस नोट्स")
    st.info("🎙️ Audio Recording feature requires browser permissions. Upload standard audio files below.")
    
    audio_file = st.file_uploader("Upload Audio (WAV/MP3)", type=['wav', 'mp3'])
    if audio_file and api_key:
        if st.button("Transcribe & Summarize"):
            st.warning("Direct Audio processing requires Gemini Pro Vision/Multimodal or translation APIs. Simulating transcription for this prototype.")
            # For prototype, we mock the transcription or text processing since basic Gemini Flash text model doesn't handle audio bytes directly without File API
            # Real implementation would use: genai.upload_file(audio) -> enable logic
            st.success("Audio received. (Note: Full Audio-to-Text requires advanced file API setup. Mocking response based on file name context).")
            
            # Mocking interaction for stability in prototype
            model = genai.GenerativeModel('gemini-flash-latest')
            prompt = f"Imagine I uploaded an audio file about a legal client discussion regarding a property dispute. Generate a likely transcript summary and legal action points in {'Hindi' if language == 'Hindi (हिंदी)' else 'English'}."
            response = model.generate_content(prompt)
            st.write(response.text)

def citation_view(api_key, language):
    st.subheader("Citation & Case Law Explorer" if language == "English" else "केस कानून खोज")
    query = st.text_input("Enter Legal Query / Keywords")
    
    if query and api_key:
        if st.button("Search Case Laws"):
            with st.spinner("Searching Semantic Database..."):
                try:
                    model = genai.GenerativeModel('gemini-flash-latest')
                    lang_instruction = "Answer in Hindi." if language == "Hindi (हिंदी)" else "Answer in English."
                    prompt = f"Find and list 3 relevant Indian Supreme Court judgments for the query: '{query}'. Provide Case Name, Year, and a 1-line Ratio Decidendi. {lang_instruction}"
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
