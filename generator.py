import random
import os
from word_lists.shared_words import articles, prepositions

def load_word_lists(theme):
    """Load the correct word lists based on theme selected."""
    try:
        if theme == "nature":
            from word_lists.nature import nouns, noun2, verbs, adjectives
        elif theme == "love":
            from word_lists.love import nouns, noun2, verbs, adjectives
        elif theme == "mystery":
            from word_lists.mystery import nouns, noun2, verbs, adjectives
        else:
            #default to nature if no valid theme is chosen
            from word_lists.nature import nouns, noun2, verbs, adjectives
    except ImportError as e:
        print(f"Error loading word lists: {e}")
        return [], [], [],[]
    
    if not all([nouns, noun2, verbs, adjectives]):
        print("Error: One or more word lists are empty.")
        return [], [], [],[]

    return nouns, noun2, verbs, adjectives



def select_word(word_pool, used_words, allow_repeat=False):
    """Select a random word from word_pool that hasn't been used yet, 
    unless allow_repeat is True for articles and articles only. Nouns, verbs, and adj should not be repeated.
    """
    if not allow_repeat:
        available_words = [word for word in word_pool if word not in used_words]
    else:
        available_words = word_pool

    if not available_words:
        return " "

    word = random.choice(available_words)

    if not allow_repeat:
        used_words.add(word)

    return word



def generate_poem(nouns, noun2, verbs, adjectives, num_lines):
    """Generate a poem with 1 to 3 lines, making sense with random word combinations."""
    #define sentence structures that use articles and prepositions
    templates = [
        "{article} {adjective} {noun} {verb}",
        "{noun} {verb} {preposition} {article} {adjective} {noun2}",
        "{adjective} {noun}",
    ]
    

    poem = []
    used_words = set()

    for _ in range(num_lines):
        template = random.choice(templates)
        line = template.format(
            article=select_word(articles, used_words),
            preposition=select_word(prepositions, used_words),
            adjective=select_word(adjectives, used_words),
            noun=select_word(nouns, used_words),
            verb=select_word(verbs, used_words),
            noun2=select_word(noun2, used_words),
        )
        poem.append(line)

    #capitalize
    if poem:
        poem[0] = poem[0].capitalize()

    for i in range(len(poem)): #punctuation
        if i == len(poem) - 1:
            poem[i] = poem[i] + "."
        elif i < 2:
            poem[i] = poem[i] + ","
    
    return "\n".join(poem)


def save_poem(poem, filename="output/poem.txt"):
    """Save generated poem to a text file in the output folder."""
    main_folder = "/Users/danatran/Documents/Fall 2024 - CS 5001/cs5001-final-danatran"
    output_path = os.path.join(main_folder, filename)

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(output_path, "w") as file:
        file.write(poem)


def main():
    """Main function to run the poem generator."""
    print("Welcome to the Random Poem Generator!\n")
    print("Themes: Nature, Love, or Mystery")
    theme_choice = input("Please choose a theme: ").strip().lower()

    nouns, noun2, verbs, adjectives = load_word_lists(theme_choice)

    #missing or empty word lists?
    if not nouns or not verbs or not adjectives:
        print("Error")
        return
    
    while True:
        try:
            num_lines = int(input("How long would you like your poem to be? It can be 1-3 lines: "))
            if num_lines <= 0:
                print("Number must be positive!")
            else:
                break
        except ValueError:
            print("Please enter a valid number.")

    while True:
        poem = generate_poem(nouns, noun2, verbs, adjectives,num_lines)
        print("\nGenerated Poem:\n")
        print(poem)
#regenerate a new poem if user is unhappy with what was generated
        regenerate_option = input("\nWould you like to generate a different poem? (yes/no): ").strip().lower()
        if regenerate_option not in {"yes", "y"}:
            break
    
    save_option = input("\nWould you like to save this poem? (yes/no): ").strip().lower()
    if save_option in {"yes", "y"}:
        save_poem(poem)
        print("Poem saved to output/poem.txt!")


if __name__ == "__main__":
    main()
