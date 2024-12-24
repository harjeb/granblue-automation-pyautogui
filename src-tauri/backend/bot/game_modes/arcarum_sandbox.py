from typing import Tuple, List

from utils.message_log import MessageLog
from utils.settings import Settings
from utils.image_utils import ImageUtils
from utils.mouse_utils import MouseUtils
from bot.combat_mode import CombatMode
import pyautogui

class ArcarumSandboxException(Exception):
    def __init__(self, message):
        super().__init__(message)


class ArcarumSandbox:
    """
    Provides the navigation and any necessary utility functions to handle the Arcarum Replicard Sandbox game mode.
    """

    _first_run: bool = True

    # The x and y coordinates are the difference between the center of the Menu button at the top-right and the center of the node itself.
    # The section refers to the left most page that the node is located in starting at page 0.

    @staticmethod
    def _navigate_to_mission(skip_to_action: bool = False):
        """Navigates to the specified Arcarum Replicard Sandbox mission inside the current Zone.

        Args:
            skip_to_action (bool, optional): True if the mission is already selected. Defaults to False.

        Returns:
            None
        """
        from bot.game import Game

        # sandbox
        pyautogui.keyDown('alt')
        pyautogui.press('4')
        pyautogui.keyUp('alt')

        Game.wait(3.0)

        # if gold chest exists, the mission may be invisible
        if Game.find_and_click_button("gold_chest"):
            ArcarumSandbox._open_gold_chest()
            return None

        if Game.find_and_click_button("mimic", suppress_error = True):
            Game.wait(3.0)
            if Game.check_for_captcha():
                Game.wait(3.0)
            if Game.find_party_and_start_mission(Settings.group_number, Settings.party_number):
                if CombatMode.start_combat_mode():
                    Game.collect_loot(is_completed = True)
            Game.find_and_click_button("expedition")
            return None

        #MouseUtils.scroll_screen_from_home_button(-500)
        #Game.wait(1.5)

        if ImageUtils.find_button("attack"):
            if CombatMode.start_combat_mode():
                Game.collect_loot(is_completed = True)
                return None

        # if ImageUtils.find_button("boost"):
        #     # 有bonus怪
        #     MessageLog.print_message(f"\n[ARCARUM.SANDBOX] Found Boost and fighting it...")
        #     action_locations: List[Tuple[int, ...]] = ImageUtils.find_all("arcarum_sandbox_action")
        #     MouseUtils.move_and_click_point(action_locations[0][0], action_locations[0][1], "arcarum_sandbox_action")
        #     return None

        # If there is no Defender, then the first action is the mission itself. Else, it is the second action.
        action_locations: List[Tuple[int, ...]] = ImageUtils.find_all("arcarum_sandbox_action")
        if len(action_locations) == 1:
            MouseUtils.move_and_click_point(action_locations[0][0], action_locations[0][1], "arcarum_sandbox_action")
        elif Settings.enable_defender and Settings.number_of_defeated_defenders < Settings.number_of_defenders:
            MouseUtils.move_and_click_point(action_locations[-2][0], action_locations[-2][1], "arcarum_sandbox_action")
            MessageLog.print_message(f"\n[ARCARUM.SANDBOX] Found Defender and fighting it...")
            Settings.engaged_defender_battle = True
        else:
            # If there is Defender,the mission should be latest
            MouseUtils.move_and_click_point(action_locations[-1][0], action_locations[-1][1], "arcarum_sandbox_action")

        return None

    @staticmethod
    def _reset_position():
        """Resets the position of the bot to be at the left-most edge of the map.

        Returns:
            None
        """
        from bot.game import Game

        MessageLog.print_message(f"[ARCARUM.SANDBOX] Now determining if bot is starting all the way at the left edge of the Zone...")
        count = 0
        while Game.find_and_click_button("arcarum_sandbox_left_arrow", tries = 1, suppress_error = True):
            Game.wait(1.0)
            count += 1
            if count > 30:
                break

        MessageLog.print_message(f"[ARCARUM.SANDBOX] Left edge of the Zone has been reached.")

        return None

    @staticmethod
    def _navigate_to_zone():
        """Navigates to the specified Arcarum Replicard Sandbox Zone.

        Returns:
            None
        """
        from bot.game import Game
        # Finally, select the mission.
        ArcarumSandbox._navigate_to_mission()

        return None

    @staticmethod
    def _refill_aap():
        """Refills AAP if necessary.

        Returns:
            None
        """
        if ImageUtils.confirm_location("aap", tries = 10):
            from bot.game import Game

            MessageLog.print_message(f"\n[ARCARUM.SANDBOX] Bot ran out of AAP. Refilling now...")
            use_locations = ImageUtils.find_all("use")
            MouseUtils.move_and_click_point(use_locations[1][0], use_locations[1][1], "use")

            Game.wait(1.0)
            Game.find_and_click_button("ok")
            Game.wait(1.0)

            MessageLog.print_message(f"[ARCARUM.SANDBOX] AAP is now refilled.")

        return None
    
    @staticmethod
    def _play_zone_boss():
        """Clicks on Play if you are fighting a zone boss.

        Returns:
            None
        """
        play_button = ImageUtils.find_button("play")
        if play_button:
            MessageLog.print_message(f"\n[ARCARUM.SANDBOX] Now fighting zone boss...")
            MouseUtils.move_and_click_point(play_button[0], play_button[1], "play")

        return None

    @staticmethod
    def _open_gold_chest():
        """Clicks on a gold chest.
        If it is a mimic, fight it, if not, click ok.

        Returns:
            None
        """
        from bot.game import Game

        #MouseUtils.move_and_click_point(action_locations[0][0], action_locations[0][1], "arcarum_sandbox_action")
        Game.find_and_click_button("ok")
        Game.wait(5.0)
        if Game.find_and_click_button("ok", suppress_error = True) is False:
            MessageLog.print_message("\n[ARCARUM.SANDBOX] Click first...")
            action_locations: List[Tuple[int, ...]] = ImageUtils.find_all("arcarum_sandbox_action")
            MouseUtils.move_and_click_point(action_locations[0][0], action_locations[0][1], "arcarum_sandbox_action")
            Game.wait(3.0)
            if Game.find_party_and_start_mission(Settings.group_number, Settings.party_number):
                if CombatMode.start_combat_mode():
                    Game.collect_loot(is_completed = True)
            Game.find_and_click_button("expedition")
                 
        Game.wait(2.0)
        ArcarumSandbox._reset_position()
        ArcarumSandbox._navigate_to_mission()

    @staticmethod
    def start():
        """Starts the process of completing Arcarum Replicard Sandbox missions.

        Returns:
            None
        """
        from bot.game import Game

        # Start the navigation process.
        if ArcarumSandbox._first_run:
            ArcarumSandbox._navigate_to_zone() 
        elif Game.find_and_click_button("play_again") is False:
            if Game.find_and_click_button("expedition"):
                # Wait out the animations that play, whether it be Treasure or Defender spawning.
                Game.wait(5.0)
                # Click away the Treasure popup if it shows up.
                Game.find_and_click_button("ok", suppress_error = True)
                if Settings.enable_gold_chest and Game.find_and_click_button("gold_chest") is True:
                    ArcarumSandbox._open_gold_chest()
                else:
                    # Start the mission again.
                    Game.wait(3.0)
                    # navigate to mission again.
                    ArcarumSandbox._navigate_to_mission(skip_to_action = True)
            elif Game.check_for_pending():
                ArcarumSandbox._first_run = True
                ArcarumSandbox._navigate_to_zone()
            elif ImageUtils.find_button("home_news") is not None:
                Game.go_back_home(confirm_location_check = True)
                ArcarumSandbox._first_run = True
                ArcarumSandbox._navigate_to_zone()
            else:
                if Game.find_and_click_button("mimic", suppress_error = True):
                    Game.wait(3.0)
                    if Game.find_and_click_button("ok", tries = 30):
                        if CombatMode.start_combat_mode():
                            Game.collect_loot(is_completed = True)
                    Game.find_and_click_button("expedition")

                if ImageUtils.find_button("attack"):
                    if CombatMode.start_combat_mode():
                        Game.collect_loot(is_completed = True)

                # If the bot find the "close" button, click.
                Game.find_and_click_button("close")

                # If the bot find the "ok" button, click.
                Game.find_and_click_button("ok")

                # If the bot cannot find the "Play Again" button, click the Expedition button.
                Game.find_and_click_button("expedition")

                # Wait out the animations that play, whether it be Treasure or Defender spawning.
                Game.wait(5.0)

                # Click away the Treasure popup if it shows up.
                Game.find_and_click_button("ok", suppress_error = True)
                if Settings.enable_gold_chest and Game.find_and_click_button("gold_chest") is True:
                    ArcarumSandbox._open_gold_chest()
                else:
                    # Start the mission again.
                    Game.wait(3.0)
                    # navigate to mission again.
                    ArcarumSandbox._first_run = True
                    ArcarumSandbox._navigate_to_zone()
                    #ArcarumSandbox._navigate_to_mission(skip_to_action = True)

        if Game.check_for_captcha():
            Game.wait(3.0)

        # Refill AAP if needed.
        #ArcarumSandbox._play_zone_boss()
        #ArcarumSandbox._refill_aap()

        if Game.find_and_click_button("ok", tries = 30):
            if CombatMode.start_combat_mode():
                Game.collect_loot(is_completed = True)

        return None
