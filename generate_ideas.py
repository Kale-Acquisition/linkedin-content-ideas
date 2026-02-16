#!/usr/bin/env python3
"""
Content Idea Generator
Pulls the last week's Fireflies meeting transcripts and generates
30 LinkedIn content ideas using Claude.
"""

import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

import requests
import anthropic
from dotenv import load_dotenv

SCRIPT_DIR = Path(__file__).parent
FIREFLIES_API_URL = "https://api.fireflies.ai/graphql"


def load_config():
    """Load environment variables from .env file."""
    load_dotenv(SCRIPT_DIR / ".env")
    fireflies_key = os.getenv("FIREFLIES_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    if not fireflies_key:
        print("Error: FIREFLIES_API_KEY not set in .env")
        sys.exit(1)
    if not anthropic_key:
        print("Error: ANTHROPIC_API_KEY not set in .env")
        sys.exit(1)
    return fireflies_key, anthropic_key


def fetch_transcripts(api_key: str, from_date: datetime, to_date: datetime) -> list:
    """Fetch transcript list from Fireflies for the given date range."""
    from_iso = from_date.strftime("%Y-%m-%dT00:00:00.000Z")
    to_iso = to_date.strftime("%Y-%m-%dT23:59:59.999Z")

    query = """
    query Transcripts($fromDate: DateTime, $toDate: DateTime) {
        transcripts(fromDate: $fromDate, toDate: $toDate) {
            id
            title
            date
            duration
            summary {
                short_summary
                keywords
                action_items
            }
        }
    }
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    payload = {
        "query": query,
        "variables": {"fromDate": from_iso, "toDate": to_iso},
    }

    resp = requests.post(FIREFLIES_API_URL, json=payload, headers=headers, timeout=30)
    resp.raise_for_status()

    data = resp.json()
    if "errors" in data:
        print(f"Fireflies API errors: {json.dumps(data['errors'], indent=2)}")
        sys.exit(1)

    transcripts = data.get("data", {}).get("transcripts", [])
    return transcripts


def format_meeting_data(transcripts: list) -> str:
    """Format transcript data into a readable context block for the prompt."""
    if not transcripts:
        return "(No meetings found in the date range.)"

    sections = []
    for t in transcripts:
        summary = t.get("summary") or {}
        short_summary = summary.get("short_summary", "No summary available.")
        keywords = summary.get("keywords") or []
        action_items = summary.get("action_items") or []

        # Format duration
        duration_mins = (t.get("duration") or 0) // 60

        section = f"### {t.get('title', 'Untitled Meeting')}\n"
        section += f"**Date:** {t.get('date', 'Unknown')} | **Duration:** {duration_mins} min\n\n"
        section += f"**Summary:** {short_summary}\n\n"
        if keywords:
            section += f"**Keywords:** {', '.join(keywords)}\n\n"
        if action_items:
            section += "**Action Items:**\n"
            for item in action_items:
                section += f"- {item}\n"
            section += "\n"

        sections.append(section)

    return "\n---\n\n".join(sections)


def load_prompt(meeting_data: str) -> str:
    """Load prompt.md, inject context.md and meeting data."""
    prompt_path = SCRIPT_DIR / "prompt.md"
    context_path = SCRIPT_DIR / "context.md"
    if not prompt_path.exists():
        print(f"Error: {prompt_path} not found.")
        sys.exit(1)
    if not context_path.exists():
        print(f"Error: {context_path} not found.")
        sys.exit(1)

    template = prompt_path.read_text()
    context = context_path.read_text()
    template = template.replace("{context}", context)
    return template.replace("{meeting_data}", meeting_data)


def generate_ideas(anthropic_key: str, prompt: str) -> str:
    """Call Claude API to generate content ideas."""
    client = anthropic.Anthropic(api_key=anthropic_key)

    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=8192,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def format_output(ideas_text: str, transcript_count: int, from_date: datetime, to_date: datetime) -> str:
    """Wrap the generated ideas in a markdown file with metadata header."""
    from_str = from_date.strftime("%b %-d")
    to_str = to_date.strftime("%b %-d, %Y")

    header = f"# LinkedIn Content Ideas - {to_date.strftime('%b %-d, %Y')}\n\n"
    header += f"**Meetings analyzed:** {transcript_count}\n"
    header += f"**Date range:** {from_str} - {to_str}\n\n"
    header += "---\n\n"

    return header + ideas_text + "\n"


def main():
    print("Loading configuration...")
    fireflies_key, anthropic_key = load_config()

    to_date = datetime.now()
    from_date = to_date - timedelta(days=7)
    print(f"Fetching meetings from {from_date.strftime('%b %-d')} to {to_date.strftime('%b %-d, %Y')}...")

    transcripts = fetch_transcripts(fireflies_key, from_date, to_date)
    print(f"Found {len(transcripts)} meeting(s).")

    if not transcripts:
        print("No meetings found in the last 7 days. Nothing to generate.")
        sys.exit(0)

    meeting_data = format_meeting_data(transcripts)
    prompt = load_prompt(meeting_data)

    print("Generating LinkedIn content ideas with Claude...")
    ideas_text = generate_ideas(anthropic_key, prompt)

    output = format_output(ideas_text, len(transcripts), from_date, to_date)

    output_filename = f"{to_date.strftime('%Y-%m-%d')}-ideas.md"
    output_path = SCRIPT_DIR / output_filename
    output_path.write_text(output)

    print(f"\nDone! Saved {output_filename}")
    print(f"  {len(transcripts)} meetings analyzed")
    print(f"  30 content ideas generated")
    print(f"  Output: {output_path}")


if __name__ == "__main__":
    main()
