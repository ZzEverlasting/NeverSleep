import pygame
import sys
import json
import csv
from user_data import register_user, update_user_customization



# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1240, 880
FONT = pygame.font.Font(None, 32)
SM_FONT = pygame.font.Font(None, 24)
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
BUTTON_COLOR = (100, 100, 180)
HOVER_COLOR = (140, 140, 220)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class CharacterCustomization:
    def __init__(self, session):
        self.session = session
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Never Sleep-Character Creation Menu")
        self.clock = pygame.time.Clock()
        self.page = 'name'
        self.initialize_data()
        self.initial_char_name_elements()
        self.initialize_buttons()
        self.customization_options()
        self.character_data = {}
        self.current_trait_index = 0
        self.traits = [
            {'name': 'Class', 'options': ['Warrior', 'Mage', 'Archer']},
            {'name': 'Gender', 'options': ['Male', 'Female', 'Non-Binary']},
            {'name': 'Race', 'options': ['Human', 'Elf', 'Dwarf', 'Orc']},
            {'name': 'Build', 'options': ['Skinny', 'Average', 'Ripped', 'Bulked']}
        ]    

    def initialize_data(self):
        self.display_user_data()

    def initial_char_name_elements(self):
        self.input_box_name = pygame.Rect(500, 400, 180, 32)
        self.name_text = ''
        self.name_message = ""
        self.active_name = False

    def initialize_buttons(self):
        self.button_confirm = pygame.Rect(900, 600, 120, 60)
        self.button_back = pygame.Rect(900, 670, 120, 60)
        self.button_help = pygame.Rect(1030, 670, 120, 60)

    def draw_char_name_elements(self, mouse_pos):
        self.screen.fill(BLACK)  # Clear screen
        self.screen.blit(FONT.render('Create A Character Name (Max 12 CHAR)', True, WHITE), (400, 450))
        self.screen.blit(FONT.render('Press ENTER KEY to Continue', True, WHITE), (420, 600))
        pygame.draw.rect(self.screen, COLOR_ACTIVE if self.active_name else COLOR_INACTIVE, self.input_box_name, 2)
        self.screen.blit(FONT.render(self.name_text, True, WHITE), (self.input_box_name.x + 5, self.input_box_name.y + 5))
        self.draw_button(self.button_help, 'Help', mouse_pos)

    def draw_selection_elements(self, mouse_pos):
        self.screen.fill(BLACK)
        current_trait = self.traits[self.current_trait_index]
        self.screen.blit(FONT.render(f'Choose your {current_trait["name"]}:', True, WHITE), (400, 350))
        button_y = 400
        for option in current_trait['options']:
            button = pygame.Rect(400, button_y, 200, 40)
            selected = (self.character_data.get(current_trait['name'].lower()) == option)
            color = HOVER_COLOR if selected else BUTTON_COLOR
            self.draw_button(button, option, mouse_pos, color)
            button_y += 50

    
    def draw_end_customization (self, mouse_pos):
        self.screen.fill(BLACK)
        self.screen.blit(FONT.render('Congratulations! You have created a character!', True, WHITE), (100, 50))
        text_y = 100
        for key, value in self.character_data.items():
            attribute_text = f"{key.capitalize()}: {value}"
            self.screen.blit(FONT.render(attribute_text, True, WHITE), (100, text_y))
            text_y += 30
        self.draw_button(self.button_back, 'Back', mouse_pos)
        self.draw_button(self.button_help, 'Help', mouse_pos)

    def draw_elements(self):
        self.screen.fill(BLACK)
        if self.page == 'name':
            self.draw_char_name_elements(pygame.mouse.get_pos())
        elif self.page == 'options':
            self.draw_selection_elements(pygame.mouse.get_pos())
        elif self.page == 'complete':
            self.draw_end_customization(pygame.mouse.get_pos())
        elif self.page == 'help':
            self.draw_help_elements(pygame.mouse.get_pos())
        pygame.display.flip()

    
    def draw_help_elements(self, mouse_pos):
        self.screen.fill(BLACK)
        lines = [
            "Welcome to Never Sleep--Character Creation!",
            "When creating a new character you can customize the following:",
            "Name, Gender, Class, Race, and Build of you character. ",
            "Here's how you can navigate through the Character Creation:",
            "You will be prompted for the options disscused previously, be cautious to the option messages",
            "1. Name: Click on the text box provided to enable name entry, there is a max.",
            "2. Gender: Choose which gender you'd like your character to have.",
            "3. Class: Choose which class you'd like your character to have.",
            "4. Race: Choose which race you'd like your character to have.",
            "5. Build: Choose which build type you'd like your character to have.",
            "","",
            "Each page will have button for you to click on if you need help or change your choice.",
            "**Class will have a preset initial statistic balance, may very between classes**"
        ]

        y_pos = 50
        for line in lines:
            if line.startswith("1.") or line.startswith("2.") or line.startswith("3.") or line.startswith("4.") or line.startswith("5."):
                text_surface = SM_FONT.render(line, True, WHITE)
            else:
                text_surface = FONT.render(line, True, WHITE)
            self.screen.blit(text_surface, (10, y_pos))
            y_pos += 40 if line.startswith("1.") else 30  # Increase spacing before a new section

        self.draw_button(self.button_back, "Back", mouse_pos)

        pygame.display.flip()

    def display_user_data(self):
        username = self.session['username']
        user_id = self.session['user_id']
        customization_data = self.get_user_customization(user_id)
        msg_y = 100
        self.screen.fill(BLACK)
        self.screen.blit(FONT.render(f"Username: {username}", True, WHITE), (50, msg_y))
        self.screen.blit(FONT.render(f"User ID: {user_id}", True, WHITE), (50, msg_y + 30))
        msg_y += 60
        for key, value in customization_data.items():
            self.screen.bilt(FONT.render(f"{key.capitalize()}: {value}", True, WHITE), (50, msg_y))
            msg_y += 30
        pygame.display.flip()

    def get_user_customization(self, user_id):
        with open('user_data.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['user_id'] == user_id:
                    return json.loads(row['customization_data'])
        return {}

    def customization_options(self):
        self.class_stats = {
            'Warrior': {'strength': 18, 'intelligence': 13, 'agility': 17},
            'Mage': {'strength': 12, 'intelligence': 19, 'agility': 14},
            'Archer': {'strength': 15, 'intelligence': 15, 'agility': 18}
        }
        self.genders = ['Male', 'Female', 'Non-Binary']
        self.races = ['Human', 'Elf', 'Dwarf', 'Orc']
        self.builds = ['Skinny', 'Average', 'Ripped', 'Bulked']
        self.classes = list(self.class_stats.keys())
        self.traits = [self.classes, self.genders, self.races, self.builds]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event)
            elif event.type == pygame.KEYDOWN:
                self.handle_key_input(event)

    def handle_mouse_click(self, event):
        mouse_x, mouse_y = event.pos
        if self.page == 'options':
            for index, trait in enumerate(self.traits[self.current_trait_index]['options']):
                button_y = 400 + (index * 50)
                button = pygame.Rect(400, button_y, 200, 40)
                if button.collidepoint(mouse_x, mouse_y):
                    self.character_data[self.traits[self.current_trait_index]['name'].lower()] = trait
                    if self.current_trait_index < len(self.traits) - 1:
                        self.current_trait_index += 1
                    else:
                        self.finalize_character_creation()
                        self.page = 'complete'
                    break

        elif self.input_box_name.collidepoint(mouse_x, mouse_y):
            self.active_name = True
        elif self.button_confirm.collidepoint(mouse_x, mouse_y):
            if self.current_trait_index < len(self.traits) - 1:
                self.current_trait_index += 1
            else:
                self.finalize_character_creation()
                self.page = 'complete'
        elif self.button_back.collidepoint(mouse_x, mouse_y):
            if self.current_trait_index > 0:
                self.current_trait_index -= 1
        elif self.button_help.collidepoint(mouse_x, mouse_y):
            self.page = 'help'


    def handle_key_input(self, event):
        if self.active_name:
            if event.key == pygame.K_BACKSPACE:
                self.name_text = self.name_text[:-1]
            elif event.key == pygame.K_RETURN:
                if len(self.name_text) > 0:  # Ensure the name is not empty
                    self.active_name = False
                    self.character_data['name'] = self.name_text
                    self.page = 'options'  # Move to the next customization option
            else:
                self.name_text += event.unicode
                if len(self.name_text) >= 12:
                    self.name_text = self.name_text[:12]  # Limit to 12 characters


    def finalize_character_creation(self):
        if all(k in self.character_data for k in ['name', 'class', 'gender', 'race', 'build']):
            self.save_character_data(
                self.character_data['name'],
                self.character_data['class'],
                self.character_data['gender'],
                self.character_data['build'],
                self.character_data['race']
            )
            self.page = 'complete'  # Move to a completion or confirmation screen
        else:
            print("Character data is incomplete, cannot save.")


    def save_character_data(self, name, char_class, gender, build, race):
        self.character_data = {'name': name, 'class': char_class, 'gender': gender, 'race': race, 'build': build}

    def draw_button(self, rect, text, mouse_pos, button_color=None):
        if not button_color:
            button_color = HOVER_COLOR if rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(self.screen, button_color, rect)
        text_render = FONT.render(text, True, WHITE)
        text_rect = text_render.get_rect(center=rect.center)
        self.screen.blit(text_render, text_rect)

    def run(self):
        while True:
            self.handle_events()
            self.draw_elements()
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    customization = CharacterCustomization()
    customization.run()
