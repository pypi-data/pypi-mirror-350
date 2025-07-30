"""Base model classes for ReeSaber configurations."""

from typing import Any, ClassVar
from pydantic import BaseModel, Field

class Vector3(BaseModel):
    """Represents a 3D vector for position, rotation, or scale."""
    x: float = Field(default=0.0, description="X coordinate")
    y: float = Field(default=0.0, description="Y coordinate")
    z: float = Field(default=0.0, description="Z coordinate")
    
    @classmethod
    def one(cls) -> "Vector3":
        """Create a Vector3 with all components set to 1.0."""
        return cls(x=1.0, y=1.0, z=1.0)


class Color(BaseModel):
    """Represents an RGBA color."""
    r: float = Field(default=1.0, ge=0.0, le=1.0, description="Red component (0-1)")
    g: float = Field(default=1.0, ge=0.0, le=1.0, description="Green component (0-1)")
    b: float = Field(default=1.0, ge=0.0, le=1.0, description="Blue component (0-1)")
    a: float = Field(default=1.0, ge=0.0, le=1.0, description="Alpha component (0-1)")
    
    @classmethod
    def from_rgb(cls, r: int, g: int, b: int, a: int = 255) -> "Color":
        """Create a Color from RGB values (0-255)."""
        return cls(r=r/255, g=g/255, b=b/255, a=a/255)
    
    @classmethod
    def black(cls) -> "Color":
        """Create a black color."""
        return cls(r=0.0, g=0.0, b=0.0, a=1.0)
    
    @classmethod
    def white(cls) -> "Color":
        """Create a white color."""
        return cls(r=1.0, g=1.0, b=1.0, a=1.0)
    
    @classmethod
    def transparent(cls) -> "Color":
        """Create a transparent color."""
        return cls(r=0.0, g=0.0, b=0.0, a=0.0)
    
    @classmethod
    def red(cls) -> "Color":
        """Create a red color."""
        return cls(r=1.0, g=0.0, b=0.0, a=1.0)
    
    @classmethod
    def green(cls) -> "Color":
        """Create a green color."""
        return cls(r=0.0, g=1.0, b=0.0, a=1.0)
    
    @classmethod
    def blue(cls) -> "Color":
        """Create a blue color."""
        return cls(r=0.0, g=0.0, b=1.0, a=1.0)


class Transform(BaseModel):
    """Represents a local transform with position, rotation, and scale."""
    position: Vector3 = Field(default_factory=Vector3, description="Position vector")
    rotation: Vector3 = Field(default_factory=Vector3, description="Rotation vector (Euler angles)")
    scale: Vector3 = Field(default_factory=Vector3.one, description="Scale vector")
    
    def model_post_init(self, __context: Any) -> None:
        """Initialize default scale to Vector3.one() if not specified."""
        if not self.scale:
            self.scale = Vector3.one()