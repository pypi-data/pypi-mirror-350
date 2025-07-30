"""Control point and interpolation models for ReeSaber configurations."""

from enum import IntEnum
from typing import Any, Dict, List, Union
from pydantic import BaseModel, Field

from reesaber.models.base import Color

class InterpolationType(IntEnum):
    """Interpolation types for ReeSaber control points."""
    LINEAR = 0
    EASE_IN_OUT = 1
    EASE_OUT = 2
    EASE_IN = 3
    CONSTANT = 4


class ControlPoint(BaseModel):
    """Represents a control point for interpolation curves."""
    time: float = Field(..., ge=0.0, le=1.0, description="Time value (0-1)")
    value: Union[float, Color] = Field(..., description="Value at this time (float or Color)")


class Mapping(BaseModel):
    """Base class for ReeSaber mappings."""
    interpolation_type: InterpolationType = Field(
        default=InterpolationType.LINEAR, 
        description="Type of interpolation between control points"
    )
    control_points: List[ControlPoint] = Field(
        default_factory=list, 
        description="List of control points"
    )
    value_from: float = Field(default=0.0, description="Minimum input value")
    value_to: float = Field(default=1.0, description="Maximum input value")
    
    class Config:
        populate_by_name = True
        json_encoders = {
            InterpolationType: lambda v: int(v)
        }
    
    def model_dump_json(self, **kwargs) -> Dict[str, Any]:
        """Convert to dictionary representation for JSON serialization."""
        result = {
            "interpolationType": int(self.interpolation_type),
            "controlPoints": [
                {
                    "time": cp.time,
                    "value": cp.value.model_dump() if isinstance(cp.value, Color) else cp.value
                } 
                for cp in self.control_points
            ],
            "valueFrom": self.value_from,
            "valueTo": self.value_to
        }
        return result


class ColorMapping(Mapping):
    """Mapping for color interpolation."""
    
    @classmethod
    def default(cls) -> "ColorMapping":
        """Create a default ColorMapping with white color."""
        return cls(
            interpolation_type=InterpolationType.LINEAR,
            control_points=[
                ControlPoint(time=0.0, value=Color.white())
            ]
        )


class AlphaMapping(Mapping):
    """Mapping for alpha interpolation."""
    
    @classmethod
    def default(cls) -> "AlphaMapping":
        """Create a default AlphaMapping with full opacity."""
        return cls(
            interpolation_type=InterpolationType.LINEAR,
            control_points=[
                ControlPoint(time=0.0, value=1.0),
                ControlPoint(time=1.0, value=1.0)
            ]
        )


class ScaleMapping(Mapping):
    """Mapping for scale interpolation."""
    
    @classmethod
    def default(cls) -> "ScaleMapping":
        """Create a default ScaleMapping with constant scale."""
        return cls(
            interpolation_type=InterpolationType.LINEAR,
            control_points=[
                ControlPoint(time=0.0, value=1.0)
            ]
        )


class CompositeMappings(BaseModel):
    """Represents a composite of color, alpha, and scale mappings."""
    color_over_value: ColorMapping = Field(
        default_factory=ColorMapping.default,
        description="Color mapping over value range"
    )
    alpha_over_value: AlphaMapping = Field(
        default_factory=AlphaMapping.default,
        description="Alpha mapping over value range"
    )
    scale_over_value: Optional[ScaleMapping] = Field(
        default=None,
        description="Scale mapping over value range"
    )
    value_from: float = Field(default=0.0, description="Minimum input value")
    value_to: float = Field(default=1.0, description="Maximum input value")
    
    def model_dump_json(self) -> Dict[str, Any]:
        """Convert to dictionary representation for JSON serialization."""
        result = {
            "colorOverValue": self.color_over_value.model_dump_json(),
            "alphaOverValue": self.alpha_over_value.model_dump_json(),
            "valueFrom": self.value_from,
            "valueTo": self.value_to
        }
        
        if self.scale_over_value:
            result["scaleOverValue"] = self.scale_over_value.model_dump_json()
            
        return result