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
 ``` python
    def lower_sound(self, instance):
    - ในส่วนนี้จะใช้จัดการระบบเสียงต่างๆทั้งเพิ่มเสียงและลดเสียง

    def create_obstacle(self, dt):
    - ในส่วนนี้จะสร้างสิ่งกีดขวางโดยมีข้อจำกัดต่างๆทั้งจำนวนสูงสุดต่ำสุด
      และจะสร้างแบบสุ่มในทั้ง 3 column

    def create_coin(self, dt):
    - สร้างเหรียญที่ช่องมุมขวาสุดของจอ

    def create_coin2(self, dt):
    - สร้างเหรียญที่ช่องมุมซ้ายสุดของจอ

    def create_heart(self, dt):
    - สร้างหัวใจที่ช่องมุมขวาสุดของจอ

    def create_borders(self):
    - สร้างช่องแบ่งต่างของแต่ละ column และขอบจอ

    def update(self, dt):
    - ใช้ update คำสั่งต่างๆแบบ realtime และสร้างสิ่งกีดขวางใหม่
      เมื่อมีสิ่งกีดขวางชนขอบจอ

    def check_collision(self):
    - ใช้ตรวจสอบว่า player มาชนสิ่งกีดขวางหรือไม่
      ถ้าชนเลือดของ player จะลดลง 1 หน่วย

    def check_coin_collection(self):
    - ใช้ตรวจสอบว่า player มาชนเหรียญหรือไม่
      ถ้าชน player จะได้รับแต้ม score 1 หน่วย
    - ถ้าเก็ยแต้ม score ได้ทุกๆ 5 แต้มเรีบกใช้ function
      สร้างหัวใจมา 1 ดวง

    def check_heart_collection(self):
    - ใช้ตรวจสอบว่า player มาชนหัวใจหรือไม่
      ถ้าชนเลือดของ player จะได้เพิ่มขึ้น 1 หน่วย

    def show_game_over(self):
    - ถ้ามีการเรียกใช้ function นี้จะแสดงข้อความ Game Over ขึ้นมา
      และหยุดการทำงานต่างๆ

    def restart_game(self, instance):
    - ถ้ามีการเรียกใช้ function นี้จะ reset ทุกอย่างไปอยู่ในจุดเริ่มต้น
   
    def _on_keyboard_closed(self):
    - เป็น function การเรียกใช้การทำงานจาก keyboard

    def _on_key_down(self, keyboard, keycode, text, modifiers):
    - เป็น function การเรียกใช้การทำงานจาก keyboard

    def _on_key_up(self, keyboard, keycode):
    - เป็น function การเรียกใช้การทำงานจาก keyboard

    def move_step(self, dt):
    - เป็น function เกี่ยวกับการเคลื่อนไหวของ player และการเรียกใช้ function keyboard
```
