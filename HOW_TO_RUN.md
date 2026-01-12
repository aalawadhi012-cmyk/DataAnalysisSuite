# How to Run Data Analysis Suite

This document explains all supported ways to run the **Data Analysis Suite** application.

---

## Method 1: Standard Run (Recommended)

### 1. Open terminal in the project folder
```bash
cd DataAnalysisSuite
```

### 2. Create virtual environment (first time only)
```bash
python -m venv venv
```

### 3. Activate virtual environment

**Windows**
```bash
venv\Scripts\activate
```

**Linux / macOS**
```bash
source venv/bin/activate
```

### 4. Install dependencies (first time only)
```bash
pip install -r requirements.txt
```

### 5. Run the application
```bash
streamlit run app.py
```

Open browser at:
```
http://localhost:8501
```

---

## Method 2: Quick Run (If dependencies already installed)

```bash
streamlit run app.py
```

---

## Method 3: Run using Python module

```bash
python -m streamlit run app.py
```

---

## Method 4: Run from VS Code

1. Open the project folder in VS Code
2. Open Terminal inside VS Code
3. Activate virtual environment
4. Run:
```bash
streamlit run app.py
```

---

## Method 5: Run with custom port

```bash
streamlit run app.py --server.port 8502
```

---

## Stop the Application

To stop the server:
```
Ctrl + C
```

---

## Common Errors & Fixes

### streamlit is not recognized
```bash
pip install streamlit
```

### ModuleNotFoundError
- Activate virtual environment
- Run:
```bash
pip install -r requirements.txt
```

### Dataset disappears
- Do not open the app in a new browser tab
- Use the same session

---

## Notes
- Python 3.10+ required
- No database needed
- Data is processed per session
