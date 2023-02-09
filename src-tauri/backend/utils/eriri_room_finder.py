import json
import re
from typing import Union

import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

from utils.message_log import MessageLog
from utils.settings import Settings


class EririRoomFinder:
    """
    Provides the functions needed to perform Twitter API-related tasks such as searching tweets for room codes for raid farming.
    """

    _already_visited_codes = []

    _list_of_raids = {
        # Omega Raids
        "Lvl 50 Tiamat Omega": "1",
        "Lvl 100 Tiamat Omega Ayr": "13",
        "Lvl 70 Colossus Omega": "3",
        "Lvl 100 Colossus Omega": "14",
        "Lvl 60 Leviathan Omega": "5",
        "Lvl 100 Leviathan Omega": "15",
        "Lvl 60 Yggdrasil Omega": "7",
        "Lvl 100 Yggdrasil Omega": "16",
        "Lvl 75 Luminiera Omega": "9",
        "Lvl 100 Luminiera Omega": "17",
        "Lvl 75 Celeste Omega": "11",
        "Lvl 100 Celeste Omega": "18",

        # Tier 1 Summon Raids
        "Lvl 100 Twin Elements": "20",
        "Lvl 120 Twin Elements": "26",
        "Lvl 100 Macula Marius": "21",
        "Lvl 120 Macula Marius": "27",
        "Lvl 100 Medusa": "22",
        "Lvl 120 Medusa": "28",
        "Lvl 100 Nezha": "19",
        "Lvl 120 Nezha": "25",
        "Lvl 100 Apollo": "23",
        "Lvl 120 Apollo": "29",
        "Lvl 100 Dark Angel Olivia": "24",
        "Lvl 120 Dark Angel Olivia": "30",

        # Tier 2 Summon Raids
        "Lvl 100 Athena": "32",
        "Lvl 100 Grani": "33",
        "Lvl 100 Baal": "34",
        "Lvl 100 Garuda": "31",
        "Lvl 100 Odin": "35",
        "Lvl 100 Lich": "36",

        # Primarch Raids
        "Lvl 100 Michael": "44",
        "Lvl 100 Gabriel": "45",
        "Lvl 100 Uriel": "46",
        "Lvl 100 Raphael": "43",
        "The Four Primarchs": "47",

        # Nightmare Raids
        "Lvl 100 Proto Bahamut": "54",
        "Lvl 100 Grand Order": "57",

        # Rise of the Beasts Raids
        "Lvl 60 Zhuque": "77",
        "Lvl 90 Agni": "81",
        "Lvl 60 Xuanwu": "78",
        "Lvl 90 Neptune": "82",
        "Lvl 60 Baihu": "79",
        "Lvl 90 Titan": "83",
        "Lvl 60 Qinglong": "76",
        "Lvl 90 Zephyrus": "80",
        "Lvl 100 Huanglong": "60",
        "Lvl 100 Qilin": "61",
        "Huanglong & Qilin (Impossible)": "62",
        "Lvl 100 Shenxian": "75",

        # Impossible Raids
        "Lvl 110 Rose Queen": "59",
        "Lvl 120 Shiva": "49",
        "Lvl 120 Europa": "50",
        "Lvl 120 Godsworn Alexiel": "51",
        "Lvl 120 Grimnir": "48",
        "Lvl 120 Metatron": "52",
        "Lvl 120 Avatar": "53",
        "Lvl 120 Prometheus": "38",
        "Lvl 120 Ca Ong": "39",
        "Lvl 120 Gilgamesh": "40",
        "Lvl 120 Morrigna": "37",
        "Lvl 120 Hector": "41",
        "Lvl 120 Anubis": "42",
        "Lvl 150 Proto Bahamut": "55",
        "Lvl 150 Ultimate Bahamut": "56",
        "Lvl 200 Ultimate Bahamut": "105",
        "Lvl 200 Grand Order": "58",
        "Lvl 200 Akasha": "66",
        "Lvl 150 Lucilius": "67",
        "Lvl 250 Lucilius": "107",
        "Lvl 250 Beelzebub": "108",
        "Lvl 250 Belial": "109",
        "Lvl 300 Super Ultimate Bahamut": "117",
        "Lvl 200 Lindwurm": "68",
        "Lvl 275 Diaspora": "122",
        "Lvl 275 Mugen": "125",

        # Malice Raids
        "Lvl 150 Tiamat Malice": "63",
        "Lvl 150 Leviathan Malice": "64",
        "Lvl 150 Phronesis": "65",
        "Lvl 150 Luminiera Malice": "106",
        "Lvl 150 Anima-Animus Core": "113",

        # Six Dragon Raids
        "Lvl 200 Wilnas": "70",
        "Lvl 200 Wamdus": "71",
        "Lvl 200 Galleon": "72",
        "Lvl 200 Ewiyar": "69",
        "Lvl 200 Lu Woh": "73",
        "Lvl 200 Fediel": "74",

        # Xeno Clash Raids
        "Lvl 100 Xeno Ifrit": "85",
        "Lvl 100 Xeno Cocytus": "86",
        "Lvl 100 Xeno Vohu Manah": "87",
        "Lvl 100 Xeno Sagittarius": "84",
        "Lvl 100 Xeno Corow": "88",
        "Lvl 100 Xeno Diablo": "89",

        # Ennead Raids
        "Lvl 120 Osiris": "118",
        "Lvl 120 Horus": "119",
        "Lvl 120 Bennu": "120",
        "Lvl 120 Atum": "121",
        "Lvl 120 Tefnut": "123",
        "Lvl 120 Ra": "124",
    }

    _list_of_id = []


    @staticmethod
    def get_room_code() -> str:
        """get a valid room code from gbs.errir.net

        Returns:
            (str): A single room code that has not been visited.
        """
        # TODO 增加多选功能
        boss_list = [Settings.mission_name]
        for i in boss_list:
            if i in EririRoomFinder._list_of_raids.keys():
                EririRoomFinder._list_of_id.append(EririRoomFinder._list_of_raids[i])
        while True:
            if len(EririRoomFinder._list_of_id) >= 1:
                boss_id_list = ",".join(EririRoomFinder._list_of_id)
                data = {"q":boss_id_list}
                api_url = "https://gbs.eriri.net/hold/"
                try:
                    s = requests.Session()
                    s.mount('https://', HTTPAdapter(max_retries=Retry(total=5)))
                    resp_get = s.get(url=api_url, params=data)
                    #r = requests.get(api_url, params=data)
                    result = resp_get.json()
                except:
                    result = {}

                if len(result.keys()) >= 1:
                    _id_list = []
                    _time_list = []
                    for v in result.values():
                        lastone = v[-1]
                        _id = lastone['id']
                        _time = lastone['t']
                        _id_list.append(_id)
                        _time_list.append(_time)

                    latest = _id_list[_time_list.index(max(_time_list))]
                    if latest not in EririRoomFinder._already_visited_codes:
                        EririRoomFinder._already_visited_codes.append(latest)
                        MessageLog.print_message(latest)
                        return latest
                    else:
                        MessageLog.print_message("[WARNING] RAID HAS JOINED.")
                else:
                    MessageLog.print_message("[WARNING] request error pops.")
            else:
                MessageLog.print_message("[WARNING] return empty.")
                return ''
