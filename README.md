# Reddit_Intel


**Reddit Intel** is an AI-powered app that generates detailed user personas by analyzing a Reddit user's public posts and comments. It uses Groq(llama-3.3-70b) Api to extract motivations, personality traits, frustrations, goals, and more — similar to what UX researchers build manually.

---

## 🚀 Features

- 🔗 Input a Reddit profile URL
- 📥 Fetch recent posts and comments using the Reddit API
- 🧠 Analyze text using llama-3.3-70b (LLM)
- 📝 Generate a full persona with:
  - Name, Age Range, Occupation, Location
  - MBTI-style Personality
  - Motivations, Behaviors, Frustrations
  - Summary Quote & Citations
- 🌐 Streamlit Web UI
- 📄 Download persona as `.txt` file

---

## 🛠️ Technologies Used

- **Python**
- **PRAW** – Reddit API wrapper
- **llama-3.3-70b** – LLM persona generation
- **Streamlit** – Frontend UI
- **Regex / Markdown** – Structured formatting

---

## 📦 Installation

### 1. Clone the repo
```bash
git clone https://github.com/Sanjaykmrjnv/Reddit_Intel.git
cd Reddit_Intel
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up API keys
Create a .env file in the root folder:

```bash
env
OPENAI_API_KEY=your_openai_key
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=redpersona-agent
```


