"""SimpleTrail module for ReeSaber configurations."""

from typing import Any, Dict, List, Optional
from pydantic import Field, Literal

from reesaber.models.base import Color
from reesaber.models.control import CompositeMappings, ControlPoint
from reesaber.models.driver import Driver
from reesaber.modules.base import ModuleBase, SaberModule

class SimpleTrailConfig(ModuleBase):
    """Configuration for SimpleTrail module."""
    length: float = Field(default=0.16, ge=0.0, description="Length of the trail")
    trail_type: int = Field(default=1, ge=0, le=2, description="Type of trail effect")
    horizontal_resolution: int = Field(default=4, ge=1, description="Horizontal resolution of the trail mesh")
    vertical_resolution: int = Field(default=60, ge=1, description="Vertical resolution of the trail mesh")
    material_type: int = Field(default=1, ge=0, le=2, description="Type of material to use for the trail")
    offset: float = Field(default=1.0, description="Offset from the saber")
    width: float = Field(default=1.0, ge=0.0, description="Width of the trail")
    mask_resolution: int = Field(default=128, ge=8, description="Resolution of the main mask texture")
    drivers_mask_resolution: int = Field(default=32, ge=8, description="Resolution of the drivers mask texture")
    render_queue: int = Field(default=3000, description="Render queue value for the trail")
    always_on_top: bool = Field(default=False, description="Whether the trail should always render on top")
    blending_mode: int = Field(default=0, ge=0, le=2, description="Blending mode for the trail material")
    
    # Advanced settings
    anim_layout: Dict[str, Any] = Field(default=None, description="Animation layout configuration")
    length_mappings: CompositeMappings = Field(default_factory=CompositeMappings, description="Length mappings configuration")
    width_mappings: CompositeMappings = Field(default_factory=CompositeMappings, description="Width mappings configuration")
    drivers_sample_mode: int = Field(default=0, ge=0, le=1, description="Sample mode for drivers")
    viewing_angle_mappings: CompositeMappings = Field(default_factory=CompositeMappings, description="Viewing angle mappings")
    surface_angle_mappings: CompositeMappings = Field(default_factory=CompositeMappings, description="Surface angle mappings")
    drivers: List[Driver] = Field(default_factory=lambda: [Driver() for _ in range(4)], description="Drivers for this trail")
    
    def model_post_init(self, __context: Any) -> None:
        """Initialize default settings if not specified."""
        if self.anim_layout is None:
            self.anim_layout = {
                "totalFrames": 1,
                "framesPerRow": 1,
                "framesPerColumn": 1,
                "frameDuration": 1.0,
            }


class SimpleTrail(SaberModule):
    """
    Represents a Simple Trail module for ReeSabers.
    
    This module creates a trail effect behind the saber.
    
    Example:
        ```python
        # Create a basic trail with red color
        trail = SimpleTrail(
            config=SimpleTrailConfig(
                name="Red Trail",
                length=0.2,
                width=1.2
            )
        )
        
        # Configure the trail color to red
        trail.config.length_mappings.color_over_value.control_points = [
            ControlPoint(time=0.0, value=Color.red())
        ]
        ```
    """
    module_id: str = Field(default="reezonate.simple-trail", Literal=True)
    config: SimpleTrailConfig
    
    def _dump_config(self) -> Dict[str, Any]:
        """Convert module-specific config to dictionary."""
        result = super()._dump_config()
        
        # Add SimpleTrail-specific configuration
        result["MeshSettings"] = {
            "TrailLength": self.config.length,
            "HorizontalResolution": self.config.horizontal_resolution,
            "VerticalResolution": self.config.vertical_resolution,
        }
        
        result["MaterialSettings"] = {
            "trailType": self.config.trail_type,
            "materialType": self.config.material_type,
            "offset": self.config.offset,
            "width": self.config.width,
            "distortionMultiplier": 1.0,
            "generalSettings": {
                "customTextureId": "",
                "animationLayout": self.config.anim_layout,
                "blendingMode": self.config.blending_mode,
                "alwaysOnTop": self.config.always_on_top,
                "renderQueue": self.config.render_queue,
            },
            "maskSettings": {
                "mainMaskResolution": self.config.mask_resolution,
                "driversMaskResolution": self.config.drivers_mask_resolution,
                "lengthMappings": self.config.length_mappings.model_dump_json(),
                "widthMappings": self.config.width_mappings.model_dump_json(),
                "driversSampleMode": self.config.drivers_sample_mode,
                "viewingAngleMappings": self.config.viewing_angle_mappings.model_dump_json(),
                "surfaceAngleMappings": self.config.surface_angle_mappings.model_dump_json(),
                "drivers": [driver.model_dump_json() for driver in self.config.drivers],
            },
        }
        
        return result
    
    @classmethod
    def create(cls, name: str, color: Color, length: float = 0.2, width: float = 1.0) -> "SimpleTrail":
        """
        Create a SimpleTrail with basic settings.
        
        Args:
            name: Display name for the trail
            color: Main color of the trail
            length: Length of the trail
            width: Width of the trail
            
        Returns:
            A configured SimpleTrail instance
        """
        config = SimpleTrailConfig(
            name=name,
            length=length,
            width=width
        )
        
        # Set trail color
        config.length_mappings.color_over_value.control_points = [
            ControlPoint(time=0.0, value=color)
        ]
        
        # Configure a velocity driver
        config.drivers[0] = Driver.velocity_driver(color)
        
        return cls(config=config)