# Capstone Submission Checklist

Use this checklist to ensure everything is ready before submitting your Kaggle Capstone.

## 1. Repository & Code
- [ ] GitHub repository is set to Public.
- [ ] `README.md` is complete, accurate, and visually clean (ASCII graphics only).
- [ ] `requirements.txt` is updated and contains only necessary packages (`duckdb`, `matplotlib`, `pandas`, `python-dotenv`).
- [ ] `.env` is properly excluded via `.gitignore`.
- [ ] `.env.example` is present in the repository with placeholder values.
- [ ] No secrets, API keys, or passwords are committed to the codebase.

## 2. Functionality
- [ ] `python demo.py` runs flawlessly from start to finish without errors.
- [ ] The local DuckDB database (`*.duckdb`) regenerates correctly when running `python -m src.database.connection`.
- [ ] Chart images (`outputs/charts/*.png`) regenerate successfully when running the demo.
- [ ] The safety refusal mechanism successfully blocks malicious prompts during the demo.
- [ ] Streamlit UI runs with `python -m streamlit run streamlit_app.py`
- [ ] Web UI can answer safe prompts.
- [ ] Web UI can display generated chart images.
- [ ] Web UI refuses unsafe prompts.
- [ ] README includes both CLI and Web UI run instructions.

## 3. Submission Materials
- [ ] YouTube video is recorded, uploaded, and under 5 minutes in length.
- [ ] Video clearly demonstrates the `demo.py` execution and highlights safety features.
- [ ] Kaggle Writeup is finalized, proofread, and under 2500 words.
- [ ] Screenshots/media gallery prepared (e.g., screenshots of terminal output and generated charts).
- [ ] Final project URL/link is copied and ready for submission.
