from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.graphics import Line, Rectangle
import random
from kivy.uix.label import Label
from kivy.uix.button import Button

OBSTACLE_SIZE = (50, 50)
OBSTACLE_SPEED = 5
OBSTACLE_INTERVAL = 1.5

class CrossingRoadGame(Widget):
    def __init__(self, **kwargs):
        super(CrossingRoadGame, self).__init__(**kwargs)
        self.obstacles = []
        Clock.schedule_interval(self.create_obstacle, OBSTACLE_INTERVAL)
        Clock.schedule_interval(self.update, 1/60)
        self.create_borders()
        self.keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self.keyboard.bind(on_key_down=self._on_key_down)
        self.keyboard.bind(on_key_up=self._on_key_up)
        with self.canvas:
            self.player = Rectangle(source="", pos=(0, 0), size=(50, 50))
        self.keysPressed =set()
        Clock.schedule_interval(self.move_step,0)
        
        self.game_over_label = Label(text="Game Over", font_size=100,
                                 pos=(Window.width / 2 - 50, Window.height / 2),
                                 color=(1, 0, 0, 1), opacity=0)
        self.add_widget(self.game_over_label)

        self.restart_button = Button(text="Restart", size=(200, 100),
                                  pos=(Window.width / 2 - 100, Window.height / 2 - 100),
                                  opacity=0)
        self.restart_button.bind(on_press=self.restart_game)
        self.add_widget(self.restart_button)
        
    def create_obstacle(self,dt):
        obstacle1 = Image(source='', size=OBSTACLE_SIZE)
        obstacle1.x = Window.width * 0.2
        obstacle1.y = Window.height * 0.2
        obstacle1.initial_y = obstacle1.y
        self.add_widget(obstacle1)
        self.obstacles.append(obstacle1)

        obstacle2 = Image(source='', size=OBSTACLE_SIZE)
        obstacle2.x = Window.width * 0.5
        obstacle2.y = Window.height * 0.5
        obstacle2.initial_y = obstacle2.y
        self.add_widget(obstacle2)
        self.obstacles.append(obstacle2)

        obstacle3 = Image(source='', size=OBSTACLE_SIZE)
        obstacle3.x = Window.width * 0.8
        obstacle3.y = Window.height * 0.8
        obstacle3.initial_y = obstacle3.y
        self.add_widget(obstacle3)
        self.obstacles.append(obstacle3)

    def create_borders(self):
        with self.canvas:
            for i in range(1, 3):
                Line(points=[0, Window.height * i / 3, Window.width, Window.height * i / 3], width=2)

    def update(self,dt):
        for obstacle in self.obstacles:
            obstacle.x -= OBSTACLE_SPEED

            if obstacle.x < -OBSTACLE_SIZE[0]:
                obstacle.x = Window.width + random.randint(50, 200)
                obstacle.y = obstacle.initial_y
        self.check_collision()

    def check_collision(self):
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
     self.game_over_label.opacity = 1
     self.restart_button.opacity = 1
     Clock.unschedule(self.create_obstacle)
     Clock.unschedule(self.update)
     Clock.unschedule(self.move_step)

    def restart_game(self, instance):
        self.game_over_label.opacity = 0
        self.restart_button.opacity = 0
        Clock.schedule_interval(self.create_obstacle, OBSTACLE_INTERVAL)
        Clock.schedule_interval(self.update, 1/60)
        Clock.schedule_interval(self.move_step, 0) 
        self.player.pos = (0, 0)

        for obstacle in self.obstacles:
            obstacle.x = Window.width + random.randint(50, 200)
            obstacle.y = obstacle.initial_y
    

    def _on_keyboard_closed(self):
        self.keyboard.unbind(on_key_down=self._on_key_down)
        self.keyboard.unbind(on_key_up=self._on_key_up)
        self.keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        self.keysPressed.add(text)

    def _on_key_up(self,keyboard,keycode):
        text = keycode[1]
        if text in self.keysPressed:
            self.keysPressed.remove(text)

    def move_step(self,dt):
        currentx = self.player.pos[0]
        currenty = self.player.pos[1]

        step_size = 200 * dt

        if "w" in self.keysPressed:
            currenty += step_size
        if "s" in self.keysPressed:
            currenty -= step_size
        if "a" in self.keysPressed:
            currentx -= step_size
        if "d" in self.keysPressed:
            currentx += step_size

        self.player.pos = (currentx, currenty)


class CrossingRoadApp(App):
    def build(self):
        return CrossingRoadGame()

if __name__ == '__main__':
    CrossingRoadApp().run()