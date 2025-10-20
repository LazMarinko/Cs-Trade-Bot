import subprocess
import sys
from install_and_setup.config import CHROME_PROFILE_PATH
from install_and_setup.models.settings_model import SettingsModel, Settings
from install_and_setup.models.chrome_setup import ChromeSetupModel
from install_and_setup.views.install_view import InstallView


class InstallController():
    def __init__(self):
        self.view = InstallView()
        self.settings_model = SettingsModel()
        self.current_step = 0

        self.chrome = ChromeSetupModel(profile_path=CHROME_PROFILE_PATH)

        self.view.on_continue = self.handle_continue
        self.view.on_launch_chrome = self.handle_launch_chrome
        self.view.on_save_info = self.handle_save_info

        self.view.render_step(self.current_step)

        saved = self.settings_model.load()
        if saved:
            self.view.fill_user_inputs(saved.steam_inventory_link, saved.discord_webhook_url)

    def handle_continue(self):
        if self.current_step < 2:
            self.current_step += 1
            self.view.render_step(self.current_step)

    def handle_launch_chrome(self):
        if self.chrome.is_running():
            # Already running — nothing to do
            self.view.set_status("Chrome is already running…")
            return

        # Start non-blocking
        ok = self.chrome.start()
        if not ok:
            self.view.set_status("Chrome is already running…")
            return

        self.view.set_status("Step 2 of 4 · Launching Chrome setup…")
        self.view.set_chrome_button_enabled(False)

        # Poll the model state
        def _poll():
            if self.chrome.is_running():
                # keep polling
                self.view.after(500, _poll)
                return

            # Thread ended — check error
            self.view.set_chrome_button_enabled(True)
            err = self.chrome.last_error()
            if err:
                self.view.set_status("Chrome setup ended with an error.")
                self.view.show_warning("Chrome setup ended", err)
            else:
                self.view.set_status("Chrome setup finished. You can continue.")

        self.view.after(500, _poll)

    # --- Save step ---
    def handle_save_info(self, steam_link: str, webhook_url: str):
        try:
            self.model.save(Settings(steam_inventory_link=steam_link, discord_webhook_url=webhook_url))
            self.view.set_status("✅ Information saved to config.json.")
        except Exception as e:
            self.view.set_status(f"Failed to save config: {e}")

    # --- Entry point ---
    def run(self):
        try:
            self.view.mainloop()
        finally:
            # Ensure background Chrome is stopped on app exit
            if self.chrome.is_running():
                self.chrome.stop()
