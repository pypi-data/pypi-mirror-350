import argparse
import json
from textblob import TextBlob

def load_json(path):
    with open(path) as f:
        return json.load(f)

def analyze_sentiment(sections):
    for section in sections:
        text = section["content"]
        sentiment = TextBlob(text).sentiment.polarity
        section["sentiment_score"] = sentiment
    return sections

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()

    sections = load_json(args.input)
    result = analyze_sentiment(sections)
    with open(args.output, "w") as f:
        json.dump(result, f, indent=2)

if __name__ == "__main__":
    main()
