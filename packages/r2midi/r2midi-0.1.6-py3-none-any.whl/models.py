from typing import Dict, List, Optional
from pydantic import BaseModel

class Device(BaseModel):
    """Model for device information"""
    name: str
    midi_port: Optional[Dict[str, str]] = None
    midi_channel: Optional[Dict[str, int]] = None

class Patch(BaseModel):
    """Model for patch information"""
    preset_name: str
    category: str
    characters: Optional[List[str]] = None
    sendmidi_command: Optional[str] = None
    cc_0: Optional[int] = None
    pgm: Optional[int] = None

class PresetRequest(BaseModel):
    """Model for preset selection request"""
    preset_name: str
    midi_port: str
    midi_channel: int
    sequencer_port: Optional[str] = None