import random

def give_hint(secret):
    if secret % 2 == 0:
        print("ℹ️ Hint: The secret number is EVEN.")
    else:
        print("ℹ️ Hint: The secret number is ODD.")

def show_attempts(attempts):
    print("Your attempts so far:", attempts)

# New function: show difference between last guess and secret
def show_difference(secret, last_guess):
    diff = abs(secret - last_guess)
    print(f"🔍 You're {diff} away from the secret number.")
# show_trend(secret, attempts) tells the player if their last guess
# is closer or further from the secret number compared to the previous guess.
def show_trend(secret, attempts):
    if len(attempts) < 2:
        return
    prev_diff = abs(secret - attempts[-2])
    curr_diff = abs(secret - attempts[-1])
    if curr_diff < prev_diff:
        print("🔥 You're getting closer!")
    elif curr_diff > prev_diff:
        print("❄️ You're moving away!")

secret = random.randint(1, 100)
attempts = []

print("🎲 Guess the number between 1 and 100!")
print("Type 0 if you want a hint!")

while True:
    guess = int(input("Your guess: "))
    attempts.append(guess)

    if guess == 0:
        give_hint(secret)
        continue

    if guess < secret:
        print("Higher!")
    elif guess > secret:
        print("Lower!")
    else:
        print(f"Correct! The number was {secret}.")
        print(f"You guessed it in {len(attempts)} attempts.")
        break

    show_attempts(attempts)
    show_difference(secret, guess)