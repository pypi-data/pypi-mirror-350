from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class Device:
    """Client-side model for device information"""
    name: str
    midi_port: Optional[Dict[str, str]] = None
    midi_channel: Optional[Dict[str, int]] = None

@dataclass
class Patch:
    """Client-side model for patch information"""
    preset_name: str
    category: str
    characters: Optional[List[str]] = None
    sendmidi_command: Optional[str] = None
    cc_0: Optional[int] = None
    pgm: Optional[int] = None
    
    def get_display_name(self) -> str:
        """Get a formatted display name for the patch"""
        return f"{self.preset_name} ({self.category})"
    
    def get_details(self) -> str:
        """Get detailed information about the patch"""
        details = [f"Name: {self.preset_name}", f"Category: {self.category}"]
        
        if self.characters:
            details.append(f"Characters: {', '.join(self.characters)}")
        
        if self.cc_0 is not None and self.pgm is not None:
            details.append(f"CC 0: {self.cc_0}, Program: {self.pgm}")
            
        return "\n".join(details)