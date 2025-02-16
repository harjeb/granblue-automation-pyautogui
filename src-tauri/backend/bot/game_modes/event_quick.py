from utils.settings import Settings
from utils.message_log import MessageLog
from utils.image_utils import ImageUtils
from utils.mouse_utils import MouseUtils
from bot.combat_mode import CombatMode
import pyautogui

class EventException(Exception):
    def __init__(self, message):
        super().__init__(message)


class Event_quick:
    """
    Provides the navigation and any necessary utility functions to handle the Event or Event (Token Drawboxes) game mode.
    """

    @staticmethod
    def go_to_event():
        from bot.game import Game
        # press alt + 1
        pyautogui.keyDown('alt')
        pyautogui.press('5')
        pyautogui.keyUp('alt')


    @staticmethod
    def _navigate():
        """Navigates to the specified Event mission.

        Returns:
            None
        """
        from bot.game import Game
        Game.find_and_click_button("home")
        pyautogui.press('f5')
        Game.wait(2)
        Event_quick.go_to_event()
        Game.wait(2)
        return None

    @staticmethod
    def start():
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


        if Game.check_for_captcha():
            return None

        if Game.find_and_click_button("party_selection_ok", tries = 10):
            if Game.find_and_click_button("attack", tries = 25):
                MessageLog.print_message(f"[GENERIC] refresh")
                pyautogui.press('f5')
                
        return None