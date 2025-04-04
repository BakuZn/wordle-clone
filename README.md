This Python program is a Wordle clone built with Pygame. The game selects a random 5-letter word from a predefined list. The player has 5 attempts to guess the word. After each guess, the game provides color-coded feedback for each letter:

🟩 Green: Correct letter in the correct position

🟨 Yellow: Correct letter in the wrong position

⬜ Gray: Incorrect letter

The interface displays:

A title and a 5x5 grid for guesses

A virtual keyboard with letter feedback

A game-over message with the correct word if the player fails

The player types guesses using the keyboard, can delete letters with backspace, and submits with Enter. Pressing "R" restarts the game once it ends.
