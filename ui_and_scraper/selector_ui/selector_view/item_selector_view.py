import customtkinter as ctk
from typing import Callable, Optional


class ItemSelectorView(ctk.CTk):

    on_select: Optional[Callable[[], None]] = None
    on_close: Optional[Callable[[], None]] = None
    on_settings: Optional[Callable[[], None]] = None

    def __init__(self):
        super().__init__()

        # More square window
        self.title("Item Selector")
        self.geometry("360x260")
        self.resizable(False, False)

        # ===== GRID =====
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # ===== TOP BAR (cog only) =====
        top_bar = ctk.CTkFrame(self, fg_color="transparent")
        top_bar.grid(row=0, column=0, sticky="ew", padx=10, pady=(6, 0))
        top_bar.grid_columnconfigure(0, weight=1)
        top_bar.grid_columnconfigure(1, weight=0)

        self.settings_button = ctk.CTkButton(
            top_bar,
            text="⚙",
            width=26,
            height=26,
            fg_color="transparent",
            hover_color=("gray70", "gray30"),
            corner_radius=12,
            command=self._handle_settings
        )
        self.settings_button.grid(row=0, column=1, sticky="e")

        # Start disabled until scraper finishes
        self.settings_button.configure(state="disabled")

        # ===== SELECTOR CARD =====
        card = ctk.CTkFrame(
            self,
            corner_radius=16,
            border_width=1
        )
        card.grid(
            row=1,
            column=0,
            sticky="n",
            padx=10,
            pady=10
        )

        card.grid_columnconfigure(0, weight=1)

        # Title text
        self.label = ctk.CTkLabel(
            card,
            text="Select item to trade",
            font=("Helvetica", 15, "bold")
        )
        self.label.grid(row=0, column=0, pady=(10, 6), padx=12)

        # Selected StringVar
        self.selected_item = ctk.StringVar(value="Loading...")

        # Non-editable ComboBox
        self.items = ctk.CTkComboBox(
            card,
            values=["Loading..."],
            variable=self.selected_item,
            width=240,
            height=34,
            corner_radius=10,
            state="readonly"
        )
        self.items.grid(row=1, column=0, pady=(0, 10), padx=12, sticky="ew")

        # Select button
        self.button = ctk.CTkButton(
            card,
            text="Select",
            command=self._handle_select,
            state="disabled",
            width=140,
            height=34,
            corner_radius=10
        )
        self.button.grid(row=2, column=0, pady=(0, 12), padx=12)

        self.protocol("WM_DELETE_WINDOW", self._handle_close)

    # ===== PUBLIC API USED BY CONTROLLER =====

    def set_loading(self):
        self.items.configure(values=["Loading..."])
        self.selected_item.set("Loading...")
        self.button.configure(state="disabled")

    def set_items(self, item_labels, enable_button=True):
        if not item_labels:
            self.items.configure(values=["No tradeable items found"])
            self.selected_item.set("No tradeable items found")
            self.button.configure(state="disabled")
            return

        self.items.configure(values=item_labels)
        self.selected_item.set(item_labels[0])
        self.button.configure(state="normal" if enable_button else "disabled")

    def get_selected_index(self):
        values = self.items.cget("values")
        try:
            return values.index(self.selected_item.get())
        except ValueError:
            return None

    # ===== SETTINGS BUTTON CONTROL =====

    def disable_settings(self):
        self.settings_button.configure(state="disabled")

    def enable_settings(self):
        self.settings_button.configure(state="normal")

    # ===== INTERNAL HANDLERS =====

    def _handle_select(self):
        if self.on_select:
            self.on_select()

    def _handle_close(self):
        if self.on_close:
            self.on_close()
        if self.winfo_exists():
            self.destroy()

    def _handle_settings(self):
        if self.on_settings:
            self.on_settings()
