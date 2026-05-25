import os
import requests
from openai import OpenAI

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

client = OpenAI(api_key=OPENAI_API_KEY)

PROMPT = """
Search for the latest gaming industry and video game news and prepare a ready-to-publish Telegram post in Russian using this editorial structure.

Aim for 6-7 news items total and prioritize quality over quantity.

Editorial structure:
1. Game / Release — major releases, announcements, launch dates, notable games (#release #aaa #indie)
2. Update / Live Service — patches, seasons, DLC, balance changes, live-service developments (#update #season #dlc)
3. Industry / Business — studios, publishers, acquisitions, layoffs, financial/business developments (#industry #studio #financial)
4. Twitch / Creator / Streaming — Twitch, YouTube, creators, streaming tools, creator economy, watchability (#twitch #streaming #creator)
5. Discovery / What's Rising — Steam trends, breakout games, viral titles, rising categories, sleeper hits (#trend #steam #community)
6. Deep Signal / Tech / Future — hardware, platform shifts, AI, engines, storefront policies, major tech shifts (#hardware #platform #ai #tech)
7. Wildcard — only if there is a genuinely major or unusual story.

Rules:
- Add relevant tags to every news item.
- Avoid duplicate storylines within 48-72h unless there is a major update.
- Max 1 AI-focused story per digest.
- Max 2 industry/business stories.
- Prioritize player-facing and streamer-relevant news over generic corporate commentary.
- Include source links.
- Finish with a short 'what this means' summary and one discussion question.
- Tone: intelligent, concise, Telegram-ready, for adult gamers with opinions rather than mass-market hype.
"""

response = client.responses.create(
    model="gpt-5.5",
    tools=[{"type": "web_search_preview"}],
    input=PROMPT,
)

digest = response.output_text

telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

payload = {
    "chat_id": TELEGRAM_CHAT_ID,
    "text": digest,
    "disable_web_page_preview": False,
}

r = requests.post(telegram_url, json=payload, timeout=30)
r.raise_for_status()

print("Digest sent to Telegram.")
