import streamlit as st
import openai
import os
from dotenv import load_dotenv

load_dotenv()

class OpenAIGenerator:
    def __init__(self, api_key):
        openai.api_key = api_key

    def generate(self, difficulty):
        # Use OpenAI API to generate volcabulary based on the given difficulty
        prompt = self._get_prompt(difficulty)
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=50,
            n=1,
            stop=None,
        )
        generated_text = response.choices[0].text.strip()
        return generated_text

    def generate_hint(self, word):
        # Use OpenAI API to generate hints based on the given word
        prompt = f"Provide a hint for the word: {word}, you can provide it' part of speech or it's definition, and remember don't use the word in your hint."
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=50,
            n=1,
            stop=None,
        )
        generated_hint = response.choices[0].text.strip()
        return generated_hint

    def _get_prompt(self, difficulty):
        if difficulty == "easy":
            return "Generate a CEFR A1 Beginner level or a easier vocabulary word."
        elif difficulty == "medium":
            return "Generate a or CEFR A2 Elementary level or CEFR B1 Intermediate level vocabulary word."
        elif difficulty == "hard":
            return "Generate a B2 Upper Intermediate level or CEFR C1 Advanced level vocabulary word."
        elif difficulty == "expert":
            return "Generate a CEFR C2 Proficient level  vocabulary word."
        else:
            return "Generate a random vocabulary word."


class HangmanGame:
    def __init__(self, word):
        self.word = word.upper()
        self.guessed_letters = set()
        self.max_attempts = 5
        self.attempts_left = self.max_attempts

    def display_word(self):
        return ''.join([letter if letter in self.guessed_letters else ' _ ' for letter in self.word])
    
    def guessed_letters_display(self):
        return ', '.join(sorted(list(self.guessed_letters)))

    def num_word(self):
        return ''.join([' _ ' for letter in self.word])

    def guess_letter(self, letter):
        # Check if the input is a single English letter
        if not letter.isalpha() or len(letter) != 1 or not letter.isalpha():
            return '⚠️ Please enter a single English letter.'
        letter = letter.upper()
        if letter in self.guessed_letters:
          self.attempts_left -= 1
          return '😵 Guessed already!'  # Letter already guessed
        self.guessed_letters.add(letter)
        if letter not in self.word:
          self.attempts_left -= 1
          return '❌ Incorrect guess!'
        return '✔️ Correct guess!'

    def is_game_over(self):
        return self.attempts_left == 0 or set(self.word).issubset(self.guessed_letters)


# generate random vocabulary
    
def generate_random_word(difficulty):
    api_key = os.getenv('API_KEY')
    generator = OpenAIGenerator(api_key)
    return generator.generate(difficulty)

# Streamlit UI

def main():
    st.set_page_config(
        page_title="AI Education Tool",
        page_icon=":books:",
        layout="centered",
        initial_sidebar_state="expanded",
    )
    st.title("Hangman Game 💭")

    # use st.session_state to store game state
    if 'game' not in st.session_state:
        st.session_state.game = None

    game = st.session_state.game

    # choose difficulty
    with st.form("difficulty_form"):
        st.subheader("😜 Select Difficulty:")
        difficulty = st.radio("Choose the difficulty level.", [
                              "Easy", "Medium", "Hard", "Expert"])
        submit_button = st.form_submit_button("Submit")

    if submit_button:
                
        # Start new Game
        word = generate_random_word(difficulty)
        print(word)
        game = HangmanGame(word)
        st.session_state.game = game

    if game:
        # num of word
        st.subheader("✨ Word to guess: " + game.num_word())

        # Hint
        if st.button("💡 Hint"):
            hint = OpenAIGenerator(os.getenv('API_KEY')
                                   ).generate_hint(game.word)
            st.write(f"Hint: {hint}")

        st.divider()

        # User Input
        st.subheader("😀Guess a letter!")
        user_input = st.text_input("Your Input: ")

        if user_input:
            st.write(game.guess_letter(user_input))

            st.divider()

            # Update user state
            # Guessed Letters
            st.subheader("🔤 Letters You've Guessed : " 
                        + game.guessed_letters_display())
            st.write("Your Guess: ", game.display_word())
            st.write("Attempts left: ", game.attempts_left)

            # Is Game over
            if game.is_game_over():
              replay_button = st.button("Play Again")
              if set(game.word).issubset(game.guessed_letters):
                  st.success(
                      f"🎉 Congratulations! You guessed the word: {game.word}.")
                  st.session_state.game = None
              else:
                  st.error(f"🤡 Game over! The word was: {game.word}") 
                  st.session_state.game = None

              # Replay
              if replay_button: 
                st.session_state.game = None
                st.rerun()
                

if __name__ == "__main__":
    main()
