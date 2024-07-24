import pygame
import random
import time

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre 800/600 avant
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Charger les images
rock_img = pygame.image.load('rock.png')
paper_img = pygame.image.load('paper.png')
scissors_img = pygame.image.load('scissors.png')
puits_img = pygame.image.load('puits.png')

# Redimensionner les images
rock_img = pygame.transform.scale(rock_img, (200, 200))
paper_img = pygame.transform.scale(paper_img, (200, 200))
scissors_img = pygame.transform.scale(scissors_img, (200, 200))
puits_img = pygame.transform.scale(puits_img, (200, 200))

images = [rock_img, paper_img, scissors_img, puits_img]

# Position et centres des images (cercles) 100 300 | 300 300 | 500 300
rock_pos = (80, 300)
paper_pos = (300, 300)
scissors_pos = (520, 300)

rock_center = (rock_pos[0] + 100, rock_pos[1] + 100)
paper_center = (paper_pos[0] + 100, paper_pos[1] + 100)
scissors_center = (scissors_pos[0] + 100, scissors_pos[1] + 100)

# Position de l'image de l'ordinateur (à vérifier)
computer_pos = (screen_width // 2 - 100, 50)

# Rayon des cercles
radius = 100

# Initialisation des polices
font = pygame.font.SysFont(None, 55)
score_font = pygame.font.SysFont(None, 40)
result_font = pygame.font.SysFont(None, 70)

# Scores
player_score = 0
computer_score = 0

# Fonction pour choisir aléatoirement
def adversaire():
    while True:
        for i in range(0,1):
            nombre = random.randint(1,100)
            print(nombre)

        if nombre <= 33:
            return "Pierre"
        elif nombre >= 34 and nombre <= 66:
            return "Feuille"
        elif nombre >= 67 and nombre <= 99:
            return "Ciseaux"
        else:
            return "Puits"

computer_choice = adversaire()

# Fonction pour déterminer le résultat
def get_result(user_choice, computer_choice):
    if (user_choice == "Pierre" and computer_choice == "Ciseaux") or \
       (user_choice == "Feuille" and computer_choice == "Pierre") or \
       (user_choice == "Ciseaux" and computer_choice == "Feuille"):
        return "Victoire", GREEN
    elif (user_choice == "Pierre" and computer_choice == "Puits") or \
       (user_choice == "Feuille" and computer_choice == "Puits") or \
       (user_choice == "Ciseaux" and computer_choice == "Puits"):
        return "Y'a triche", RED
    elif user_choice == computer_choice:
        return "Égalité", BLACK
    else:
        return "Défaite", RED

# Fonction pour vérifier si le clic est à l'intérieur du cercle
def is_inside_circle(center, radius, pos):
    return (center[0] - pos[0]) ** 2 + (center[1] - pos[1]) ** 2 <= radius ** 2

# Boucle principale du jeu
running = True
user_choice = None
computer_choice = None
result = ""
result_color = BLACK
start_time = None
show_result = False
score_updated = False
animation_index = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and not start_time:
            mouse_pos = event.pos

            # Vérifier si l'utilisateur a cliqué à l'intérieur d'un des cercles
            if is_inside_circle(rock_center, radius, mouse_pos):
                user_choice = "Pierre"
            elif is_inside_circle(paper_center, radius, mouse_pos):
                user_choice = "Feuille"
            elif is_inside_circle(scissors_center, radius, mouse_pos):
                user_choice = "Ciseaux"
            else:
                user_choice = None

            if user_choice:
                computer_choice = adversaire()
                result, result_color = get_result(user_choice, computer_choice)
                start_time = time.time()
                show_result = False
                score_updated = False

    # Dessiner l'écran
    screen.fill(WHITE)

    # Afficher les images ou l'image choisie par l'utilisateur
    if user_choice and computer_choice:
        elapsed_time = time.time() - start_time
        if elapsed_time < 3:
            # Animation de défilement des images de l'ordinateur
            animation_index = int(elapsed_time * 10) % 3
            screen.blit(images[animation_index], computer_pos)

            # Dessiner le cadre pour le chrono 2 40
            countdown = 3 - int(elapsed_time)
            countdown_text = font.render(f"{countdown}", True, RED)
            text_rect = countdown_text.get_rect(center=(screen_width // 2, 30))
            screen.blit(countdown_text, text_rect)
        else:
            # Afficher le résultat et l'image de l'ordinateur après 3 secondes
            show_result = True
            if not score_updated:
                if result == "Victoire":
                    player_score += 1
                elif result == "Défaite":
                    computer_score += 1
                elif result == "Y'a triche":
                    computer_score += 1    
                score_updated = True

    if show_result and user_choice and computer_choice:
        # Afficher le résultat au milieu de l'écran, légèrement remonté
        result_text = result_font.render(f"{result}", True, result_color)
        result_rect = result_text.get_rect(center=(screen_width // 2, screen_height // 2 - 30))
        screen.blit(result_text, result_rect)

        # Afficher l'image choisie par l'ordinateur au-dessus
        if computer_choice == "Pierre":
            screen.blit(rock_img, computer_pos)
        elif computer_choice == "Feuille":
            screen.blit(paper_img, computer_pos)
        elif computer_choice == "Ciseaux":
            screen.blit(scissors_img, computer_pos)
        elif computer_choice == "Puits":
            screen.blit(puits_img, computer_pos)

        # Réinitialiser les choix après affichage du résultat
        if elapsed_time >= 5:
            user_choice = None
            computer_choice = None
            show_result = False
            start_time = None

    # Afficher les images fixes des choix de l'utilisateur
    screen.blit(rock_img, rock_pos)
    screen.blit(paper_img, paper_pos)
    screen.blit(scissors_img, scissors_pos)

    # Afficher les scores sur une même ligne en bas de l'écran
    player_score_text = score_font.render(f"Mon score: {player_score}", True, GREEN)
    computer_score_text = score_font.render(f"Adversaire: {computer_score}", True, RED)
    screen.blit(player_score_text, (screen_width // 2 - 200, screen_height - 50))
    screen.blit(computer_score_text, (screen_width // 2 + 20, screen_height - 50))

    pygame.display.flip()

pygame.quit()
