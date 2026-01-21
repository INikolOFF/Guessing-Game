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
        self.bind_shortcuts()

    def bind_shortcuts(self):
        self.window.bind("<Return>", lambda e: self.make_guess())
        self.window.bind("<Control-n>", lambda e: self.start_game())
        self.window.bind("<Control-r>", lambda e: self.start_game())
        self.window.bind("<Escape>", lambda e: self.window.destroy())

    def setup_ui(self):
        header_frame = tk.Frame(self.window, bg="#16213e", height=80)
        header_frame.pack(fill="x", pady=(0, 20))

        tk.Label(
            header_frame,
            text="🎯 GUESS THE NUMBER",
            font=("Arial", 24, "bold"),
            bg="#16213e",
            fg="#00ff88"
        ).pack(pady=20)

        main_container = tk.Frame(self.window, bg="#1a1a2e")
        main_container.pack(expand=True, fill="both", padx=20)

        difficulty_frame = tk.LabelFrame(
            main_container,
            text="🎮 Select Difficulty",
            font=("Arial", 12, "bold"),
            bg="#0f3460",
            fg="#00ff88",
            padx=20,
            pady=15
        )
        difficulty_frame.pack(pady=10, fill="x")

        self.difficulty_var = tk.StringVar(value="Medium")

        for text, value in [
            ("Easy (1–50)", "Easy"),
            ("Medium (1–100)", "Medium"),
            ("Hard (1–200)", "Hard")
        ]:
            tk.Radiobutton(
                difficulty_frame,
                text=text,
                variable=self.difficulty_var,
                value=value,
                bg="#0f3460",
                fg="white",
                selectcolor="#16213e",
                command=self.update_difficulty_display
            ).pack(anchor="w", pady=3)

        self.start_btn = tk.Button(
            main_container,
            text="🚀 START NEW GAME (Ctrl+N)",
            command=self.start_game,
            font=("Arial", 14, "bold"),
            bg="#00ff88",
            fg="#1a1a2e",
            height=2
        )
        self.start_btn.pack(pady=15, fill="x")

        info_frame = tk.Frame(main_container, bg="#0f3460", padx=15, pady=15)
        info_frame.pack(pady=10, fill="x")

        self.range_label = tk.Label(
            info_frame,
            text="Press START to begin!",
            bg="#0f3460",
            fg="#00ff88",
            font=("Arial", 12, "bold")
        )
        self.range_label.pack()

        self.attempts_label = tk.Label(
            info_frame,
            text="Attempts: 0",
            bg="#0f3460",
            fg="white"
        )
        self.attempts_label.pack(pady=5)

        self.best_score_label = tk.Label(
            info_frame,
            text="Best Score: -",
            bg="#0f3460",
            fg="#ffd700"
        )
        self.best_score_label.pack()

        input_frame = tk.Frame(main_container, bg="#1a1a2e")
        input_frame.pack(pady=15)

        tk.Label(
            input_frame,
            text="Your Guess:",
            bg="#1a1a2e",
            fg="white"
        ).pack()

        self.guess_entry = tk.Entry(
            input_frame,
            font=("Arial", 18, "bold"),
            justify="center",
            width=12
        )
        self.guess_entry.pack(pady=5)

        self.guess_btn = tk.Button(
            input_frame,
            text="🎲 GUESS (Enter)",
            command=self.make_guess,
            font=("Arial", 12, "bold"),
            state="disabled"
        )
        self.guess_btn.pack(pady=10)

        self.result_label = tk.Label(
            main_container,
            text="",
            bg="#1a1a2e",
            fg="white",
            font=("Arial", 16, "bold")
        )
        self.result_label.pack(pady=10)

        self.hint_label = tk.Label(
            main_container,
            text="",
            bg="#1a1a2e",
            fg="#aaa"
        )
        self.hint_label.pack()

    def update_difficulty_display(self):
        best = self.best_scores[self.difficulty_var.get()]
        self.best_score_label.config(
            text=f"Best Score: {best}" if best else "Best Score: -"
        )

    def start_game(self):
        self.attempts = 0
        self.guess_history.clear()
        self.game_active = True

        difficulty = self.difficulty_var.get()
        self.max_range = {"Easy": 50, "Medium": 100, "Hard": 200}[difficulty]
        self.secret_number = random.randint(1, self.max_range)

        self.range_label.config(text=f"Guess a number between 1 and {self.max_range}")
        self.attempts_label.config(text="Attempts: 0")
        self.result_label.config(text="Good luck!")
        self.hint_label.config(text="")
        self.guess_btn.config(state="normal")
        self.guess_entry.config(state="normal")
        self.guess_entry.delete(0, tk.END)
        self.guess_entry.focus()
        self.update_difficulty_display()

    def make_guess(self):
        if not self.game_active:
            return

        try:
            guess = int(self.guess_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number")
            return

        if not 1 <= guess <= self.max_range:
            messagebox.showwarning("Out of range", f"1–{self.max_range}")
            return

        self.attempts += 1
        self.attempts_label.config(text=f"Attempts: {self.attempts}")

        if guess < self.secret_number:
            self.result_label.config(text="📈 TOO LOW")
        elif guess > self.secret_number:
            self.result_label.config(text="📉 TOO HIGH")
        else:
            self.game_active = False
            self.result_label.config(text=f"🎉 CORRECT! {self.secret_number}")
            self.hint_label.config(text=f"Attempts: {self.attempts}")
            self.guess_btn.config(state="disabled")
            self.guess_entry.config(state="disabled")

            diff = self.difficulty_var.get()
            if not self.best_scores[diff] or self.attempts < self.best_scores[diff]:
                self.best_scores[diff] = self.attempts
                messagebox.showinfo("New Record!", "🏆 New best score!")

        self.guess_entry.delete(0, tk.END)
        self.guess_entry.focus()

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    GuessNumberGame().run()