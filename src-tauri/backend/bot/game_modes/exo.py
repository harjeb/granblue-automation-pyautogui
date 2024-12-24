from utils.settings import Settings
from utils.message_log import MessageLog
from utils.image_utils import ImageUtils
from utils.mouse_utils import MouseUtils
from bot.combat_mode import CombatMode


class EventException(Exception):
    def __init__(self, message):
        super().__init__(message)


class Exo:
    """
    Provides the navigation and any necessary utility functions to handle the Event or Event (Token Drawboxes) game mode.
    """

    @staticmethod
    def _navigate():
        """Navigates to the specified Event mission.

        Returns:
            None
        """
        from bot.game import Game

        # Switch over to the navigation logic for Event (Token Drawboxes) if needed.
        if True:
            MessageLog.print_message(f"[EVENT] Now beginning process to navigate to the mission: {Settings.mission_name}...")

            # Go to the Home screen.
            Game.go_back_home(confirm_location_check = True)

            # Go to the Event by clicking on the "Menu" button and then click the very first banner.
            Game.find_and_click_button("home_menu")
            Game.wait(1.0)
            banner_locations = ImageUtils.find_all("event_banner", custom_confidence = 0.7)
            if len(banner_locations) == 0:
                banner_locations = ImageUtils.find_all("event_banner_blue", custom_confidence = 0.7)
                if len(banner_locations) == 0:
                    Game.go_back_home()
                    MessageLog.print_message("\n[ERROR]Failed to find the Event banner.Go back Home...")
                    return None
                    #raise EventException("Failed to find the Event banner.")

            if Settings.first_event:
                MouseUtils.move_and_click_point(banner_locations[0][0], banner_locations[0][1], "event_banner")
            else:
                MouseUtils.move_and_click_point(banner_locations[1][0], banner_locations[1][1], "event_banner")
            Game.wait(3.0)

            # Remove the difficulty prefix from the mission name.
            difficulty = ""
            if Settings.mission_name.find("Solo") == 0:
                difficulty = "Solo"
            elif Settings.mission_name.find("Ex") == 0:
                difficulty = "Extreme"


            if ImageUtils.confirm_location("event_battles"):
                Game.wait(1)
                # Find all the round "Play" buttons.
                round_play_button_locations = ImageUtils.find_all("solo_battle")


                # Now select the chosen difficulty.
                try:
                    if difficulty == "Solo":
                        MouseUtils.move_and_click_point(round_play_button_locations[0][0], round_play_button_locations[0][1], "solo_battle")
                        Game.find_and_click_button("play")
                    elif difficulty == "Extreme":
                        MouseUtils.move_and_click_point(round_play_button_locations[1][0], round_play_button_locations[1][1], "solo_battle")
                        round_play_button_locations2 = ImageUtils.find_all("play_round_button")
                        MouseUtils.move_and_click_point(round_play_button_locations2[1][0], round_play_button_locations2[1][1], "play_round_button")
                except:
                    if len(round_play_button_locations) >= 1:
                        # 没有找到多个开始按钮，应该是前面步骤没点好，打开默认第一个
                        MessageLog.print_message("Select first one instead of interrupt")
                        MouseUtils.move_and_click_point(round_play_button_locations[0][0], round_play_button_locations[0][1], "solo_battle")
                    else:
                        raise EventException("Failed to arrive at the Special Quest screen.")

            else:
                # 可能在resume game界面，需要重新进战斗
                if ImageUtils.confirm_location("resume_quests"):
                    MessageLog.print_message(f"RELOAD combat")
                else:
                    MessageLog.print_message(f"NOT FOUND RELOAD BTN,TRY RELOAD")
                    Game.find_and_click_button("reload")
                    #raise EventException("Failed to arrive at the Special Quest screen.")

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
            Exo._navigate()
        elif Settings.mission_name.find("Solo Next") == 0:
            if Game.find_and_click_button("next_level"):
                Game.find_and_click_button("ok")
                if not Game.find_and_click_button("play_next"):
                    Game.find_and_click_button("close")
                else:
                    Game.find_and_click_button("play_next")
                if Game.check_for_popups():
                    Exo._navigate()
        elif Game.find_and_click_button("play_again"):
            if Game.check_for_popups():
                Exo._navigate()
        else:
            # If the bot cannot find the "Play Again" button, check for Pending Battles and then perform navigation again.
            Game.check_for_pending()
            Exo._navigate()

        # Check for AP.
        #Game.check_for_ap()

        # Check for resume.
        if ImageUtils.confirm_location("resume_quests", tries = 5):
            Game.find_and_click_button("resume")
            Game.wait(5)
            # Now start Combat Mode and detect any item drops.
            if CombatMode.start_combat_mode(["enablefullauto"]):
                Game.collect_loot(is_completed = True)

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

        return None
