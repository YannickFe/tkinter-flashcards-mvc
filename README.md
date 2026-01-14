# TKINTER MVC MULTI-FRAME

Tkinter is a common library for making Graphical User Interface (GUI) in Python. In this project, I designed a moderately complex Tkinter project with multiple frames following the MVC design pattern. I wrote an [article](https://nazmul-ahsan.medium.com/how-to-organize-multi-frame-tkinter-application-with-mvc-pattern-79247efbb02b) about it on Medium where I used this project as the example.

To run the project,

1. Clone the project
2. Create a virtual enviroment and activate it.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install the required packages

```bash
pip install -r requirements.txt
```

User accounts are stored locally in `app.db` (SQLite, managed via SQLAlchemy) and created the first time you sign up. Passwords are stored as salted hashes.

## Features
- MVC structure with frames for sign up, sign in, home, deck list, deck detail, and study.
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
