"""Installation wizard UI for CS Trade Bot."""
import os
import sys
import subprocess
import customtkinter as ctk
import tkinter.messagebox as messagebox
from temp import run_initial_chrome_setup


class InstallWizard(ctk.CTk):
    """First page of the installation wizard with bot information."""

    WINDOW_WIDTH = 780
    WINDOW_HEIGHT = 560

    def __init__(self) -> None:
        super().__init__()

        self.start_chrome_button = None
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("CS Trade Bot • Setup")
        self.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        self.resizable(False, False)

        self.build_layout()
        self._current_step = 0
        self.show_current_step()

    def build_layout(self) -> None:
        """Create the static structure of the wizard window."""

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
            wraplength=self.WINDOW_WIDTH - 120,
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
            command=self.handle_continue,
            height=42,
            font=("Segoe UI", 16, "bold"),
        )
        self.continue_button.pack(side="right")

        self.status_label = ctk.CTkLabel(
            footer_frame,
            text="Step 1 of 2 · Review the information above before continuing.",
            font=("Segoe UI", 13),
            anchor="w",
        )
        self.status_label.pack(side="left")

    def show_current_step(self) -> None:
        """Render the frame for the current step index."""

        for child in self.step_container.winfo_children():
            child.destroy()

        if self._current_step == 0:
            self.show_welcome_step()
        elif self._current_step == 1:
            self.show_chrome_step()

    def show_welcome_step(self) -> None:
        """Display the introductory information for the wizard."""

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
                wraplength=self.WINDOW_WIDTH - 140,
                anchor="w",
            )
            body_label.pack(fill="x", padx=16, pady=(0, 16))

        self.continue_button.configure(text="Begin setup", state="normal")
        self.status_label.configure(
            text="Step 1 of 2 · Review the information above before continuing."
        )

    def show_chrome_step(self) -> None:
        """Display Chrome setup guidance and placeholder controls."""

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
            wraplength=self.WINDOW_WIDTH - 140,
        )
        body_label.pack(fill="x", padx=24)

        chrome_button = ctk.CTkButton(
            chrome_frame,
            text="Launch Chrome",
            height=42,
            font=("Segoe UI", 16, "bold"),
            command=self.handle_launch_chrome,
        )
        chrome_button.pack(padx=24, pady=(32, 12), anchor="w")

        self.continue_button.configure(text="Finish", state="disabled")
        self.status_label.configure(
            text="Step 2 of 2 · Chrome launch automation will be added shortly."
        )

    def handle_continue(self) -> None:
        """Advance the wizard to the next step."""

        if self._current_step < 1:
            self._current_step += 1
            self.show_current_step()

    # --- replace your handler with this ---
    def handle_launch_chrome(self) -> None:
        """Kick off the external Chrome setup (temp.py) without blocking the UI."""
        # Resolve temp.py path relative to this file
        here = os.path.dirname(os.path.abspath(__file__))
        temp_script = os.path.join(here, "temp.py")

        if not os.path.exists(temp_script):
            messagebox.showerror(
                "Missing file",
                f"Could not find temp.py at:\n{temp_script}\n\nMake sure it exists next to install_ui.py.",
            )
            return

        # Update UI before launch
        self.status_label.configure(text="Step 2 of 2 · Launching Chrome setup…")
        # If you have a dedicated button attribute, disable it while running:
        try:
            self.start_chrome_button.configure(state="disabled")
        except Exception:
            pass

        # Launch temp.py in a separate process (non-blocking)
        try:
            proc = subprocess.Popen(
                [sys.executable, "-u", temp_script],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT,
            )
        except Exception as e:
            messagebox.showerror("Failed to start Chrome setup", str(e))
            try:
                self.start_chrome_button.configure(state="normal")
            except Exception:
                pass
            return

        # Poll for completion without freezing the Tk loop
        def _poll():
            if proc.poll() is None:
                # still running
                self.after(500, _poll)
            else:
                # finished
                try:
                    self.start_chrome_button.configure(state="normal")
                except Exception:
                    pass
                if proc.returncode == 0:
                    self.status_label.configure(text="Chrome setup finished. You can continue.")
                    # If you have a next step, trigger it here (optional):
                    # self._advance_to_next_step()
                else:
                    self.status_label.configure(text="Chrome setup ended with an error. See logs if available.")
                    messagebox.showwarning(
                        "Chrome setup ended",
                        "The Chrome setup process exited with a non-zero status.\n"
                        "If this was intentional, you can continue. Otherwise, please rerun.",
                    )

        self.after(500, _poll)


if __name__ == "__main__":
    InstallWizard().mainloop()