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
from bot.combat_mode import CombatMode
import pyautogui

class GenericException(Exception):
    def __init__(self, message):
        super().__init__(message)


class Generic:
    """
    Provides any lightweight utility functions necessary to repeat a setup that supports the "Play Again" logic.
    """

    @staticmethod
    def start():
        """Starts the process of completing a generic setup that supports the 'Play Again' logic.

        Returns:
            None
        """
        from bot.game import Game
    
        MessageLog.print_message(f"\n[GENERIC] GO to bookmark...")
        
        # 按下 Alt 键
        pyautogui.keyDown('alt')
        # 按下 1 键
        pyautogui.press('1')
        # 抬起 Alt 键
        pyautogui.keyUp('alt')

        if Game.find_and_click_button("ok", tries = 30):
            # Now start Combat Mode and detect any item drops.
            if CombatMode.start_combat_mode():
                Game.collect_loot(is_completed = True)

        if ImageUtils.find_button("attack", tries = 5):
            MessageLog.print_message(f"[GENERIC] Bot is at the Combat screen. Starting Combat Mode now...")
            if CombatMode.start_combat_mode():
                Game.collect_loot(is_completed = True)

        return None
