"""Base module classes for ReeSaber configurations."""

from typing import Any, Dict, Literal
from pydantic import BaseModel, Field

from reesaber.models.base import Transform

class ModuleBase(BaseModel):
    """Base fields for all module configurations."""
    enabled: bool = Field(default=True, description="Whether this module is enabled")
    name: str = Field(..., description="Display name of this module")
    local_transform: Transform = Field(
        default_factory=Transform, 
        description="Local transform for this module"
    )


class SaberModule(BaseModel):
    """Base class for all ReeSaber modules."""
    module_id: str = Field(..., description="Unique identifier for this module type")
    version: int = Field(default=1, description="Module version")
    config: ModuleBase = Field(..., description="Module configuration")
    
    def model_dump_json(self) -> Dict[str, Any]:
        """Convert the module to a dictionary for JSON serialization."""
        return {
            "ModuleId": self.module_id,
            "Version": self.version,
            "Config": self._dump_config()
        }
    
    def _dump_config(self) -> Dict[str, Any]:
        """Convert module-specific config to dictionary."""
        return {
            "Enabled": self.config.enabled,
            "Name": self.config.name,
            "LocalTransform": {
                "Position": self.config.local_transform.position.model_dump(),
                "Rotation": self.config.local_transform.rotation.model_dump(),
                "Scale": self.config.local_transform.scale.model_dump()
            }
        }