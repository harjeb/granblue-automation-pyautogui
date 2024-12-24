from utils.settings import Settings
from utils.message_log import MessageLog
from utils.image_utils import ImageUtils
from utils.mouse_utils import MouseUtils
from bot.combat_mode import CombatMode


class ProvingGroundsException(Exception):
    def __init__(self, message):
        super().__init__(message)


class ProvingGrounds:
    """
    Provides the navigation and any necessary utility functions to handle the Proving Grounds game mode.
    """

    _first_time = True

    @staticmethod
    def _navigate():
        """Navigates to the specified Proving Grounds mission.

        Returns:
            None
        """
        from bot.game import Game

        # Go to the Home screen.
        Game.go_back_home(confirm_location_check = True)

        MessageLog.print_message(f"\n[PROVING.GROUNDS] Now navigating to Proving Grounds...")

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

        difficulty = ""
        if Settings.mission_name == "Extreme":
            difficulty = "Extreme"
        elif Settings.mission_name == "Extreme+":
            difficulty = "Extreme+"

        # Select the difficulty.
        if ImageUtils.confirm_location("proving_grounds"):
            if Game.find_and_click_button("proving_grounds_missions"):
                difficulty_button_locations = ImageUtils.find_all("play_round_button")

                if difficulty == "Extreme":
                    MouseUtils.move_and_click_point(difficulty_button_locations[1][0], difficulty_button_locations[1][1], "play_round_button")
                elif difficulty == "Extreme+":
                    MouseUtils.move_and_click_point(difficulty_button_locations[2][0], difficulty_button_locations[2][1], "play_round_button")

                # After the difficulty has been selected, click "Play" to land the bot at the Proving Grounds' Summon Selection screen.
                #Game.find_and_click_button("play")
        else:
            MessageLog.print_message("Failed to arrive at the main screen for Proving Grounds.")

        return None

    @staticmethod
    def start(first_run: bool):
        """Starts the process to complete a run for Proving Grounds Farming Mode and returns the number of items detected.

        Args:
            first_run (bool): Flag that determines whether or not to run the navigation process again. Should be False if the Farming Mode supports the "Play Again" feature for repeated runs.

        Returns:
            None
        """
        from bot.game import Game

        # Start the navigation process.
        if first_run and ProvingGrounds._first_time:
            ProvingGrounds._navigate()
        elif ProvingGrounds._first_time and Game.find_and_click_button("play_again"):
            MessageLog.print_message("\n[PROVING.GROUNDS] Starting Proving Grounds Mission again...")
        else:
            # Go to the Home screen.
            Game.go_back_home(confirm_location_check = True)            
            ProvingGrounds._navigate()
            ProvingGrounds._first_time = False
        # Check for AP.
        #Game.check_for_ap()
        Game.wait(2.0)
        Game.find_and_click_button("proving_grounds_open_chest")
        Game.find_and_click_button("play_again")
        Game.find_and_click_button("close")
        # Check for resume.
        if ImageUtils.find_button("attack", tries = 5) is not None:
            # Now start Combat Mode and detect any item drops.
            if CombatMode.start_combat_mode(["enablefullauto"]):
                Game.collect_loot(is_completed = True)

        # Check if the bot is at the Summon Selection screen.
        if ImageUtils.confirm_location("proving_grounds_summon_selection", tries = 30):
            summon_check = Game.select_summon(Settings.summon_list, Settings.summon_element_list)
            if summon_check:
                Game.wait(2.0)

                # No need to select a Party. Just click "OK" to start the mission and confirming the selected summon.
                Game.find_and_click_button("ok")

                Game.wait(2.0)

                MessageLog.print_message("\n[PROVING.GROUNDS] Now starting Mission for Proving Grounds...")
                Game.find_and_click_button("proving_grounds_start")

                # Now start Combat Mode and detect any item drops.
                if CombatMode.start_combat_mode():
                    Game.collect_loot(is_completed = False)

                    # Click the "Next Battle" button if there are any battles left.
                    if Game.find_and_click_button("proving_grounds_next_battle"):
                        MessageLog.print_message("\n[PROVING.GROUNDS] Moving onto the next battle for Proving Grounds...")
                        Game.find_and_click_button("ok")
                        ProvingGrounds._first_time = False
                        Game.wait(3)
        if ProvingGrounds._first_time is False:
            if ImageUtils.find_button("proving_grounds_start") is None and ImageUtils.find_button("attack", tries = 10) is None:
                return None
            Game.find_and_click_button("proving_grounds_start")
            # No need to select a Summon again as it is reused.
            if CombatMode.start_combat_mode():
                Game.collect_loot(is_completed = False)

                # Click the "Next Battle" button if there are any battles left.
                if Game.find_and_click_button("proving_grounds_next_battle"):
                    MessageLog.print_message("\n[PROVING.GROUNDS] Moving onto the next battle for Proving Grounds...")
                    Game.find_and_click_button("ok")
                else:
                    # Otherwise, all battles for the Mission has been completed. Collect the completion rewards at the end.
                    MessageLog.print_message("\n[PROVING.GROUNDS] Proving Grounds Mission has been completed.")
                    Game.find_and_click_button("event")

                    # Check for friend request.
                    Game.check_for_friend_request()

                    # Check for trophy.
                    Game.find_and_click_button("close", suppress_error = True)

                    Game.wait(2.0)
                    Game.find_and_click_button("proving_grounds_open_chest")
                    Game.wait(2.0)
                    if ImageUtils.confirm_location("proving_grounds_completion_loot"):
                        MessageLog.print_message("\n[PROVING.GROUNDS] Completion rewards has been acquired.")
                        Game.collect_loot(is_completed = True, skip_popup_check = True)

                        # Reset the First Time flag so the bot can select a Summon and select the Mission again.
                        if Settings.item_amount_farmed < Settings.item_amount_to_farm:
                            ProvingGrounds._first_time = True
                    else:
                        MessageLog.print_message("Failed to detect the Completion Loot screen for completing this Proving Grounds mission.")
        else:
            MessageLog.print_message("Failed to arrive at the Summon Selection screen.")

        return None
