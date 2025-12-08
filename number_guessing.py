import random

def give_hint(secret):
    if secret % 2 == 0:
        print("ℹ️ Hint: The secret number is EVEN.")
    else:
        print("ℹ️ Hint: The secret number is ODD.")

secret = random.randint(1, 100)
attempts = []

print("🎲 Guess the number between 1 and 100!")
print("Type 0 if you want a hint!")

while True:
    guess = int(input("Your guess: "))
    attempts.append(guess)

    if guess < secret:
        print("Higher!")
    elif guess > secret:
        print("Lower!")
    else:
        print(f"Correct! The number was {secret}.")
        print(f"You guessed it in {len(attempts)} attempts.")
        break
