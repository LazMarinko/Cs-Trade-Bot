# ui_and_scraper/close_ui/close_controller.py
import threading

from ui_and_scraper.close_ui.close_ui_model.close_ui_model import CloseModel
from ui_and_scraper.close_ui.close_ui_view.close_ui_view import CloseView


class CloseController:
    """
    Controller: wires CloseView and CloseModel, manages the background thread,
    and provides a run() method for main.py.
    """

    def __init__(self, selected_index: int):
        self.model = CloseModel(selected_index)
        self.view = CloseView()

        self.stop_event = threading.Event()
        self.worker_thread = threading.Thread(
            target=self.model.run_bot_cycles,
            args=(self.stop_event,),
            daemon=True
        )

        # Wire callbacks
        self.view.on_stop = self.handle_stop

        # Start background worker
        self.worker_thread.start()

    def handle_stop(self):
        """
        Called when the user clicks Stop or closes the window.
        """
        print("[CloseController] Stop requested by user.")
        self.stop_event.set()

        if self.view.winfo_exists():
            self.view.destroy()

    def run(self):
        """
        Block here in the Tk mainloop until the window is closed.
        """
        self.view.mainloop()
