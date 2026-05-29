# Flashcards: Project 3
import json
import random

class Flashcard:
    def __init__(self, question, answer, difficulty):
        self.question = question
        self.answer = answer
        self.difficulty = difficulty


def main():
    # Loading in the flashcards
    try:
        with open("cards.json", "r") as file:
            cards_data = json.load(file)
            cards = [Flashcard(**card) for card in cards_data]

    except(json.JSONDecodeError, FileNotFoundError):
        cards = []
    

    # Printing menu and obtaining user input
    while True:
        menu()

        try:
            user_choice = int(input("Please select an option (1-4): "))
        except ValueError:
            print("Please enter a valid number (1-4)\n")
            continue
        
        if user_choice in [1, 2, 3, 4]:
            user_action(user_choice, cards)
            if user_choice == 4:
                break
        
        else:
            print("Please enter a valid number (1-4)\n")
            continue


# Determining user action and calling appropriate function
def user_action(user_choice, cards):
    if user_choice == 1:
        add_flashcard(cards)
    elif user_choice == 2:
        study_flashcards(cards)
    elif user_choice == 3:
        view_flashcards(cards)
    elif user_choice == 4:
        quit_program(cards)
    else:
        print("Must be a number that is 1-4\n")

# Creates a new flashcard and adds it to the list
def add_flashcard(cards):
    new_question = input("Enter the new flashcard question: ")
    new_answer = input("Enter the answer to the flashcard: ")

    # Validating difficulty input
    new_difficulty = ""

    while new_difficulty.lower() not in ["easy", "medium", "hard"]:
        new_difficulty = input("Enter the difficulty of the flashcard (easy, medium, hard): ")

        if new_difficulty.lower() not in ["easy", "medium", "hard"]:
            print("Please enter a valid difficulty (easy, medium, hard)\n")
        
    # Creating new card and adding it to flashcards list
    new_card = Flashcard(new_question, new_answer, new_difficulty)
    cards.append(new_card)

def choose_difficulty(cards):
    new_difficulty = ""

    while new_difficulty.lower() not in ["easy", "medium", "hard"]:
        new_difficulty = input("Easy, Medium, or Hard difficulty?: ")

        if new_difficulty.lower() not in ["easy", "medium", "hard"]:
            print("Please enter a valid difficulty (easy, medium, hard)\n")
    
    correct_cards = [card for card in cards if card.difficulty.lower() == new_difficulty.lower()]
    return correct_cards



def study_flashcards(cards):
    if not cards:
        print("No flashcards available to study. Please add some flashcards first.\n")
        return

    # Filtering flashcards based on user-selected difficulty and shuffling them
    correct_cards = choose_difficulty(cards)

    if not correct_cards:
        print("No flashcards found for the selected difficulty. Please add some flashcards of that difficulty first.\n")
        return

    shuffled_cards = random.sample(correct_cards, len(correct_cards))
    
    score_counter = 0

    for card in shuffled_cards:
        print(f"\nQuestion: {card.question}")
        user_answer = input("\nYour Answer: ")

        if user_answer.strip().lower() == card.answer.strip().lower():
            score_counter += 1
            print("Correct!\n")
        else:
            print(f"Close, but the right answer is: {card.answer}\n")

    # Printing score
    print(f"Nice work, ninja! Your score is: {score_counter}/{len(shuffled_cards)}")

    
def view_flashcards(cards):
    print("\n=== YOUR FLASHCARDS ===\n")
    for index, card in enumerate(cards, start=1):
        print(f"{index}.\n Q: {card.question}\n A: {card.answer}\n Difficulty: {card.difficulty}\n")


def quit_program(cards):
    try:
        with open("cards.json", "w") as file:
            json.dump([card.__dict__ for card in cards], file, indent=4)
    except IOError:
        print("An error occurred while saving the flashcards.")

    print("Farewell. Never leave for tomorrow what can be done today...")


def menu():
    print("\n=== Flashcards: Ninjago Edition ===\n")

    print("1. Add a flashcard")
    print("2. Study flashcards")
    print("3. View all flashcards")
    print("4. Save & Exit\n")


if __name__ == "__main__":
    main()
