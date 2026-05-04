import os
from dotenv import load_dotenv
import anthropic
import time
load_dotenv()

def generate_weekly_focus(prev_plus, prev_minus, prev_next, retries=3):
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    for attempt in range(retries):
        try:
            response = client.messages.create(
                model="claude-opus-4-5",
                max_tokens=500,
                messages=[{
                    "role": "user",
                    "content": f"""Based on last week's review, suggest a weekly focus and 3 main goals.

Plus (what went well): {prev_plus}
Minus (what didn't): {prev_minus}
Next (actions planned): {prev_next}

Return in this format:
Focus: <one sentence>
Goals:
- <goal 1>
- <goal 2>
- <goal 3>"""
                }]
            )
            return response.content[0].text
        except anthropic.APIStatusError as e:
            if e.status_code == 529:
                if attempt < retries - 1:
                    time.sleep(5)
                else:
                    return None
            else:
                raise