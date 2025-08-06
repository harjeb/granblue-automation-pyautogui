from utils.settings import Settings
from utils.message_log import MessageLog
from utils.image_utils import ImageUtils
from utils.mouse_utils import MouseUtils
from bot.combat_mode import CombatMode
import pyautogui

class RiseOfTheBeastsException(Exception):
    def __init__(self, message):
        super().__init__(message)


class RiseOfTheBeasts:
    """
    Provides the navigation and any necessary utility functions to handle the Rise of the Beasts game mode.
    """

    @staticmethod
    def check_for_rotb_extreme_plus():
        """Checks for Extreme+ for Rise of the Beasts and if it appears and the user enabled it in user settings, start it.

        Returns:
            (bool): Return True if Extreme+ was detected and successfully completed. Otherwise, return False.
        """
        from bot.game import Game

        if Settings.enable_nightmare and ImageUtils.find_button("play_next", tries = 3):
            MessageLog.print_message("\n[ROTB] Detected Extreme+. Starting it now...")

            MessageLog.print_message("\n********************************************************************************")
            MessageLog.print_message("********************************************************************************")
            MessageLog.print_message(f"[ROTB] Rise of the Beasts Extreme+")
            MessageLog.print_message(f"[ROTB] Rise of the Beasts Extreme+ Summon Elements: {Settings.nightmare_summon_elements_list}")
            MessageLog.print_message(f"[ROTB] Rise of the Beasts Extreme+ Summons: {Settings.nightmare_summon_list}")
            MessageLog.print_message(f"[ROTB] Rise of the Beasts Extreme+ Group Number: {Settings.nightmare_group_number}")
            MessageLog.print_message(f"[ROTB] Rise of the Beasts Extreme+ Party Number: {Settings.nightmare_party_number}")
            MessageLog.print_message(f"[ROTB] Rise of the Beasts Extreme+ Combat Script: {Settings.nightmare_combat_script_name}")
            MessageLog.print_message("********************************************************************************")
            MessageLog.print_message("********************************************************************************\n")

            # Click the "Play Next" button to head to the Summon Selection screen.
            Game.find_and_click_button("play_next")

            Game.wait(1)

            # Once the bot is at the Summon Selection screen, select your Summon and Party and start the mission.
            if ImageUtils.confirm_location("select_a_summon", tries = 30):
                Game.select_summon(Settings.nightmare_summon_list, Settings.nightmare_summon_elements_list)
                start_check = Game.find_party_and_start_mission(int(Settings.nightmare_group_number), int(Settings.nightmare_party_number), bypass_first_run = True)

                # Once preparations are completed, start Combat mode.
                if start_check and CombatMode.start_combat_mode(is_nightmare = True):
                    Game.collect_loot(is_completed = False, is_event_nightmare = True)
                    return True

        elif not Settings.enable_nightmare and ImageUtils.find_button("play_next", tries = 3):
            MessageLog.print_message("\n[ROTB] Rise of the Beasts Extreme+ detected go default fight. Moving on...")
            # Click the "Play Next" button to head to the Summon Selection screen.
            Game.find_and_click_button("play_next")
            Game.wait(1)
            round_play_button_locations = ImageUtils.find_all("play_round_button")
            MessageLog.print_message("\n[ROTB] Play qinglong ex +...")
            try:
                MouseUtils.move_and_click_point(round_play_button_locations[3][0], round_play_button_locations[3][1], "play_round_button")
            except:
                pass
            # Check if the bot is at the Summon Selection screen.
            if ImageUtils.confirm_location("select_a_summon", tries = 30):
                summon_check = Game.select_default_summon()
                if summon_check:
                    # Find and click the "OK" button to start the mission.
                    Game.find_and_click_button("ok")

                    # Now start Combat Mode and detect any item drops.
                    if CombatMode.start_combat_mode():
                        Game.collect_loot(is_completed = True)
                        return True

        else:
            MessageLog.print_message("\n[ROTB] No Rise of the Beasts Extreme+ detected. Moving on...")

        return False

    @staticmethod
    def _trade():
        from bot.game import Game
        # Go to the Home screen.
        Game.go_back_home(confirm_location_check = True)
        MessageLog.print_message(f"\n[ROTB] Now navigating to trade...")
        # Go to the Event by clicking on the "Menu" button and then click the very first banner.
        Game.find_and_click_button("home_menu")
        Game.wait(1.0)
        banner_locations = ImageUtils.find_all("event_banner", custom_confidence = 0.7)
        if len(banner_locations) == 0:
            banner_locations = ImageUtils.find_all("event_banner_blue", custom_confidence = 0.7)
            if len(banner_locations) == 0:
                MessageLog.print_message("Failed to find the Event banner.")
        if len(banner_locations)>0:
            if Settings.first_event:
                MouseUtils.move_and_click_point(banner_locations[0][0], banner_locations[0][1], "event_banner")
            else:
                MouseUtils.move_and_click_point(banner_locations[1][0], banner_locations[1][1], "event_banner")
        Game.wait(3.0)

        # Check for resume.
        if ImageUtils.confirm_location("resume_quests", tries = 5):
            Game.find_and_click_button("resume")
            Game.wait(5)
            # Now start Combat Mode and detect any item drops.
            if CombatMode.start_combat_mode(["enablefullauto"]):
                Game.collect_loot(is_completed = True)
        Game.find_and_click_button("loot")
        Game.wait(1.0)

        trade_locations = ImageUtils.find_all("trade")
        if len(trade_locations) > 0:
            MouseUtils.move_and_click_point(trade_locations[0][0], trade_locations[0][1], "trade")
        if ImageUtils.find_button("trade_for"):
            MessageLog.print_message(f"\n999...")
            Game.find_and_click_button("trade_for")
            for i in range(30):
                pyautogui.press('down')
                Game.wait(0.5)
            pyautogui.press("enter")
            Game.find_and_click_button("trade")
            Game.find_and_click_button("ok")
        else:
            if ImageUtils.find_button("trade_long"):
                MessageLog.print_message(f"\n11111...")
                Game.find_and_click_button("trade_long")
                Game.wait(1)
                Game.find_and_click_button("ok")
                MessageLog.print_message(f"\n2222...")
                Game.wait(3)

    @staticmethod
    def _navigate():
        """Navigates to the specified Rise of the Beasts mission.

        Returns:
            None
        """
        from bot.game import Game
        import datetime

        # Go to the Home screen.
        Game.go_back_home(confirm_location_check = True)

        # Get current hour to determine which shortcut to use
        current_hour = datetime.datetime.now().hour

        # Determine which navigation method to use based on Settings.rotb_method
        if Settings.rotb_method == 1:
            # Method 1: Alt+Shift+1-4 (original method)
            shortcut_key = '1'  # Default value

            # Logic for determining the shortcut key based on time and rotb_first setting
            if 23 <= current_hour or current_hour < 1:
                # 23:00-1:00 time slot
                if Settings.rotb_first == 1:
                    shortcut_key = '1'
                elif Settings.rotb_first == 2:
                    shortcut_key = '2'
                elif Settings.rotb_first == 3:
                    shortcut_key = '3'
                elif Settings.rotb_first == 4:
                    shortcut_key = '4'
            elif 1 <= current_hour < 3:
                # 1:00-3:00 time slot
                if Settings.rotb_first == 1:
                    shortcut_key = '2'
                elif Settings.rotb_first == 2:
                    shortcut_key = '3'
                elif Settings.rotb_first == 3:
                    shortcut_key = '4'
                elif Settings.rotb_first == 4:
                    shortcut_key = '1'
            elif 3 <= current_hour < 5:
                # 3:00-5:00 time slot
                if Settings.rotb_first == 1:
                    shortcut_key = '3'
                elif Settings.rotb_first == 2:
                    shortcut_key = '4'
                elif Settings.rotb_first == 3:
                    shortcut_key = '1'
                elif Settings.rotb_first == 4:
                    shortcut_key = '2'
            elif 5 <= current_hour < 7:
                # 5:00-7:00 time slot
                if Settings.rotb_first == 1:
                    shortcut_key = '4'
                elif Settings.rotb_first == 2:
                    shortcut_key = '1'
                elif Settings.rotb_first == 3:
                    shortcut_key = '2'
                elif Settings.rotb_first == 4:
                    shortcut_key = '3'
            elif 7 <= current_hour < 9:
                # 7:00-9:00 time slot - cycle back to the first pattern
                if Settings.rotb_first == 1:
                    shortcut_key = '1'
                elif Settings.rotb_first == 2:
                    shortcut_key = '2'
                elif Settings.rotb_first == 3:
                    shortcut_key = '3'
                elif Settings.rotb_first == 4:
                    shortcut_key = '4'
            elif 9 <= current_hour < 11:
                # 9:00-11:00 time slot
                if Settings.rotb_first == 1:
                    shortcut_key = '2'
                elif Settings.rotb_first == 2:
                    shortcut_key = '3'
                elif Settings.rotb_first == 3:
                    shortcut_key = '4'
                elif Settings.rotb_first == 4:
                    shortcut_key = '1'
            elif 11 <= current_hour < 13:
                # 11:00-13:00 time slot
                if Settings.rotb_first == 1:
                    shortcut_key = '3'
                elif Settings.rotb_first == 2:
                    shortcut_key = '4'
                elif Settings.rotb_first == 3:
                    shortcut_key = '1'
                elif Settings.rotb_first == 4:
                    shortcut_key = '2'
            elif 13 <= current_hour < 15:
                # 13:00-15:00 time slot
                if Settings.rotb_first == 1:
                    shortcut_key = '4'
                elif Settings.rotb_first == 2:
                    shortcut_key = '1'
                elif Settings.rotb_first == 3:
                    shortcut_key = '2'
                elif Settings.rotb_first == 4:
                    shortcut_key = '3'
            elif 15 <= current_hour < 17:
                # 15:00-17:00 time slot - cycle back to the first pattern
                if Settings.rotb_first == 1:
                    shortcut_key = '1'
                elif Settings.rotb_first == 2:
                    shortcut_key = '2'
                elif Settings.rotb_first == 3:
                    shortcut_key = '3'
                elif Settings.rotb_first == 4:
                    shortcut_key = '4'
            elif 17 <= current_hour < 19:
                # 17:00-19:00 time slot
                if Settings.rotb_first == 1:
                    shortcut_key = '2'
                elif Settings.rotb_first == 2:
                    shortcut_key = '3'
                elif Settings.rotb_first == 3:
                    shortcut_key = '4'
                elif Settings.rotb_first == 4:
                    shortcut_key = '1'
            elif 19 <= current_hour < 21:
                # 19:00-21:00 time slot
                if Settings.rotb_first == 1:
                    shortcut_key = '3'
                elif Settings.rotb_first == 2:
                    shortcut_key = '4'
                elif Settings.rotb_first == 3:
                    shortcut_key = '1'
                elif Settings.rotb_first == 4:
                    shortcut_key = '2'
            elif 21 <= current_hour < 23:
                # 21:00-23:00 time slot
                if Settings.rotb_first == 1:
                    shortcut_key = '4'
                elif Settings.rotb_first == 2:
                    shortcut_key = '1'
                elif Settings.rotb_first == 3:
                    shortcut_key = '2'
                elif Settings.rotb_first == 4:
                    shortcut_key = '3'

            MessageLog.print_message(f"[ROTB] Method 1: Current time: {current_hour}:00, using shortcut Alt+Shift+{shortcut_key} based on rotb_first={Settings.rotb_first}")

            # Press Alt+Shift+key shortcut
            pyautogui.keyDown('alt')
            pyautogui.keyDown('shift')
            pyautogui.press(shortcut_key)
            pyautogui.keyUp('shift')
            pyautogui.keyUp('alt')

        elif Settings.rotb_method == 2:
            # Method 2: Alt+Shift+5-8
            shortcut_key = '5'  # Default value

            # Logic for determining the shortcut key based on time and rotb_first setting
            if 23 <= current_hour or current_hour < 1:
                # 23:00-1:00 time slot
                if Settings.rotb_first == 1:
                    shortcut_key = '5'
                elif Settings.rotb_first == 2:
                    shortcut_key = '6'
                elif Settings.rotb_first == 3:
                    shortcut_key = '7'
                elif Settings.rotb_first == 4:
                    shortcut_key = '8'
            elif 1 <= current_hour < 3:
                # 1:00-3:00 time slot
                if Settings.rotb_first == 1:
                    shortcut_key = '6'
                elif Settings.rotb_first == 2:
                    shortcut_key = '7'
                elif Settings.rotb_first == 3:
                    shortcut_key = '8'
                elif Settings.rotb_first == 4:
                    shortcut_key = '5'
            elif 3 <= current_hour < 5:
                # 3:00-5:00 time slot
                if Settings.rotb_first == 1:
                    shortcut_key = '7'
                elif Settings.rotb_first == 2:
                    shortcut_key = '8'
                elif Settings.rotb_first == 3:
                    shortcut_key = '5'
                elif Settings.rotb_first == 4:
                    shortcut_key = '6'
            elif 5 <= current_hour < 7:
                # 5:00-7:00 time slot
                if Settings.rotb_first == 1:
                    shortcut_key = '8'
                elif Settings.rotb_first == 2:
                    shortcut_key = '5'
                elif Settings.rotb_first == 3:
                    shortcut_key = '6'
                elif Settings.rotb_first == 4:
                    shortcut_key = '7'
            elif 7 <= current_hour < 9:
                # 7:00-9:00 time slot - cycle back to the first pattern
                if Settings.rotb_first == 1:
                    shortcut_key = '5'
                elif Settings.rotb_first == 2:
                    shortcut_key = '6'
                elif Settings.rotb_first == 3:
                    shortcut_key = '7'
                elif Settings.rotb_first == 4:
                    shortcut_key = '8'
            elif 9 <= current_hour < 11:
                # 9:00-11:00 time slot
                if Settings.rotb_first == 1:
                    shortcut_key = '6'
                elif Settings.rotb_first == 2:
                    shortcut_key = '7'
                elif Settings.rotb_first == 3:
                    shortcut_key = '8'
                elif Settings.rotb_first == 4:
                    shortcut_key = '5'
            elif 11 <= current_hour < 13:
                # 11:00-13:00 time slot
                if Settings.rotb_first == 1:
                    shortcut_key = '7'
                elif Settings.rotb_first == 2:
                    shortcut_key = '8'
                elif Settings.rotb_first == 3:
                    shortcut_key = '5'
                elif Settings.rotb_first == 4:
                    shortcut_key = '6'
            elif 13 <= current_hour < 15:
                # 13:00-15:00 time slot
                if Settings.rotb_first == 1:
                    shortcut_key = '8'
                elif Settings.rotb_first == 2:
                    shortcut_key = '5'
                elif Settings.rotb_first == 3:
                    shortcut_key = '6'
                elif Settings.rotb_first == 4:
                    shortcut_key = '7'
            elif 15 <= current_hour < 17:
                # 15:00-17:00 time slot - cycle back to the first pattern
                if Settings.rotb_first == 1:
                    shortcut_key = '5'
                elif Settings.rotb_first == 2:
                    shortcut_key = '6'
                elif Settings.rotb_first == 3:
                    shortcut_key = '7'
                elif Settings.rotb_first == 4:
                    shortcut_key = '8'
            elif 17 <= current_hour < 19:
                # 17:00-19:00 time slot
                if Settings.rotb_first == 1:
                    shortcut_key = '6'
                elif Settings.rotb_first == 2:
                    shortcut_key = '7'
                elif Settings.rotb_first == 3:
                    shortcut_key = '8'
                elif Settings.rotb_first == 4:
                    shortcut_key = '5'
            elif 19 <= current_hour < 21:
                # 19:00-21:00 time slot
                if Settings.rotb_first == 1:
                    shortcut_key = '7'
                elif Settings.rotb_first == 2:
                    shortcut_key = '8'
                elif Settings.rotb_first == 3:
                    shortcut_key = '5'
                elif Settings.rotb_first == 4:
                    shortcut_key = '6'
            elif 21 <= current_hour < 23:
                # 21:00-23:00 time slot
                if Settings.rotb_first == 1:
                    shortcut_key = '8'
                elif Settings.rotb_first == 2:
                    shortcut_key = '5'
                elif Settings.rotb_first == 3:
                    shortcut_key = '6'
                elif Settings.rotb_first == 4:
                    shortcut_key = '7'

            MessageLog.print_message(f"[ROTB] Method 2: Current time: {current_hour}:00, using shortcut Alt+Shift+{shortcut_key} based on rotb_first={Settings.rotb_first}")

            # Press Alt+Shift+key shortcut
            pyautogui.keyDown('alt')
            pyautogui.keyDown('shift')
            pyautogui.press(shortcut_key)
            pyautogui.keyUp('shift')
            pyautogui.keyUp('alt')

        elif Settings.rotb_method == 3:
            # Method 3: Alt+!
            MessageLog.print_message(f"[ROTB] Method 3: Using Alt+1 shortcut")

            # Press Alt+! shortcut
            pyautogui.keyDown('alt')
            pyautogui.press('1')
            pyautogui.keyUp('alt')

        Game.wait(1.5)

        return None

    @staticmethod
    def start(first_run: bool):
        """Starts the process to complete a run for Rise of the Beasts Farming Mode and returns the number of items detected.

        Args:
            first_run (bool): Flag that determines whether or not to run the navigation process again. Should be False if the Farming Mode supports the "Play Again" feature for repeated runs.

        Returns:
            None
        """
        from bot.game import Game
        is_loot = 1
        if not first_run:
            if Settings.rotb_method == 1:
                is_loot = Settings.item_amount_farmed % 400
            elif Settings.rotb_method == 2:
                is_loot = Settings.item_amount_farmed % 20
            else:
                is_loot = Settings.item_amount_farmed % 14

        Game.find_and_click_button("ok")
        # Start the navigation process.
        if first_run:
          print(111)
          RiseOfTheBeasts._trade()
          RiseOfTheBeasts._navigate()
        elif is_loot == 0:
            print(222)
            MessageLog.print_message("Go to trade.")
            RiseOfTheBeasts._trade()
            RiseOfTheBeasts._navigate()
            # is_exp = Settings.item_amount_farmed % 8
            # if Game.check_for_popups():
            #     RiseOfTheBeasts._navigate()
            # elif is_exp == 0:
            #     RiseOfTheBeasts._navigate()
        else:
            print(444)
            RiseOfTheBeasts._navigate()

        # Check for AP.
        #Game.check_for_ap()
        if Game.check_for_captcha():
            return None

        # Check if the bot is at the Summon Selection screen.
        if Game.find_and_click_button("party_selection_ok", tries = 30):
            # Now start Combat Mode and detect any item drops.
            if CombatMode.start_combat_mode():
                Game.collect_loot(is_completed = True)
                Game.find_and_click_button("ok")
        else:
            MessageLog.print_message("Failed to arrive at the Summon Selection screen.")

        return None
