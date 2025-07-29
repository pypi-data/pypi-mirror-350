from typing import Dict, List, Optional, Callable
import logging
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, 
    QGroupBox, QFormLayout, QSpinBox
)
from PyQt6.QtCore import pyqtSignal

from ..models import Device

# Configure logger
logger = logging.getLogger('midi_patch_client.ui.device_panel')

class DevicePanel(QWidget):
    """Panel for device and MIDI port selection"""

    # Signals emitted when selections change
    device_changed = pyqtSignal(str)
    midi_in_port_changed = pyqtSignal(str)
    midi_out_port_changed = pyqtSignal(str)
    sequencer_port_changed = pyqtSignal(str)
    midi_channel_changed = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.devices = []
        self.midi_ports = {"in": [], "out": []}
        self.current_device = None
        self.initUI()

    def initUI(self):
        """Initialize the UI components"""
        # Main layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Device selection
        device_box = QGroupBox("Device Selection")
        device_layout = QFormLayout()
        device_box.setLayout(device_layout)

        self.device_combo = QComboBox()
        self.device_combo.currentTextChanged.connect(self.on_device_changed)
        # Set size policy to adjust to content
        self.device_combo.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        # Set a minimum width to ensure text is visible
        self.device_combo.setMinimumWidth(200)
        device_layout.addRow("Device:", self.device_combo)

        main_layout.addWidget(device_box)

        # MIDI port selection
        port_box = QGroupBox("MIDI Port Configuration")
        port_layout = QFormLayout()
        port_box.setLayout(port_layout)

        self.midi_in_combo = QComboBox()
        self.midi_in_combo.currentTextChanged.connect(self.on_midi_in_port_changed)
        self.midi_in_combo.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.midi_in_combo.setMinimumWidth(200)
        port_layout.addRow("MIDI In Port:", self.midi_in_combo)

        self.midi_out_combo = QComboBox()
        self.midi_out_combo.currentTextChanged.connect(self.on_midi_out_port_changed)
        self.midi_out_combo.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.midi_out_combo.setMinimumWidth(200)
        port_layout.addRow("MIDI Out Port:", self.midi_out_combo)

        self.sequencer_combo = QComboBox()
        self.sequencer_combo.addItem("None", None)
        self.sequencer_combo.currentTextChanged.connect(self.on_sequencer_port_changed)
        self.sequencer_combo.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.sequencer_combo.setMinimumWidth(200)
        port_layout.addRow("Sequencer Port:", self.sequencer_combo)

        self.channel_spin = QSpinBox()
        self.channel_spin.setMinimum(1)
        self.channel_spin.setMaximum(16)
        self.channel_spin.setValue(1)
        self.channel_spin.valueChanged.connect(self.on_midi_channel_changed)
        port_layout.addRow("MIDI Channel:", self.channel_spin)

        main_layout.addWidget(port_box)

    def set_devices(self, devices: List[Device]):
        """Set the available devices"""
        logger.info(f"Setting devices: {[d.name for d in devices]}")
        self.devices = devices

        # Update device combo box
        self.device_combo.clear()
        for device in devices:
            logger.info(f"Adding device to combo box: {device.name}")
            self.device_combo.addItem(device.name)

        # Select first device if available
        if devices:
            self.current_device = devices[0]
            logger.info(f"Selected first device: {self.current_device.name}")
            self.update_midi_channels()
            # Note: We don't call update_midi_ports_from_device() here because
            # MIDI ports might not be loaded yet. The main_window.py will call
            # set_midi_ports after this, and then we'll update the ports in
            # on_device_changed when the user selects a device.

    def set_midi_ports(self, ports: Dict[str, List[str]]):
        """Set the available MIDI ports"""
        logger.info(f"Setting MIDI ports: in={ports.get('in', [])}, out={ports.get('out', [])}")
        self.midi_ports = ports

        # Update MIDI in port combo box
        self.midi_in_combo.clear()
        for port in ports.get("in", []):
            logger.info(f"Adding MIDI in port to combo box: {port}")
            self.midi_in_combo.addItem(port)

        # Update MIDI out port combo box
        self.midi_out_combo.clear()
        for port in ports.get("out", []):
            logger.info(f"Adding MIDI out port to combo box: {port}")
            self.midi_out_combo.addItem(port)

        # Update sequencer port combo box (use out ports)
        self.sequencer_combo.clear()
        self.sequencer_combo.addItem("None", None)
        for port in ports.get("out", []):
            logger.info(f"Adding sequencer port to combo box: {port}")
            self.sequencer_combo.addItem(port)

        # Now that MIDI ports are loaded, update the ports based on the selected device
        if self.current_device:
            logger.info(f"Updating MIDI ports from device: {self.current_device.name}")
            self.update_midi_ports_from_device()

    def update_midi_channels(self):
        """Update MIDI channel based on selected device"""
        if self.current_device and self.current_device.midi_channel:
            # Use the OUT channel if available
            channel = self.current_device.midi_channel.get("OUT", 1)
            self.channel_spin.setValue(channel)

    def update_midi_ports_from_device(self):
        """Update MIDI ports based on selected device"""
        if not self.current_device:
            logger.info("No current device selected, cannot update MIDI ports")
            return
        if not self.current_device.midi_port:
            logger.info(f"Device {self.current_device.name} has no MIDI ports defined")
            return

        logger.info(f"Updating MIDI ports from device: {self.current_device.name}, ports: {self.current_device.midi_port}")

        # Set MIDI in port if available
        in_port = self.current_device.midi_port.get("IN")
        if in_port and self.midi_in_combo.count() > 0:
            logger.info(f"Setting MIDI in port to: {in_port}")
            index = self.midi_in_combo.findText(in_port)
            if index >= 0:
                logger.info(f"Found MIDI in port at index {index}")
                self.midi_in_combo.setCurrentIndex(index)
            else:
                logger.info(f"MIDI in port {in_port} not found in combo box")

        # Set MIDI out port if available
        out_port = self.current_device.midi_port.get("OUT")
        if out_port and self.midi_out_combo.count() > 0:
            logger.info(f"Setting MIDI out port to: {out_port}")
            index = self.midi_out_combo.findText(out_port)
            if index >= 0:
                logger.info(f"Found MIDI out port at index {index}")
                self.midi_out_combo.setCurrentIndex(index)
            else:
                logger.info(f"MIDI out port {out_port} not found in combo box")

    def get_selected_device(self) -> Optional[str]:
        """Get the name of the selected device"""
        return self.device_combo.currentText() if self.device_combo.count() > 0 else None

    def get_selected_midi_in_port(self) -> Optional[str]:
        """Get the selected MIDI in port"""
        return self.midi_in_combo.currentText() if self.midi_in_combo.count() > 0 else None

    def get_selected_midi_out_port(self) -> Optional[str]:
        """Get the selected MIDI out port"""
        return self.midi_out_combo.currentText() if self.midi_out_combo.count() > 0 else None

    def get_selected_sequencer_port(self) -> Optional[str]:
        """Get the selected sequencer port"""
        text = self.sequencer_combo.currentText()
        return None if text == "None" else text

    def get_selected_midi_channel(self) -> int:
        """Get the selected MIDI channel"""
        return self.channel_spin.value()

    # Event handlers
    def on_device_changed(self, device_name: str):
        """Handle device selection change"""
        # Find the selected device
        for device in self.devices:
            if device.name == device_name:
                self.current_device = device
                self.update_midi_channels()
                self.update_midi_ports_from_device()
                break

        self.device_changed.emit(device_name)

    def on_midi_in_port_changed(self, port_name: str):
        """Handle MIDI in port selection change"""
        self.midi_in_port_changed.emit(port_name)

    def on_midi_out_port_changed(self, port_name: str):
        """Handle MIDI out port selection change"""
        self.midi_out_port_changed.emit(port_name)

    def on_sequencer_port_changed(self, port_name: str):
        """Handle sequencer port selection change"""
        if port_name == "None":
            self.sequencer_port_changed.emit("")
        else:
            self.sequencer_port_changed.emit(port_name)

        # Update the main window's selected_sequencer_port
        # This ensures the port is updated even if the signal is not connected
        if hasattr(self.parent(), "selected_sequencer_port"):
            if port_name == "None":
                self.parent().selected_sequencer_port = None
            else:
                self.parent().selected_sequencer_port = port_name

    def on_midi_channel_changed(self, channel: int):
        """Handle MIDI channel selection change"""
        self.midi_channel_changed.emit(channel)
