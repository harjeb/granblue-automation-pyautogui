from utils.settings import Settings
from utils.message_log import MessageLog
from utils.image_utils import ImageUtils
from utils.mouse_utils import MouseUtils
from bot.combat_mode import CombatMode
import pyautogui

class SpecialException(Exception):
    def __init__(self, message):
        super().__init__(message)


class Special:
    """
    Provides the navigation and any necessary utility functions to handle the Special game mode.
    """

    _dimensional_halo_amount = 0

    @staticmethod
    def start(first_run: bool):
        """Starts the process of completing a generic setup that supports the 'Play Again' logic.

        Returns:
            None
        """
        from bot.game import Game
    
        MessageLog.print_message(f"\n[GENERIC] GO to bookmark...")
        
        # 按下 Alt 键
        pyautogui.keyDown('alt')
        # 按下 1 键
        pyautogui.press('1')
        # 抬起 Alt 键
        pyautogui.keyUp('alt')

        Game.wait(2)


        if Game.find_and_click_button("checkpoint", tries = 10):
            MessageLog.print_message(f"f5")
            Game.find_and_click_button("reload", tries = 10)
        elif Game.find_and_click_button("route", tries = 10):
            Game.wait(5)
            if Game.find_and_click_button("box_150", tries = 10):
                Game.find_and_click_button("box_select", tries = 20)
                Game.wait(2)
                Game.find_and_click_button("route_ok", tries = 20)
            elif Game.find_and_click_button("box_red", tries = 10):
                Game.find_and_click_button("box_select", tries = 20)
                Game.wait(2)
                Game.find_and_click_button("route_ok", tries = 20)
            elif Game.find_and_click_button("box_100", tries = 10):
                Game.find_and_click_button("box_select", tries = 20)
                Game.wait(2)
                Game.find_and_click_button("route_ok", tries = 20)
        elif Game.find_and_click_button("haven", tries = 10):
            Game.wait(2)
            Game.find_and_click_button("goal", tries = 20)
        elif Game.find_and_click_button("goal", tries = 10):
            Game.find_and_click_button("reload", tries = 10)

        Game.find_and_click_button("reload", tries = 10)
        MessageLog.print_message(f"f5")

        return None

