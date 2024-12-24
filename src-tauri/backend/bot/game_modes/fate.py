from utils.settings import Settings
from utils.message_log import MessageLog
from utils.image_utils import ImageUtils
from utils.mouse_utils import MouseUtils
from bot.combat_mode import CombatMode


class SpecialException(Exception):
    def __init__(self, message):
        super().__init__(message)


class Fate:
    """
    Provides the navigation and any necessary utility functions to handle the Special game mode.
    """

    @staticmethod
    def _navigate():
        """Navigates to the specified Special mission.

        Returns:
            None
        """
        from bot.game import Game

        if ImageUtils.find_button("fate_episodes") == None:

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
                if not ImageUtils.find_button("skip"):
                    if CombatMode.start_combat_mode(["enablefullauto"]):
                        Game.collect_loot(is_completed = True)
                # Now start Combat Mode and detect any item drops.
                Game.find_and_click_button("skip")
                Game.find_and_click_button("skip_btn")
                Game.wait(3)
                Game.find_and_click_button("ok")

            # Check for the "You retreated from the raid battle" popup.
            Game.wait(3.0)
            if ImageUtils.confirm_location("you_retreated_from_the_raid_battle", tries = 3):
                Game.find_and_click_button("ok")

            if ImageUtils.confirm_location("quest"):
                # Scroll the screen down to make way for smaller screens.
                MouseUtils.scroll_screen_from_home_button(-1500)

                # Go to the Special screen.
                Game.find_and_click_button("fate_episode")
        else:
            Game.find_and_click_button("fate_episodes")
            Game.wait(1)
            Game.find_and_click_button("ok")

        return None

    @staticmethod
    def start(first_run: bool):
        """Starts the process to complete a run for Special Farming Mode and returns the number of items detected.

        Args:
            first_run (bool): Flag that determines whether or not to run the navigation process again. Should be False if the Farming Mode supports the "Play Again" feature for repeated runs.

        Returns:
            None
        """
        from bot.game import Game

        # Start the navigation process.
        if first_run:
            Fate._navigate()
        elif Game.find_and_click_button("play_again"):
            if Game.check_for_popups():
                Fate._navigate()
        else:
            # If the bot cannot find the "Play Again" button, check for Pending Battles and then perform navigation again.
            Game.check_for_pending()
            Fate._navigate()

        # Check for AP.
        #Game.check_for_ap()

        # Check if the bot is at the Summon Selection screen.
        if ImageUtils.find_button("bjs", tries = 10):
            Game.find_and_click_button("bjs")
            Game.wait(2)
            if ImageUtils.find_button("spoil_me", tries = 10):
                Game.find_and_click_button("spoil_me")
                Game.find_and_click_button("play")
                Game.wait(2)
            Game.find_and_click_button("skip")
            Game.find_and_click_button("skip_btn")
            Game.wait(3)
            Game.find_and_click_button("ok")
            Settings.amount_of_runs_finished += 1
            Settings.item_amount_farmed += 1
        else:
            print("Failed to arrive at the Summon Selection screen.")

        return None
