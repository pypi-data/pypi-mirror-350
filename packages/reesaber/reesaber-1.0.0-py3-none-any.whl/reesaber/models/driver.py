"""Driver models for ReeSaber configurations."""

from enum import IntEnum
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

from reesaber.models.base import Color
from reesaber.models.control import CompositeMappings, ControlPoint, ColorMapping, InterpolationType

class DriverType(IntEnum):
    """Enumeration of all available ReeSaber driver types."""
    NONE = 0
    TIP_VELOCITY = 1
    SWINGS_PER_SECOND = 2
    TIME_DEPENDENCE = 3
    TIP_ACCELERATION = 4
    ANGULAR_VELOCITY = 5
    SCORE_PERCENTAGE = 6
    COMBO = 7
    MISSES = 8
    ENERGY = 9
    MULTIPLIER = 10
    CUT_SCORE = 11
    CUT_ACC_SCORE = 12
    CUT_PRE_SCORE = 13
    CUT_POST_SCORE = 14
    CUTS_PER_SECOND = 15
    TIME_AFTER_CUT = 16
    DIRECTION_X = 17
    DIRECTION_Y = 18
    DIRECTION_Z = 19


class Driver(BaseModel):
    """
    Represents a ReeSaber driver that controls saber effects based on game parameters.
    
    A driver maps gameplay elements (like velocity, score, etc.) to visual effects.
    """
    driver_type: DriverType = Field(
        default=DriverType.NONE, 
        description="Type of driver"
    )
    mappings: CompositeMappings = Field(
        default_factory=CompositeMappings,
        description="Color and alpha mappings"
    )
    increase_resistance: float = Field(
        default=0.0, 
        ge=0.0, 
        description="Resistance to value increases"
    )
    decrease_resistance: float = Field(
        default=0.0, 
        ge=0.0, 
        description="Resistance to value decreases"
    )
    
    class Config:
        populate_by_name = True
        json_encoders = {
            DriverType: lambda v: int(v)
        }
    
    def model_dump_json(self) -> Dict[str, Any]:
        """Convert to dictionary representation for JSON serialization."""
        return {
            "valueType": int(self.driver_type),
            "increaseResistance": self.increase_resistance,
            "decreaseResistance": self.decrease_resistance,
            "mappings": self.mappings.model_dump_json()
        }
    
    @classmethod
    def velocity_driver(cls, color: Optional[Color] = None) -> "Driver":
        """
        Create a driver that responds to saber tip velocity.
        
        Args:
            color: The color to use at maximum velocity (defaults to red)
        """
        color = color or Color.red()
        
        driver = cls(
            driver_type=DriverType.TIP_VELOCITY,
            increase_resistance=0.1,
            decrease_resistance=0.5
        )
        
        # Configure color mapping
        driver.mappings.color_over_value = ColorMapping(
            interpolation_type=InterpolationType.EASE_IN_OUT,
            control_points=[
                ControlPoint(time=0.0, value=Color.white()),
                ControlPoint(time=1.0, value=color)
            ]
        )
        
        return driver