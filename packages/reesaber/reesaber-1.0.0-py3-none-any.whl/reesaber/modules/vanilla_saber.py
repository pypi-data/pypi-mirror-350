"""VanillaSaber module for ReeSaber configurations."""

from pydantic import Field, Literal

from reesaber.modules.base import ModuleBase, SaberModule

class VanillaSaberConfig(ModuleBase):
    """Configuration for VanillaSaber module."""
    with_trail: bool = Field(default=False, description="Whether to include the default trail")


class VanillaSaber(SaberModule):
    """
    Represents a Vanilla Saber module for ReeSabers.
    
    This module creates a standard Beat Saber saber.
    
    Example:
        ```python
        # Create a vanilla saber with trail
        saber = VanillaSaber(
            config=VanillaSaberConfig(
                name="Standard Saber",
                with_trail=True
            )
        )
        ```
    """
    module_id: str = Field(default="reezonate.vanilla-saber", Literal=True)
    config: VanillaSaberConfig
    
    def _dump_config(self) -> Dict[str, Any]:
        """Convert module-specific config to dictionary."""
        result = super()._dump_config()
        
        # Add VanillaSaber-specific configuration
        result["WithTrail"] = self.config.with_trail
        
        return result
    
    @classmethod
    def create(cls, name: str, with_trail: bool = True) -> "VanillaSaber":
        """
        Create a VanillaSaber with basic settings.
        
        Args:
            name: Display name for the saber
            with_trail: Whether to include the default trail
            
        Returns:
            A configured VanillaSaber instance
        """
        return cls(config=VanillaSaberConfig(name=name, with_trail=with_trail))