import customtkinter as ctk


class GeneralSettingsPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.grid_columnconfigure(0, weight=1)

        self.inv_label = ctk.CTkLabel(self, text="Steam Inventory Link:")
        self.inv_label.grid(row=0, column=0, sticky="w", pady=(2, 2))

        self.inv_entry = ctk.CTkEntry(self, width=350)
        self.inv_entry.grid(row=1, column=0, pady=(0, 10), sticky="ew")

        self.webhook_label = ctk.CTkLabel(self, text="Discord Webhook:")
        self.webhook_label.grid(row=2, column=0, sticky="w", pady=(2, 2))

        self.webhook_entry = ctk.CTkEntry(self, width=350)
        self.webhook_entry.grid(row=3, column=0, pady=(0, 10), sticky="ew")

    def load_values(self, inventory_link: str, webhook: str):
        self.inv_entry.delete(0, "end")
        self.inv_entry.insert(0, inventory_link or "")

        self.webhook_entry.delete(0, "end")
        self.webhook_entry.insert(0, webhook or "")

    def get_inventory_link(self) -> str:
        return self.inv_entry.get().strip()

    def get_webhook(self) -> str:
        return self.webhook_entry.get().strip()
