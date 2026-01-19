# TKINTER MVC FLASHCARD APP

> This is a fork of [AhsanShihab/tkinter-multiframe-mvc](https://github.com/AhsanShihab/tkinter-multiframe-mvc); see the
> repo
> and [the original article](https://nazmul-ahsan.medium.com/how-to-organize-multi-frame-tkinter-application-with-mvc-pattern-79247efbb02b)
> for the baseline implementation. Changes here are built on their architectural foundation.

A flashcard application built with Tkinter following the MVC pattern. Users can sign up, create decks of flashcards, and
study them with spaced repetition based on card scores.

To run the project,

1. Clone the project
2. Create a virtual environment and activate it.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install the required packages

```bash
pip install -r requirements.txt
```

User accounts are stored locally in `app.db` (SQLite, managed via SQLAlchemy) and created the first time you sign up.
Passwords are stored as salted hashes so identical passwords produce different hashes and precomputed tables are
ineffective.

## Features

- MVC structure with dedicated views/forms for signup, sign-in, home, deck list, deck detail (with card table), deck
  form, card form, and study.
- Decks and cards are persisted per user. Cards store a score; studying presents lower-score cards more often. Marking “Memorized” increases the score, “Not Memorized” decreases it (floored at zero).
- A sample deck seeds on first login to demonstrate flows.

## Usage
```bash
python main.py
```
Sign up or sign in, create decks, add cards, open a deck to manage cards, and start a study session to rate each card.

## Tests
Unit tests cover deck scoring and selection logic:
```bash
python -m unittest
```
