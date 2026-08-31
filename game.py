import pygame
from starting import Nyx, Gods, items, ememies

pygame.init() # This turns Pygame on
screen = pygame.display.set_mode((800, 600)) # Creates an 800x600 pixel window
pygame.display.set_caption("The Ballad of Nyx")
font_title = pygame.font.SysFont(None,40)
font_option = pygame.font.SysFont(None, 30)


state = "GOD_SELECTION"
running = True

while running:
    # 1. CHECK FOR EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # Check for keyboard presses
        if event.type == pygame.KEYDOWN and state == "GOD_SELECTION":
            if event.key == pygame.K_1:
                Nyx["ally_god"] = "Apolo"
            elif event.key == pygame.K_2:
                Nyx["ally_god"] = "Ares"
            elif event.key == pygame.K_3:
                Nyx["ally_god"] = "Athena"
            elif event.key == pygame.K_4:
                Nyx["ally_god"] = "Poseidon"
            elif event.key == pygame.K_5:
                Nyx["ally_god"] = "Artemis"
                
            # If a valid key was pressed, apply the stats and change state!
            if Nyx["ally_god"] != "":
                # (You would run your stat update logic here)
                state = "SHOW_CONFIRMATION" 
            elif state == "SHOW_CONFIRMATION":
                if event.key == pygame.K_SPACE:
                    state = "MAIN_MENU"
    # 2. DRAW THE SCREEN
    screen.fill((0, 0, 0)) # Clear the screen with black
    
    if state == "GOD_SELECTION":
        title_text = font_title.render("--- Select your God to ally you in battle ---", True, (255, 255, 0))
        screen.blit(title_text, (50, 50))
        menu_options = [
            "1. Apolo (Fire)",
            "2. Ares (Rage)",
            "3. Athena (Clear Mind)",
            "4. Poseidon (Water)",
            "5. Artemis (Nature)"
        ]
        # Loop through the list and draw each option, moving down the screen
        y_position = 120
        for option in menu_options:
            option_text = font_option.render(option, True, (255, 255, 255)) # White text
            screen.blit(option_text, (50, y_position))
            y_position += 40 # Move down 40 pixels for the next line

    elif state == "SHOW_CONFIRMATION":
            # 1. Get the chosen god's stats from your dictionaries
            ally = Nyx["ally_god"]
            weapon = Gods[ally]["weapon"]
            element = Gods[ally]["element"]
            
            # 2. Render the text lines
            line1 = font_title.render(f"You have chosen {ally} as your ally!", True, (0, 255, 0)) # Green
            line2 = font_option.render(f"The {weapon} appears in Nyx's hand.", True, (255, 255, 255))
            line3 = font_option.render(f"She is granted the power of {element}!", True, (255, 255, 255))
            prompt = font_option.render("Press SPACE to begin the journey...", True, (255, 255, 0)) # Yellow
            
            # 3. Draw them to the screen
            screen.blit(line1, (50, 100))
            screen.blit(line2, (50, 160))
            screen.blit(line3, (50, 200))
            screen.blit(prompt, (50, 300))

    # 3. UPDATE DISPLAY
    pygame.display.flip()