# 🎥 Video Insights AI

An AI-powered application that converts YouTube videos into structured insights.

The application downloads audio from a YouTube video, transcribes the speech, generates a summary, extracts action items, key decisions, and open questions, and allows users to ask questions about the video using Retrieval-Augmented Generation (RAG).

---

## Features

- 🎬 Process YouTube videos and local videos
- 📝 Speech-to-text transcription
- 📄 AI-generated summary
- ✅ Extract action items
- 🔑 Identify key decisions
- ❓ Extract open questions
- 💬 Chat with the transcript using RAG
- 🌐 Supports English and Hinglish

---

## Tech Stack

→ Python
→ OpenAI Whisper (local, free)
→ Sarvam AI (Hindi/Hinglish transcription)
→ LangChain LCEL (modern pipeline)
→ Mistral AI (free API)
→ ChromaDB (vector database for RAG)
→ HuggingFace Embeddings (local, free)
→ Streamlit (UI)

---

## Project Workflow

                          

                 YouTube URL / Local Video File
                              │
                              ▼
                    Input Validation
                              │
                              ▼
               Download / Extract Audio (FFmpeg)
                              │
                              ▼
          Split Audio into Smaller Chunks (30-60 sec)
                              │
                              ▼
       Speech-to-Text using Whisper / Sarvam AI API
                              │
                              ▼
            Merge All Chunks into One Transcript
                              │
                              ▼
         Generate Meeting Title using Mistral AI
                              │
                              ▼
             Generate AI Summary of Transcript
                              │
                              ▼
         Extract Important Information using LLM
        ┌─────────────┬──────────────┬──────────────┐
        │             │              │
        ▼             ▼              ▼
   Action Items   Key Decisions   Open Questions
        │             │              │
        └─────────────┴──────────────┘
                      │
                      ▼
      Create Embeddings from Transcript Chunks
                      │
                      ▼
      Store Embeddings in Chroma Vector Database
                      │
                      ▼
             Build Retrieval-Augmented (RAG) Pipeline
                      │
                      ▼
           User Asks Questions About the Meeting
                      │
                      ▼
     Retrieve Relevant Transcript Chunks from Vector DB
                      │
                      ▼
     Mistral AI Generates Context-Aware Final Answer
                      │
                      ▼
             Display Results in Streamlit Dashboard

---

## Project Screenshots

### Home Page

![Home](assets/homepage1.png)

---

### Analysis Dashboard

![Dashboard](assets/homepage2.png)

---

### Chat with Transcript

![Chat](assets/Chat.png)

---

### Transcript

![Transcript](assets/transcript.png)

---

## Installation

Clone the repository

```bash
git clone https://github.com/yourusername/video-insights.git
```

Move into the project

```bash
cd video-insights
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```

---

## Environment Variables

Create a `.env` file in the project root and add the following API keys:

```env
MISTRAL_API_KEY=your_mistral_api_key
SARVAM_API_KEY=your_sarvam_api_key
```
---

## Future Improvements

- Support multiple languages
- PDF report export
- Speaker diarization
- Cloud deployment

---

## Author

**Monika Bhadauriya**

Project Link:https://github.com/Monikabhadauriya/Video_Insights 
