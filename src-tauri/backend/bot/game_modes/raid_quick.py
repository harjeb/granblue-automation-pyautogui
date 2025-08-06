from utils.settings import Settings
from utils.message_log import MessageLog
from utils.image_utils import ImageUtils
from utils.mouse_utils import MouseUtils
from bot.combat_mode import CombatMode
import re
import pyautogui

class RaidException(Exception):
    def __init__(self, message):
        super().__init__(message)


class Raid:
    """
    Provides the navigation and any necessary utility functions to handle the Raid game mode.
    """

    _raids_joined = 0


    @staticmethod
    def go_to_finder():
        from bot.game import Game
        # press alt + 1
        pyautogui.keyDown('alt')
        pyautogui.press('1')
        pyautogui.keyUp('alt')

            
        
    @staticmethod
    def go_to_pending():
        # press alt + 2
        pyautogui.keyDown('alt')
        pyautogui.press('2')
        pyautogui.keyUp('alt')

    @staticmethod
    def _check_for_joined_raids():
        """Check and update the number of raids currently joined.

        Returns:
            None
        """
        # Find out the number of currently joined raids.
        joined_locations = ImageUtils.find_all("joined")

        if joined_locations is not None:
            Raid._raids_joined = len(joined_locations)
            MessageLog.print_message(f"\n[RAID] There are currently {Raid._raids_joined} raids joined.")

        return None

    @staticmethod
    def _clear_joined_raids():
        """Begin process to wait out the joined raids if there are 3 or more currently active.

        Returns:
            None
        """
        from bot.game import Game

        # If the maximum number of raids has been joined, collect any pending rewards with a interval of 30 seconds in between until the number of joined raids is below 3.
        while Raid._raids_joined >= 3:
            MessageLog.print_message(f"\n[RAID] Maximum raids of 3 has been joined. Waiting 30 seconds to see if any finish.")
            Game.wait(30)

            Game.go_back_home(confirm_location_check = True)
            Game.find_and_click_button("quest")

            if Game.check_for_pending():
                Game.find_and_click_button("quest")
                Game.wait(3.0)

            Game.find_and_click_button("raid")
            Game.wait(3.0)
            Game.find_and_click_button("recent")
            Raid._check_for_joined_raids()

        return None

    @staticmethod
    def _join_raid() -> bool:
        """Start the process to fetch a valid room code and join it.

        Returns:
            (bool): True if the bot arrived at the Summon Selection screen.
        """
        from bot.game import Game

        recovery_time = 15

        Game.wait(2.0)
        # Now click on the first Room.
        room_locations = ImageUtils.find_all("pending_battle_sidebar")
        c = 0
        while len(room_locations) == 0:
            c += 1
            MouseUtils.scroll_screen_from_home_button(-500)
            Game.wait(1.0)
            room_locations = ImageUtils.find_all("pending_battle_sidebar")
            if len(room_locations) == 0:
                MouseUtils.scroll_screen_from_home_button(500)
                Game.wait(2.0)
                Game.find_and_click_button("reload_room")
                Game.wait(2.0)
                room_locations = ImageUtils.find_all("pending_battle_sidebar")
            if c > 5:
                break
        
        Game.wait(1.0)

        MouseUtils.move_and_click_point(room_locations[0][0], room_locations[0][1], "pending_battle_sidebar")
        Game.wait(2.0)

        # If the room code is valid and the raid is able to be joined, break out and head to the Summon Selection screen.
        if Game.find_and_click_button("ok", suppress_error = True) is False:
            return ImageUtils.confirm_location("select_a_summon", tries = 30)
        elif Game.check_for_pending() is False:
            MessageLog.print_message(f"[WARNING] already ended or invalid.")
        else:
            # Move from the Home screen back to the Backup Requests screen after clearing out all the Pending Battles.
            Game.find_and_click_button("quest")
            Game.find_and_click_button("raid")
            #Game.find_and_click_button("finder")

        Game.wait(recovery_time)

    @staticmethod
    def find_the_best() -> int:
        "find the best room"
        roomid = 1
        logpath = "C:\\Users\\harjeb\\AppData\\Local\\Google\\Chrome\\User Data\\chrome_debug.log"
        # read logpath
        with open(logpath, "r") as f:
            lines = f.readlines()
            # find last line contains CONSOLE(56)
            for line in reversed(lines):
                if "CONSOLE(56)" in line:
                    break
            print(line)
            str = re.findall(r'CONSOLE\(56\)\] "(.*) ', line)
            print(str)
            roomid = int(str[0])
            return roomid
            

    @staticmethod
    def _navigate():
        """Navigates to the specified Raid.

        Returns:
            None
        """
        from bot.game import Game

        MessageLog.print_message(f"\n[RAID] Beginning process to navigate to the raid: {Settings.mission_name}...")

        # Head to the Home screen.
        #Game.go_back_home(confirm_location_check = True)

        # Then navigate to the Quest screen.
        #Game.find_and_click_button("quest")

        #Game.wait(3.0)

        # Check for the "You retreated from the raid battle" popup.
        #if ImageUtils.confirm_location("you_retreated_from_the_raid_battle", tries = 3):
        #    Game.find_and_click_button("ok")

        # Check for any Pending Battles popup.
        #if Game.check_for_pending():
        #    Game.find_and_click_button("quest")

        #Game.wait(3.0)
        # Now navigate to the Raid screen.
        #Game.find_and_click_button("raid")
        Game.find_and_click_button("home")
        MessageLog.print_message(f"\n[RAID] Now moving to the \"home\" screen.")
        #Raid._clear_joined_raids()
        Raid.go_to_finder()
        # Click on the "Enter ID" button and then start the process to join a raid.

        MessageLog.print_message(f"\n[RAID] Now moving to the \"Finder\" screen.")
        Raid._join_raid()


    @staticmethod
    def start(first_run: bool):
        """Starts the process to complete a run for Raid Farming Mode and returns the number of items detected.

        Args:
            first_run (bool): Flag that determines whether or not to run the navigation process again. Should be False if the Farming Mode supports the "Play Again" feature for repeated runs.

        Returns:
            None
        """
        from bot.game import Game

        # Start the navigation process.
        if first_run:
            Raid._navigate()
        else:
            # Check for Pending Battles and then perform navigation again.
            Game.check_for_pending()
            Raid._navigate()
        # No Check.
        # Game.check_for_ep()

        # Check if the bot is at the Summon Selection screen.
        if ImageUtils.confirm_location("select_a_summon", tries = 30):
            if Settings.summon_default:
                summon_check = Game.select_default_summon()
            else:
                summon_check = Game.select_summon(Settings.summon_list, Settings.summon_element_list)
            if summon_check:
                if Game.check_for_captcha():
                    Game.select_default_summon()
                # Select the Party.
                if Game.quick_start_mission():
                    Settings.item_amount_farmed += 1
                    # Handle the rare case where joining the Raid after selecting the Summon and Party led the bot to the Quest Results screen with no loot to collect.
                    if ImageUtils.confirm_location("no_loot", disable_adjustment = True):
                        MessageLog.print_message("\n[RAID] Seems that the Raid just ended. Moving back to the Home screen and joining another Raid...")
                    elif CombatMode.start_combat_mode():
                        Game.collect_loot(is_completed = True, direct_battle=True)
                        # go back to the Home screen.
                        #Game.find_and_click_button("home")
                        # Close the Skyscope mission popup.
                        #Game.check_for_skyscope()
                else:
                    MessageLog.print_message("\n[RAID] Seems that the Raid ended before the bot was able to join. Now looking for another Raid to join...")
        else:
            # DO NOT EXIT
            MessageLog.print_message("\n[ERROR] Failed to arrive at the Summon Selection screen.")

        return None
