from kivy.config import Config

# Disable resizable window
Config.set('graphics', 'resizable', False)

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.graphics import Line, Rectangle
from kivy.uix.label import Label
from kivy.uix.button import Button
import random

# Constants
OBSTACLE_SIZE = (50, 50)
OBSTACLE_SPEED = 3
OBSTACLE_INTERVAL = 1.5
ASPECT_RATIO = 16 / 9  # Fixed aspect ratio


class CrossingRoadGame(Widget):
    def __init__(self, **kwargs):
        super(CrossingRoadGame, self).__init__(**kwargs)
        
        # Initialize coins and scheduling
        self.coins = []
        self.coin_count = 0
        Clock.schedule_interval(self.create_coin,1)
        self.coin_spawned = True
        # Calculate window size based on aspect ratio
        screen_width = Window.width
        screen_height = Window.height
        if screen_width / screen_height > ASPECT_RATIO:
            Window.size = (int(screen_height * ASPECT_RATIO), int(screen_height))
        else:
            Window.size = (int(screen_width), int(screen_width / ASPECT_RATIO))

        # Initialize obstacles and scheduling
        self.obstacles = []
        Clock.schedule_interval(self.create_obstacle, OBSTACLE_INTERVAL)
        Clock.schedule_interval(self.update, 1/60)

        # Initialize player movement
        self.keysPressed = set()
        Clock.schedule_interval(self.move_step, 0)

        # Initialize game over label and restart button
        self.game_over_label = Label(text="Game Over", font_size=100,
                                     pos=(Window.width / 2 - 50, Window.height / 2),
                                     color=(1, 0, 0, 1), opacity=0)
        self.add_widget(self.game_over_label)

        self.restart_button = Button(text="Restart", size=(200, 100),
                                     pos=(Window.width / 2 - 100, Window.height / 2 - 100),
                                     opacity=0)
        self.restart_button.bind(on_press=self.restart_game)
        self.add_widget(self.restart_button)

        # Initialize player rectangle
        with self.canvas:
            self.player = Rectangle(source="", pos=(50,200), size=(50, 50))

        # Create borders
        self.create_borders()

        # Request keyboard and bind events
        self.keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self.keyboard.bind(on_key_down=self._on_key_down)
        self.keyboard.bind(on_key_up=self._on_key_up)

    def create_obstacle(self, dt):
        # Create three obstacles
        for _ in range(3):
            obstacle = Image(source='', size=OBSTACLE_SIZE)
            obstacle.x = Window.width * random.choice([0.25, 0.44, 0.63])
            obstacle.y = -OBSTACLE_SIZE[1]  # Start from the top of the window
            obstacle.initial_y = obstacle.y
            self.add_widget(obstacle)
            self.obstacles.append(obstacle)

    def create_coin(self, dt):
        # Only spawn a new coin if it hasn't been spawned
        if self.coin_spawned:
            coin = Image(source='', size=(30, 30))  # Replace 'coin_image.png' with the actual image file
            coin.x = Window.width * random.choice([0.90])  # Random x position within window boundaries
            coin.y = 200  # Spawn at the player's row
            self.add_widget(coin)
            self.coins.append(coin)

            # Set the flag to True to indicate that the coin has been spawned
            self.coin_spawned = False

    def create_borders(self):
        # Draw borders
        with self.canvas:
            border_width = 2
            border_color = (0, 0, 1, 1)

            # Draw left border
            Line(points=[0, 0, 0, Window.height], width=border_width, color=border_color)
            # Draw starter border
            Line(points=[150, 0, 150, Window.height], width=border_width, color=border_color)
            # Draw obstacle border
            Line(points=[300, 0, 300, Window.height], width=border_width, color=border_color)
            Line(points=[450, 0, 450, Window.height], width=border_width, color=border_color)
            Line(points=[600, 0, 600, Window.height], width=border_width, color=border_color)

            # Draw right border
            Line(points=[Window.width, 0, Window.width, Window.height], width=border_width, color=border_color)

            # Draw top border
            Line(points=[0, Window.height, Window.width, Window.height], width=border_width, color=border_color)

            # Draw bottom border
            Line(points=[0, 0, Window.width, 0], width=border_width, color=border_color)

    def update(self, dt):
        # Update obstacle positions
        for obstacle in self.obstacles:
            obstacle.y += OBSTACLE_SPEED  # Move obstacles downwards
            if obstacle.y > Window.height:  # If obstacle goes out of the window
                obstacle.x = Window.width * random.choice([0.25, 0.44, 0.63])  # Reset x position
                obstacle.y = -OBSTACLE_SIZE[1]  # Start from the top of the window
                obstacle.initial_y = obstacle.y
        self.check_collision()
        self.check_coin_collection()

    def check_collision(self):
        # Check collision between player and obstacles
        player_x, player_y = self.player.pos
        player_width, player_height = self.player.size

        for obstacle in self.obstacles:
            obstacle_x, obstacle_y = obstacle.pos
            obstacle_width, obstacle_height = obstacle.size

            if (
                player_x < obstacle_x + obstacle_width
                and player_x + player_width > obstacle_x
                and player_y < obstacle_y + obstacle_height
                and player_y + player_height > obstacle_y
            ):
                self.show_game_over()

    def check_coin_collection(self):
        # Check if player collects a coin
        player_x, player_y = self.player.pos
        player_width, player_height = self.player.size

        for coin in self.coins:
            coin_x, coin_y = coin.pos
            coin_width, coin_height = coin.size

            if (
                player_x < coin_x + coin_width
                and player_x + player_width > coin_x
                and player_y < coin_y + coin_height
                and player_y + player_height > coin_y
            ):
                self.coin_count += 1  # Increment coin count
                print(f"Coins collected: {self.coin_count}")
                self.coins.remove(coin)
                self.remove_widget(coin)
                self.coin_spawned = True

    def show_game_over(self):
        # Show game over label and restart button
        self.game_over_label.opacity = 1
        self.restart_button.opacity = 1
        Clock.unschedule(self.create_obstacle)
        Clock.unschedule(self.update)
        Clock.unschedule(self.move_step)

    def restart_game(self, instance):
        # Restart the game
        self.game_over_label.opacity = 0
        self.restart_button.opacity = 0
        Clock.schedule_interval(self.create_obstacle, OBSTACLE_INTERVAL)
        Clock.schedule_interval(self.update, 1/60)
        Clock.schedule_interval(self.move_step, 0)
        for coin in self.coins:
            self.remove_widget(coin)
        self.coins = []
        self.coin_count = 0
        Clock.schedule_interval(self.create_coin, 10)
        self.player.pos = (50,300)
        for obstacle in self.obstacles:
            obstacle.x = Window.width + random.randint(50, 200)
            obstacle.y = -OBSTACLE_SIZE[1]  # Start from the top of the window
            obstacle.initial_y = obstacle.y

    def _on_keyboard_closed(self):
        # Unbind keyboard events
        self.keyboard.unbind(on_key_down=self._on_key_down)
        self.keyboard.unbind(on_key_up=self._on_key_up)
        self.keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        # Handle key down event
        if keycode[1] in ('w', 'up'):
            self.keysPressed.add('up')
        elif keycode[1] in ('s', 'down'):
            self.keysPressed.add('down')
        elif keycode[1] in ('a', 'left'):
            self.keysPressed.add('left')
        elif keycode[1] in ('d', 'right'):
            self.keysPressed.add('right')

    def _on_key_up(self, keyboard, keycode):
        # Handle key up event
        if keycode[1] in ('w', 'up'):
            self.keysPressed.discard('up')
        elif keycode[1] in ('s', 'down'):
            self.keysPressed.discard('down')
        elif keycode[1] in ('a', 'left'):
            self.keysPressed.discard('left')
        elif keycode[1] in ('d', 'right'):
            self.keysPressed.discard('right')

    def move_step(self, dt):
        # Move player based on pressed keys
        currentx, currenty = self.player.pos
        step_size = 200 * dt

        if 'up' in self.keysPressed:
            currenty += step_size  # Move up when 'up' or 'w' is pressed
        if 'down' in self.keysPressed:
            currenty -= step_size  # Move down when 'down' or 's' is pressed
        if 'left' in self.keysPressed:
            currentx -= step_size  # Move left when 'left' or 'a' is pressed
        if 'right' in self.keysPressed:
            currentx += step_size  # Move right when 'right' or 'd' is pressed

        # Limit player movement within window boundaries
        currentx = max(0, min(currentx, Window.width - self.player.size[0]))
        currenty = max(0, min(currenty, Window.height - self.player.size[1]))

        self.player.pos = (currentx, currenty)

class CrossingRoadApp(App):
    def build(self):
        return CrossingRoadGame()

if __name__ == '__main__':
    CrossingRoadApp().run()
