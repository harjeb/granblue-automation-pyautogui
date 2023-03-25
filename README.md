# Granblue Automation using Template Matching (It is like Full Auto, but with Full Customization!)

![GitHub commit activity](https://img.shields.io/github/commit-activity/m/steve1316/granblue-automation-pyautogui?logo=GitHub) ![GitHub last commit](https://img.shields.io/github/last-commit/steve1316/granblue-automation-pyautogui?logo=GitHub) ![GitHub issues](https://img.shields.io/github/issues/steve1316/granblue-automation-pyautogui?logo=GitHub) ![GitHub pull requests](https://img.shields.io/github/issues-pr/steve1316/granblue-automation-pyautogui?logo=GitHub) ![GitHub](https://img.shields.io/github/license/steve1316/granblue-automation-pyautogui?logo=GitHub)

> Discord here: https://discord.gg/5Yv4kqjAbm

> Android version here: https://github.com/steve1316/granblue-automation-android

> Checkout [Granblue Automation Statistics](https://granblue-automation-statistics.com/) and its project over at https://github.com/steve1316/granblue-automation-statistics

https://user-images.githubusercontent.com/18709555/143183561-f6296c1b-350b-4a34-b262-294be3888fae.mp4

This Python application is designed for educational research purposes on studying how to automate certain workflows via image template matching using OpenCV. The application uses PyAutoGUI for direct mouse control, hence why it is recommended to run this on a separate machine than the one that you use daily. This can be circumvented by running this on a virtual machine like VMWare Workstation Player so you can keep using your main computer without interruption.

Screenshots are taken and cropped by PyAutoGUI for OpenCV to perform image template matching. This will determine where the bot is currently at and will inform the bot on what to do next from there.

There is a feature already in-game that can automate gameplay called "Semi/Full Auto" but does not offer any way to customize what each character does on a turn-by-turn basis. This program's primary goal is to provide that customization. Users can create their own combat scripts using predefined case-insensitive keywords and can indicate which turns the bot will execute their script, somewhat akin to constructing pseudocode.

For example:

```
// This is a comment. The bot will ignore this line.
# This is also a comment.

Turn 1:
    // On Turn 1, the following commands will be executed in order:
    // 6th Summon is invoked, character 1 uses Skill 2 and then Skill 4,
    // and finally character 3 uses Skill 3.
    summon(6)
    character1.useSkill(2).useSkill(4)
    character3.useSkill(3)
end

# The bot will keep clicking the Attack button until it reaches the 5th turn.
Turn 5:
    character2.useSkill(2)
end

// Use the exit keyword to leave the raid without retreating.
// Useful when you want to farm multiple raids at once.
exit

```

## ！！！本项目仅供学习使用！！！

## 汉化后的qt界面
![Gbf Automation ExReborn](https://github.com/harjeb/granblue-automation-pyautogui/blob/custom_dev/qt_gui/image/gbf_auto.png)

## Changelog
2023/3/16 Beta v2.5更新：更新新六道Farm流程，优化FA时刷新，修复其他小问题

2023/2/9 Beta v2.4更新：修复勇气之地Farm流程问题，修复大公多人战找房问题，修复其他小问题

2023/1/14 Beta v1.7更新：古战场模式已经能稳定15小时运行无中断了，新增修改后的pyclick,需要安装完环境后手动安装。把原来的鼠标轨迹点减少至1/3，鼠标拟人移动时间最高降低了750%左右

2023/1/4 Beta v1.0更新:完成新GUI的基本功能，增加队列执行，替换twitter api的舔表功能，不再需要开发者权限才能舔，discord统计功能和部分设置暂时移除

## Custom Ver Goal
- 原作者的tauri桌面程序会出现日志显示不同步，无法显示中文和无法正常停止等问题，改用pyqt重新编写
- 用舔表网API替代twitter API降低工具使用难度
- 优化部分代码逻辑，增加执行效率
- 增加等待功能
- 增加验证码码识别
- 增加队列执行功能，可以多选任务按顺序执行
- 增加日课任务等


## TODO
- [x] 功能汉化
- [x] 新qt界面
- [x] raid功能优化
- [x] 修复游戏更新导致的阻塞问题等
- [x] 沙盒设置
- [x] 增加验证码识别功能

## Disclaimer

By downloading this program, you consent to your account potentially getting flagged for excessive amounts of farming for multiple hours straight and banned in the next banwave by KMR. I hold no responsibility for how much or how long you use this program for. I trust you have the self-control necessary to only farm in reasonable bursts of time with breaks in between and to always be alert for when the bot encounters the CAPTCHA.

# Table of Contents

-   [Features](#features)
-   [Wiki](#wiki)
-   [Requirements](#requirements)
    -   [Python Dependencies (make sure to have these installed before moving on to the instructions)](#python-dependencies-make-sure-to-have-these-installed-before-moving-on-to-the-instructions)
-   [Instructions](#instructions)
    -   [Instructions to set up Discord integration](#instructions-to-set-up-discord-integration)
    -   [How to create my own Combat Script?](#how-to-create-my-own-combat-script)
    -   [What Missions/Items/Summons are supported?](#what-missionsitemssummons-are-supported)
    -   [Instructions for farming Raids (optional, only if you want to farm Raids)](#instructions-for-farming-raids-optional-only-if-you-want-to-farm-raids)
    -   [Virtual Machine Setup (optional)](#virtual-machine-setup-optional)
-   [Build Instructions](#build-instructions)
-   [Technologies Used](#technologies-used)

# Features

-   [x] Customize what skills to use during each turn in a user-created plan. Users can select which plan to use when starting the bot.
-   [x] A launchable GUI to keep track of logs, adjust settings and selecting what combat script to use.
-   [x] Farm user-defined amounts of specified materials from the supported Farming Modes.
-   [x] A user-defined timer for how long the bot should run for.
-   [x] Support for the following game modes:
    -   [x] Quest
    -   [x] Special
    -   [x] Coop
    -   [x] Raid
    -   [x] Event
    -   [x] Guild Wars
    -   [x] Rise of the Beasts
    -   [x] Dread Barrage
    -   [x] Proving Grounds
    -   [x] Xeno Clash
    -   [x] Arcarum
    -   [x] Replicard Sandbox Part 1
    -   [x] Replicard Sandbox Part 2
-   [x] Alert for when anti-bot CAPTCHA pops up.
-   [x] Discord integration for informing you of status updates like loot drops via private DMs.

# Wiki

Visit the [Wiki here](https://github.com/steve1316/granblue-automation-pyautogui/wiki) for detailed documentation and examples.

# Requirements

1. [Python 3.8.3 (any version higher than this breaks PyTorch) (In addition: make sure Install to PATH is selected)](https://www.python.org/downloads/release/python-383/)
2. [Granblue Fantasy account](http://game.granbluefantasy.jp/)
3. [Twitter Developer account (optional, needed to farm Raids)](https://developer.twitter.com/en)
4. [VMware Workstation Player (optional, if your computer is strong enough to support virtualization)](https://www.vmware.com/products/workstation-player.html)
5. [Microsoft Edge WebView2](https://developer.microsoft.com/en-us/microsoft-edge/webview2/) (Windows 11 comes with this by default. Failure to install this leads to nothing showing up on the screen when the executable is launched.)
6. [Microsoft Visual C++ 2015-2019 Redistibutable (x64)](https://docs.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170)
7. 1080p or 1440p screen resolution at 100% window scaling.

## Python Dependencies (make sure to have these installed before moving on to the instructions)

```
# Open a command terminal inside the /backend/ folder with the method of your choice or by holding SHIFT + RMB and selecting `Open Powershell window here` and then execute this command to install all of these requirements:

pip install -r requirements.txt
```

-   [PyTorch](https://pytorch.org/) (Installing the CUDA version will improve the speed of template matching if you have a CUDA-compatible GPU)
-   [PyAutoGUI](https://pypi.org/project/PyAutoGUI/)
-   [Pillow](https://pypi.org/project/Pillow/)
-   [opencv-python](https://pypi.org/project/opencv-python/)
-   [EasyOCR](https://pypi.org/project/easyocr/)
-   [numpy](https://pypi.org/project/numpy/)
-   [playsound](https://pypi.org/project/playsound/)
-   [pyclick](https://pypi.org/project/pyclick/)
-   [pyperclip](https://pypi.org/project/pyperclip/)
-   [tweepy](https://pypi.org/project/tweepy)
-   [discord.py](https://pypi.org/project/discord.py/)
-   [dictor](https://github.com/perfecto25/dictor)
-   [websockets](https://pypi.org/project/websockets/)

# Instructions

1. Download the latest release by heading to the [Releases page](https://github.com/steve1316/granblue-automation-pyautogui/releases) and downloading the latest .zip file. You will know its the correct one to download as it has a .exe executable file in it called `Granblue Automation.exe`. Alternatively if you want to build it by yourself, download the entire project itself and then head over to [Build Instructions](#build-instructions) and follow the steps. Executing `yarn build` will create the .exe and the necessary files in `/src-tauri/target/release/`.
2. Make sure you installed the project dependencies by having Python 3.8.3 installed and ran `pip install -r requirements.txt` as stated above.
3. Open up the game on a Chromium-based browser and log in if you haven't already done so. Click away any daily log in popups until you are at the Main/Home screen.

    1. `[REQUIRED] Make sure the window size is set to this or else the bot will not be able to detect the "Home" button and proceed any further:`

        ![Correct Window Size](src-tauri/images/readme_assets/correct_window_size.png)

    2. `[REQUIRED] Make sure that BOTH of the Auto Restore settings are enabled in the ingame settings.`

        ![Auto Restore Settings](src-tauri/images/readme_assets/auto_restore.png)

4. Now open up the program executable and follow the onscreen instructions and checking that the Settings page is filled out. You will be informed that the bot is ready to start by the status message at the top of the window.
    1. `(Optional) Additionally, you can check the Extra Settings page for more general settings like Twitter, Discord and Configuration settings.`
5. You can now head back to the Home page of the program and hit the "Start" button to begin.
    1. `Message logs are stored in the /logs/ folder after the bot ends or encounters an error/unexpected situation.`

## Instructions for farming Raids (optional, only if you want to farm Raids)

-   Visit the [Instructions for Farming Raids wiki page](https://github.com/steve1316/granblue-automation-pyautogui/wiki/Instructions-for-Farming-Raids) for setting up Raid farming.

---

## Instructions to set up Discord integration

-   Visit the [Instructions for Discord integration wiki page](https://github.com/steve1316/granblue-automation-pyautogui/wiki/Instructions-for-Discord-integration) for setting up the program notifying you of status updates like loot drops via private DMs.

---

## How to create my own Combat Script?

-   Visit the [Combat Scripting Documentation and Examples wiki page](https://github.com/steve1316/granblue-automation-pyautogui/wiki/Combat-Scripting-Documentation-and-Examples) for combat scripting usage and examples.

---

## What Missions/Items/Summons are supported?

-   Visit the [List of Supported Missions and their Farmable Items wiki page](https://github.com/steve1316/granblue-automation-pyautogui/wiki/List-of-Supported-Missions-and-their-Farmable-Items) for supported content.
-   Visit the [Selectable Summons wiki page](https://github.com/steve1316/granblue-automation-pyautogui/wiki/Selectable-Summons) for available Summons.

---

## Virtual Machine Setup (optional)

-   Visit the [Virtual Machine Setup wiki page](https://github.com/steve1316/granblue-automation-pyautogui/wiki/Virtual-Machine-Setup) for setting up a Virtual Machine to run this program on.

# Build Instructions

> Note: If your changes are only in the Python files, you can just replace the files in your GA folder. But if the Javascript files were changed, then a build is needed.

> Note 2: Adjust the `/src-tauri/tauri.conf.json` for build-specific adjustments to your environment. It is already set up for building on Windows.

> Note 3: Adjust `/src-tauri/update.json` to update version number of your build.

1. Open up root folder in VSCode. Type `yarn install` in terminal to install Javascript dependencies.
2. Then follow your environment's instructions for [Tauri](https://tauri.studio/docs/getting-started/prerequisites).
3. Now refer to the following 2 commands below for your use case.

-   `yarn start` Starts up the Metro server for hot code reloading.

-   `yarn build` Bundles and builds the executable in `/src-tauri/target/release/`. Also includes a installer in `../bundle/` as well.

# Technologies Used

1. [Python - The main language](https://www.python.org/)
2. [Qt - Application development framework for the GUI (old frontend)](https://www.qt.io/product/development-tools)
3. [Typescript - Language for the new GUI (new frontend)](https://www.typescriptlang.org/)
4. [Tauri - Toolkit to transform the Typescript frontend framework into a desktop application](https://tauri.studio/en/)
5. [PyAutoGUI - Primarily for screenshot capturing and mouse control](https://pyautogui.readthedocs.io/en/latest/)
6. [pyclick - For making mouse movements human-like via Bezier Curves](https://pypi.org/project/pyclick/)
7. [OpenCV-Python - Image template matching](https://pypi.org/project/opencv-python/)
8. [EasyOCR - For text recognition and detection](https://github.com/JaidedAI/EasyOCR)
9. [Twitter Standard API 1.1 - For searching and parsing texts for Raid room codes to join](https://developer.twitter.com/en/docs/twitter-api/v1)
10. [VMWare Workstation Player - For virtualizing the program to circumvent control of the main cursor](https://www.vmware.com/products/workstation-player.html)
