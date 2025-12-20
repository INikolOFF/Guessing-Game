import tkinter as tk
import random
from tkinter import messagebox

# Game variables
secret_number = 0
attempts = 0
max_range = 100

# Start new game
def start_game():
    global secret_number, attempts, max_range

    attempts = 0

    # Choose difficulty
    if difficulty_var.get() == "Easy":
        max_range = 50
    elif difficulty_var.get() == "Medium":
        max_range = 100
    else:
        max_range = 200

    # Generate number
    secret_number = random.randint(1, max_range)

    result_label.config(text=f"Guess number 1–{max_range}")
    attempts_label.config(text="Attempts: 0")

# Check guess
def make_guess():
    global attempts

    try:
        guess = int(guess_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Enter a number")
        return

    attempts += 1
    attempts_label.config(text=f"Attempts: {attempts}")

    if guess < secret_number:
        result_label.config(text="Higher")
    elif guess > secret_number:
        result_label.config(text="Lower")
    else:
        result_label.config(text=f"Correct! Number was {secret_number}")
        messagebox.showinfo("Win", f"You won in {attempts} attempts")

# Create window
root = tk.Tk()
root.title("Guess the Number")
root.geometry("350x300")

# Difficulty
tk.Label(root, text="Difficulty").pack()

difficulty_var = tk.StringVar(value="Medium")

tk.Radiobutton(root, text="Easy", variable=difficulty_var, value="Easy").pack()
tk.Radiobutton(root, text="Medium", variable=difficulty_var, value="Medium").pack()
tk.Radiobutton(root, text="Hard", variable=difficulty_var, value="Hard").pack()

# Buttons and input
tk.Button(root, text="Start Game", command=start_game).pack(pady=10)

guess_entry = tk.Entry(root)
guess_entry.pack()

tk.Button(root, text="Guess", command=make_guess).pack(pady=5)

# Info labels
result_label = tk.Label(root, text="")
result_label.pack(pady=10)

attempts_label = tk.Label(root, text="Attempts: 0")
attempts_label.pack()

# Run app
root.mainloop()