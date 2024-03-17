# Crossing Road Game
### พื้นฐานของตัวเกม
- ตัวละครเริ่มต้นมามีเลือดอยู่ 3 หน่วย
- ถ้าชนรถขนาดเล็กเลือดจะลด 1 หนวย
- ถ้าชนรถขนาดใหญ่เลือดจะลด 2 หนวย
- ถ้าเก็บเหรียญทองจะได้แต้มมา 1 แต้ม
### วิธีการเล่น
- เราจะต้องบังคับตัวละครไปเก็บเหรียญที่อยู่ฝั่งตรงข้าม
  โดยไม่ให้โดนรถชน
- ถ้าเก็บเหรียญครบทุกๆ 5 เหรียญจะมี heal เกิดโดย
  ถ้าเก็บจะเพิ่มเลือด 1 หน่วย
### หลักการทำงานของ code


    def lower_sound(self, instance):


    def create_obstacle(self, dt):



    def create_coin(self, dt):


    def create_coin2(self, dt):


    def create_heart(self, dt):


    def create_borders(self):


    def update(self, dt):


    def check_collision(self):


    def check_coin_collection(self):


    def check_heart_collection(self):



    def show_game_over(self):


    def restart_game(self, instance):

    


    def _on_keyboard_closed(self):


    def _on_key_down(self, keyboard, keycode, text, modifiers):


    def _on_key_up(self, keyboard, keycode):


    def move_step(self, dt):

