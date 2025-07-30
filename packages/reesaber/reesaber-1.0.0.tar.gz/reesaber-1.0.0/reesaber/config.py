"""Configuration management for ReeSaber sabers."""

import json
import logging
import os
from typing import Any, Dict, List, Optional

from PIL import Image
from pydantic import BaseModel, Field

from reesaber.models.base import Color, Transform, Vector3
from reesaber.models.control import ControlPoint
from reesaber.modules.base import SaberModule
from reesaber.modules.blur_saber import BlurSaber, BlurSaberConfig

class SaberConfig(BaseModel):
    """
    Manages a complete ReeSaber configuration.
    
    This class allows creating and exporting full saber configurations with multiple modules.
    
    Example:
        ```python
        # Create a saber configuration
        config = SaberConfig()
        
        # Add a red blur saber
        config.add_module(BlurSaber.create("Red Saber", Color.red()))
        
        # Add a trail
        config.add_module(SimpleTrail.create("Red Trail", Color.red()))
        
        # Export the configuration
        config.export("my_saber.json")
        ```
    """
    mod_version: str = Field(default="0.3.9", description="ReeSabers mod version")
    version: int = Field(default=1, description="Configuration version")
    local_transform: Transform = Field(default_factory=Transform, description="Global transform for all modules")
    modules: List[SaberModule] = Field(default_factory=list, description="List of saber modules")
    
    def add_module(self, module: SaberModule) -> None:
        """
        Add a module to this configuration.
        
        Args:
            module: The SaberModule to add
        """
        self.modules.append(module)
        
    def create_from_image(
        self, 
        image_path: str, 
        pixel_size: float = 0.02, 
        spacing: float = 0.005,
        base_z: float = 0.0
    ) -> None:
        """
        Create a configuration from an image, with each pixel represented by a saber.
        
        Args:
            image_path: Path to the image file
            pixel_size: Size of each pixel saber
            spacing: Spacing between pixel sabers
            base_z: Base Z position for the configuration
            
        Raises:
            FileNotFoundError: If the image file does not exist
            ValueError: If the image cannot be processed
        """
        try:
            # Validate the image path
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image file not found: {image_path}")
                
            # Open and process the image
            with Image.open(image_path) as img:
                img = img.convert("RGBA")
                width, height = img.size
                
                # Calculate total width and height for centering
                total_width = width * (pixel_size + spacing) - spacing
                total_height = height * (pixel_size + spacing) - spacing
                
                # Clear any existing modules
                self.modules = []
                
                # Create a saber for each pixel
                for y in range(height):
                    for x in range(width):
                        # Get pixel color
                        r, g, b, a = img.getpixel((x, y))
                        
                        # Skip fully transparent pixels
                        if a == 0:
                            continue
                            
                        # Calculate position (centered)
                        pos_x = (x * (pixel_size + spacing)) - (total_width / 2)
                        pos_y = -((y * (pixel_size + spacing)) - (total_height / 2))
                        pos_z = base_z
                        
                        # Create a BlurSaber with the pixel color
                        pixel_color = Color.from_rgb(r, g, b, a)
                        
                        # Create transform for this pixel
                        transform = Transform(position=Vector3(x=pos_x, y=pos_y, z=pos_z))
                        
                        # Create the BlurSaber configuration
                        config = BlurSaberConfig(
                            name=f"Pixel_{x}_{y}",
                            local_transform=transform,
                            z_offset_from=0,
                            z_offset_to=0.01,
                            saber_thickness=1.0,
                            blur_frames=0,
                            glow_multiplier=0,
                            handle_color=Color.transparent()
                        )
                        
                        # Set the blade color
                        config.blade_mappings.color_over_value.control_points = [
                            ControlPoint(time=0.0, value=pixel_color)
                        ]
                        
                        # Add the saber to the configuration
                        self.add_module(BlurSaber(config=config))
                        
                logging.info(f"Created {len(self.modules)} pixel sabers from image")
                
        except Exception as e:
            logging.error(f"Error creating sabers from image: {e}")
            raise ValueError(f"Failed to process image: {e}")
        
    def export(self, filepath: str) -> None:
        """
        Export the configuration to a JSON file.
        
        Args:
            filepath: Path to save the JSON file
            
        Raises:
            IOError: If the file cannot be written
        """
        try:
            # Create the configuration dictionary
            config = {
                "ModVersion": self.mod_version,
                "Version": self.version,
                "LocalTransform": {
                    "Position": self.local_transform.position.model_dump(),
                    "Rotation": self.local_transform.rotation.model_dump(),
                    "Scale": self.local_transform.scale.model_dump()
                },
                "Modules": [module.model_dump_json() for module in self.modules],
            }
            
            # Write to file
            with open(filepath, "w") as f:
                json.dump(config, f, indent=2)
                
            logging.info(f"Exported configuration to {filepath}")
            
        except Exception as e:
            logging.error(f"Failed to export configuration: {e}")
            raise IOError(f"Failed to export configuration: {e}")
    
    @classmethod
    def from_json(cls, filepath: str) -> "SaberConfig":
        """
        Load a SaberConfig from a JSON file.
        
        Args:
            filepath: Path to the JSON file
            
        Returns:
            A SaberConfig instance
            
        Raises:
            FileNotFoundError: If the file does not exist
            ValueError: If the file cannot be parsed
        """
        try:
            with open(filepath, "r") as f:
                data = json.load(f)
                
            # Create base config
            config = cls(
                mod_version=data.get("ModVersion", "0.3.9"),
                version=data.get("Version", 1)
            )
            
            # Parse local transform
            transform_data = data.get("LocalTransform", {})
            position_data = transform_data.get("Position", {})
            rotation_data = transform_data.get("Rotation", {})
            scale_data = transform_data.get("Scale", {})
            
            config.local_transform = Transform(
                position=Vector3(**position_data),
                rotation=Vector3(**rotation_data),
                scale=Vector3(**scale_data)
            )
            
            # Parse modules
            for module_data in data.get("Modules", []):
                module_id = module_data.get("ModuleId", "")
                
                if module_id == "reezonate.blur-saber":
                    # TODO: Implement proper module loading
                    # This would require parsing the full hierarchy
                    pass
                    
            return config
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file not found: {filepath}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in config file: {e}")
        except Exception as e:
            logging.error(f"Error loading config from JSON: {e}")
            raise ValueError(f"Failed to load config: {e}")