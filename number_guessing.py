import tkinter as tk
from tkinter import messagebox
import random


class GuessNumberGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("🎯 Guess the Number")
        self.window.geometry("450x600")
        self.window.resizable(False, False)
        self.window.configure(bg="#1a1a2e")

        self.secret_number = 0
        self.attempts = 0
        self.max_range = 100
        self.best_scores = {"Easy": None, "Medium": None, "Hard": None}
        self.guess_history = []
        self.game_active = False

        self.setup_ui()

    def setup_ui(self):
        # Header Frame
        header_frame = tk.Frame(self.window, bg="#16213e", height=80)
        header_frame.pack(fill="x", pady=(0, 20))

        tk.Label(header_frame, text="🎯 GUESS THE NUMBER",
                 font=("Arial", 24, "bold"), bg="#16213e", fg="#00ff88").pack(pady=20)

        # Main Container
        main_container = tk.Frame(self.window, bg="#1a1a2e")
        main_container.pack(expand=True, fill="both", padx=20)

        # Difficulty Selection
        difficulty_frame = tk.LabelFrame(main_container, text="🎮 Select Difficulty",
                                         font=("Arial", 12, "bold"), bg="#0f3460",
                                         fg="#00ff88", padx=20, pady=15)
        difficulty_frame.pack(pady=10, fill="x")

        self.difficulty_var = tk.StringVar(value="Medium")

        difficulties = [
            ("Easy (1-50)", "Easy", "#27ae60"),
            ("Medium (1-100)", "Medium", "#f39c12"),
            ("Hard (1-200)", "Hard", "#e74c3c")
        ]

        for text, value, color in difficulties:
            rb = tk.Radiobutton(difficulty_frame, text=text, variable=self.difficulty_var,
                                value=value, font=("Arial", 11), bg="#0f3460", fg="white",
                                selectcolor="#16213e", activebackground="#0f3460",
                                activeforeground="white", command=self.update_difficulty_display)
            rb.pack(anchor="w", pady=3)

        # Start Game Button
        self.start_btn = tk.Button(main_container, text="🚀 START NEW GAME",
                                   command=self.start_game, font=("Arial", 14, "bold"),
                                   bg="#00ff88", fg="#1a1a2e", activebackground="#00cc70",
                                   cursor="hand2", height=2)
        self.start_btn.pack(pady=15, fill="x")

        # Game Info Frame
        info_frame = tk.Frame(main_container, bg="#0f3460", padx=15, pady=15)
        info_frame.pack(pady=10, fill="x")

        self.range_label = tk.Label(info_frame, text="Press START to begin!",
                                    font=("Arial", 12, "bold"), bg="#0f3460", fg="#00ff88")
        self.range_label.pack()

        self.attempts_label = tk.Label(info_frame, text="Attempts: 0",
                                       font=("Arial", 11), bg="#0f3460", fg="white")
        self.attempts_label.pack(pady=5)

        self.best_score_label = tk.Label(info_frame, text="Best Score: -",
                                         font=("Arial", 10, "italic"), bg="#0f3460", fg="#ffd700")
        self.best_score_label.pack()

        # Input Frame
        input_frame = tk.Frame(main_container, bg="#1a1a2e")
        input_frame.pack(pady=15)

        tk.Label(input_frame, text="Your Guess:", font=("Arial", 11),
                 bg="#1a1a2e", fg="white").pack()

        self.guess_entry = tk.Entry(input_frame, font=("Arial", 18, "bold"),
                                    justify="center", width=12, bg="#0f3460",
                                    fg="white", insertbackground="white")
        self.guess_entry.pack(pady=5)
        self.guess_entry.bind("<Return>", lambda e: self.make_guess())

        self.guess_btn = tk.Button(input_frame, text="🎲 MAKE GUESS",
                                   command=self.make_guess, font=("Arial", 12, "bold"),
                                   bg="white", fg="black", activebackground="#2980b9",
                                   cursor="hand2", state="disabled", width=15)
        self.guess_btn.pack(pady=10)

        # Result Frame
        self.result_frame = tk.Frame(main_container, bg="#16213e", padx=20, pady=15)
        self.result_frame.pack(pady=10, fill="x")

        self.result_label = tk.Label(self.result_frame, text="",
                                     font=("Arial", 16, "bold"), bg="#16213e", fg="white")
        self.result_label.pack()

        self.hint_label = tk.Label(self.result_frame, text="",
                                   font=("Arial", 11), bg="#16213e", fg="#aaa")
        self.hint_label.pack(pady=5)

        # History Frame
        history_frame = tk.LabelFrame(main_container, text="📊 Guess History",
                                      font=("Arial", 10, "bold"), bg="#0f3460",
                                      fg="#00ff88", height=60)
        history_frame.pack(pady=10, fill="x")

        self.history_label = tk.Label(history_frame, text="No guesses yet",
                                      font=("Arial", 9), bg="#0f3460", fg="white")
        self.history_label.pack(pady=10)

    def update_difficulty_display(self):
        difficulty = self.difficulty_var.get()
        best = self.best_scores[difficulty]
        best_text = f"Best Score: {best}" if best else "Best Score: -"
        self.best_score_label.config(text=best_text)

    def start_game(self):
        self.attempts = 0
        self.guess_history = []
        self.game_active = True

        # Set difficulty
        difficulty = self.difficulty_var.get()
        if difficulty == "Easy":
            self.max_range = 50
        elif difficulty == "Medium":
            self.max_range = 100
        else:
            self.max_range = 200

        # Generate secret number
        self.secret_number = random.randint(1, self.max_range)

        # Update UI
        self.range_label.config(text=f"🎯 Guess a number between 1 and {self.max_range}")
        self.attempts_label.config(text="Attempts: 0")
        self.result_label.config(text="Good luck!", fg="white")
        self.hint_label.config(text="")
        self.history_label.config(text="No guesses yet")
        self.guess_entry.delete(0, tk.END)
        self.guess_entry.config(state="normal")
        self.guess_btn.config(state="normal")
        self.guess_entry.focus()

        self.update_difficulty_display()

    def make_guess(self):
        if not self.game_active:
            messagebox.showwarning("Game Not Started", "Please start a new game first!")
            return

        try:
            guess = int(self.guess_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number!")
            self.guess_entry.delete(0, tk.END)
            return

        if guess < 1 or guess > self.max_range:
            messagebox.showwarning("Out of Range",
                                   f"Please enter a number between 1 and {self.max_range}!")
            self.guess_entry.delete(0, tk.END)
            return

        self.attempts += 1
        self.attempts_label.config(text=f"Attempts: {self.attempts}")
        self.guess_history.append(guess)

        # Update history
        history_text = " → ".join([str(g) for g in self.guess_history[-8:]])
        if len(self.guess_history) > 8:
            history_text = "... → " + history_text
        self.history_label.config(text=history_text)

        # Check guess
        difference = abs(guess - self.secret_number)

        if guess < self.secret_number:
            self.result_label.config(text="📈 TOO LOW!", fg="#3498db")
            if difference <= 5:
                self.hint_label.config(text="🔥 Very close! Go higher!")
            elif difference <= 10:
                self.hint_label.config(text="🌡️ Close! Go higher!")
            else:
                self.hint_label.config(text="❄️ Go much higher!")

        elif guess > self.secret_number:
            self.result_label.config(text="📉 TOO HIGH!", fg="#e74c3c")
            if difference <= 5:
                self.hint_label.config(text="🔥 Very close! Go lower!")
            elif difference <= 10:
                self.hint_label.config(text="🌡️ Close! Go lower!")
            else:
                self.hint_label.config(text="❄️ Go much lower!")

        else:
            self.game_active = False
            self.result_label.config(text=f"🎉 CORRECT! The number was {self.secret_number}",
                                     fg="#00ff88")
            self.hint_label.config(text=f"You won in {self.attempts} attempts!")
            self.guess_entry.config(state="disabled")
            self.guess_btn.config(state="disabled")

            # Update best score
            difficulty = self.difficulty_var.get()
            if self.best_scores[difficulty] is None or self.attempts < self.best_scores[difficulty]:
                self.best_scores[difficulty] = self.attempts
                self.best_score_label.config(text=f"Best Score: {self.attempts} 🏆")
                messagebox.showinfo("🎊 New Record!",
                                    f"Congratulations! New best score for {difficulty} mode:\n"
                                    f"{self.attempts} attempts!")
            else:
                messagebox.showinfo("🎉 You Won!",
                                    f"Congratulations! You found the number in {self.attempts} attempts!\n"
                                    f"Best score for {difficulty}: {self.best_scores[difficulty]} attempts")

        self.guess_entry.delete(0, tk.END)
        self.guess_entry.focus()

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    game = GuessNumberGame()
    game.run()