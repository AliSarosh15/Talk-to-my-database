import requests
import os
import json
from dotenv import load_dotenv
import re

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

def parse_with_llm(query: str, schema:dict):
    url = "https://openrouter.ai/api/v1/chat/completions"

    prompt = f"""
Convert the user query into structured JSON for SQL generation.

STRICT RULES:
- Only use tables and columns from schema
- Do NOT hallucinate
- Return ONLY JSON
- No explanation

Schema:
{json.dumps(schema, indent=2)}

User Query:
{query}

Output format:
{{
  "tables": [],
  "columns": [],
  "filters": [],
  "operation": "read/count/sum/avg/min/max",
  "aggregation_column": "",
  "group_by": "",
  "order_by": "",
  "order": "asc/desc",
  "limit": 10
}}
"""

    response = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "meta-llama/llama-3-8b-instruct",  # fast + free
            "messages": [
                {"role": "system", "content": "You are a strict JSON generator."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0
        }
    )

    data = response.json()

    print("FULL LLM RESPONSE:", data)
    content = data["choices"][0]["message"]["content"]
    print("LLM CONTENT:", content)
    if "choices" not in data:
        print("LLM ERROR RESPONSE:", data)
        raise ValueError("LLM API FAILED")

    # extract JSON only
    json_match = re.search(r"\{.*\}", content, re.DOTALL)
    if json_match:
        parsed=json.loads(json_match.group())
        print("PARSED JSON:", parsed)
        return parsed
    print("JSON EXTRACTION FAILED")
        

    raise ValueError("No valid JSON found")

    