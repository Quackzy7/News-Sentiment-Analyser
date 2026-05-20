from groq import Groq
import os
import json
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

ANALYSIS_PROMPT = """
You are an expert media analyst specializing in Nepali and English news analysis.

Analyze the following news article and return a JSON response with exactly this structure:

{{
    "language": "nepali or english",
    "sentiment": {{
        "overall": "positive, negative, or neutral",
        "score": a number between -1.0 (very negative) and 1.0 (very positive)
    }},
    "bias": {{
        "detected": true or false,
        "lean": "left, right, center, or none",
        "score": a number between 0.0 (no bias) and 1.0 (extreme bias),
        "explanation": "brief explanation of why bias was detected or not"
    }},
    "propaganda_techniques": [
        {{
            "technique": "name of technique",
            "explanation": "where and how it appears in the article",
            "severity": "low, medium, or high"
        }}
    ],
    "loaded_language": ["list", "of", "emotionally", "charged", "words", "or", "phrases"],
    "credibility_indicators": {{
        "has_sources": true or false,
        "has_quotes": true or false,
        "has_data": true or false,
        "credibility_score": a number between 0.0 and 1.0
    }},
    "summary": "2-3 sentence objective summary of the article in English"
}}

Propaganda techniques to look for:
- Fear Appeal: using fear to influence opinion
- Name Calling: using negative labels
- Bandwagon: everyone is doing it
- Loaded Language: emotionally charged words
- False Dilemma: only two choices presented
- Whataboutism: deflecting criticism
- Appeal to Authority: citing authority without evidence
- Repetition: repeating claims to make them seem true
- Scapegoating: blaming one group for problems

Article to analyze:
{article_text}

Return ONLY the JSON object. No explanation, no markdown, no extra text.
"""

async def analyze_article(text: str) -> dict:
    prompt = ANALYSIS_PROMPT.format(article_text=text[:6000])

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1,
    )

    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()

    result = json.loads(raw)
    return result