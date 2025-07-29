import asyncio
import json
import logging
from typing import Dict, List, Optional, Any
import httpx

from .models import Device, Patch

# Configure logger
logger = logging.getLogger('midi_patch_client.api_client')

class ApiClient:
    """Client for communicating with the MIDI Patch Selection API"""

    def __init__(self, base_url: str = "http://localhost:7777"):
        """
        Initialize the API client

        Args:
            base_url: Base URL of the server API
        """
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=base_url, timeout=10.0)

    async def get_devices(self) -> List[Device]:
        """
        Fetch devices from server

        Returns:
            List of Device objects
        """
        try:
            logger.info("Fetching devices from server...")
            response = await self.client.get("/devices")
            response.raise_for_status()

            devices_data = response.json()
            devices = [Device(**device) for device in devices_data]
            logger.info(f"Fetched {len(devices)} devices: {[d.name for d in devices]}")
            return devices

        except httpx.HTTPError as e:
            logger.error(f"Error fetching devices: {str(e)}")
            return []

    async def get_patches(self) -> List[Patch]:
        """
        Fetch patches from server

        Returns:
            List of Patch objects
        """
        try:
            logger.info("Fetching patches from server...")
            response = await self.client.get("/patches")
            response.raise_for_status()

            patches_data = response.json()
            patches = [Patch(**patch) for patch in patches_data]
            logger.info(f"Fetched {len(patches)} patches: {[p.preset_name for p in patches[:5]]}...")
            return patches

        except httpx.HTTPError as e:
            logger.error(f"Error fetching patches: {str(e)}")
            return []

    async def get_midi_ports(self) -> Dict[str, List[str]]:
        """
        Fetch MIDI ports from server

        Returns:
            Dictionary with 'in' and 'out' keys containing lists of port names
        """
        try:
            logger.info("Fetching MIDI ports from server...")
            response = await self.client.get("/midi_port")
            response.raise_for_status()

            ports = response.json()
            logger.info(f"Fetched MIDI ports: in={ports.get('in', [])}, out={ports.get('out', [])}")
            return ports

        except httpx.HTTPError as e:
            logger.error(f"Error fetching MIDI ports: {str(e)}")
            return {"in": [], "out": []}

    async def send_preset(self, preset_name: str, midi_port: str, midi_channel: int, 
                          sequencer_port: Optional[str] = None) -> Dict[str, Any]:
        """
        Send preset selection to server

        Args:
            preset_name: Name of the preset to select
            midi_port: MIDI port to send the command to
            midi_channel: MIDI channel to use
            sequencer_port: Optional sequencer port to send the command to

        Returns:
            Response from the server
        """
        try:
            data = {
                "preset_name": preset_name,
                "midi_port": midi_port,
                "midi_channel": midi_channel
            }

            if sequencer_port:
                data["sequencer_port"] = sequencer_port

            response = await self.client.post("/preset", json=data)
            response.raise_for_status()

            return response.json()

        except httpx.HTTPError as e:
            logger.error(f"Error sending preset: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    return {"status": "error", "message": error_data.get("detail", str(e))}
                except json.JSONDecodeError:
                    pass
            return {"status": "error", "message": str(e)}

    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()
