# ⚖️ High Court Legal Assistant (AI Agent)

A professional AI-powered legal assistant designed for Indian Advocates and High Court utilization. Built with **Streamlit** and **Google Gemini 2.0 Flash**.

## 🚀 Features
- **🤖 AI Legal Research**: Answers queries with Indian law citations.
- **📝 Drafting Agent**: Auto-generates Bail Apps, Affidavits, etc.
- **📄 Document Analyzer**: Summarizes and finds risks in PDF legal documents.
- **🗣️ Voice Notes**: (Prototype) Audio transcription support.
- **🇮🇳 Multilingual**: Full support for English and Hindi.

## 🛠️ Tech Stack
- **Frontend**: Streamlit
- **AI Engine**: Google Gemini 2.0 Flash (`google-generativeai`)
- **PDF Processing**: `pypdf`

## 📦 How to Run Locally
1. Clone the repo.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Add your API Key in `.streamlit/secrets.toml`.
4. Run the app:
   ```bash
   streamlit run main.py
   ```

## ☁️ Deployment
This app is ready for [Streamlit Community Cloud](https://streamlit.io/cloud).
**Note**: Add `GEMINI_API_KEY` in the Advanced Settings > Secrets section during deployment.
