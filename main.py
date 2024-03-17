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
from kivy.core.audio import SoundLoader 
import random

# Constants
OBSTACLE_SIZE = (50, 50)  # Original obstacle size
OBSTACLE_SIZE_LONG = (50, 100)  # Double size obstacle
OBSTACLE_SPEED = 3
OBSTACLE_INTERVAL = 1.5
ASPECT_RATIO = 16 / 9  # Fixed aspect ratio
MIN_COOLDOWN = 2  # Minimum cooldown for obstacle spawning (seconds)
MAX_COOLDOWN = 6  # Maximum cooldown for obstacle spawning (seconds)
LONG_OBSTACLE_COOLDOWN = 5  # Cooldown for spawning long obstacles (seconds)
MAX_OBSTACLES = 9

class CrossingRoadGame(Widget):
    def __init__(self, **kwargs):
        super(CrossingRoadGame, self).__init__(**kwargs)
        
        # Initialize coins and scheduling
        self.coins = []
        self.coin_count = 0
        self.live_count = 3
        self.best_scores = 0
        Clock.schedule_interval(self.create_coin, 1)
        self.coin_spawned = True
        self.coin2_spawned = False
        #Initialize heart
        self.heart = []
        self.heart_spawned = False
        
        # Calculate window size based on aspect ratio
        screen_width = Window.width
        screen_height = Window.height
        if screen_width / screen_height > ASPECT_RATIO:
            Window.size = (int(screen_height * ASPECT_RATIO), int(screen_height))
        else:
            Window.size = (int(screen_width), int(screen_width / ASPECT_RATIO))
       
        # Background sound settings
        self.background_sound = SoundLoader.load('Sound/nbcground.mp3')
        self.getscore_sound = SoundLoader.load('Sound/scores.mp3')
        self.gethurt_sound = SoundLoader.load('Sound/nget_hurt.mp3')
        self.restart_sound = SoundLoader.load('Sound/restart.mp3')
        self.heal_sound = SoundLoader.load('Sound/heal.mp3')
        if self.background_sound:
            self.background_sound.loop = True
            self.background_sound.play()

        # Initialize obstacles and scheduling
        self.obstacles = []
        self.schedule_obstacle_creation()
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
                                    background_color=(0, 0.7, 0.3, 1),
                                    font_size=24, color=(1, 1, 1, 1),
                                    background_normal='', background_down='',
                                    opacity=0, disabled=True)
        
        # Live Modal
        self.live_count_label = Label(text="Lives: 3", font_size=20,
                                      pos=(8,10),
                                      color=(1, 1, 1, 1))
        self.add_widget(self.live_count_label)

        # Lower sound button
        self.sound_level = 'max'
        self.max_sound = 0
        self.lower_sound_button = Button(size=(10, 10),
                                         pos=(740,400),
                                         background_normal='Picture/soundmax.png',
                                         opacity=1)      
        self.lower_sound_button.bind(on_press=self.lower_sound)
        self.add_widget(self.lower_sound_button)

        # Score Modal
        self.score_label = Label(text="Score: 0", font_size=20,
                                 pos=(8,-10),
                                 color=(1, 1, 1, 1))
        self.add_widget(self.score_label)

        self.best_scores_label = Label(text="Best Score: 0", font_size=20,
                                 pos=(30,-30),
                                 color=(1, 1, 1, 1))
        self.add_widget(self.best_scores_label)

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

        # Initialize obstacle cooldown timer
        self.obstacle_spawn_cooldown = 0
        self.long_obstacle_cooldown = 0

    def schedule_obstacle_creation(self):
        Clock.schedule_interval(self.create_obstacle, OBSTACLE_INTERVAL)

    def lower_sound(self, instance):
        # Lower the background sound volume
        if self.sound_level == 'max':
            self.max_sound = self.background_sound.volume
            self.background_sound.volume *= 0.5
            self.restart_sound.volume *= 0.5
            self.gethurt_sound.volume *= 0.5
            self.getscore_sound.volume *= 0.5
            self.heal_sound.volume *= 0.5
            self.sound_level = 'mid'
            instance.background_normal = 'Picture/soundmid.png'
            print(self.sound_level)
       
        elif self.sound_level == 'mid':
            self.background_sound.volume *= 0
            self.restart_sound.volume *= 0
            self.gethurt_sound.volume *= 0
            self.getscore_sound.volume *= 0
            self.heal_sound.volume *= 0
            self.sound_level = 'off'
            instance.background_normal = 'Picture/soundoff.png'
            print(self.sound_level)
        
        elif self.sound_level == 'off':
            self.background_sound.volume = self.max_sound
            self.restart_sound.volume = self.max_sound
            self.gethurt_sound.volume = self.max_sound
            self.getscore_sound.volume = self.max_sound
            self.heal_sound.volume = self.max_sound
            self.sound_level = 'max'
            instance.background_normal = 'Picture/soundmax.png'
            print(self.sound_level)

    def create_obstacle(self, dt):
        car_images = ['Picture/car1.png', 'Picture/car2.png', 'Picture/car3.png']
        if self.obstacle_spawn_cooldown <= 0 and len(self.obstacles) < MAX_OBSTACLES:
            self.obstacle_spawn_cooldown = random.uniform(MIN_COOLDOWN, MAX_COOLDOWN)

            # Create three obstacles
            for _ in range(3):
                obstacle_size = random.choices([OBSTACLE_SIZE, OBSTACLE_SIZE_LONG], weights=[70, 30])[0]
                obstacle_image = random.choice(car_images) if obstacle_size == OBSTACLE_SIZE else 'Picture/truck.png'

                if obstacle_size == OBSTACLE_SIZE_LONG and self.long_obstacle_cooldown <= 0:
                    self.long_obstacle_cooldown = LONG_OBSTACLE_COOLDOWN

                obstacle = Image(source=obstacle_image, size=obstacle_size)
                obstacle.x = Window.width * random.choice([0.25, 0.44, 0.63])
                obstacle.y = -obstacle_size[1]  # Start from the top of the window

                self.add_widget(obstacle)
                self.obstacles.append(obstacle)

                # Adjust the obstacle spawn cooldown based on its size
                if obstacle_size == OBSTACLE_SIZE_LONG:
                    self.obstacle_spawn_cooldown += 2  # Increase cooldown for long obstacles
        else:
            self.obstacle_spawn_cooldown -= dt


    def create_coin(self, dt):
        # Only spawn when self.coin_spawned == True
        if self.coin_spawned:
            coin = Image(source='Picture/coin.png', size=(30, 30))
            coin.x = Window.width * random.choice([0.90])#set x position of coin
            coin.y = 200  #set y position of coin
            self.add_widget(coin)
            self.coins.append(coin)
            self.coin_spawned = False

    def create_coin2(self, dt):
        # Only spawn when self.coin2_spawned == True
        if self.coin2_spawned:
            coin = Image(source='Picture/coin.png', size=(30, 30))
            coin.x = Window.width * random.choice([0.1])#set x position of coin
            coin.y = 200  #set y position of coin
            self.add_widget(coin)
            self.coins.append(coin)
            self.coin2_spawned = False

    def create_heart(self, dt):
        # Only spawn when self.coin_count % 5 == 0
        if self.heart_spawned:
            heart = Image(source='Picture/heart.png', size=(30, 30))
            heart.x = Window.width * random.choice([0.90])#set x position of coin
            heart.y = 300  #set y position of coin
            self.add_widget(heart)
            self.heart.append(heart)
            self.heart_spawned = False

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
        self.check_heart_collection()

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
                #make live can not lower than 0
                if self.live_count == 3:
                    self.live_count = 2
                elif self.live_count == 2:
                    self.live_count = 1
                elif self.live_count == 1:
                    self.live_count = 0
                self.gethurt_sound.play()
                self.player.pos = (50, 200)
                self.live_count_label.text = f"Lives: {self.live_count}"
                print('Live Left :',self.live_count)
                if self.live_count == 0:
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
                self.coin_count += 1  # counting coin
                self.getscore_sound.play()
                self.score_label.text = f"Score: {self.coin_count}"
                print(f"Coins collected: {self.coin_count}")
                self.coins.remove(coin)
                self.remove_widget(coin)
                if not self.coin2_spawned and self.coin_count%2 != 0:
                    self.coin2_spawned = True
                    Clock.schedule_once(self.create_coin2, 1)
                else:
                    self.coin_spawned = True
                    Clock.schedule_once(self.create_coin, 1)
                #change heal spawn rate here
                if self.coin_count % 5 == 0:
                    self.heart_spawned = True
                    Clock.schedule_once(self.create_heart, 1)

    def check_heart_collection(self):
        # Check if player collects a heart
        player_x, player_y = self.player.pos
        player_width, player_height = self.player.size

        for heart in self.heart:
            heart_x, heart_y = heart.pos
            heart_width, heart_height = heart.size

            if (
                player_x < heart_x + heart_width
                and player_x + player_width > heart_x
                and player_y < heart_y + heart_height
                and player_y + player_height > heart_y
            ):
                self.heal_sound.play()
                self.heart.remove(heart)
                self.remove_widget(heart)
                self.live_count += 1
                self.heart_spawned = False
                self.live_count_label.text = f"Lives: {self.live_count}"


    def show_game_over(self):
        # Show game over label and restart button
        self.game_over_label.opacity = 1
        self.restart_button.opacity = 1
        self.restart_button.disabled = False  # Enable restart button
        Clock.unschedule(self.create_obstacle)
        Clock.unschedule(self.update)
        Clock.unschedule(self.move_step)
        self.background_sound.stop()

    def restart_game(self, instance):
        # Hide game over label and restart button
        self.game_over_label.opacity = 0
        self.restart_button.opacity = 0
        self.restart_button.disabled = True  # Disable restart button

        # Unscheduling old intervals
        Clock.unschedule(self.create_obstacle)
        Clock.unschedule(self.update)
        Clock.unschedule(self.move_step)
    
        # Scheduling new intervals
        Clock.schedule_interval(self.create_obstacle, OBSTACLE_INTERVAL)
        Clock.schedule_interval(self.update, 1/60)
        Clock.schedule_interval(self.move_step, 0)
    
        # Remove existing coins
        for coin in self.coins:
            self.remove_widget(coin)
        self.coins = []
        # Reset Live
        self.live_count = 3
        self.live_count_label.text = f"Lives: {self.live_count}"
        # Reset coin-related variables
        if self.best_scores < self.coin_count:
            self.best_scores = self.coin_count
        self.coin_count = 0
        self.score_label.text = f"Score: {self.coin_count}"
        self.best_scores_label.text = f"Best Scores: {self.best_scores}"
        self.coin_spawned = True
        self.coin2_spawned = False
    
        # Schedule the initial coin spawn
        Clock.schedule_interval(self.create_coin, 1)
    
        # Reset player position
        self.player.pos = (50, 200)
        self.restart_sound.play()
        self.background_sound.play()
    
        # Reset obstacle positions
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
