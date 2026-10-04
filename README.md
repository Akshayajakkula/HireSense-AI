# HireSense AI

An AI-powered resume screening assistant built with Python and Streamlit.

## Features (in progress)
- Upload a resume (PDF) and extract its text
- Match resumes against a job description
- Skill extraction and gap analysis

## Tech Stack
Python 3.11, Streamlit, spaCy, NLTK, sentence-transformers, scikit-learn, Gemini API

## Setup
1. Create a virtual environment: `python -m venv venv`
2. Activate it (Windows): `venv\Scripts\activate`
3. Install packages: `pip install -r requirements.txt`
4. Create a `.env` file with: `GEMINI_API_KEY=your_key_here`
5. Run the app: `streamlit run app.py`