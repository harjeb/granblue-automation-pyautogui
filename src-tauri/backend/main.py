import multiprocessing
import time
import os,sys
from utils.message_log import MessageLog



class MainDriver:
    """
    This driver class allows the Game class to be run on a separate Thread.
    """

    def __init__(self, set_path):
        super().__init__()
        self._game = None
        self.set_path = set_path
        self._bot_process = None
        self.root_path = os.path.abspath('.') 

    def is_running(self) -> bool:
        """Check the status of the bot process.

        Returns:
            (bool): Flag that indicates whether the bot process is still running or not.
        """
        return self._bot_process.is_alive()

    def _run_bot(self):
        """Starts the main bot process on this Thread.

        Returns:
            None
        """
        # Initialize the Game class and start Farming Mode.
        # c = 0
        # for filename in os.listdir(self.root_path+'/backend'):
        #     setname = 'settings%s'% str(c)
        #     if setname in filename and '_' not in filename:
        #         _file = self.root_path + '/backend/' + setname + '.json'
        #         os.rename(_file,self.root_path+'/backend/settings.json')
        #         from utils.settings import Settings
        #         Settings.update()
        #         from bot.game import Game
        #         self._game = Game()
        #         self._game.start_farming_mode()
        #         os.remove(self.root_path+'/backend/settings.json')
        #         c += 1
        #     elif setname in filename and '_'  in filename:
        #         sleeptime = int(setname.split('_')[1])
        #         time.sleep(sleeptime)
        #         c += 1
        from bot.game import Game
        self._game = Game(self.set_path)
        self._game.start_farming_mode(self.set_path)
        return None

    def start_bot(self):
        """Starts the bot's Game class on a new Thread.

        Returns:
            None
        """
        # Create a new Process whose target is the MainDriver's run_bot() method.
        from utils.settings import Settings
        Settings.update(self.set_path)
        self._bot_process = multiprocessing.Process(target = self._run_bot)

        MessageLog.print_message("[STATUS] Starting bot process on a new thread now...")


        # Now start the new Process on a new Thread.
        self._bot_process.start()
        self._bot_process.is_alive()

        return None

    def stop_bot(self):
        """Stops the bot and terminates the Process.

        Returns:
            None
        """
        if self._bot_process is not None:
            MessageLog.print_message("\n[STATUS] Stopping the bot and terminating its Thread.")
            self._bot_process.terminate()

        return None


if __name__ == "__main__":
    # Start the bot.
    set_file = sys.argv[1]
    print(set_file)
    bot_object = MainDriver(set_file)
    bot_object.start_bot()
    while True:
        if bot_object.is_running() is False:
            break
        else:
            time.sleep(1.0)

    bot_object.stop_bot()

    MessageLog.print_message("[STATUS] Closing Python process...")
