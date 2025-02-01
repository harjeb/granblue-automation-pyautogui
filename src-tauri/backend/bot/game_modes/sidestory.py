'''
Author: cjju@nreal.ai
Date: 2024-12-02 18:12:38
LastEditors: cjju@nreal.ai
LastEditTime: 2024-12-02 18:43:48
Description: 

Copyright (c) 2024 by cjju@nreal.ai, All Rights Reserved. 
'''
from utils.message_log import MessageLog
from utils.settings import Settings
from utils.image_utils import ImageUtils
from utils.mouse_utils import MouseUtils
from bot.combat_mode import CombatMode
import pyautogui

class SSException(Exception):
    def __init__(self, message):
        super().__init__(message)


class SideStory:
    """
    Provides any lightweight utility functions necessary to repeat a setup that supports the "Play Again" logic.
    """

    @staticmethod
    def _navigate():
        """Starts the process of completing a generic setup that supports the 'Play Again' logic.

        Returns:
            None
        """
        from bot.game import Game
        MessageLog.print_message(f"\n[GENERIC] GO to bookmark...")
        # 按下 Alt 键
        pyautogui.keyDown('alt')
        # 按下 1 键
        pyautogui.press('8')
        # 抬起 Alt 键
        pyautogui.keyUp('alt')

        Game.wait(3.0)
        Game.find_and_click_button("treasure_trade", tries = 10)
        if ImageUtils.find_button("draw", tries = 5):
            if ImageUtils.find_button("trade", tries = 5):
                Game.find_and_click_button("trade")
                Game.find_and_click_button("trade_long")
                Game.find_and_click_button("ok")
            return True
        else:
            return False

    @staticmethod
    def finish_story():
        from bot.game import Game
        MessageLog.print_message(f"\n[GENERIC] Finish Side Story...")

        Game.find_and_click_button("skip")
        Game.find_and_click_button("skip_btn")
        Game.wait(3)
        Game.find_and_click_button("reload")

        # 点击 最上任务相对位置
        Game.wait(2)
        window_dimensions = ImageUtils.get_window_dimensions()
        while True:
            if not ImageUtils.find_button("ok"):
                Game.find_and_click_button("close")
                MouseUtils.move_and_click_point(window_dimensions[0]+186, window_dimensions[1]+512,"item1")
            if ImageUtils.find_button("attack", tries = 5):
                 # 如果选择队伍 ，则已完成剧情
                 break
            else:
                Game.find_and_click_button("ok")
                Game.wait(3)
                Game.find_and_click_button("skip")
                Game.find_and_click_button("skip_btn")
                Game.wait(4)
                while ImageUtils.find_button("ok", tries = 5):
                     Game.find_and_click_button("ok")
                while ImageUtils.find_button("dialog_point", tries = 5):
                    Game.find_and_click_button("dialog_point")
                    if ImageUtils.find_button("attack"):
                        break
                if ImageUtils.find_button("attack", tries = 10):
                    #开始战斗
                    #设置fa
                    Game.find_and_click_button("menu")
                    Game.find_and_click_button("set_full")
                    Game.find_and_click_button("set_on")
                    Game.find_and_click_button("close")
                    MessageLog.print_message(f"[GENERIC] Bot is at the Combat screen. Starting Combat Mode now...")
                    if CombatMode.start_combat_mode(is_ss=True):
                        Game.collect_loot(is_completed = True)
                        Game.find_and_click_button("reload")
                        Game.find_and_click_button("story")
                        Game.find_and_click_button("reload")
                        Game.find_and_click_button("story")



    @staticmethod
    def start():
        from bot.game import Game

        result = SideStory._navigate()

        if result:
            all_draws = ImageUtils.find_all("draw")
            print(all_draws)
            MouseUtils.move_and_click_point(all_draws[0][0]+80, all_draws[0][1]-10,"item1")

            if Game.find_and_click_button("goto_ss", tries = 5):
                Game.wait(2)
                if ImageUtils.find_button("skip", tries = 5):
                    # 处理剧情
                    SideStory.finish_story()
                else:
                    # 直接打最上副本
                    window_dimensions = ImageUtils.get_window_dimensions()
                    MouseUtils.move_and_click_point(window_dimensions[0]+186, window_dimensions[1]+512,"item1")
                    if Game.check_for_captcha():
                        return None

                    if Game.find_and_click_button("party_selection_ok", tries = 30):
                        # Now start Combat Mode and detect any item drops.
                        if CombatMode.start_combat_mode():
                            Game.collect_loot(is_completed = True)

                    Game.find_and_click_button("cancel")

                    if ImageUtils.find_button("attack", tries = 5):
                            MessageLog.print_message(f"[GENERIC] Bot is at the Combat screen. Starting Combat Mode now...")
                            if CombatMode.start_combat_mode():
                                Game.collect_loot(is_completed = True)

            return None
        else:
            return None
