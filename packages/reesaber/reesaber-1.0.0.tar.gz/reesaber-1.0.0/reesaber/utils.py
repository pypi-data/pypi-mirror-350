"""Utility functions for ReeSaber configurations."""

import logging
import os
from typing import Dict, List

from reesaber.models.base import Color
from reesaber.models.control import ControlPoint
from reesaber.models.driver import Driver, DriverType
from reesaber.modules.base import SaberModule
from reesaber.modules.blur_saber import BlurSaber
from reesaber.config import SaberConfig

def configure_logging(level=logging.INFO, filename="ReeSaber_Python.log"):
    """
    Configure logging for the ReeSaber module.
    
    Args:
        level: The logging level
        filename: The log file name
    """
    logging.basicConfig(
        filename=filename,
        level=level,
        format="%(asctime)s - [%(levelname)s] - %(message)s",
    )
    logging.info("Logging configured")
    
def create_gradient_saber(name: str, start_color: Color, end_color: Color, length: float = 1.0) -> BlurSaber:
    """Create a saber with a gradient from start to end color."""
    saber = BlurSaber.create(name, start_color, length)
    
    # Set up gradient
    saber.config.blade_mappings.color_over_value.control_points = [
        ControlPoint(time=0.0, value=start_color),
        ControlPoint(time=1.0, value=end_color)
    ]
    
    return saber

def color_palette(name: str) -> List[Color]:
    """
    Create a color palette.
    
    Args:
        name: Name of the palette ('rainbow', 'fire', etc.)
        
    Returns:
        List of Color objects
    """
    if name.lower() == "rainbow":
        return [
            Color(r=1.0, g=0.0, b=0.0),  # Red
            Color(r=1.0, g=0.5, b=0.0),  # Orange
            Color(r=1.0, g=1.0, b=0.0),  # Yellow
            Color(r=0.0, g=1.0, b=0.0),  # Green
            Color(r=0.0, g=0.0, b=1.0),  # Blue
            Color(r=0.5, g=0.0, b=1.0),  # Indigo
            Color(r=1.0, g=0.0, b=1.0),  # Violet
        ]
    elif name.lower() == "fire":
        return [
            Color(r=1.0, g=0.0, b=0.0),  # Red
            Color(r=1.0, g=0.5, b=0.0),  # Orange
            Color(r=1.0, g=1.0, b=0.0),  # Yellow
        ]
    else:
        # Default to white
        return [Color.white()]

def create_rainbow_saber(name: str = "Rainbow Saber") -> SaberConfig:
    """Create a rainbow color changing saber."""
    config = SaberConfig()
    
    saber = BlurSaber.create(name, Color.red(), length=1.0, glow=1.5)
    
    # Set up time-based color driver
    driver = Driver(
        driver_type=DriverType.TIME_DEPENDENCE,
        increase_resistance=0.0,
        decrease_resistance=0.0
    )
    
    # Rainbow colors
    rainbow_colors = color_palette("rainbow")
    control_points = []
    
    for i, color in enumerate(rainbow_colors):
        time = i / (len(rainbow_colors) - 1) if len(rainbow_colors) > 1 else 0
        control_points.append(ControlPoint(time=time, value=color))
    
    driver.mappings.color_over_value.control_points = control_points
    driver.mappings.value_from = 0.0
    driver.mappings.value_to = 10.0  # This creates a 10-second cycle
    
    saber.config.drivers[0] = driver
    
    config.add_module(saber)
    
    return config

def clone_module(module: SaberModule) -> SaberModule:
    """Create a deep copy of a module."""
    from reesaber.modules.blur_saber import BlurSaber, BlurSaberConfig
    from reesaber.modules.simple_trail import SimpleTrail, SimpleTrailConfig
    from reesaber.modules.vanilla_saber import VanillaSaber, VanillaSaberConfig
    
    if isinstance(module, BlurSaber):
        return BlurSaber(config=BlurSaberConfig(**module.config.model_dump()))
    elif isinstance(module, SimpleTrail):
        return SimpleTrail(config=SimpleTrailConfig(**module.config.model_dump()))
    elif isinstance(module, VanillaSaber):
        return VanillaSaber(config=VanillaSaberConfig(**module.config.model_dump()))
    else:
        raise ValueError(f"Unknown module type: {type(module)}")

def merge_configs(configs: List[SaberConfig]) -> SaberConfig:
    """Merge multiple saber configurations into one."""
    merged = SaberConfig()
    
    for config in configs:
        for module in config.modules:
            merged.add_module(clone_module(module))
            
    return merged

def export_config_for_all_sabers(configs: Dict[str, SaberConfig], output_dir: str) -> None:
    """Export multiple saber configurations to separate files."""
    os.makedirs(output_dir, exist_ok=True)
    
    for name, config in configs.items():
        safe_name = "".join(c for c in name if c.isalnum() or c in "_ -").replace(" ", "_")
        filepath = os.path.join(output_dir, f"{safe_name}.json")
        config.export(filepath)