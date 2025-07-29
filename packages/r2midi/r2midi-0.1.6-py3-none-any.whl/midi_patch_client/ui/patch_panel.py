from typing import Dict, List, Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, 
    QLabel, QTextEdit, QComboBox, QGroupBox
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QColor, QBrush

from ..models import Patch

class PatchPanel(QWidget):
    """Panel for displaying and selecting patches"""

    # Signal emitted when a patch is selected
    patch_selected = pyqtSignal(object)

    # Signal emitted when a patch is double-clicked
    patch_double_clicked = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.patches = []
        self.filtered_patches = []
        self.current_category = None
        self.category_colors = {}
        self.initUI()

    def initUI(self):
        """Initialize the UI components"""
        # Main layout
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        # Left side - Patch selection
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_panel.setLayout(left_layout)

        # Category filter
        filter_box = QGroupBox("Filter by Category")
        filter_layout = QVBoxLayout()
        filter_box.setLayout(filter_layout)

        self.category_combo = QComboBox()
        self.category_combo.addItem("All Categories", None)
        self.category_combo.currentIndexChanged.connect(self.on_category_changed)
        self.category_combo.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.category_combo.setMinimumWidth(200)
        filter_layout.addWidget(self.category_combo)

        left_layout.addWidget(filter_box)

        # Patch list
        list_box = QGroupBox("Patches")
        list_layout = QVBoxLayout()
        list_box.setLayout(list_layout)

        self.patch_list = QListWidget()
        self.patch_list.itemClicked.connect(self.on_patch_clicked)
        self.patch_list.itemDoubleClicked.connect(self.on_patch_double_clicked)
        list_layout.addWidget(self.patch_list)

        left_layout.addWidget(list_box)

        # Right side - Patch details
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_panel.setLayout(right_layout)

        details_box = QGroupBox("Patch Details")
        details_layout = QVBoxLayout()
        details_box.setLayout(details_layout)

        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        details_layout.addWidget(self.details_text)

        right_layout.addWidget(details_box)

        # Add panels to main layout
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 1)

    def set_patches(self, patches: List[Patch]):
        """Set the patches to display"""
        self.patches = patches

        # Extract unique categories and assign colors
        categories = sorted(set(patch.category for patch in patches))

        # Generate colors for categories
        self.category_colors = {}
        hue_step = 360 / (len(categories) or 1)
        for i, category in enumerate(categories):
            # Create a pastel color with HSV
            hue = i * hue_step
            self.category_colors[category] = QColor.fromHsv(int(hue), 120, 240)

        # Update category combo box
        self.category_combo.clear()
        self.category_combo.addItem("All Categories", None)
        for category in categories:
            self.category_combo.addItem(category, category)

        self.update_display()

    def filter_by_category(self, category: Optional[str]):
        """Filter patches by category"""
        self.current_category = category
        self.update_display()

    def update_display(self):
        """Update the patch display based on current filters"""
        self.patch_list.clear()

        # Filter patches by category if needed
        if self.current_category:
            self.filtered_patches = [p for p in self.patches if p.category == self.current_category]
        else:
            self.filtered_patches = self.patches

        # Add patches to list widget
        for patch in self.filtered_patches:
            item = QListWidgetItem(patch.get_display_name())

            # Set background color based on category
            if patch.category in self.category_colors:
                item.setBackground(QBrush(self.category_colors[patch.category]))

            # Store the patch object with the item
            item.setData(Qt.ItemDataRole.UserRole, patch)

            self.patch_list.addItem(item)

    def on_category_changed(self, index):
        """Handle category selection change"""
        category = self.category_combo.itemData(index)
        self.filter_by_category(category)

    def on_patch_clicked(self, item):
        """Handle patch selection"""
        patch = item.data(Qt.ItemDataRole.UserRole)
        if patch:
            # Update details display
            self.details_text.setText(patch.get_details())

            # Emit signal
            self.patch_selected.emit(patch)

    def on_patch_double_clicked(self, item):
        """Handle patch double-click"""
        patch = item.data(Qt.ItemDataRole.UserRole)
        if patch:
            # Update details display (same as single click)
            self.details_text.setText(patch.get_details())

            # Emit both signals - first select the patch, then emit double-click
            self.patch_selected.emit(patch)
            self.patch_double_clicked.emit(patch)
