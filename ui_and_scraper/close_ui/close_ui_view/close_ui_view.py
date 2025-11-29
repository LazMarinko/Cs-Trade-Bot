# ui_and_scraper/close_ui/close_view.py
import customtkinter as ctk
from typing import Callable, Optional


class CloseView(ctk.CTk):
    """
    View: small window with 'bot running' info and a Stop button.
    Exposes on_stop callback for the controller.
    """

    on_stop: Optional[Callable[[], None]] = None

    def __init__(self):
        super().__init__()

        # Tk error handler to avoid "invalid command name" spam after destroy
        self.report_callback_exception = self._handle_callback_exception

        self.title("Bot running...")
        self.geometry("260x120")
        self.resizable(False, False)

        # Layout
        self.label = ctk.CTkLabel(
            self,
            text="Bot is running.\nPress the button to stop it.",
            justify="center"
        )
        self.label.pack(pady=10, padx=10)

        self.stop_button = ctk.CTkButton(
            self,
            text="Stop",
            command=self._handle_stop,
            width=80
        )
        self.stop_button.pack(pady=(0, 10))

        # When user closes window via [X]
        self.protocol("WM_DELETE_WINDOW", self._handle_stop)

    # ---- public helpers (if controller ever wants to tweak UI) ----
    def set_status_text(self, text: str):
        self.label.configure(text=text)

    # ---- internal handlers ----
    def _handle_stop(self):
        if self.on_stop:
            self.on_stop()

    def _handle_callback_exception(self, exc, val, tb):
        # Suppress specific 'invalid command name' errors, print others
        if "invalid command name" in str(val):
            print("⚠️ Ignored harmless Tkinter callback error:", val)
        else:
            import traceback
            traceback.print_exception(exc, val, tb)
