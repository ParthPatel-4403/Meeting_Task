# Meeting Task Assignment --- Automated Task Extraction & Assignment

## ⭐ Project Overview

This project automatically extracts actionable tasks from meeting
transcripts or audio recordings and assigns them to the most appropriate
team members using a custom rule-based logic system.

The system identifies: - Tasks - Deadlines - Priorities - Dependencies -
Suitable assignees based on skills and roles

Optional Speech-to-Text (STT) support is included for audio input.

## 📂 Project Structure

    .
    ├── run.py
    ├── stt.py
    ├── logic/
    │   ├── extractor.py
    │   ├── assignment.py
    │   ├── parser.py
    │   └── utils.py
    ├── sample_data/
    │   ├── team.json
    │   ├── sample_transcript.txt
    │   └── sample_audio.wav
    ├── outputs/
    │   ├── extracted_tasks.json
    │   └── extracted_tasks.csv
    ├── requirements.txt
    └── README.md

## ⚙️ Installation

### 1. Create virtual environment

    python -m venv venv
    source venv/bin/activate
    venv\Scripts\activate

### 2. Install dependencies

    pip install -r requirements.txt

### 3. Install spaCy model (if used)

    python -m spacy download en_core_web_sm

## 📝 Prepare Your Data

### ✔ Team Members File

Edit team roles and skills:

    sample_data/team.json

### ✔ Transcript File

    sample_data/sample_transcript.txt

### ✔ Optional Audio File

    sample_data/sample_audio.wav

## ▶️ Run Using Transcript

    python run.py --team sample_data/team.json --transcript sample_data/sample_transcript.txt --out outputs

Outputs: - outputs/extracted_tasks.json - outputs/extracted_tasks.csv

## 🎙 Run Using Audio (Optional)

1.  Choose STT method inside `stt.py`
2.  Uncomment STT block inside `run.py`

Run:

    python run.py --team sample_data/team.json --transcript audio:/path/to/audio.wav --out outputs

## 🧠 System Logic Summary

### Transcript / Audio Processing

-   Cleaning
-   Optional STT

### Task Extraction

Detects: - Action verbs - Deadlines - Priorities - Dependencies

### Assignment Logic

Matches tasks to members using: - Skills - Roles - Mentions - Context

### Output

-   JSON
-   CSV

## 📦 Submission Deliverables

-   Source code
-   requirements.txt
-   sample_data folder
-   outputs folder
-   Demo video
-   README.md

