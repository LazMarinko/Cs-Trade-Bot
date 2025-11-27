# ui_and_scraper/selector_ui/settings_controller/settings_view.py
import customtkinter as ctk
from ui_and_scraper.selector_ui.pages.page_general import GeneralSettingsPage
from ui_and_scraper.selector_ui.pages.page_trade import TradeSettingsPage


class SettingsView(ctk.CTkToplevel):

    on_close = None   # wired by controller
    on_save = None    # wired by controller

    def __init__(self, parent):
        super().__init__(parent)

        self.title("Settings")
        self.geometry("500x320")
        self.resizable(False, False)

        # make it modal-ish
        self.transient(parent)
        self.grab_set()

        # layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=1)

        # Tabs
        self.tabs = ctk.CTkTabview(self)
        self.tabs.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        tab_general = self.tabs.add("General")
        tab_trade = self.tabs.add("Trading")

        self.general_page_frame = GeneralSettingsPage(tab_general)
        self.general_page_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.trade_page_frame = TradeSettingsPage(tab_trade)
        self.trade_page_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Bottom button bar
        button_bar = ctk.CTkFrame(self, fg_color="transparent")
        button_bar.grid(row=1, column=0, sticky="e", padx=10, pady=(0, 10))
        button_bar.grid_columnconfigure(0, weight=1)
        button_bar.grid_columnconfigure(1, weight=0)
        button_bar.grid_columnconfigure(2, weight=0)

        self.save_button = ctk.CTkButton(
            button_bar, text="Save", width=80, command=self._handle_save
        )
        self.save_button.grid(row=0, column=1, padx=(0, 5))

        self.close_button = ctk.CTkButton(
            button_bar, text="Close", width=80, command=self._handle_close
        )
        self.close_button.grid(row=0, column=2)

        self.protocol("WM_DELETE_WINDOW", self._handle_close)

    def _handle_close(self):
        if self.on_close:
            self.on_close()
        self.destroy()

    def _handle_save(self):
        if self.on_save:
            self.on_save()
