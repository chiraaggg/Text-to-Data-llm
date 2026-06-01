---
title: Text to Data LLM
emoji: 🛒
colorFrom: yellow
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
---

# ShopEasy DataBot — Text to Data

Ask questions in plain English. The AI writes SQL, runs it, and explains the results.

## Demo Dataset
- 900 orders · 150 customers · 56 products · 8 categories
- Cities: Mumbai, Delhi, Bangalore, Chennai, Hyderabad + 10 more
- Payments: UPI, Card, Cash, Wallet

## Stack
- **LangChain** SQL Agent
- **OpenAI GPT-4o / GPT-4o-mini**
- **Chainlit** UI
- **SQLite** (demo dataset)

## Setup (local)
```bash
cp .env.example .env          # add your OPENAI_API_KEY
pip install -r requirements.txt
chainlit run agent_ui.py
```
