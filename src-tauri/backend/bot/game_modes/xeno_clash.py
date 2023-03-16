from utils.settings import Settings
from utils.message_log import MessageLog
from utils.image_utils import ImageUtils
from utils.mouse_utils import MouseUtils
from bot.combat_mode import CombatMode


class XenoClashException(Exception):
    def __init__(self, message):
        super().__init__(message)


class XenoClash:
    """
    Provides the navigation and any necessary utility functions to handle the Xeno Clash game mode.

    Attributes
    ----------
    game_object (bot.Game): The Game object.

    mission_name (str): The name of the Xeno Clash mission.

    """

    @staticmethod
    def _navigate():
        """Navigates to the specified Xeno Clash mission.

        Returns:
            None
        """
        from bot.game import Game
        formatted_mission_name = Settings.mission_name
        MessageLog.print_message(f"\n[SPECIAL] Beginning process to navigate to the mission: {Settings.mission_name}...")

        # Go to the Home screen.
        Game.go_back_home(confirm_location_check = True)

        # Go to the Quest screen.
        Game.find_and_click_button("quest", suppress_error = True)

        Game.wait(1)

        # Check for resume.
        if ImageUtils.confirm_location("resume_quests", tries = 5):
            Game.find_and_click_button("resume")
            Game.wait(5)
            # Now start Combat Mode and detect any item drops.
            if CombatMode.start_combat_mode(["enablefullauto"]):
                Game.collect_loot(is_completed = True)

        # Check for the "You retreated from the raid battle" popup.
        Game.wait(3.0)
        if ImageUtils.confirm_location("you_retreated_from_the_raid_battle", tries = 3):
            Game.find_and_click_button("ok")

        if ImageUtils.confirm_location("quest"):
            # Go to the Special screen.
            Game.find_and_click_button("special")

        if ImageUtils.confirm_location("special"):
            tries = 2
            # Try to select the specified Special mission for a number of tries.
            while tries != 0:
                MouseUtils.scroll_screen_from_home_button(-500)
                Game.wait(3)

                mission_select_button = ImageUtils.find_button("showdowns")
                if mission_select_button is not None:
                    MessageLog.print_message(f"[SPECIAL] Navigating to {Settings.map_name}...")

                    # Move to the specified Special by clicking its "Select" button.
                    special_quest_select_button = (mission_select_button[0] + 145, mission_select_button[1] + 75)
                    MouseUtils.move_and_click_point(special_quest_select_button[0], special_quest_select_button[1], "select")

                    Game.wait(1)

                    # click clashes
                    Game.find_and_click_button("clashes")
                    Game.wait(2)
                    locations = ImageUtils.find_all("play_round_button")
                    if formatted_mission_name == "火六道 Extreme":
                        # Navigate to Ifrit Showdown.
                        MessageLog.print_message(f"[SPECIAL] Selecting 火六道 Extreme...")
                        MouseUtils.move_and_click_point(locations[0][0], locations[0][1], "play_round_button")
                    elif formatted_mission_name == "水六道 Extreme":
                        # Navigate to Cocytus Showdown.
                        MessageLog.print_message(f"[SPECIAL] Selecting 水六道 Extreme...")
                        MouseUtils.move_and_click_point(locations[1][0], locations[1][1], "play_round_button")
                    elif formatted_mission_name == "土六道 Extreme":
                        # Navigate to Vohu Manah Showdown.
                        MessageLog.print_message(f"[SPECIAL] Selecting 土六道 Extreme...")
                        MouseUtils.move_and_click_point(locations[2][0], locations[2][1], "play_round_button")
                    elif formatted_mission_name == "风六道 Extreme":
                        # Navigate to Sagittarius Showdown.
                        MessageLog.print_message(f"[SPECIAL] Selecting 风六道 Extreme...")
                        MouseUtils.move_and_click_point(locations[3][0], locations[3][1], "play_round_button")
                    elif formatted_mission_name == "光六道 Extreme":
                        # Navigate to Corow Showdown.
                        MessageLog.print_message(f"[SPECIAL] Selecting 光六道 Extreme...")
                        MouseUtils.move_and_click_point(locations[4][0], locations[4][1], "play_round_button")
                    elif formatted_mission_name == "暗六道 Extreme":
                        # Navigate to Diablo Showdown.
                        MessageLog.print_message(f"[SPECIAL] Selecting 暗六道 Extreme...")
                        MouseUtils.move_and_click_point(locations[5][0], locations[5][1], "play_round_button")

                    # Now start the clash with the specified difficulty.
                    Game.wait(1)
                    MessageLog.print_message(f"[SPECIAL] Now navigating to ex...")
                    locations = ImageUtils.find_all("play_round_button")

                    MouseUtils.move_and_click_point(locations[0][0], locations[0][1], "play_round_button")
                break

        return None

    @staticmethod
    def start(first_run: bool):
        """Starts the process to complete a run for Xeno Clash Farming Mode and returns the number of items detected.

        Args:
            first_run (bool): Flag that determines whether or not to run the navigation process again. Should be False if the Farming Mode supports the "Play Again" feature for repeated runs.

        Returns:
            None
        """
        from bot.game import Game

        # Start the navigation process.
        if first_run:
            XenoClash._navigate()
        elif Game.find_and_click_button("play_again"):
            if Game.check_for_popups():
                XenoClash._navigate()
        else:
            # If the bot cannot find the "Play Again" button, check for Pending Battles and then perform navigation again.
            Game.check_for_pending()
            XenoClash._navigate()

        # Check for AP.
        #Game.check_for_ap()

        # Check if the bot is at the Summon Selection screen.
        if ImageUtils.confirm_location("select_a_summon", tries = 30):
            summon_check = Game.select_summon(Settings.summon_list, Settings.summon_element_list)
            if summon_check:
                # Select the Party.
                Game.find_party_and_start_mission(Settings.group_number, Settings.party_number)

                # Now start Combat Mode and detect any item drops.
                if CombatMode.start_combat_mode():
                    Game.collect_loot(is_completed = True)
        else:
            raise XenoClashException("Failed to arrive at the Summon Selection screen.")

        return None
