"""BlurSaber module for ReeSaber configurations."""

from typing import Any, Dict, List, Optional
from pydantic import Field, Literal

from reesaber.models.base import Color
from reesaber.models.control import CompositeMappings, ControlPoint
from reesaber.models.driver import Driver
from reesaber.modules.base import ModuleBase, SaberModule

class BlurSaberConfig(ModuleBase):
    """Configuration for BlurSaber module."""
    z_offset_from: float = Field(default=-0.17, description="Start position of the saber blade")
    z_offset_to: float = Field(default=1.0, description="End position of the saber blade")
    saber_thickness: float = Field(default=1.0, ge=0.0, description="Thickness of the saber blade")
    start_cap: bool = Field(default=True, description="Whether to include a start cap on the blade")
    end_cap: bool = Field(default=True, description="Whether to include an end cap on the blade")
    vertical_resolution: int = Field(default=20, ge=1, description="Vertical resolution of the saber mesh")
    horizontal_resolution: int = Field(default=10, ge=1, description="Horizontal resolution of the saber mesh")
    blur_frames: float = Field(default=2.0, ge=0.0, description="Number of frames to use for blur effect")
    glow_multiplier: float = Field(default=1.0, ge=0.0, description="Multiplier for the glow effect")
    handle_roughness: float = Field(default=2.0, ge=0.0, description="Roughness of the handle material")
    handle_color: Color = Field(default_factory=Color.black, description="Color of the handle")
    render_queue: int = Field(default=3002, description="Render queue value for the saber")
    cull_mode: int = Field(default=0, ge=0, le=2, description="Culling mode for rendering")
    depth_write: bool = Field(default=False, description="Whether to write to the depth buffer")
    
    # Advanced settings
    blade_mask_resolution: int = Field(default=256, ge=8, description="Resolution of the blade mask texture")
    drivers_mask_resolution: int = Field(default=32, ge=8, description="Resolution of the drivers mask texture")
    handle_mask: Dict[str, Any] = Field(default=None, description="Handle mask configuration")
    blade_mappings: CompositeMappings = Field(default_factory=CompositeMappings, description="Blade mappings")
    drivers_sample_mode: int = Field(default=0, ge=0, le=1, description="Sample mode for drivers")
    viewing_angle_mappings: CompositeMappings = Field(default_factory=CompositeMappings, description="Viewing angle mappings")
    surface_angle_mappings: CompositeMappings = Field(default_factory=CompositeMappings, description="Surface angle mappings")
    saber_profile: Dict[str, Any] = Field(default=None, description="Saber profile configuration")
    drivers: List[Driver] = Field(default_factory=lambda: [Driver() for _ in range(4)], description="Drivers for this saber")
    
    def model_post_init(self, __context: Any) -> None:
        """Initialize default settings if not specified."""
        if self.handle_mask is None:
            self.handle_mask = {
                "interpolationType": 2,
                "controlPoints": [
                    {"time": 0.0, "value": 0.0},
                    {"time": 0.028, "value": 1.0},
                    {"time": 0.128, "value": 0.0},
                    {"time": 0.145, "value": 1.0},
                    {"time": 0.17, "value": 0.0},
                ],
            }
            
        if self.saber_profile is None:
            self.saber_profile = {
                "interpolationType": 1,
                "controlPoints": [
                    {"time": 0.0, "value": 1.0}, 
                    {"time": 1.0, "value": 1.0}
                ],
            }


class BlurSaber(SaberModule):
    """
    Represents a Blur Saber module for ReeSabers.
    
    This module creates a saber with blur effects and customizable properties.
    
    Example:
        ```python
        # Create a basic red blur saber
        saber = BlurSaber(
            name="Red Saber",
            config=BlurSaberConfig(
                z_offset_from=-0.17,
                z_offset_to=1.0,
                saber_thickness=1.0,
                blur_frames=2.0,
                glow_multiplier=1.5,
            )
        )
        
        # Configure the blade color to red
        saber.config.blade_mappings.color_over_value.control_points = [
            ControlPoint(time=0.0, value=Color.red())
        ]
        ```
    """
    module_id: str = Field(default="reezonate.blur-saber", Literal=True)
    config: BlurSaberConfig
    
    def _dump_config(self) -> Dict[str, Any]:
        """Convert module-specific config to dictionary."""
        result = super()._dump_config()
        
        # Add BlurSaber-specific configuration
        result["SaberSettings"] = {
            "zOffsetFrom": self.config.z_offset_from,
            "zOffsetTo": self.config.z_offset_to,
            "thickness": self.config.saber_thickness,
            "saberProfile": self.config.saber_profile,
            "startCap": self.config.start_cap,
            "endCap": self.config.end_cap,
            "verticalResolution": self.config.vertical_resolution,
            "horizontalResolution": self.config.horizontal_resolution,
            "renderQueue": self.config.render_queue,
            "cullMode": self.config.cull_mode,
            "depthWrite": self.config.depth_write,
            "blurFrames": self.config.blur_frames,
            "glowMultiplier": self.config.glow_multiplier,
            "handleRoughness": self.config.handle_roughness,
            "handleColor": self.config.handle_color.model_dump(),
            "maskSettings": {
                "bladeMaskResolution": self.config.blade_mask_resolution,
                "driversMaskResolution": self.config.drivers_mask_resolution,
                "handleMask": self.config.handle_mask,
                "bladeMappings": self.config.blade_mappings.model_dump_json(),
                "driversSampleMode": self.config.drivers_sample_mode,
                "viewingAngleMappings": self.config.viewing_angle_mappings.model_dump_json(),
                "surfaceAngleMappings": self.config.surface_angle_mappings.model_dump_json(),
                "drivers": [driver.model_dump_json() for driver in self.config.drivers],
            },
        }
        
        return result
    
    @classmethod
    def create(cls, name: str, color: Color, length: float = 1.0, glow: float = 1.0) -> "BlurSaber":
        """
        Create a BlurSaber with basic settings.
        
        Args:
            name: Display name for the saber
            color: Main color of the saber blade
            length: Length of the saber blade
            glow: Glow multiplier (0.0 - no glow, higher values = more glow)
            
        Returns:
            A configured BlurSaber instance
        """
        config = BlurSaberConfig(
            name=name,
            z_offset_from=-0.17,
            z_offset_to=length,
            glow_multiplier=glow
        )
        
        # Set blade color
        config.blade_mappings.color_over_value.control_points = [
            ControlPoint(time=0.0, value=color)
        ]
        
        # Configure a velocity driver
        config.drivers[0] = Driver.velocity_driver(color)
        
        return cls(config=config)