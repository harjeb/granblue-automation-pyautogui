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
            Game.wait(2)

            if 'summon' in Settings.combat_script_name:
                Game.wait(2)
                if ImageUtils.find_button("attack", tries = 25):
                    if ImageUtils.find_button("quick_summon_not_ready", bypass_general_adjustment = True) is None and \
                        (Game.find_and_click_button("quick_summon1", bypass_general_adjustment = True) or Game.find_and_click_button("quick_summon2", bypass_general_adjustment = True)):
                        MessageLog.print_message(f"[GENERIC] refresh")
                        pyautogui.press('f5')
                        Settings.item_amount_farmed += 1
            elif 'fa' in Settings.combat_script_name:
                MessageLog.print_message(f"fa")
                Game.wait(2)
                if ImageUtils.find_button("attack", tries = 25):
                    CombatMode._enable_full_auto()
            elif Game.find_and_click_button("attack", tries = 25):
                MessageLog.print_message(f"[GENERIC] refresh")
                pyautogui.press('f5')
                Settings.item_amount_farmed += 1
        else:
            Game.find_and_click_button("attack", tries = 30)
            MessageLog.print_message(f"[GENERIC] refresh")
            pyautogui.press('f5')
            Settings.item_amount_farmed += 1
    
        Game.wait(2)
                
        return None