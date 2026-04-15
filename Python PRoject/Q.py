import tkinter as tk
from tkinter import messagebox
import random

# ---------------- GAME DATA ----------------
levels = {
    "EASY": {
        "movies": [
            ("SHOLAY", "Famous Gabbar Singh movie"),
            ("BORDER", "War based movie"),
            ("JUDWAA", "Twin brothers comedy")
        ],
        "chances": 3
    },
    "MEDIUM": {
        "movies": [
            ("KARAN ARJUN", "Brother revenge story"),
            ("BOL BACHCHAN", "Rohit Shetty comedy")
        ],
        "chances": 5
    },
    "HARD": {
        "movies": [
            ("DRISHYAM", "Crime + family thriller"),
            ("GANGUBAI KATHIAWADI", "Based on real life")
        ],
        "chances": 6
    }
}

# ---------------- VARIABLES ----------------
word = ""
hint = ""
display = ""
attempts = 0
hint_used = False

# ---------------- FUNCTIONS ----------------
def start_game(level):
    global word, display, attempts, hint, hint_used

    choice = random.choice(levels[level]["movies"])
    word = choice[0]
    hint = choice[1]

    attempts = levels[level]["chances"]
    hint_used = False

    display = ""
    for ch in word:
        if ch in "AEIOU ":
            display += ch + " "
        else:
            display += "_ "

    label_word.config(text=display)
    label_attempts.config(text=f"Attempts Left: {attempts}")
    label_hint.config(text="")
    entry_guess.delete(0, tk.END)

def guess_word():
    global attempts, hint_used

    guess = entry_guess.get().upper()

    if guess == "":
        messagebox.showwarning("Warning", "Enter a guess!")
        return

    entry_guess.delete(0, tk.END)

    if guess == word:
        messagebox.showinfo("Result", "🎉 Correct Guess!")
    else:
        attempts -= 1
        label_attempts.config(text=f"Attempts Left: {attempts}")

        if not hint_used:
            label_hint.config(text=f"💡 Hint: {hint}")
            hint_used = True

        if attempts == 0:
            messagebox.showerror("Game Over", f"💀 You Lost!\nWord was: {word}")

# ----------- NEW: CLEAR INPUT -----------
def clear_input():
    entry_guess.delete(0, tk.END)

# ----------- NEW: RESET GAME -----------
def reset_game():
    global word, attempts
    word = ""
    attempts = 0

    label_word.config(text="")
    label_attempts.config(text="")
    label_hint.config(text="")
    entry_guess.delete(0, tk.END)

# ---------------- GUI ----------------
root = tk.Tk()
root.title("Bollywood Hangman 🎬")
root.geometry("420x450")

tk.Label(root, text="🎬 Bollywood Hangman", font=("Arial", 16)).pack(pady=10)

# Level buttons
tk.Button(root, text="Easy", command=lambda: start_game("EASY")).pack(pady=5)
tk.Button(root, text="Medium", command=lambda: start_game("MEDIUM")).pack(pady=5)
tk.Button(root, text="Hard", command=lambda: start_game("HARD")).pack(pady=5)

# Word display
label_word = tk.Label(root, text="", font=("Arial", 14))
label_word.pack(pady=10)

# Attempts
label_attempts = tk.Label(root, text="")
label_attempts.pack()

# Hint
label_hint = tk.Label(root, text="", fg="blue")
label_hint.pack(pady=5)

# Entry
entry_guess = tk.Entry(root)
entry_guess.pack(pady=10)

# Buttons
tk.Button(root, text="Guess Movie", command=guess_word).pack(pady=5)
tk.Button(root, text="Clear Input ", command=clear_input).pack(pady=5)
tk.Button(root, text="Reset Game ", command=reset_game).pack(pady=5)

# Run app
root.mainloop()