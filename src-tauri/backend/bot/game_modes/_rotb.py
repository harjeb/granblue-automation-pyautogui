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
        if ImageUtils.find_button("gold"):
            Game.find_and_click_button("trade")
        else:
            MouseUtils.scroll_screen_from_home_button(-1500)
            Game.wait(1.0)
            Game.find_and_click_button("secondpage")
            Game.wait(1.0)
            MouseUtils.scroll_screen_from_home_button(1500)
            Game.wait(3.0)
            Game.find_and_click_button("trade")
            MessageLog.print_message(f"\n00000...")
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

        MessageLog.print_message(f"\n[ROTB] Now navigating to Rise of the Beasts...")

        # Go to the Event by clicking on the "Menu" button and then click the very first banner.
        Game.find_and_click_button("home_menu")
        Game.wait(1.0)
        banner_locations = ImageUtils.find_all("event_banner", custom_confidence = 0.7)
        if len(banner_locations) == 0:
            banner_locations = ImageUtils.find_all("event_banner_blue", custom_confidence = 0.7)
            if len(banner_locations) == 0:
                MessageLog.print_message("Failed to find the Event banner.")

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

        if ImageUtils.confirm_location("rotb"):
            # Scroll the screen down to make way for smaller screens.
            MouseUtils.scroll_screen_from_home_button(-400)
            # Remove the difficulty prefix from the mission name.
            difficulty = ""
            temp_mission_name = ""
            if ImageUtils.find_button("extreme_p"):
                difficulty = "Extreme+"
            elif Settings.mission_name.find("VH ") == 0:
                difficulty = "Very Hard"
                temp_mission_name = Settings.mission_name[3:]
            elif Settings.mission_name.find("EX") == 0:
                difficulty = "Extreme"
                if ImageUtils.find_button("zhuque"):
                    temp_mission_name = "Zhuque"
                elif ImageUtils.find_button("baihu"):
                    temp_mission_name = "Baihu"
                elif ImageUtils.find_button("qinglong"):
                    temp_mission_name = "Qinglong"
                elif ImageUtils.find_button("sixiang_all"):
                    temp_mission_name = "Qinglong"
                elif ImageUtils.find_button("xuanwu"):
                    temp_mission_name = "Xuanwu"
                else:
                    MessageLog.print_message("Failed to find any EX beasts.")

            # Only Raids are marked with Extreme difficulty.
            if difficulty == "Extreme":
                # Click on the Raid banner.
                MessageLog.print_message(f"[ROTB] Now hosting {temp_mission_name} Raid...")
                Game.find_and_click_button("rotb_extreme")

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

            elif Settings.mission_name == "Lvl 100 Shenxian":
                # Click on Shenxian to host.
                MessageLog.print_message(f"[ROTB] Now hosting Shenxian Raid...")
                Game.find_and_click_button("rotb_shenxian_host")

                if ImageUtils.wait_vanish("rotb_shenxian_host", timeout = 10) is False:
                    MessageLog.print_message(f"[ROTB] There are no more Shenxian hosts left. Alerting user...")
                    raise RiseOfTheBeastsException("There are no more Shenxian hosts left.")

            elif difficulty == "Extreme+":
                MessageLog.print_message("[ROTB] Now hosting EX+ Quest...")
                Game.find_and_click_button("extreme_p")
                if Game.find_and_click_button("rotb_qinglong_p"):
                    MessageLog.print_message(f"[ROTB] Now starting EX+ qinglong Raid...")
            else:
                MessageLog.print_message(f"[ROTB] Now hosting {temp_mission_name} Quest...")

                # Scroll the screen down to make way for smaller screens.
                #MouseUtils.scroll_screen_from_home_button(-400)

                # Find all instances of the "Select" button on the screen and click on the first instance.
                select_button_locations = ImageUtils.find_all("select")
                MouseUtils.move_and_click_point(select_button_locations[0][0], select_button_locations[0][1], "select")

                if ImageUtils.confirm_location("rotb_rising_beasts_showdown", tries = 30):
                    # Find all the round "Play" buttons.
                    round_play_button_locations = ImageUtils.find_all("play_round_button")

                    if temp_mission_name == "Zhuque":
                        MouseUtils.move_and_click_point(round_play_button_locations[0][0], round_play_button_locations[0][1], "play_round_button")
                    elif temp_mission_name == "Xuanwu":
                        MouseUtils.move_and_click_point(round_play_button_locations[1][0], round_play_button_locations[1][1], "play_round_button")
                    elif temp_mission_name == "Baihu":
                        MouseUtils.move_and_click_point(round_play_button_locations[2][0], round_play_button_locations[2][1], "play_round_button")
                    elif temp_mission_name == "Qinglong":
                        MouseUtils.move_and_click_point(round_play_button_locations[3][0], round_play_button_locations[3][1], "play_round_button")

                    Game.wait(2.0)

                    # Find all the round "Play" buttons again.
                    round_play_button_locations = ImageUtils.find_all("play_round_button")

                    # Only Very Hard difficulty will be supported for farming efficiency
                    MouseUtils.move_and_click_point(round_play_button_locations[2][0], round_play_button_locations[2][1], "play_round_button")
                else:
                    raise(RiseOfTheBeastsException("Failed to open the ROTB Rising Beasts Showdown popup."))
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
            if Settings.mission_name != "Lvl 100 Shenxian":
                is_loot = Settings.item_amount_farmed % 40
            else:
                is_loot = Settings.item_amount_farmed % 7

        # Start the navigation process.
        if first_run:
          RiseOfTheBeasts._trade()
          RiseOfTheBeasts._navigate()
        elif is_loot == 1:
            MessageLog.print_message("Go to trade.")
            RiseOfTheBeasts._trade()
            RiseOfTheBeasts._navigate()
        elif Game.find_and_click_button("play_again"):
            is_exp = Settings.item_amount_farmed % 8
            if Game.check_for_popups():
                RiseOfTheBeasts._navigate()
            elif is_exp == 0:
                RiseOfTheBeasts._navigate()
        else:
            # If the bot cannot find the "Play Again" button, check for Pending Battles and then perform navigation again.
            Game.check_for_pending()
            RiseOfTheBeasts._navigate()

        # Check for AP.
        #Game.check_for_ap()

        # Check if the bot is at the Summon Selection screen.
        if ImageUtils.confirm_location("select_a_summon", tries = 30):
            if Settings.mission_name != "Lvl 100 Shenxian":
                summon_check = Game.select_default_summon()
                if summon_check:
                    # Find and click the "OK" button to start the mission.
                    Game.find_and_click_button("ok")
                    # Now start Combat Mode and detect any item drops.
                    if CombatMode.start_combat_mode():
                        Game.collect_loot(is_completed = True)
            else:
                summon_check = Game.select_summon(Settings.summon_list, Settings.summon_element_list)
                if summon_check:
                    # Find and click the "OK" button to start the mission.
                    Game.find_party_and_start_mission(Settings.group_number, Settings.party_number)
                    # Now start Combat Mode and detect any item drops.
                    if CombatMode.start_combat_mode():
                        Game.collect_loot(is_completed = True)
        else:
            MessageLog.print_message("Failed to arrive at the Summon Selection screen.")

        return None
