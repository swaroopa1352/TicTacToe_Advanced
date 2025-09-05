# Tic Tac Toe — Django + Vanilla JS

![Python](https://img.shields.io/badge/Python-3.x-informational)
![Django](https://img.shields.io/badge/Django-4.2-brightgreen)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

A clean Tic-Tac-Toe web app with a **Django** backend and lightweight **HTML/CSS/JS** front end.  
Per-game state is stored in the database (no globals), the UI calls JSON endpoints via **Fetch**, and there’s an **AI opponent** with **Easy/Medium/Hard** (minimax) difficulty.

---

## Features
- ✅ Two modes: **2-Player** and **vs Computer** (AI).
- 🧠 **AI difficulty**: Easy (random), Medium (win/block/center/corner), Hard (**minimax**).
- 🧭 Server-side truth: requests hit JSON endpoints; backend validates moves and detects winner/tie.
- 🗂️ **Per-game UUID** URLs; multiple games can run in parallel.
- 🔒 Mutations use **POST** + **CSRF** protection.
- 🎨 Responsive, animated UI (hover, press, winner glow, “thinking” spinner).
- 🧩 Zero front-end frameworks (vanilla HTML/CSS/JS).

---

## Tech Stack
**Frontend**
- HTML5 (Django Template Language)
- CSS3 (custom responsive styles)
- JavaScript (ES6) + Fetch API
- SVG favicon

**Backend**
- Python 3
- Django 4.2 (MVT)
- Django ORM `Game` model for persistence

**Database**
- SQLite (development default)

---

## Project Structure
