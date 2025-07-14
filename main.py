import os
import praw
from dotenv import load_dotenv
from urllib.parse import urlparse
import textwrap
from groq import Groq
load_dotenv()

# LLM API details
client = Groq(api_key=os.getenv("groq_key"))

# Reddit API details
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

# Extract username from profile URL
def extract_username(profile_url: str):
    parsed = urlparse(profile_url)
    return parsed.path.strip("/").split("/")[-1]




# Getting Comments and Posts from a Reddit User
def fetch_user_activity(username: str, limit: int = 100):
    try:
        user = reddit.redditor(username)
        posts = [f"[Post] {s.title}\n{s.selftext}" for s in user.submissions.new(limit=limit)]
        comments = [f"[Comment] {c.body}" for c in user.comments.new(limit=limit)]
        return posts + comments
    except Exception as e:
        print("Error fetching user activity:", e)
        return []

def chunk_text(texts, max_tokens=3000):
    """Split list of texts into manageable chunks for LLM input."""
    chunks, current_chunk = [], ""
    for t in texts:
        if len(current_chunk) + len(t) < max_tokens:
            current_chunk += "\n\n" + t
        else:
            chunks.append(current_chunk)
            current_chunk = t
    if current_chunk:
        chunks.append(current_chunk)
    return chunks


def build_persona_prompt(user_text: str, profile_url: str):
    return f"""
You are an expert UX researcher and behavioral analyst.

Given the Reddit user activity(posts + comments) below, generate a structured **User Persona** with the following:

- Name: {extract_username(profile_url)} or Name of person if mentioned
- Age Range (guess if possible)
- Occupation (e.g., student, developer, etc.)
- Status (e.g., single, married, etc.)
- Location (guess if mentioned)
- Archetype (The Creator, Explorer, Helper, etc.)
- Motivations (bullets with reasoning)
- Personality Traits (MBTI-style e.g., INTJ or descriptive tags)
- Behavior & Habits (patterns in lifestyle, hobbies, speech)
- Frustrations (specific annoyances or problems expressed)
- Goals & Needs (what they're trying to accomplish)
- Summary Quote (from their own words or summarizing them)
- Citations (original post/comment that supports each insight)

Activity:
{textwrap.shorten(user_text, width=8000)}
"""

def generate_persona(profile_url: str):
    username = extract_username(profile_url)
    activity = fetch_user_activity(username)

    if not activity:
        return {"error": "No data found or user may be private."}

    chunks = chunk_text(activity)
    persona_parts = []

    for chunk in chunks:
        prompt = build_persona_prompt(chunk, profile_url)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You analyze Reddit profiles to generate UX personas."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        persona_parts.append(response.choices[0].message.content.strip())

    combined = "\n\n---\n\n".join(persona_parts)
    print("Combined Persona:----->",combined)
    return {
        "username": username,
        "raw_text": combined,
        "parsed": persona_parts[0]  
    }
