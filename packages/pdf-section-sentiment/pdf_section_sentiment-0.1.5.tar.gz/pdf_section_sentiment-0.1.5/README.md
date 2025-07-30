# PDF Section Sentiment

[![PyPI version](https://badge.fury.io/py/pdf-section-sentiment.svg)](https://pypi.org/project/pdf-section-sentiment/)

A lightweight CLI tool to extract structured sections from PDFs and perform sentiment analysis on each section.

---

## 🚀 Features

- Extracts headers and sections from PDFs
- Supports Markdown-like structure
- Performs sentiment scoring (`-1` to `+1`)
- Labels sentiment as `positive`, `neutral`, or `negative`
- Outputs clean JSON

---

## 📦 Installation

```bash
pip install pdf-section-sentiment

## ⚙️ Usage
pdf-extract --input path/to/document.pdf --output sections.json
pdf-sentiment --input sections.json --output sentiment.json

## 📝 Output Format
[
  {
    "header": "Executive Summary",
    "content": "Lyft reported strong revenue growth and operational efficiency...",
    "sentiment_score": 0.28,
    "sentiment": "positive"
  },
  {
    "header": "Risk Factors",
    "content": "There is uncertainty in market regulation...",
    "sentiment_score": -0.15,
    "sentiment": "negative"
  }
]

## 🧪 Example
pdf-extract --input data/Lyft-Annual.pdf --output output/sections.json
pdf-sentiment --input output/sections.json --output output/sentiment.json
