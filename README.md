# 🍳 The Cookbook — Recipe Management System

A console-based Recipe Management System built in Python with a MySQL backend. Supports two roles — Admin and User — for curating and exploring a recipe database.

Developed collaboratively as a school Computer Science project by:
- Aysha Suha
- Sai Prathama Gouri
- Shreya Prakash Issani

---

## Features

### 👤 User Mode
- Create an account and sign in securely (password entry hidden via Tkinter dialog)
- Search recipes by ingredients (matches on 3+ ingredients) or browse the full list
- View ingredients and step-by-step instructions for any recipe
- Add/remove recipes to a personal favourites list
- Rate and review recipes; view existing reviews
- Get ingredient suggestions logged when a searched ingredient isn't in any recipe

### 🔐 Admin Mode
- Add new recipes (name, ingredients, steps)
- Delete existing recipes
- View all ingredient suggestions submitted by users
- View all recipes currently in the system

---

## Tech Stack

- **Language:** Python
- **Database:** MySQL (via `mysql-connector-python`)
- **GUI element:** Tkinter (secure password entry)
- **Data storage:** CSV, pickle (`.dat`) files, and MySQL tables (`review`, `comment`)
- **Display:** PrettyTable for formatted console output

---

## Project Structure

```
cookbook_project/
├── cookbookmain.py       # Entry point — main menu and program flow
├── functions.py          # User-side logic: auth, search, favourites, reviews
├── dishes.py              # Admin-side logic: add/delete recipes, suggestions
├── config_example.py      # Template for DB credentials (copy to config.py)
├── requirements.txt
└── README.md
```

## Data Files (created automatically at runtime, not included in repo)
- `passwords.dat` — stored user credentials
- `recipes.dat` — stored recipe steps
- `dishes.csv` — recipe names + ingredients
- `suggestions.txt` — ingredient suggestions log
- `<username>.txt` — each user's favourites list

---

## Setup & Running

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set up MySQL
Create a database named `cookbook` with two tables:
```sql
CREATE TABLE review (
    name VARCHAR(100) PRIMARY KEY,
    avg_stars FLOAT DEFAULT 0,
    count INT DEFAULT 0
);

CREATE TABLE comment (
    name VARCHAR(100),
    stars INT,
    username VARCHAR(100),
    comment TEXT
);
```

### 3. Configure credentials
Copy `config_example.py` to `config.py` and fill in your local MySQL username/password:
```bash
cp config_example.py config.py
```

### 4. Run the app
```bash
python cookbookmain.py
```

**Admin access key:** `sas`

---

## Notes

This was built as an early Computer Science project, so the code favours straightforward, procedural logic (file I/O, CSV, pickle) over more advanced patterns — a good snapshot of foundational Python and database integration skills.

## Future Improvements
- Move all persistent storage (CSV/pickle) fully into MySQL for consistency
- Add input validation and error handling
- Replace the console interface with a GUI or web front-end
- Hash stored passwords instead of storing them in plaintext

