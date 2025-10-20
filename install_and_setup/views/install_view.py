import customtkinter as ctk
import tkinter.messagebox as messagebox
from typing import Callable, Optional
from install_and_setup.config import APP_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT


class InstallView(ctk.CTk):
    """
    Pure UI. Exposes callbacks; no business logic.
    Controller calls `render_step(index)` to switch screens.
    """

    # Controller-provided callbacks
    on_continue: Optional[Callable[[], None]] = None
    on_launch_chrome: Optional[Callable[[], None]] = None
    on_save_info: Optional[Callable[[str, str], None]] = None

    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title(APP_TITLE)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.resizable(False, False)

        self._start_chrome_button = None  # used to enable/disable
        self._steam_entry = None
        self._webhook_entry = None

        self._build_shell()

    # ----- Shell (static chrome) -----
    def _build_shell(self):
        self.outer_frame = ctk.CTkFrame(self, corner_radius=16)
        self.outer_frame.pack(expand=True, fill="both", padx=24, pady=24)

        self.header_frame = ctk.CTkFrame(self.outer_frame, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=18, pady=(18, 12))

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="Welcome to the CS Trade Bot Installer",
            font=("Segoe UI", 26, "bold"),
            anchor="w",
        )
        self.title_label.pack(fill="x")

        self.subtitle_label = ctk.CTkLabel(
            self.header_frame,
            text=(
                "This guided setup will prepare the automation bot that helps you browse "
                "Counter-Strike 2 trade offers and pre-fills the offer window with your "
                "selected inventory item."
            ),
            font=("Segoe UI", 15),
            wraplength=WINDOW_WIDTH - 120,
            justify="left",
        )
        self.subtitle_label.pack(fill="x", pady=(12, 0))

        self.step_container = ctk.CTkFrame(self.outer_frame, corner_radius=12)
        self.step_container.pack(expand=True, fill="both", padx=18, pady=12)

        footer_frame = ctk.CTkFrame(self.outer_frame, fg_color="transparent")
        footer_frame.pack(fill="x", padx=18, pady=(0, 18))

        self.continue_button = ctk.CTkButton(
            footer_frame,
            text="Begin setup",
            command=self._continue_clicked,
            height=42,
            font=("Segoe UI", 16, "bold"),
        )
        self.continue_button.pack(side="right")

        self.status_label = ctk.CTkLabel(
            footer_frame,
            text="Step 1 of 4 · Review the information above before continuing.",
            font=("Segoe UI", 13),
            anchor="w",
        )
        self.status_label.pack(side="left")

    # ----- Public helpers for Controller -----
    def set_status(self, text: str):
        self.status_label.configure(text=text)

    def set_continue_text(self, text: str):
        self.continue_button.configure(text=text)

    def set_chrome_button_enabled(self, enabled: bool):
        if self._start_chrome_button is None:
            return
        self._start_chrome_button.configure(state="normal" if enabled else "disabled")

    def fill_user_inputs(self, steam_link: str, webhook_url: str):
        if self._steam_entry is not None:
            self._steam_entry.delete(0, "end")
            self._steam_entry.insert(0, steam_link or "")
        if self._webhook_entry is not None:
            self._webhook_entry.delete(0, "end")
            self._webhook_entry.insert(0, webhook_url or "")

    def get_user_inputs(self) -> tuple[str, str]:
        steam = self._steam_entry.get().strip() if self._steam_entry else ""
        hook = self._webhook_entry.get().strip() if self._webhook_entry else ""
        return steam, hook

    # ----- Steps -----
    def render_step(self, index: int):
        # clear
        for child in self.step_container.winfo_children():
            child.destroy()

        if index == 0:
            self._render_welcome()
            self.set_continue_text("Begin setup")
            self.set_status("Step 1 of 4 · Review the information above before continuing.")
        elif index == 1:
            self._render_chrome()
            self.set_continue_text("Next step")
            self.set_status("Step 2 of 4 · Setup Chrome browser for the bot.")
        elif index == 2:
            self._render_user_inputs()
            self.set_continue_text("Next step")
            self.set_status("Step 3 of 4 · Input the required information")

    def _render_welcome(self):
        info_frame = ctk.CTkScrollableFrame(self.step_container, corner_radius=12, fg_color="transparent")
        info_frame.pack(expand=True, fill="both")

        sections = (
            (
                "What the bot does",
                (
                    "The bot will load your inventory, allowing you to select up to 10 of your most expensive skins. "
                    "You can then choose an item from your inventory that you want to trade. "
                    "The bot will search for trades that meet your desired profit percentage."
                ),
            ),
            (
                "What you'll need to do for the installation",
                (
                    "You will need to have Google Chrome installed on your device and a Counter-Strike inventory to trade with. "
                    "You must also follow the installation instructions and create a Discord webhook. "
                    "In addition, you need to install the CS2 Trader extension for Chrome. "
                    "All of these steps will be explained in the YouTube video below."
                ),
            ),
            (
                "Safety and responsibility",
                (
                    "The bot does not violate the Steam Community Terms of Service. "
                    "It only helps you find potentially profitable trades — it does not determine whether items are liquid or valuable. "
                    "Only accept and send the trades that you personally feel are worth it."
                ),
            )
        )

        for heading, body in sections:
            section_frame = ctk.CTkFrame(info_frame, corner_radius=10)
            section_frame.pack(fill="x", expand=False, padx=6, pady=(0, 12))

            heading_label = ctk.CTkLabel(
                section_frame,
                text=heading,
                font=("Segoe UI", 18, "bold"),
                anchor="w",
            )
            heading_label.pack(fill="x", padx=16, pady=(16, 8))

            body_label = ctk.CTkLabel(
                section_frame,
                text=body,
                font=("Segoe UI", 14),
                justify="left",
                wraplength=WINDOW_WIDTH - 140,
                anchor="w",
            )
            body_label.pack(fill="x", padx=16, pady=(0, 16))

    def _render_chrome(self):
        chrome_frame = ctk.CTkFrame(self.step_container, corner_radius=12)
        chrome_frame.pack(expand=True, fill="both", padx=6, pady=6)

        heading_label = ctk.CTkLabel(
            chrome_frame,
            text="Step 2 · Prepare Google Chrome",
            font=("Segoe UI", 22, "bold"),
            anchor="w",
        )
        heading_label.pack(fill="x", padx=24, pady=(24, 12))

        body_text = (
            "Here’s what you need to do to set up Chrome for use with this bot. "
            "First, log in to your Steam profile — the button below will take you directly to the Steam login page. "
            "After logging in, make sure to install the CS2 Trader extension "
            "and set it up as explained in the installation video guide."
        )

        body_label = ctk.CTkLabel(
            chrome_frame,
            text=body_text,
            font=("Segoe UI", 15),
            justify="left",
            wraplength=WINDOW_WIDTH - 140,
        )
        body_label.pack(fill="x", padx=24)

        # Keep a ref so controller can enable/disable
        self._start_chrome_button = ctk.CTkButton(
            chrome_frame,
            text="Launch Chrome",
            height=42,
            font=("Segoe UI", 16, "bold"),
            command=self._launch_chrome_clicked,
        )
        self._start_chrome_button.pack(padx=24, pady=(32, 12), anchor="w")

    def _render_user_inputs(self):
        user_input_frame = ctk.CTkFrame(self.step_container, corner_radius=12)
        user_input_frame.pack(expand=True, fill="both", padx=6, pady=6)

        user_input_heading = ctk.CTkLabel(
            user_input_frame,
            text="Step 3 · Inputting the required information",
            font=("Segoe UI", 20, "bold"),
            anchor="w",
        )
        user_input_heading.pack(fill="x", padx=20, pady=(16, 8))

        input_container = ctk.CTkFrame(user_input_frame, corner_radius=8)
        input_container.pack(fill="x", padx=20, pady=(0, 12))

        inner_frame = ctk.CTkFrame(input_container, fg_color="transparent")
        inner_frame.pack(fill="x", padx=16, pady=16)

        steam_label = ctk.CTkLabel(
            inner_frame,
            text="Steam Inventory Link:",
            font=("Segoe UI", 14, "bold"),
            anchor="w",
        )
        steam_label.pack(fill="x", pady=(0, 4))

        self._steam_entry = ctk.CTkEntry(
            inner_frame,
            placeholder_text="https://steamcommunity.com/id/yourname/inventory",
            height=32,
            font=("Segoe UI", 13),
        )
        self._steam_entry.pack(fill="x", pady=(0, 10))

        webhook_label = ctk.CTkLabel(
            inner_frame,
            text="Discord Webhook URL:",
            font=("Segoe UI", 14, "bold"),
            anchor="w",
        )
        webhook_label.pack(fill="x", pady=(0, 4))

        self._webhook_entry = ctk.CTkEntry(
            inner_frame,
            placeholder_text="https://discord.com/api/webhooks/...",
            height=32,
            font=("Segoe UI", 13),
        )
        self._webhook_entry.pack(fill="x")

        button_frame = ctk.CTkFrame(user_input_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(8, 16), padx=20)

        save_button = ctk.CTkButton(
            button_frame,
            text="Save Information",
            width=160,
            height=36,
            font=("Segoe UI", 14, "bold"),
            corner_radius=6,
            command=self._save_clicked,
        )
        save_button.pack(anchor="e")

    # ----- UI -> Controller triggers -----
    def _continue_clicked(self):
        if self.on_continue:
            self.on_continue()

    def _launch_chrome_clicked(self):
        if self.on_launch_chrome:
            self.on_launch_chrome()

    def _save_clicked(self):
        if not self.on_save_info:
            return
        steam, hook = self.get_user_inputs()

        # lightweight input check mirroring original behavior
        if not steam or not hook or not steam.startswith("http") or not hook.startswith("http"):
            self.set_status("Please enter valid URLs for both fields.")
            return

        self.on_save_info(steam, hook)

    # ----- Minor helpers the controller can reuse -----
    def show_error(self, title: str, message: str):
        messagebox.showerror(title, message)

    def show_warning(self, title: str, message: str):
        messagebox.showwarning(title, message)
