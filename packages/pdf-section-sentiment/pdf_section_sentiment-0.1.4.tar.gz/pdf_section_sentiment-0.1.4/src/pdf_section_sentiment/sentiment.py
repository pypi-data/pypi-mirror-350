import argparse
import json
from textblob import TextBlob
import logging

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

def analyze_sentiment(sections):
    for section in sections:
        text = section.get("content", "")
        sentiment_score = TextBlob(text).sentiment.polarity
        section["sentiment_score"] = round(sentiment_score, 3)

        # Determine sentiment label
        if sentiment_score > 0.05:
            section["sentiment"] = "positive"
        elif sentiment_score < -0.05:
            section["sentiment"] = "negative"
        else:
            section["sentiment"] = "neutral"

    return sections

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Input JSON file with headers/content")
    parser.add_argument("--output", required=True, help="Output JSON file with sentiment")
    args = parser.parse_args()

    logger.info(f"Loading file: {args.input}")
    with open(args.input, "r", encoding="utf-8") as f:
        sections = json.load(f)

    logger.info("Analyzing sentiment...")
    enriched = analyze_sentiment(sections)

    logger.info(f"Saving result to {args.output}")
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(enriched, f, indent=2)

if __name__ == "__main__":
    main()
