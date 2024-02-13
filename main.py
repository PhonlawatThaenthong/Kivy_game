from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.core.window import Window

OBSTACLE_SIZE = (50, 50)
OBSTACLE_SPEED = 5
OBSTACLE_INTERVAL = 1.5

class CrossingRoadGame(Widget):
    def __init__(self, **kwargs):
        super(CrossingRoadGame, self).__init__(**kwargs)
        self.obstacles = []
        
    def create_obstacle(self, dt):
        obstacle1 = Image(source='', size=OBSTACLE_SIZE)
        obstacle1.x = Window.width * 0.2
        obstacle1.y = Window.height * 0.2
        obstacle1.initial_y = obstacle1.y
        self.add_widget(obstacle1)
        self.obstacles.append(obstacle1)


class CrossingRoadApp(App):
    def build(self):
        return CrossingRoadGame()

if __name__ == '__main__':
    CrossingRoadApp().run()