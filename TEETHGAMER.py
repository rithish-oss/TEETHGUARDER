import pygame
import random
import sys
import os

def main():
    pygame.init()
    pygame.mixer.init()

    WIDTH, HEIGHT = 1400, 800
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tooth Guard")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("comic sans ms", 40)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Load background image
    bg_path = os.path.join(BASE_DIR, "bgg2.png")
    if not os.path.isfile(bg_path):
        print(f"Background image not found: {bg_path}")
        sys.exit(1)
    bg = pygame.image.load(bg_path)
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

    # Load sounds (no 'assets')
    def load_sound(file_name):
        path = os.path.join(BASE_DIR, file_name)
        if not os.path.isfile(path):
            print(f"Missing sound file: {path}")
            sys.exit(1)
        return path

    pygame.mixer.music.load(load_sound("guitar.mp3"))
    pygame.mixer.music.play(-1)
    correct_sound = pygame.mixer.Sound(load_sound("correct-156911.mp3"))
    buzzer_sound = pygame.mixer.Sound(load_sound("buzzer.mp3"))

    # Load player image
    player_img_path = os.path.join(BASE_DIR, "toofairy.png")
    if not os.path.isfile(player_img_path):
        print(f"Player image not found: {player_img_path}")
        sys.exit(1)
    player_img = pygame.image.load(player_img_path).convert_alpha()
    player_img = pygame.transform.scale(player_img, (170, 150))
    player = pygame.Rect(WIDTH // 2, HEIGHT - 170, 100, 100)

    # Food dictionary (image file name: (vitamin, benefit, type))
    food_images = {
        "almond2.png": ("Vitamin E", "Heals inflamed oral tissues", "good"),
        "milk2.png": ("Vitamin D", "Strengthens teeth and bones", "good"),
        "guava2.png": ("Vitamin C", "Reduces gingival inflammation", "good"),
        "meat2.png": ("Vitamin B", "Prevents mouth sores", "good"),
        "spinach2.png": ("Vitamin K", "Helps blood clotting and bones", "good"),
        "choci2.png": ("Chocolate", "High sugar content", "bad"),
        "cookie2.png": ("Cookie", "Too much sugar", "bad"),
        "soda2.png": ("Soda", "Enamel erosion", "bad"),
        "ciggs2.png": ("Cigarette", "Extremely harmful", "bad"),
    }

    foods = []
    FOOD_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(FOOD_EVENT, 1000)

    score = 5
    game_over = False
    message = ""

    def draw_text(text, y, color=(0, 0, 0), outline=(255, 255, 255)):
        outline_font = font.render(text, True, outline)
        base_font = font.render(text, True, color)
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            screen.blit(outline_font, (40 + dx, y + dy))
        screen.blit(base_font, (40, y))

    def reset_game():
        nonlocal foods, score, game_over, message
        foods.clear()
        score = 5
        game_over = False
        message = ""
        player.x = WIDTH // 2
        pygame.mixer.music.play(-1)

    running = True
    while running:
        screen.blit(bg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == FOOD_EVENT and not game_over:
                name = random.choice(list(food_images.keys()))
                x = random.randint(0, WIDTH - 100)
                food_img_path = os.path.join(BASE_DIR, name)
                if not os.path.isfile(food_img_path):
                    print(f"Food image missing: {food_img_path}")
                    continue
                img = pygame.image.load(food_img_path).convert_alpha()
                img = pygame.transform.scale(img, (100, 100))
                foods.append({"rect": pygame.Rect(x, 0, 100, 100), "img": img, "name": name, "speed": 5})

        keys = pygame.key.get_pressed()
        if not game_over:
            if keys[pygame.K_LEFT] and player.left > 0:
                player.x -= 10
            if keys[pygame.K_RIGHT] and player.right < WIDTH:
                player.x += 10

            for food in foods[:]:
                food["rect"].y += food["speed"]
                screen.blit(food["img"], food["rect"])

                if food["rect"].colliderect(player):
                    vitamin, benefit, ftype = food_images[food["name"]]
                    if ftype == "bad":
                        buzzer_sound.play()
                        score -= 1
                        message = f"{vitamin}: {benefit} (-1)"
                        if score <= 0:
                            pygame.mixer.music.stop()
                            game_over = True
                            message = f"{vitamin} destroyed your health. Game Over!"
                    else:
                        correct_sound.play()
                        score += 1
                        message = f"{vitamin}: {benefit} (+1)"
                    foods.remove(food)

            screen.blit(player_img, player)
            draw_text(f"Health: {score}", 10)
            if message:
                draw_text(message, 70)

        else:
            draw_text("Bad food destroyed your health.", HEIGHT // 2 - 50)
            draw_text("Press R to Retry or ESC to Quit", HEIGHT // 2 + 20)
            if keys[pygame.K_r]:
                reset_game()
            if keys[pygame.K_ESCAPE]:
                running = False

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()