import os
import json
import logging
from typing import Dict, List, Optional
from models import Device, Patch

# Get logger
logger = logging.getLogger(__name__)

class DeviceManager:
    """Handles scanning and managing device data"""

    def __init__(self, devices_folder="devices"):
        """Initialize the device manager with the path to the devices folder"""
        self.devices_folder = devices_folder
        self.devices = {}  # Map of device name to device data

    def scan_devices(self) -> Dict[str, Dict]:
        """
        Scan devices folder for JSON files and load them into memory
        Returns a dictionary of device names to device data
        """
        logger.info(f"Scanning devices folder: {self.devices_folder}")

        # Clear existing devices
        self.devices = {}

        # Check if devices folder exists
        if not os.path.exists(self.devices_folder):
            logger.warning(f"Devices folder '{self.devices_folder}' does not exist")
            return {}

        try:
            # Get list of JSON files in devices folder
            json_files = [f for f in os.listdir(self.devices_folder) if f.endswith('.json')]
            logger.info(f"Found {len(json_files)} JSON files in devices folder")

            # Process each JSON file
            for filename in json_files:
                file_path = os.path.join(self.devices_folder, filename)
                logger.debug(f"Processing device file: {filename}")

                try:
                    with open(file_path, 'r') as f:
                        device_data = json.load(f)

                        # Check if device has a name
                        if 'name' in device_data:
                            device_name = device_data['name']
                            self.devices[device_name] = device_data
                            logger.info(f"Loaded device: {device_name}")
                        else:
                            logger.warning(f"Device file '{filename}' does not have a name field")
                except json.JSONDecodeError as e:
                    logger.error(f"Invalid JSON in device file '{filename}': {str(e)}")
                except Exception as e:
                    logger.error(f"Error loading device file '{filename}': {str(e)}")

            logger.info(f"Loaded {len(self.devices)} devices")
            return self.devices

        except Exception as e:
            logger.error(f"Error scanning devices folder: {str(e)}")
            return self.devices

    def get_device_by_name(self, name: str) -> Optional[Dict]:
        """Get device data by name"""
        logger.debug(f"Getting device by name: {name}")
        device = self.devices.get(name)
        if device:
            logger.debug(f"Found device: {name}")
        else:
            logger.debug(f"Device not found: {name}")
        return device

    def get_all_devices(self) -> List[Device]:
        """
        Get all devices with their MIDI ports and channels
        Returns a list of Device objects
        """
        logger.info(f"Getting all devices ({len(self.devices)} available)")
        result = []

        try:
            for name, data in self.devices.items():
                try:
                    device = Device(
                        name=name,
                        midi_port=data.get('midi_ports'),
                        midi_channel=data.get('midi_channels')
                    )
                    result.append(device)
                    logger.debug(f"Added device: {name}, MIDI ports: {data.get('midi_ports')}, MIDI channels: {data.get('midi_channels')}")
                except Exception as e:
                    logger.error(f"Error creating Device object for {name}: {str(e)}")

            logger.info(f"Returning {len(result)} devices")
            return result
        except Exception as e:
            logger.error(f"Error getting all devices: {str(e)}")
            return result

    def get_all_patches(self) -> List[Patch]:
        """
        Get all patches from all devices
        Returns a list of Patch objects
        """
        logger.info("Getting all patches from all devices")
        result = []

        try:
            patch_count = 0

            for device_name, device_data in self.devices.items():
                logger.debug(f"Processing device: {device_name}")

                if 'presets' in device_data:
                    presets = device_data['presets']
                    logger.debug(f"Device {device_name} has {len(presets)} presets")

                    for preset in presets:
                        try:
                            patch = Patch(
                                preset_name=preset.get('preset_name', ''),
                                category=preset.get('category', ''),
                                characters=preset.get('characters', []),
                                sendmidi_command=preset.get('sendmidi_command', ''),
                                cc_0=preset.get('cc_0'),
                                pgm=preset.get('pgm')
                            )
                            result.append(patch)
                            patch_count += 1
                            logger.debug(f"Added patch: {patch.preset_name} ({patch.category})")
                        except Exception as e:
                            preset_name = preset.get('preset_name', 'unknown')
                            logger.error(f"Error creating Patch object for {preset_name}: {str(e)}")
                else:
                    logger.debug(f"Device {device_name} has no presets")

            logger.info(f"Returning {patch_count} patches from {len(self.devices)} devices")
            return result
        except Exception as e:
            logger.error(f"Error getting all patches: {str(e)}")
            return result

    def get_patch_by_name(self, preset_name: str) -> Optional[Dict]:
        """Get patch data by preset name"""
        for device_data in self.devices.values():
            if 'presets' in device_data:
                for preset in device_data['presets']:
                    if preset.get('preset_name') == preset_name:
                        return preset
        return None
