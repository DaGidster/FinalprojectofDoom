import pygame
import random
import time

pygame.init()


Width = 800
Height = 600
screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Fruit-Loop (Stroop Test)")


font = pygame.font.SysFont(None, 72)
small_font = pygame.font.SysFont(None, 36)


game_active = False


COLOR_MAP = {
    "red": (255, 0, 0),
    "blue": (0, 0, 255),
    "green": (0, 200, 0),
    "yellow": (255, 255, 0),
    "purple": (128, 0, 128),
    "orange": (255, 102, 0),
    "teal": (0, 255, 255)
}


words = list(COLOR_MAP.keys())


key_map = {
    pygame.K_r: "red",
    pygame.K_b: "blue",
    pygame.K_g: "green",
    pygame.K_y: "yellow",
    pygame.K_p: "purple",
    pygame.K_o: "orange",
    pygame.K_t: "teal"
}


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

running = True
clock = pygame.time.Clock()

while running:
    elapsed = time.time() - start_time
    time_left = max(0, int(game_duration - elapsed))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            
            if not game_active or time_left <= 0:
                    game_active = True
                    start_time = time.time()
                    score = 0
                    rounds = 0
                    reaction_times.clear()
                    new_round()

            
            elif game_active and time_left > 0:
                if event.key in key_map:
                    answer = key_map[event.key]

                    reaction_time = time.time() - round_start
                    reaction_times.append(reaction_time)

                    if answer == current_color:
                        score += 1

                    rounds += 1
                    new_round()

  
    screen.fill((30, 30, 30))

    if not game_active:
        title = font.render("FLoop(Stroop) Test", True, (255, 255, 255))
        instruction = small_font.render("Press SPACE to start", True, (255, 255, 255))

        screen.blit(title, (250, 200))
        screen.blit(instruction, (260, 300))

    elif time_left <= 0:
        accuracy = (score / rounds * 100) if rounds > 0 else 0

        text1 = small_font.render("Game Over!", True, (255, 255, 255))
        text2 = small_font.render(f"Score: {score}", True, (255, 255, 255))
        text3 = small_font.render(f"Accuracy: {round(accuracy, 1)}%", True, (255, 255, 255))
        text4 = small_font.render("Press SPACE to restart", True, (255, 255, 255))

        screen.blit(text1, (300, 200))
        screen.blit(text2, (300, 250))
        screen.blit(text3, (300, 300))
        screen.blit(text4, (230, 350))

    else:
        word_surface = font.render(current_word.upper(), True, COLOR_MAP[current_color])
        rect = word_surface.get_rect(center=(Width // 2, Height // 2))
        screen.blit(word_surface, rect)

        score_text = small_font.render(f"Score: {score}", True, (255, 255, 255))
        time_text = small_font.render(f"Time: {time_left}", True, (255, 255, 255))

        screen.blit(score_text, (10, 10))
        screen.blit(time_text, (650, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()


if reaction_times:
    avg_time = sum(reaction_times) / len(reaction_times)
    print(f"Average Reaction Time: {round(avg_time, 2)} seconds")
