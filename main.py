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
OBSTACLE_SPEED = 5
OBSTACLE_INTERVAL = 1.5

class CrossingRoadGame(Widget):
    def __init__(self, **kwargs):
        super(CrossingRoadGame, self).__init__(**kwargs)

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
            self.player = Rectangle(source="", pos=(0, 0), size=(50, 50))

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
            obstacle.x = Window.width * random.choice([0.2, 0.5, 0.8])
            obstacle.y = -OBSTACLE_SIZE[1]  # Start from the top of the window
            obstacle.initial_y = obstacle.y
            self.add_widget(obstacle)
            self.obstacles.append(obstacle)

    def create_borders(self):
        # Draw borders
        with self.canvas:
            for i in range(1, 3):
                Line(points=[0, Window.height * i / 3, Window.width, Window.height * i / 3], width=2)

    def update(self, dt):
        # Update obstacle positions
        for obstacle in self.obstacles:
            obstacle.y += OBSTACLE_SPEED  # Move obstacles downwards
            if obstacle.y > Window.height:  # If obstacle goes out of the window
                obstacle.x = Window.width * random.choice([0.2, 0.5, 0.8])  # Reset x position
                obstacle.y = -OBSTACLE_SIZE[1]  # Start from the top of the window
                obstacle.initial_y = obstacle.y
        self.check_collision()

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
        self.player.pos = (0, 0)
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
        self.keysPressed.add(text)

    def _on_key_up(self, keyboard, keycode):
        # Handle key up event
        text = keycode[1]
        if text in self.keysPressed:
            self.keysPressed.remove(text)

    def move_step(self, dt):
        # Move player based on pressed keys
        currentx, currenty = self.player.pos
        step_size = 200 * dt
    
        if "w" in self.keysPressed:
            currenty += step_size  # Move up when 'w' is pressed
        if "s" in self.keysPressed:
            currenty -= step_size  # Move down when 's' is pressed
        if "a" in self.keysPressed:
            currentx -= step_size
        if "d" in self.keysPressed:
            currentx += step_size
    
        # Limit player movement within window boundaries
        currentx = max(0, min(currentx, Window.width - self.player.size[0]))
        currenty = max(0, min(currenty, Window.height - self.player.size[1]))
    
        self.player.pos = (currentx, currenty)
    

class CrossingRoadApp(App):
    def build(self):
        return CrossingRoadGame()

if __name__ == '__main__':
    CrossingRoadApp().run()
