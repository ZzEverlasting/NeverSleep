import pygame
import sys
import csv
from login_system import LoginSystem
from user_data import login_user, register_user, update_user_customization, initialize_user_data
from customization import CharacterCustomization

# Initialize pygame
pygame.init()

# Constants for GUI
SCREEN_WIDTH, SCREEN_HEIGHT = 1240, 880
TITLE_FONT = pygame.font.Font(None, 100)
FONT = pygame.font.Font(None, 32)
SM_FONT = pygame.font.Font(None, 24)
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
BUTTOFF_COLOR = (0, 123, 255)
BUTTON_COLOR = (100, 100, 180)
HOVER_COLOR = (140, 140, 220)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
initialize_user_data()

class GUI:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Never Sleep-Login Menu")
        self.clock = pygame.time.Clock()
        self.login_system = LoginSystem()
        self.active_button = None
        self.customization = None
        self.active_section = 'login'
        self.user_session = {}
        self.login_successful = False
        self.initialize_login_elements()
        self.initialize_registration_elements()
        self.initialize_buttons()

    def initialize_login_elements(self):
        self.input_box_username = pygame.Rect(620, 400, 180, 32)
        self.input_box_password = pygame.Rect(620, 450, 180, 32)
        self.username_text = ''
        self.password_text = ''
        self.active_username = False
        self.active_password = False
        self.show_password = False
        self.login_message = ""
    
    def initialize_registration_elements(self):
        self.input_box_confirm = pygame.Rect(620, 500, 180, 32)
        self.confirm_password_text = ''
        self.register_message = ''
        self.active_confirm_password = False
    
    def initialize_help_elements(self):
        self.help_message = ''

    def initialize_buttons(self):
        self.button_login = pygame.Rect(770, 770, 110, 50)
        self.button_register = pygame.Rect(890, 770, 110, 50)
        self.button_see_password = pygame.Rect(810, 450, 40, 32)
        self.button_confirm_register = pygame.Rect(1010, 700, 110, 50)
        self.button_back_to_login = pygame.Rect(890, 700, 110, 50)
        self.button_help = pygame.Rect(1010, 770, 110, 50)
        self.button_continue = pygame.Rect(580, 600, 140, 50)


    def draw_elements(self):
        self.screen.fill(BLACK)
        if self.active_section == 'login':
            self.draw_login_elements(pygame.mouse.get_pos())
        elif self.active_section == 'register':
            self.draw_registration_elements(pygame.mouse.get_pos())
        elif self.active_section == 'help':
            self.draw_help_elements(pygame.mouse.get_pos())
        if self.login_successful:
            self.draw_button(self.button_continue, "Load Game", pygame.mouse.get_pos())
        pygame.display.flip()

    def draw_help_elements(self, mouse_pos):
        self.screen.fill(BLACK)
        lines = [
            "...Welcome to Never Sleep!...",
            "Thank you for choosing to play this game!",
            " This is game intends to create an environment that users can be emersed in, Creating a character and exploring the world of Never Sleep.",
            " When you have registerd and created an account, you can create your character and design it to your preference.",
            " You will be able to then dive into the world and gain GLORY and POWER!"
            "Here's how you can navigate through the game using the buttons provided:",
            "* Register: Click the 'Register' button to create a new account.",
            "* Login: If you already have an account, click 'Login' to enter the game.",
            "* New Account: Enter a desired username and password, confirm the password.",
            "   You will need to match your password inputs to continue with registration",
            "* SEE: This button converts you password from hidden to visiable.",
            "* Help: Return to this screen anytime by clicking the 'Help' button in the main menu.",
            "","","","",
            "Use the buttons below to dive into the world of NEVER SLEEP"
        ]

        y_pos = 50
        title = pygame.font.Font(None, 45)
        for line in lines:
            if line.startswith("*") or line.startswith(" "):
                text_surface = SM_FONT.render(line, True, WHITE)
            elif line.startswith("..."):
                text_surface = title.render(line, True, WHITE)
            else:
                text_surface = FONT.render(line, True, WHITE)
            self.screen.blit(text_surface, (10, y_pos))
            y_pos += 20 if line.startswith("-") else 15
            y_pos += 20 if line.startswith("") else 15

        self.draw_button(self.button_back_to_login, "Login", mouse_pos)
        self.draw_button(self.button_register, "Register", mouse_pos)

        pygame.display.flip()

    
    def draw_login_elements(self, mouse_pos):
        self.screen.blit(TITLE_FONT.render(' >.< NEVER SLEEP >.< ', True, WHITE), (50, 170))
        self.screen.blit(FONT.render('LOGIN SCREEN', True, WHITE), (780, 50))
        self.draw_user_password_inputs(mouse_pos)
        self.draw_button(self.button_login, "Login", mouse_pos)
        self.draw_button(self.button_register, "Register", mouse_pos)
        self.draw_button(self.button_see_password, "See", mouse_pos, small=True)
        self.draw_button(self.button_help, "Help", mouse_pos)
        self.screen.blit(FONT.render(self.login_message, True, WHITE), (550, 550))

    def draw_registration_elements(self, mouse_pos):
        self.screen.blit(TITLE_FONT.render(' >.< NEVER SLEEP >.< ', True, WHITE), (50, 170))
        self.draw_user_password_inputs(mouse_pos)
        self.draw_button(self.button_register, "Register", mouse_pos)
        self.draw_button(self.button_confirm_register, "Confirm", mouse_pos)
        self.draw_button(self.button_back_to_login, "Login", mouse_pos)
        self.draw_button(self.button_help, "Help", mouse_pos)

        self.screen.blit(FONT.render('Confirm Password:', True, WHITE), (350, 500))
        self.screen.blit(FONT.render('CREATE AN ACCOUNT', True, WHITE), (780, 50))
        self.screen.blit(FONT.render('Enter a Username and Password', True, WHITE), (100, 650))
        self.screen.blit(FONT.render('After Entering Info: Click "REGISTER" Followed by "CONFIRM"', True, WHITE), (100, 700))
        self.screen.blit(FONT.render(self.register_message, True, WHITE), (550, 550))
        pygame.draw.rect(self.screen, COLOR_ACTIVE if self.active_confirm_password else COLOR_INACTIVE, self.input_box_confirm, 2)
        displayed_confirm_password = self.confirm_password_text if self.show_password else '*' * len(self.confirm_password_text)
        self.screen.blit(FONT.render(displayed_confirm_password, True, WHITE), (self.input_box_confirm.x + 5, self.input_box_confirm.y + 5))

    def draw_user_password_inputs(self, mouse_pos):
        self.screen.blit(FONT.render('Username:', True, WHITE), (350, 400))
        self.screen.blit(FONT.render('Password:', True, WHITE), (350, 450))
        self.screen.blit(SM_FONT.render('For additional information Click On HELP Button', True, WHITE),(780, 160))
        self.screen.blit(SM_FONT.render('Log in or create an account using the REGISTER Button', True, WHITE),(780, 120))
        pygame.draw.rect(self.screen, COLOR_ACTIVE if self.active_username else COLOR_INACTIVE, self.input_box_username, 2)
        pygame.draw.rect(self.screen, COLOR_ACTIVE if self.active_password else COLOR_INACTIVE, self.input_box_password, 2)
        self.screen.blit(FONT.render(self.username_text, True, WHITE), (self.input_box_username.x + 5, self.input_box_username.y + 5))
        displayed_password = self.password_text if self.show_password else '*' * len(self.password_text)
        self.screen.blit(FONT.render(displayed_password, True, WHITE), (self.input_box_password.x + 5, self.input_box_password.y + 5))
        self.draw_button(self.button_see_password, "See", mouse_pos, small=True)

    def draw_button(self, rect, text, mouse_pos, small=False):
        color = HOVER_COLOR if rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(self.screen, color, rect)
        font = FONT if not small else pygame.font.Font(None, 20)
        self.screen.blit(font.render(text, True, BLACK), (rect.x + 10, rect.y + 10))

    def check_click(self, event, rect):
        return rect.collidepoint(event.pos)

    def toggle_active_input(self, input_type):
        if input_type == 'username':
            self.active_username = True
            self.active_password = False
            self.active_confirm_password = False
        elif input_type == 'password':
            self.active_username = False
            self.active_password = True
            self.active_confirm_password = False
        elif input_type == 'confirm':
            self.active_username = False
            self.active_password = False
            self.active_confirm_password = True
        self.draw_elements()
    
    def start_customization(self):
        self.customization = CharacterCustomization(self.user_session)
        self.customization.run()

    def switch_to_register(self):
        if self.active_section == 'login' or self.active_section == 'help':
            self.active_section = 'register'
            self.initialize_registration_elements()
        self.draw_elements()
    
    def switch_to_help(self):
        if self.active_section == 'login' or self.active_section == 'register':
            self.active_section = 'help'
            self.initialize_help_elements()
        self.draw_elements()

    def toggle_password_visibility(self):
        self.show_password = not self.show_password
        self.draw_elements()
    
    def get_user_id(self, username):
        with open('user_data.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['username'] == username:
                    return row['user_id']
        return None

    def process_login(self):
        response = login_user(self.username_text, self.password_text)
        if response['success']:
            pygame.time.set_timer(pygame.USEREVENT, 10000)
            self.login_message = response['message']
            self.user_session = response['session_data']
            self.login_successful = True
            self.draw_elements()
            self.confirm_next()
        else:
            self.login_message = response['message']
            self.login_successful = False
            self.draw_elements()

    def process_registration(self):
        if self.password_text == self.confirm_password_text:
            response = register_user(self.username_text, self.password_text)
            if 'successfully' in response:
                self.register_message = response
                self.username_text = ''
                self.password_text = ''
                self.confirm_password_text = ''
                self.switch_to_register()
            else:
                self.register_message = response
        else:
            self.register_message = "Passwords do not match. Try again."
        self.draw_elements()

    def confirm_next(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_continue.collidepoint(event.pos):
                        waiting = False
            self.draw_button(self.button_continue, 'Load Game', pygame.mouse.get_pos())
            pygame.display.flip()
        self.start_customization()

    def return_to_login(self):
        self.active_section = 'login'
        self.initialize_login_elements()
        self.draw_elements()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 0)
                self.start_customization()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event)
            elif event.type == pygame.KEYDOWN:
                self.handle_key_input(event)

    def handle_mouse_click(self, event):
        if self.check_click(event, self.input_box_username):
            self.toggle_active_input('username')
        elif self.check_click(event, self.input_box_password):
            self.toggle_active_input('password')
        elif self.check_click(event, self.input_box_confirm):
            self.toggle_active_input('confirm')
        elif self.check_click(event, self.button_login):
            self.process_login()
        elif self.check_click(event, self.button_register):
            self.switch_to_register()
        elif self.check_click(event, self.button_see_password):
            self.toggle_password_visibility()
        elif self.check_click(event, self.button_confirm_register):
            self.process_registration()
            self.return_to_login()
        elif self.check_click(event, self.button_back_to_login):
            self.return_to_login()
        elif self.check_click(event, self.button_help):
            self.switch_to_help()
        if self.login_successful:
            if self.check_click(event, self.button_continue):
                self.start_customization()
            elif self.check_click(event, self.button_help):
                self.switch_to_help()

    def handle_key_input(self, event):
        input_mapping = {
            'active_username': 'username_text',
            'active_password': 'password_text',
            'active_confirm_password': 'confirm_password_text'
        }

        for active_key, text_key in input_mapping.items():
            if getattr(self, active_key):
                self.handle_text_input(event, text_key, active_key)
                break

    def handle_text_input(self, event, text_key, active_key):
        max_length = 14
        text = getattr(self, text_key)
        if event.key == pygame.K_BACKSPACE:
            setattr(self, text_key, text[:-1])
        elif event.key == pygame.K_RETURN:
            setattr(self, active_key, False)
        else:
            new_text = text + event.unicode
            if len(new_text) > max_length:
                setattr(self, active_key, False)
            else:
                setattr(self, text_key, new_text)

    def run(self):
        while True:
            self.handle_events()
            self.draw_elements()
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == '__main__':
    gui = GUI()
    gui.run()

