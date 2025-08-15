
# Log Classification With Hybrid Classification Framework

This project implements a hybrid log classification system, combining three complementary approaches to handle varying levels of complexity in log patterns. The classification methods ensure flexibility and effectiveness in processing predictable, complex, and poorly-labeled data patterns.

---

## Log Classification – Hybrid Approach (Regex + BERT + LLM)

An end‑to‑end log classification app with a simple web UI and a REST API. It combines:
- **Regex rules** for predictable patterns
- **Sentence Transformers + Logistic Regression** for general patterns
- **LLM fallback** (optional via GROQ) for tricky/low‑data cases

### Architecture
![Architecture](resources/arch.png)

### UI Preview
Place your UI screenshot at `resources/ui.png` and it will render here:

![App UI](resources/ui.png)

---

## Features
- Drag‑and‑drop CSV upload, live preview, validation
- Server health indicator, progress bar, clear success/error states
- Manual download button (no auto‑download after processing)
- API endpoint to classify CSVs programmatically
- Caching set to temp directories for easy deployment (Windows/Linux/Containers)

---

## Project Structure
- `app.py`: Flask application (web UI + API)
- `classify.py`: Batch utility to classify a CSV locally
- `processor_regex.py`: Regex classifier
- `processor_bert.py`: SentenceTransformer embeddings + logistic regression model loader
- `processor_llm.py`: Optional LLM fallback via GROQ (env var `GROQ_API_KEY`)
- `templates/index.html`: Frontend UI
- `models/`: Trained scikit‑learn classifier (`log_classifier.joblib`)
- `resources/`: Sample/test data and images

---

## Quickstart (Local)

### 1) Environment
```bash
python -m venv venv
# Windows PowerShell
./venv/Scripts/Activate.ps1
# macOS/Linux
source venv/bin/activate
```

### 2) Install dependencies
```bash
pip install -r requirements.txt
```

### 3) Run the web app
```bash
python app.py
```
Open `http://localhost:5000` in your browser.

Optional: classify sample CSV locally and produce `output.csv`:
```bash
python classify.py
```

---

## CSV Format
Your CSV must contain the columns:
- `source`
- `log_message`

Example rows:
```csv
source,log_message
ModernCRM,"IP 192.168.133.114 blocked due to potential attack"
BillingSystem,"User 12345 logged in."
```

The API returns a CSV with an added column `target_label`.

---
<img width="2849" height="1380" alt="image" src="https://github.com/user-attachments/assets/afee589a-f943-463d-849d-949fbaa22df9" />

<img width="2779" height="1483" alt="image" src="https://github.com/user-attachments/assets/ebfa6d4b-9155-47c0-8b67-af7dc1dbb6f2" />

