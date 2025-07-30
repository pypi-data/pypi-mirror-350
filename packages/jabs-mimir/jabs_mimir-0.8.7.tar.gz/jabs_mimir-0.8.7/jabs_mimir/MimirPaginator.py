from typing import List
import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.widgets import Treeview
import tkinter.font as tkFont

from jabs_mimir.mimirThemeManager import MimirThemeManager
from jabs_mimir.MimirUtils  import MimirUtils

class MimirPaginator:
    def __init__(self, items: List, itemsPerPage: int, parent: tk.Widget):
        self.items = items
        self.itemsPerPage = itemsPerPage
        self.itemsByPage = self._split(items, itemsPerPage)
        self.maxPage = len(self.itemsByPage) - 1
        self.state = {"page": 0}
        self.pageLabelVar = tk.StringVar()
        self.tree = Treeview(parent, show="tree")
        self.utils = MimirUtils()
        MimirThemeManager.subscribeToThemeChange(self.setupStyle)
        self._styleTree(self.tree)
        self._createWidgets(parent)

    def setupStyle(self, tree):
        style = tb.Style()
        colors = MimirThemeManager.getCurrentTheme().colors
        style.configure("Treeview", rowheight=25)  # Adjust to taste
        
        tree.tag_configure("odd", background=colors.secondary)
        tree.tag_configure("strike", foreground="#888888", background="#f0f0f0", font=(self.utils.getCurrentFont(), 12, "overstrike"))
        tree.tag_configure("highlight", background="lightblue", foreground="black")

        # Font configuration (reset on theme change)
        rowFont = tkFont.Font(font=self.utils.getCurrentFont())
        headerFont = tkFont.Font(font=self.utils.getCurrentFont())
        style.configure("Treeview", font=(rowFont, 12))
        style.configure("Treeview.Heading", font=(headerFont, 13))

    def _split(self, items, perPage):
        return [items[i:i + perPage] for i in range(0, len(items), perPage)]

    def _createWidgets(self, parent):
        parent.rowconfigure(0, weight=1)  # Treeview
        parent.rowconfigure(1, weight=0)  # Button row
        parent.columnconfigure(0, weight=1)

        self.tree.grid(row=0, column=0, sticky="nsew")
        self._populateTree()

        self.buttonGrid = tb.Frame(parent)
        self.buttonGrid.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        for i in range(3):
            self.buttonGrid.columnconfigure(i, weight=1)

        self.backButton = tb.Button(
            self.buttonGrid, text="Back",
            command=self.goToPreviousPage
        )
        self.backButton.grid(row=0, column=0, sticky="ew", padx=5)

        tb.Label(
            self.buttonGrid, textvariable=self.pageLabelVar,
            anchor="center"
        ).grid(row=0, column=1, sticky="ew")

        self.nextButton = tb.Button(
            self.buttonGrid, text="Next",
            command=self.goToNextPage
        )
        self.nextButton.grid(row=0, column=2, sticky="ew", padx=5)

    def _populateTree(self):
        self.tree.delete(*self.tree.get_children())
        for i, item in enumerate(self.itemsByPage[self.state["page"]]):
            tag = "even" if i % 2 == 0 else "odd"
            self.tree.insert("", "end", text=item, tags=(tag,))
        self.pageLabelVar.set(str(self.state["page"] + 1))

    def goToNextPage(self):
        self.state["page"] = min(self.state["page"] + 1, self.maxPage)
        self._populateTree()

    def goToPreviousPage(self):
        self.state["page"] = max(0, self.state["page"] - 1)
        self._populateTree()
