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
    def start(first_run: bool):
        """Starts the process to complete a run for Event or Event (Token Drawboxes) Farming Mode and returns the number of items detected.

        Args:
            first_run (bool): Flag that determines whether or not to run the navigation process again. Should be False if the Farming Mode supports the "Play Again" feature for repeated runs.

        Returns:
            None
        """
        from bot.game import Game

        # Start the navigation process.
        if first_run:
            Event_quick._navigate()
        else:
            # If the bot cannot find the "Play Again" button, check for Pending Battles and then perform navigation again.
            Game.check_for_pending()
            Event_quick._navigate()


        # Check if the bot is at the Summon Selection screen.
        if ImageUtils.confirm_location("select_a_summon", tries = 30):
            if Settings.summon_default:
                summon_check = Game.select_default_summon()
                if summon_check:
                    if Game.check_for_captcha():
                        Game.select_default_summon()
                    Game.quick_start_mission()
                    if CombatMode.start_combat_mode():
                        Game.collect_loot(is_completed = True)
            else:
                summon_check = Game.select_summon(Settings.summon_list, Settings.summon_element_list)
                if summon_check:
                    if Game.check_for_captcha():
                        Game.select_default_summon()
                    # Select the Party.
                    Game.find_party_and_start_mission(Settings.group_number, Settings.party_number)
                    # Now start Combat Mode and detect any item drops.
                    if CombatMode.start_combat_mode():
                        Game.collect_loot(is_completed = True)
                else:
                    # DO NOT EXIT
                    MessageLog.print_message("\n[ERROR] Failed to arrive at the Summon Selection screen.")
        elif ImageUtils.find_button("ok", tries = 10):
            Game.quick_start_mission()
            if CombatMode.start_combat_mode():
                Game.collect_loot(is_completed = True)
        # Check for battle.
        elif ImageUtils.find_button("attack", tries = 10):
            Game.wait(2)
            # Now start Combat Mode and detect any item drops.
            if CombatMode.start_combat_mode(["enablefullauto"]):
                Game.collect_loot(is_completed = True)

        return None
