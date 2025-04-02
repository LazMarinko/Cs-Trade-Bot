import customtkinter as ctk
import threading
import time
from bot_browser_control.bot import TradeBot  # Adjust if needed
import subprocess

class CloseUI(ctk.CTk):
    def __init__(self, selected_index):
        super().__init__()
        self.is_stopped = False
        self.selected_index = selected_index
        self.bot = None
        # Suppress "invalid command name" errors caused by after() scripts post-destroy
        self.report_callback_exception = self._handle_callback_exception


        self.title("Bot running...")
        self.geometry("200x100")

        self.label = ctk.CTkLabel(self, text="Press this button to stop the bot")
        self.label.pack(pady=10)

        self.button = ctk.CTkButton(self, text="Stop", command=self.stop)
        self.button.pack(pady=10)

        # ✅ Start bot in a new thread so it doesn't block the UI
        threading.Thread(target=self.start_bot, daemon=True).start()

    def stop(self):
        self.is_stopped = True
        self.destroy()
        return

    def start_bot(self):
        while True:
            try:
                # 🔪 Kill all existing Chrome processes
                try:
                    subprocess.call("taskkill /F /IM chrome.exe /T", shell=True)
                except Exception as e:
                    print(e)
                time.sleep(2)  # Give a moment for Chrome to shut down

                print("🔁 Running bot cycle...")
                self.bot = TradeBot(self.selected_index)
                self.bot.run()
                time.sleep(3600*3)  # Wait time between cycles
                print("Timer done")

                if self.is_stopped:
                    break

            except Exception as e:
                print(f"❌ Exception during bot cycle: {e}")
    def _handle_callback_exception(self, exc, val, tb):
        # Suppress specific 'invalid command name' errors, print others
        if "invalid command name" in str(val):
            print("⚠️ Ignored harmless Tkinter callback error:", val)
        else:
            import traceback
            traceback.print_exception(exc, val, tb)
