import logging
import sys
import os
import uvicorn
import threading
import time
import socket
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from device_manager import DeviceManager
from midi_utils import MidiUtils
from models import Device, Patch, PresetRequest
from ui_launcher import UILauncher
from version import __version__

# Configure logging
# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(os.path.join('logs', 'main.log'), mode='a'),
        logging.FileHandler(os.path.join('logs', 'all.log'), mode='a')
    ]
)

# Configure module-specific loggers
device_manager_logger = logging.getLogger('device_manager')
device_manager_logger.setLevel(logging.INFO)
device_manager_handler = logging.FileHandler(os.path.join('logs', 'device_manager.log'), mode='a')
device_manager_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
device_manager_logger.addHandler(device_manager_handler)

midi_utils_logger = logging.getLogger('midi_utils')
midi_utils_logger.setLevel(logging.INFO)
midi_utils_handler = logging.FileHandler(os.path.join('logs', 'midi_utils.log'), mode='a')
midi_utils_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
midi_utils_logger.addHandler(midi_utils_handler)

ui_launcher_logger = logging.getLogger('ui_launcher')
ui_launcher_logger.setLevel(logging.INFO)
ui_launcher_handler = logging.FileHandler(os.path.join('logs', 'ui_launcher.log'), mode='a')
ui_launcher_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
ui_launcher_logger.addHandler(ui_launcher_handler)

logger = logging.getLogger(__name__)

def is_port_in_use(port: int) -> bool:
    """
    Check if a port is already in use

    Args:
        port: Port number to check

    Returns:
        True if the port is in use, False otherwise
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def find_available_port(start_port: int, max_attempts: int = 10) -> int:
    """
    Find an available port starting from start_port

    Args:
        start_port: Port number to start checking from
        max_attempts: Maximum number of ports to check

    Returns:
        An available port number
    """
    port = start_port
    for _ in range(max_attempts):
        if not is_port_in_use(port):
            return port
        port += 1
    # If we couldn't find an available port, return the original port
    # This will likely fail, but it's better than returning an invalid port
    logger.warning(f"Could not find an available port after {max_attempts} attempts")
    return start_port

# Initialize components
device_manager = DeviceManager()
ui_launcher = None  # Will be initialized after server starts with correct URL

# Function to launch UI client after a delay
def launch_ui_client_with_delay(delay_seconds: int = 3):
    """
    Launch the UI client after a specified delay to ensure the server is ready

    Args:
        delay_seconds: Number of seconds to wait before launching the UI client
    """
    global ui_launcher

    # Wait for the server to initialize
    logger.info(f"Waiting {delay_seconds} seconds before launching UI client...")
    time.sleep(delay_seconds)

    # Launch UI client if ui_launcher is initialized
    if ui_launcher:
        logger.info("Launching UI client...")
        success = ui_launcher.launch_client()
        if success:
            logger.info("UI client launched successfully")
        else:
            logger.warning("Failed to launch UI client")
    else:
        logger.warning("UI launcher not initialized, skipping client launch")

# Define lifespan context manager (replaces on_event handlers)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize the application
    logger.info("Application starting up...")

    try:
        # Scan for devices
        logger.info("Scanning for MIDI devices...")
        device_manager.scan_devices()
        logger.info(f"Found {len(device_manager.devices)} devices")

        # Check if SendMIDI is installed
        if not MidiUtils.is_sendmidi_installed():
            logger.warning("SendMIDI is not installed. MIDI commands will not work.")
        else:
            logger.info("SendMIDI is installed and available")
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")

    # Yield control to FastAPI
    yield

    # Shutdown: Clean up resources
    logger.info("Application shutting down...")
    try:
        if ui_launcher:
            ui_launcher.shutdown_client()
            logger.info("UI client shut down")
        else:
            logger.warning("UI launcher not initialized, skipping client shutdown")
    except Exception as e:
        logger.error(f"Error during shutdown: {str(e)}")

# Create FastAPI app with lifespan
app = FastAPI(
    title="MIDI Patch Selection API",
    description="API for selecting MIDI patches and controlling MIDI devices",
    version=__version__,
    lifespan=lifespan
)

# API Routes
@app.get("/devices", response_model=List[Device])
async def get_devices():
    """Return all devices with their MIDI ports and channels"""
    try:
        devices = device_manager.get_all_devices()
        logger.info(f"Returning {len(devices)} devices: {[d.name for d in devices]}")
        for device in devices:
            logger.debug(f"Device: {device.name}, MIDI ports: {device.midi_port}, MIDI channels: {device.midi_channel}")
        return devices
    except Exception as e:
        logger.error(f"Error getting devices: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting devices: {str(e)}")

@app.get("/patches", response_model=List[Patch])
async def get_patches():
    """Return all patches with their preset_name and category"""
    try:
        patches = device_manager.get_all_patches()
        logger.info(f"Returning {len(patches)} patches")
        if patches:
            logger.debug(f"First 5 patches: {[p.preset_name for p in patches[:5]]}")
        return patches
    except Exception as e:
        logger.error(f"Error getting patches: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting patches: {str(e)}")

@app.get("/midi_port", response_model=Dict[str, List[str]])
async def get_midi_ports():
    """Return dictionary of in/out MIDI ports available on the system"""
    try:
        ports = MidiUtils.get_midi_ports()
        logger.info(f"Returning MIDI ports: in={len(ports.get('in', []))}, out={len(ports.get('out', []))}")
        logger.debug(f"MIDI ports details: {ports}")
        return ports
    except Exception as e:
        logger.error(f"Error getting MIDI ports: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting MIDI ports: {str(e)}")

@app.post("/preset")
async def send_preset(preset: PresetRequest):
    """Send MIDI command for specified preset to specified port/channel"""
    logger.info(f"Received preset request: {preset.preset_name} to port {preset.midi_port} on channel {preset.midi_channel}")

    try:
        # Get the patch data
        patch_data = device_manager.get_patch_by_name(preset.preset_name)
        if not patch_data:
            logger.warning(f"Preset '{preset.preset_name}' not found")
            raise HTTPException(status_code=404, detail=f"Preset '{preset.preset_name}' not found")

        # Get the bank select (cc_0) and program change (pgm) values
        cc_0 = patch_data.get('cc_0')
        pgm = patch_data.get('pgm')

        if cc_0 is None or pgm is None:
            logger.warning(f"Missing cc_0 or pgm values for preset '{preset.preset_name}'")
            raise HTTPException(status_code=400, detail=f"Missing cc_0 or pgm values for preset '{preset.preset_name}'")

        # Construct the SendMIDI command using the selected MIDI port, channel, cc_0, and pgm values
        command = f'sendmidi dev "{preset.midi_port}" ch {preset.midi_channel} cc 0 {cc_0} pc {pgm}'
        logger.info(f"Sending MIDI command: {command}")

        # Execute the command
        try:
            success, message = await MidiUtils.asend_midi_command(command, preset.sequencer_port)

            if not success:
                logger.error(f"MIDI command failed: {message}")
                raise HTTPException(status_code=500, detail=message)

            logger.info(f"MIDI command succeeded: {message}")

            # If sequencer port is specified, log it
            if preset.sequencer_port:
                logger.info(f"Also sent to sequencer port: {preset.sequencer_port}")

            return {"status": "success", "message": message}

        except Exception as e:
            logger.error(f"Error executing MIDI command: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error executing MIDI command: {str(e)}")

    except HTTPException:
        # Re-raise HTTP exceptions to preserve their status codes
        raise
    except Exception as e:
        logger.error(f"Unexpected error sending preset: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

# Run the application
if __name__ == '__main__':
    # Get port from environment variable with default of 7777
    requested_port = int(os.getenv("PORT", 7777))

    # Find an available port starting from the requested port
    port = find_available_port(requested_port)

    if port != requested_port:
        logger.info(f"Port {requested_port} is in use, using port {port} instead")

    logger.info(f"Starting server on port {port}")

    # Initialize UI launcher with the correct server URL
    server_url = f"http://localhost:{port}"
    logger.info(f"Server URL: {server_url}")
    ui_launcher = UILauncher(server_url=server_url)

    # Start a thread to launch the UI client after a delay
    ui_thread = threading.Thread(target=launch_ui_client_with_delay, args=(3,))
    ui_thread.daemon = True  # Thread will exit when main thread exits
    ui_thread.start()
    logger.info("UI client launch thread started")

    # Start the server
    logger.info(f"Starting server on port {port}...")

    # Add a log message to indicate server is about to start
    print(f"\n{'='*50}\nServer is starting on http://0.0.0.0:{port}\nPress Ctrl+C to stop\n{'='*50}\n")

    # Configure uvicorn logging to use our logging setup
    uvicorn_log_config = uvicorn.config.LOGGING_CONFIG
    uvicorn_log_config["handlers"]["default"]["stream"] = sys.stdout
    uvicorn_log_config["handlers"]["access"]["stream"] = sys.stdout

    # Add a file handler for uvicorn logs
    uvicorn_log_config["handlers"]["file"] = {
        "class": "logging.FileHandler",
        "formatter": "default",
        "filename": os.path.join('logs', 'uvicorn.log'),
        "mode": "a"
    }
    uvicorn_log_config["loggers"]["uvicorn"]["handlers"].append("file")
    uvicorn_log_config["loggers"]["uvicorn.access"]["handlers"].append("file")

    # Run the server
    uvicorn.run(app, host="0.0.0.0", port=port, log_config=uvicorn_log_config)
