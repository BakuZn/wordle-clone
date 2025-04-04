import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 700
GRID_SIZE = 5
MAX_TURNS = 5
CELL_SIZE = 60
PADDING = 10
FONT_SIZE = 36

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (120, 124, 126)
YELLOW = (201, 180, 88)
GREEN = (106, 170, 100)

# Word list (100 common 5-letter words)
WORDS = [
    "apple", "beach", "brain", "bread", "brush", "chair", "chest", "chord", 
    "click", "clock", "cloud", "dance", "diary", "drink", "earth", "flame", 
    "fleet", "fruit", "ghost", "grape", "green", "happy", "heart", "house", 
    "juice", "light", "money", "music", "party", "pizza", "plant", "radio", 
    "river", "salad", "sheep", "shoes", "smile", "snack", "snake", "snowy", 
    "socks", "sugar", "swing", "table", "toast", "tiger", "train", "water", 
    "whale", "wheel", "angel", "anger", "angle", "badge", "baker", "beard", 
    "began", "begin", "blame", "blank", "blend", "bless", "blind", "block", 
    "blood", "board", "boost", "brake", "brand", "brave", "break", "brick", 
    "brief", "bring", "broke", "brown", "build", "burst", "cabin", "cable", 
    "calm", "candy", "carry", "catch", "cause", "chain", "chair", "charm", 
    "chase", "cheek", "cheer", "chest", "chief", "child", "class", "clean", 
    "clear", "clerk", "click", "clock", "close", "cloth", "cloud", "coach", 
    "coast", "count", "court", "cover", "craft", "crash", "cream", "crime"
]

class WordleGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Wordle Clone")
        self.font = pygame.font.SysFont("Arial", FONT_SIZE)
        self.small_font = pygame.font.SysFont("Arial", FONT_SIZE - 10)
        self.reset_game()

    def reset_game(self):
        self.target_word = random.choice(WORDS).upper()
        self.guesses = []
        self.current_guess = ""
        self.turn = 0
        self.game_over = False

    def draw(self):
        self.screen.fill(WHITE)
        
        # Draw title
        title = self.font.render("WORDLE", True, BLACK)
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 30))
        
        # Draw grid
        for i in range(MAX_TURNS):
            for j in range(GRID_SIZE):
                rect = pygame.Rect(
                    WIDTH//2 - (GRID_SIZE * (CELL_SIZE + PADDING))//2 + j * (CELL_SIZE + PADDING),
                    100 + i * (CELL_SIZE + PADDING),
                    CELL_SIZE, CELL_SIZE
                )
                pygame.draw.rect(self.screen, GRAY if i >= len(self.guesses) else BLACK, rect, 2)
                
                if i < len(self.guesses):
                    letter = self.guesses[i][j]
                    color = self.get_letter_color(letter, j, i)
                    pygame.draw.rect(self.screen, color, rect)
                    text = self.font.render(letter, True, WHITE)
                    self.screen.blit(text, (
                        rect.x + CELL_SIZE//2 - text.get_width()//2,
                        rect.y + CELL_SIZE//2 - text.get_height()//2
                    ))
                elif i == len(self.guesses) and j < len(self.current_guess):
                    text = self.font.render(self.current_guess[j], True, BLACK)
                    self.screen.blit(text, (
                        rect.x + CELL_SIZE//2 - text.get_width()//2,
                        rect.y + CELL_SIZE//2 - text.get_height()//2
                    ))

        # Draw keyboard
        self.draw_keyboard()
        
        # Draw game over message
        if self.game_over:
            message = "You won!" if self.guesses[-1] == self.target_word else f"Word: {self.target_word}"
            text = self.font.render(message, True, GREEN if self.guesses[-1] == self.target_word else BLACK)
            self.screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT - 100))
            restart = self.small_font.render("Press R to restart", True, BLACK)
            self.screen.blit(restart, (WIDTH//2 - restart.get_width()//2, HEIGHT - 60))

        pygame.display.update()

    def draw_keyboard(self):
        keyboard = [
            "QWERTYUIOP",
            "ASDFGHJKL",
            "ZXCVBNM"
        ]
        
        for row_idx, row in enumerate(keyboard):
            for col_idx, letter in enumerate(row):
                key_width = 40 if len(row) > 7 else 45
                x = WIDTH//2 - (len(row) * (key_width + 5))//2 + col_idx * (key_width + 5)
                y = 450 + row_idx * (key_width + 10)
                rect = pygame.Rect(x, y, key_width, key_width)
                
                # Determine key color
                color = GRAY
                for guess in self.guesses:
                    if letter in guess:
                        if letter in self.target_word:
                            if any(guess[i] == letter and self.target_word[i] == letter for i in range(GRID_SIZE)):
                                color = GREEN
                            else:
                                color = YELLOW if color != GREEN else GREEN
                
                pygame.draw.rect(self.screen, color, rect)
                text = self.small_font.render(letter, True, WHITE)
                self.screen.blit(text, (
                    rect.x + key_width//2 - text.get_width()//2,
                    rect.y + key_width//2 - text.get_height()//2
                ))

    def get_letter_color(self, letter, pos, turn):
        if self.guesses[turn][pos] == self.target_word[pos]:
            return GREEN
        elif letter in self.target_word:
            return YELLOW
        return GRAY

    def handle_input(self, letter):
        if not self.game_over and len(self.current_guess) < GRID_SIZE:
            self.current_guess += letter.upper()

    def handle_backspace(self):
        if not self.game_over and len(self.current_guess) > 0:
            self.current_guess = self.current_guess[:-1]

    def handle_enter(self):
        global WORDS
        if self.game_over:
            return
            
        if len(self.current_guess) == GRID_SIZE:
            self.guesses.append(self.current_guess)
            if self.current_guess == self.target_word or len(self.guesses) == MAX_TURNS:
                self.game_over = True
            self.current_guess = ""
            self.turn += 1

    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_r and self.game_over:
                        self.reset_game()
                    elif event.key == pygame.K_BACKSPACE:
                        self.handle_backspace()
                    elif event.key == pygame.K_RETURN:
                        self.handle_enter()
                    elif event.unicode.isalpha():
                        self.handle_input(event.unicode)
            
            self.draw()
            clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = WordleGame()
    game.run()
