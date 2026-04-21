import pygame
import random
import time


pygame.init()


Width = 800
Height = 600
screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Fruit-Loop(Stroop) Test")


font = pygame.font.SysFont(None, 72)
small_font = pygame.font.SysFont(None, 36)


COLOR_MAP = {
    "red": (255, 0, 0),
    "blue": (0, 0, 255),
    "green": (0, 200, 0),
    "yellow": (255, 255, 0)
}

words = list(COLOR_MAP.keys())


score = 0
rounds = 0
start_time = time.time()
game_duration = 30  

current_word = ""
current_color = ""

reaction_times = []
round_start = time.time()

def new_round():
    global current_word, current_color, round_start
    current_word = random.choice(words)
    current_color = random.choice(words)
    round_start = time.time()

new_round()

running = True
clock = pygame.time.Clock()

while running:
    screen.fill((30, 30, 30))

    elapsed = time.time() - start_time
    time_left = max(0, int(game_duration - elapsed))

    
    if time_left <= 0:
        text = small_font.render(f"Game Over! Score: {score}", True, (255, 255, 255))
        screen.blit(text, (150, 180))
        pygame.display.flip()
        continue

    
    word_surface = font.render(current_word.upper(), True, COLOR_MAP[current_color])
    screen.blit(word_surface, (Width // 2 - 100, Height // 2 - 50))

    
    score_text = small_font.render(f"Score: {score}", True, (255, 255, 255))
    time_text = small_font.render(f"Time: {time_left}", True, (255, 255, 255))

    screen.blit(score_text, (10, 10))
    screen.blit(time_text, (500, 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            key_map = {
                pygame.K_r: "red",
                pygame.K_b: "blue",
                pygame.K_g: "green",
                pygame.K_y: "yellow"
            }

            if event.key in key_map:
                answer = key_map[event.key]

                reaction_time = time.time() - round_start
                reaction_times.append(reaction_time)

                if answer == current_color:
                    score += 1

                rounds += 1
                new_round()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

# gives player reaction
if reaction_times:
    avg_time = sum(reaction_times) / len(reaction_times)
    print(f"Average Reaction Time: {round(avg_time, 2)} seconds")
