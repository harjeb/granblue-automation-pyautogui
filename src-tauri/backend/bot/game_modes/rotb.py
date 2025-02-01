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

        # Go to the Home screen.
        Game.go_back_home(confirm_location_check = True)

        # 按下 Alt 键
        pyautogui.keyDown('alt')
        # 按下 1 键
        pyautogui.press('1')
        # 抬起 Alt 键
        pyautogui.keyUp('alt')

        Game.wait(1.5)

        # Check for resume.
        if ImageUtils.confirm_location("resume_quests", tries = 5):
            Game.find_and_click_button("resume")
            Game.wait(5)
            # Now start Combat Mode and detect any item drops.
            if CombatMode.start_combat_mode(["enablefullauto"]):
                Game.collect_loot(is_completed = True)

        if ImageUtils.confirm_location("rotb"):
            # Remove the difficulty prefix from the mission name.
            temp_mission_name = ""
            if Settings.mission_name == "EX+":
                difficulty = "Extreme+"
            else:
                difficulty = "Extreme"
                if ImageUtils.find_button("zhuque"):
                    Game.find_and_click_button("zhuque")
                    temp_mission_name = "Zhuque"
                elif ImageUtils.find_button("baihu"):
                    Game.find_and_click_button("baihu")
                    temp_mission_name = "Baihu"
                elif ImageUtils.find_button("qinglong"):
                    Game.find_and_click_button("qinglong")
                    temp_mission_name = "Qinglong"
                elif ImageUtils.find_button("sixiang_all"):
                    Game.find_and_click_button("sixiang_all")
                    temp_mission_name = "Qinglong"
                elif ImageUtils.find_button("xuanwu"):
                    Game.find_and_click_button("xuanwu")
                    temp_mission_name = "Xuanwu"
                elif ImageUtils.find_button("rotb_extreme"):
                    Game.find_and_click_button("rotb_extreme")
                    temp_mission_name = "Qinglong"
                else:
                    MessageLog.print_message("Failed to find any EX beasts.")

            # Only Raids are marked with Extreme difficulty.
            if difficulty == "Extreme":
                # Click on the Raid banner.
                MessageLog.print_message(f"[ROTB] Now hosting {temp_mission_name} Raid...")

                if ImageUtils.confirm_location("rotb_battle_the_beasts", tries = 30):
                    if temp_mission_name == "Zhuque":
                        MessageLog.print_message(f"[ROTB] Now starting EX Zhuque Raid...")
                        Game.find_and_click_button("rotb_raid_zhuque")
                    elif temp_mission_name == "Xuanwu":
                        MessageLog.print_message(f"[ROTB] Now starting EX Xuanwu Raid...")
                        Game.find_and_click_button("rotb_raid_xuanwu")
                    elif temp_mission_name == "Baihu":
                        MessageLog.print_message(f"[ROTB] Now starting EX Baihu Raid...")
                        Game.find_and_click_button("rotb_raid_baihu")
                    elif temp_mission_name == "Qinglong":
                        MessageLog.print_message(f"[ROTB] Now starting EX Qinglong Raid...")
                        Game.find_and_click_button("rotb_raid_qinglong")
                else:
                    MessageLog.print_message("Failed to open the ROTB Battle the Beasts popup.")

            else:
                MessageLog.print_message(f"[ROTB] Now hosting {temp_mission_name} Quest...")
                Game.find_and_click_button("extreme_p")
                # Find all instances of the "Select" button on the screen and click on the first instance.
                
        else:
            MessageLog.print_message("Failed to arrive at the ROTB page.")

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
            if Settings.mission_name != "EX+":
                is_loot = Settings.item_amount_farmed % 100
            else:
                is_loot = Settings.item_amount_farmed % 18

        Game.find_and_click_button("ok")
        # Start the navigation process.
        if first_run:
          print(1)
          RiseOfTheBeasts._trade()
          RiseOfTheBeasts._navigate()
        elif is_loot == 0:
            print(2)
            MessageLog.print_message("Go to trade.")
            RiseOfTheBeasts._trade()
            RiseOfTheBeasts._navigate()
        elif Game.find_and_click_button("play_again"):
            print(3)
            Game.find_and_click_button("cancel")
            Game.find_and_click_button("close")
            # is_exp = Settings.item_amount_farmed % 8
            # if Game.check_for_popups():
            #     RiseOfTheBeasts._navigate()
            # elif is_exp == 0:
            #     RiseOfTheBeasts._navigate()
        else:
            print(4)
            # If the bot cannot find the "Play Again" button, check for Pending Battles and then perform navigation again.
            Game.check_for_pending()
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
