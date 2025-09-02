# Import the random module to generate a random number
import random

# 1. Generate a random number between 1 and 100
secret_number = random.randint(1, 100)

# 2. Welcome the player
print("Welcome to the Number Guessing Game!")
print("I'm thinking of a number between 1 and 100.")

# Initialize the guess variable and a counter for attempts
guess = None
attempts = 0

# 3. Start the game loop
while guess != secret_number:
    try:
        # 4. Get the player's guess
        guess = int(input("\nWhat's your guess? "))
        attempts += 1  # Increase the attempt counter

        # 5. Check the guess
        if guess == secret_number:
            print(f"\n🎉 Congratulations! You guessed it in {attempts} attempts! The number was {secret_number}.")
        elif guess > secret_number:
            print("⬇️ Too high! Try a lower number.")
        else:
            print("⬆️ Too low! Try a higher number.")

    except ValueError:
        # This handles the error if the user types something that isn't a number
        print("Please enter a valid number!")

# Optional friendly message after the game ends
print("\nThanks for playing!")
