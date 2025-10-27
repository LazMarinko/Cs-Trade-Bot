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
        self.view.on_save_info = self.handle_input_save_info
        self.view.on_final_save = self.handle_final_save

        self.view.render_step(self.current_step)

        saved = self.settings_model.load()
        if saved:
            self.view.fill_user_inputs(saved.steam_inventory_link, saved.discord_webhook_url)

    def handle_continue(self):
        # If we're not yet on the last step, advance as usual
        if self.current_step < 3:
            self.current_step += 1
            self.view.render_step(self.current_step)
            return

        # We're on the last step (index 3) -> Finish clicked
        try:
            if self.chrome.is_running():
                self.chrome.stop()
        except Exception:
            pass

        self.view.destroy()  # closes the window; mainloop() will exit

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
    def handle_input_save_info(self, steam_link: str, webhook_url: str):
        try:
            # you don't need to load here
            self.settings_model.initial_save(
                Settings(steam_inventory_link=steam_link, discord_webhook_url=webhook_url)
            )
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

    def handle_final_save(self, min_profit_str: str, max_profit_str: str, min_value_str: str):
        def pct_to_float(s: str) -> float:
            return float(s.strip().replace("%", ""))

        # Parse raw strings like "8%", "60%"
        min_profit = pct_to_float(min_profit_str)
        max_profit = pct_to_float(max_profit_str)
        min_target = pct_to_float(min_value_str)

        # Validate ranges
        if not (2 <= min_profit <= 15):
            self.view.set_status("Min profit must be between 2% and 15%.")
            return
        if not (5 <= max_profit <= 25):
            self.view.set_status("Max profit must be between 5% and 25%.")
            return
        if max_profit < min_profit:
            self.view.set_status("Max profit % must be ≥ Min profit %.")
            return

        # Persist (model converts to 1.xx / 0.x as previously implemented)
        self.settings_model.final_save_trade_settings(min_profit, max_profit, min_target)
        self.view.set_status("✅ Trade settings saved to config.json.")
