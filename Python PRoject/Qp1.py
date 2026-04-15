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
    label_reveal.config(text="")
    entry_guess.delete(0, tk.END)

# ----------- REVEAL FUNCTION -----------
def reveal_one_letter():
    global display

    display_list = display.split()
    revealed_letter = ""

    for i in range(len(word)):
        if display_list[i] == "_" and word[i] != " ":
            display_list[i] = word[i]
            revealed_letter = word[i]
            break

    display_updated = " ".join(display_list)
    label_word.config(text=display_updated)

    return revealed_letter

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

        # Reveal one letter
        letter = reveal_one_letter()

        # Show revealed letter in GUI
        label_reveal.config(text=f"Revealed Letter: {letter}")

        # Show messagebox
        messagebox.showinfo("Wrong Guess", f"❌ Wrong guess!\nRevealed letter: {letter}")

        if not hint_used:
            label_hint.config(text=f"💡 Hint: {hint}")
            hint_used = True

        if attempts == 0:
            messagebox.showerror("Game Over", f"💀 You Lost!\nWord was: {word}")

# ----------- CLEAR INPUT -----------
def clear_input():
    entry_guess.delete(0, tk.END)

# ----------- RESET GAME -----------
def reset_game():
    global word, attempts
    word = ""
    attempts = 0

    label_word.config(text="")
    label_attempts.config(text="")
    label_hint.config(text="")
    label_reveal.config(text="")
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

# NEW: Revealed Letter Label
label_reveal = tk.Label(root, text="", fg="green", font=("Arial", 12))
label_reveal.pack(pady=5)

# Entry
entry_guess = tk.Entry(root)
entry_guess.pack(pady=10)

# Buttons
tk.Button(root, text="Guess Movie", command=guess_word).pack(pady=5)
tk.Button(root, text="Clear Input", command=clear_input).pack(pady=5)
tk.Button(root, text="Reset Game", command=reset_game).pack(pady=5)

# Run app
root.mainloop()