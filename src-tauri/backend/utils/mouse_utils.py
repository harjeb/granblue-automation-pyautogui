import random

import pyautogui
import pyperclip
from pyHM import mouse
#from utils.cBezier import bezierTrajectory
from pyclick import HumanClicker
from utils.settings import Settings
from utils.message_log import MessageLog
import time

class MouseUtils:
    """
    Provides the utility functions needed to perform mouse-related actions.
    """
    hc = HumanClicker()

    if Settings.enable_bezier_curve_mouse_movement is False:
        pyautogui.MINIMUM_DURATION = 0
        pyautogui.MINIMUM_SLEEP = 0
        pyautogui.PAUSE = 0.008



    @staticmethod
    def quadratic_bezier(t, start, control, end):
        """
        二次贝塞尔曲线公式
        :param t: 在0到1之间的参数
        :param start: 起始点位置 (x1, y1)
        :param control: 控制点位置 (x2, y2)
        :param end: 结束点位置 (x3, y3)
        :return: 点的坐标 (x, y)
        """
        x = (1 - t) ** 2 * start[0] + 2 * (1 - t) * t * control[0] + t ** 2 * end[0]
        y = (1 - t) ** 2 * start[1] + 2 * (1 - t) * t * control[1] + t ** 2 * end[1]
        return (x, y)

    @staticmethod
    def smooth_mouse_move(start, end, control, duration):
        """
        使鼠标沿曲线平滑移动
        :param start: 起始坐标 (x, y)
        :param end: 结束坐标 (x, y)
        :param control: 控制点坐标 (x, y)
        :param duration: 移动持续时间（秒）
        """
        steps = 100
        step_time = duration / steps
        
        for i in range(steps + 1):
            t = i / steps
            x, y = MouseUtils.quadratic_bezier(t, start, control, end)
            
            # 移动鼠标到当前位置
            pyautogui.moveTo(x + random.uniform(-3, 3), y + random.uniform(-3, 3))  # 加入一些随机性

            # 等待下一步
            time.sleep(step_time)



    @staticmethod
    def click():
        pyautogui.click()

    @staticmethod
    def move(x,y):
        MouseUtils.hc.move((x,y),2)
        #bezierTrajectory.move(x, y)
        #mouse.move(x, y, multiplier=round(random.uniform(3.5, 5.5), 3))
        # 鼠标当前的位置


    @staticmethod
    def move_to(x: int, y: int, custom_mouse_speed: float = 0.0):
        """Move the cursor to the coordinates on the screen.

        Args:
            x (int): X coordinate on the screen.
            y (int): Y coordinate on the screen.
            custom_mouse_speed (float, optional): Time in seconds it takes for the mouse to move to the specified point. Defaults to 0.0.

        Returns:
            None
        """
        MouseUtils.move(x, y)

        return None


    @staticmethod
    def obfuscate_click(maxclick=3):
        Settings.window_left
        Settings.window_top
        Settings.window_width
        Settings.window_height


    @staticmethod
    def move_and_click_point(x: int, y: int, image_name: str, custom_mouse_speed: float = 0.0, mouse_clicks: int = 1):
        """Move the cursor to the specified point on the screen and clicks it.

        Args:
            x (int): X coordinate on the screen.
            y (int): Y coordinate on the screen.
            image_name (str): File name of the image in /images/buttons/ folder.
            custom_mouse_speed (float, optional): Time in seconds it takes for the mouse to move to the specified point. Defaults to 0.0.
            mouse_clicks (int, optional): Number of mouse clicks. Defaults to 1.

        Returns:
            None
        """
        if Settings.debug_mode:
            MessageLog.print_message(f"[DEBUG] Old coordinates: ({x}, {y})")

        new_x, new_y = MouseUtils._randomize_point(x, y, image_name)

        if Settings.debug_mode:
            MessageLog.print_message(f"[DEBUG] New coordinates: ({new_x}, {new_y})")

        # Move the mouse to the specified coordinates.
        MouseUtils.move(new_x, new_y)

        from bot.game import Game
        if image_name == "attack" or image_name == "back" or image_name == "ok":
            #obfuscate_click(maxclick=5)
            pyautogui.click(clicks = mouse_clicks)
            try:
                post = pyautogui.position()
                with open('mouse.log','a') as f:
                    f.write(str(post)+'\n')
            except:
                pass
        
        else:
            # 混淆点击
            p = 15
            R = random.randint(1,100)
            if R >= p:
                pyautogui.click(clicks = mouse_clicks)
                try:
                    post = pyautogui.position()
                    with open('mouse.log','a') as f:
                        f.write(str(post)+'\n')
                except:
                    pass
            else:
                pyautogui.click(clicks = 2)
                try:
                    post = pyautogui.position()
                    with open('mouse.log','a') as f:
                        f.write(str(post)+'\n')
                        f.write(str(post)+'\n')
                except:
                    pass
        # 混淆移动
        #当前坐标
        #Game.wait(random.uniform(0.85, 1.79))
        # fix_x = new_x + random.randint(-300,300)
        # fix_y = new_y + random.randint(-300,300)
        # MouseUtils.move(fix_x, fix_y)

        if Settings.farming_mode == "Raid":
            Game.wait(random.uniform(0.51, 0.94))
        else:
            Game.wait(random.uniform(0.97, 2.54))
        
        # This delay is necessary as ImageUtils will take the screenshot too fast and the bot will use the last frame before clicking to navigate.

        return None

    @staticmethod
    def _randomize_point(x: int, y: int, image_name: str):
        """Randomize the clicking location in an attempt to avoid clicking the same location that may make the bot look suspicious.

        Args:
            x (int): X coordinate on the screen of the center of the match location.
            y (int): Y coordinate on the screen of the center of the match location.
            image_name (str): File name of the image in /images/buttons/ folder.

        Returns:
            (int, int): Tuple of the newly randomized location to click.
        """
        # Get the width and height of the template image.
        from utils.image_utils import ImageUtils
        width, height = ImageUtils.get_button_dimensions(image_name)

        dimensions_x0 = x - (width // 2)
        dimensions_x1 = x + (width // 2)

        dimensions_y0 = y - (height // 2)
        dimensions_y1 = y + (height // 2)

        while True:
            new_width = random.randint(int(width * 0.2), int(width * 0.8))
            new_height = random.randint(int(height * 0.2), int(height * 0.8))

            new_x = dimensions_x0 + new_width
            new_y = dimensions_y0 + new_height

            # If the new coordinates are within the bounds of the template image, break out of the loop and return the coordinates.
            if new_x > dimensions_x0 or new_x < dimensions_x1 or new_y > dimensions_y0 or new_y < dimensions_y1:
                break

        return new_x, new_y

    @staticmethod
    def scroll_screen(x: int, y: int, scroll_clicks: int):
        """Attempt to scroll the screen to reveal more UI elements from the provided x and y coordinates.

        Args:
            x (int): X coordinate on the screen.
            y (int): Y coordinate on the screen.
            scroll_clicks (int): How much to scroll the screen. Positive for scrolling up and negative for scrolling down.

        Returns:
            None
        """
        if Settings.debug_mode:
            MessageLog.print_message(f"[DEBUG] Now scrolling the screen from ({x}, {y}) by {scroll_clicks} clicks...")

        MouseUtils.move_to(x, y)

        pyautogui.scroll(scroll_clicks, x = x, y = y)

        return None

    @staticmethod
    def scroll_screen_from_home_button(scroll_clicks: int):
        """Attempt to scroll the screen using the "Home" button coordinates to reveal more UI elements.

        Args:
            scroll_clicks (int): How much to scroll the screen. Positive for scrolling up and negative for scrolling down.

        Returns:
            None
        """
        x = Settings.home_button_location[0]
        y = Settings.home_button_location[1] - 50

        if Settings.debug_mode:
            MessageLog.print_message(f"[DEBUG] Now scrolling the screen from the \"Home\" button's coordinates at ({x}, {y}) by {scroll_clicks} clicks...")

        MouseUtils.move_to(x, y)


        pyautogui.scroll(scroll_clicks, x = x, y = y)

        return None

    @staticmethod
    def clear_textbox():
        """Clear the selected textbox of all text by selecting all text by CTRL + A and then pressing DEL.

        Returns:
            None
        """
        pyautogui.keyDown("ctrl")
        pyautogui.press("a")
        pyautogui.keyUp("ctrl")
        pyautogui.press("del")
        return None

    @staticmethod
    def copy_to_clipboard(message: str):
        """Copy the message to the clipboard.

        Args:
            message (str): The message to be copied.

        Returns:
            None
        """
        pyperclip.copy(message)
        return None

    @staticmethod
    def paste_from_clipboard():
        """Paste from the clipboard. Make sure that the textbox is already selected.

        Returns:
            None
        """
        message = pyperclip.paste()
        pyautogui.write(message.lower())
        return None
