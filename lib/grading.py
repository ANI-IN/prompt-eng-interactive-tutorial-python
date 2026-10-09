"""Tiny, deterministic grading helpers used by the exercises."""

import re


def lower(text) -> str:
    return str(text).lower()


def includes_all(text, words) -> bool:
    """True if every word appears in text (case-insensitive)."""
    return all(lower(w) in lower(text) for w in words)


def includes_any(text, words) -> bool:
    """True if at least one word appears in text (case-insensitive)."""
    return any(lower(w) in lower(text) for w in words)


def word_count(text) -> int:
    return len(str(text).split())


def equals_exact(text, expected) -> bool:
    return text == expected


def line_count(text) -> int:
    """Number of non-blank lines."""
    return sum(1 for line in str(text).split("\n") if line.strip())


def last_token(text) -> str:
    """Last whitespace-separated token, lowercased, letters only."""
    tokens = str(text).split()
    return re.sub(r"[^a-z]", "", tokens[-1].lower()) if tokens else ""


def grade(response, passed: bool) -> None:
    """Pretty-print a Claude response and its pass/fail grade in a notebook cell."""
    print(response)
    print("\n--------------------------- GRADING ---------------------------")
    print("This exercise has been correctly solved:", passed)
