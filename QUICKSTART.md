# 🚀 Quick Start Guide - Cluster and Persona Agent

## 3-Minute Setup

### Step 1: Install (30 seconds)
```bash
pip install streamlit pandas numpy scikit-learn matplotlib seaborn Pillow
```

### Step 2: Run (10 seconds)
```bash
streamlit run cluster_persona_agent.py
```

### Step 3: Use (2 minutes)
1. **Upload** your CSV file (must include: State, Industry, Job Title, Education Level, Age_range, Years of Experience, Gender, Lead Source, is_sale)
2. **Wait** for automatic processing
3. **Review** personas ranked by conversion rate
4. **Download** results

## That's It! 🎉

Your browser will open automatically to `http://localhost:8501`

---

## Expected Output

### Left Side:
- Upload section
- Cluster analysis dashboard (4 charts)
- PCA cluster visualization

### Right Side:
- 4 persona tabs (ranked by conversion rate)
- Each shows: conversion metrics, demographics, geography, professional info, acquisition channels

### Downloads Available:
- ✅ Personas JSON
- ✅ Clustered CSV
- ✅ Dashboard PNG
- ✅ Visualization PNG

---

## Example Command Line Session

```bash
# Navigate to project directory
cd /path/to/cluster-persona-agent

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run cluster_persona_agent.py

# Output:
# You can now view your Streamlit app in your browser.
# Local URL: http://localhost:8501
# Network URL: http://192.168.1.x:8501
```

---

## Troubleshooting One-Liners

**Port in use?**
```bash
streamlit run cluster_persona_agent.py --server.port 8502
```

**Dependencies missing?**
```bash
pip install --upgrade -r requirements.txt
```

**Need to stop the app?**
Press `Ctrl+C` in the terminal

---

## CSV Format Quick Reference

**Required columns:**
```
State, Industry, Job Title, Education Level, Age_range, 
Years of Experience, Gender, Lead Source, is_sale
```

**`is_sale` values:**
- TRUE/FALSE or 1/0

**Missing values:**
- Automatically filled with "Unknown"

---

## First Time User Checklist

- [ ] Python 3.8+ installed
- [ ] Dependencies installed
- [ ] CSV file ready with correct columns
- [ ] `is_sale` column contains conversion data
- [ ] At least 100+ rows of data (500+ recommended)

---

**Ready to go?** Run `streamlit run cluster_persona_agent.py` now! 🎯
