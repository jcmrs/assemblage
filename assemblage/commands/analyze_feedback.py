"""
assemblage.commands.analyze_feedback

Logic for the 'analyze_feedback' command.
"""

import re
import sys
from collections import Counter
from pathlib import Path

import yaml

# --- Constants and ANSI Colors ---
BLUE = "\033[0;34m"
YELLOW = "\033[1;33m"
NC = "\033[0m"

# Simple stop words list
STOP_WORDS = {
    "the",
    "and",
    "for",
    "are",
    "was",
    "but",
    "not",
    "this",
    "that",
    "a",
    "an",
    "is",
    "in",
    "it",
    "to",
    "of",
    "i",
    "you",
    "he",
    "she",
    "we",
    "they",
    "me",
    "him",
    "her",
    "us",
    "them",
    "my",
    "your",
    "his",
    "its",
    "our",
    "their",
    "mine",
    "yours",
    "hers",
    "ours",
    "theirs",
    "what",
    "which",
    "who",
    "whom",
    "whose",
    "be",
    "been",
    "being",
    "have",
    "has",
    "had",
    "do",
    "does",
    "did",
    "will",
    "would",
    "shall",
    "should",
    "can",
    "could",
    "may",
    "might",
    "must",
    "with",
    "at",
    "from",
    "by",
    "on",
    "about",
    "against",
    "between",
    "into",
    "through",
    "during",
    "before",
    "after",
    "above",
    "below",
    "up",
    "down",
    "out",
    "off",
    "over",
    "under",
    "again",
    "further",
    "then",
    "once",
    "here",
    "there",
    "when",
    "where",
    "why",
    "how",
    "all",
    "any",
    "both",
    "each",
    "few",
    "more",
    "most",
    "other",
    "some",
    "such",
    "no",
    "nor",
    "only",
    "own",
    "same",
    "so",
    "than",
    "too",
    "very",
    "s",
    "t",
    "just",
    "don",
    "now",
}


def _load_all_feedback():
    """Loads all feedback files from the feedback/ directory."""
    feedback_dir = Path("feedback/")
    if not feedback_dir.exists():
        return []

    all_feedback = []
    for feedback_file in feedback_dir.glob("*.yml"):
        with open(feedback_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            if data:
                all_feedback.append(data)
    return all_feedback


def _calculate_and_print_stats(all_feedback):
    """Calculates and prints aggregate stats for ratings."""
    print(f"\n{YELLOW}--- Aggregate Feedback Statistics ---{NC}")

    reviews = [fb.get("vision_owner_review", {}) for fb in all_feedback]
    if not reviews:
        print("No reviews found to analyze.")
        return

    ratings = {
        "clarity": [],
        "efficiency": [],
        "correctness": [],
    }

    for review in reviews:
        if review.get("clarity_rating"):
            ratings["clarity"].append(review["clarity_rating"])
        if review.get("efficiency_rating"):
            ratings["efficiency"].append(review["efficiency_rating"])
        if review.get("correctness_rating"):
            ratings["correctness"].append(review["correctness_rating"])

    print(f"Based on {len(reviews)} feedback file(s):\n")
    for key, values in ratings.items():
        if values:
            avg = sum(values) / len(values)
            print(f"  - Average {key.capitalize()} Rating: {avg:.2f} / 5.0")
        else:
            print(f"  - Average {key.capitalize()} Rating: N/A")


def _analyze_and_propose_nudges(all_feedback):
    """Analyzes improvement areas and proposes new nudges."""
    print(f"\n{YELLOW}--- Nudge Proposal Analysis ---{NC}")

    corpus = " ".join(
        fb.get("vision_owner_review", {}).get("improvement_areas", "")
        for fb in all_feedback
    )

    if not corpus.strip():
        print("No 'improvement_areas' text found to analyze.")
        return

    # Normalize and extract words
    words = re.findall(
        r"\b[a-z]{4,}\b", corpus.lower()
    )  # Words of 4+ chars, only letters

    # Filter stop words
    filtered_words = [word for word in words if word not in STOP_WORDS]

    # Get most common keywords
    word_counts = Counter(filtered_words)
    top_keywords = word_counts.most_common(3)

    if not top_keywords:
        print("No recurring improvement themes found.")
        return

    print("\nBased on recurring themes, here are some proposed new nudges:")
    print("(Copy these into 'config/nudges.yml' if you agree)\n")

    for keyword, count in top_keywords:
        nudge_id = f"nudge_{keyword}_check"
        nudge_text = f"Did you remember to address {keyword} in this change?"
        print(f'  {nudge_id}: "{nudge_text}"  # Found {count} times')


def run(args):
    """Orchestrates the feedback analysis."""
    print(f"{BLUE}--- Running Feedback Analysis Loop ---{NC}")

    all_feedback = _load_all_feedback()
    if not all_feedback:
        print("No feedback files found in the 'feedback/' directory.")
        sys.exit(0)

    _calculate_and_print_stats(all_feedback)
    _analyze_and_propose_nudges(all_feedback)

    print(f"\n{BLUE}--- Analysis Complete ---{NC}")
    sys.exit(0)
