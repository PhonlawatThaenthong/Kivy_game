from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.graphics import Line
import random
from kivy.graphics import Rectangle

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
        
    def create_obstacle(self,dod):
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

    def update(self,dod):
        for obstacle in self.obstacles:
            obstacle.x -= OBSTACLE_SPEED

            if obstacle.x < -OBSTACLE_SIZE[0]:
                obstacle.x = Window.width + random.randint(50, 200)
                obstacle.y = obstacle.initial_y

    def _on_keyboard_closed(self):
        self.keyboard.unbind(on_key_down=self._on_key_down)
        self.keyboard.unbind(on_key_up=self._on_key_up)
        self.keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        self.keysPressed.add(text)


class CrossingRoadApp(App):
    def build(self):
        return CrossingRoadGame()

if __name__ == '__main__':
    CrossingRoadApp().run()