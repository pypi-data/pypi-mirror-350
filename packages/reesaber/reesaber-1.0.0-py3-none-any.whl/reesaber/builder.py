"""Builder for creating ReeSaber configurations."""

from reesaber.models.base import Color
from reesaber.modules.blur_saber import BlurSaber
from reesaber.modules.simple_trail import SimpleTrail
from reesaber.modules.vanilla_saber import VanillaSaber
from reesaber.modules.base import SaberModule
from reesaber.config import SaberConfig

class ReeSaberBuilder:
    """
    Builder class for creating complete ReeSaber configurations.
    
    This provides a fluent interface for creating saber configurations.
    
    Example:
        ```python
        # Create a configuration with a blur saber and trail
        config = (
            ReeSaberBuilder()
            .add_blur_saber("Main Saber", Color.red(), length=1.2, glow=1.5)
            .add_trail("Trail", Color.red(), length=0.25)
            .build()
        )
        
        # Export the configuration
        config.export("my_saber.json")
        ```
    """
    def __init__(self):
        """Initialize a new ReeSaberBuilder."""
        self.config = SaberConfig()
    
    def add_module(self, module: SaberModule) -> "ReeSaberBuilder":
        """
        Add a module to the configuration.
        
        Args:
            module: The module to add
            
        Returns:
            Self for method chaining
        """
        self.config.add_module(module)
        return self
    
    def add_blur_saber(
        self, 
        name: str, 
        color: Color, 
        length: float = 1.0, 
        glow: float = 1.0
    ) -> "ReeSaberBuilder":
        """
        Add a blur saber to the configuration.
        
        Args:
            name: Display name for the saber
            color: Main color of the saber blade
            length: Length of the saber blade
            glow: Glow multiplier
            
        Returns:
            Self for method chaining
        """
        self.add_module(BlurSaber.create(name, color, length, glow))
        return self
    
    def add_trail(
        self, 
        name: str, 
        color: Color, 
        length: float = 0.2, 
        width: float = 1.0
    ) -> "ReeSaberBuilder":
        """
        Add a trail to the configuration.
        
        Args:
            name: Display name for the trail
            color: Main color of the trail
            length: Length of the trail
            width: Width of the trail
            
        Returns:
            Self for method chaining
        """
        self.add_module(SimpleTrail.create(name, color, length, width))
        return self
    
    def add_vanilla_saber(self, name: str, with_trail: bool = True) -> "ReeSaberBuilder":
        """
        Add a vanilla saber to the configuration.
        
        Args:
            name: Display name for the saber
            with_trail: Whether to include the default trail
            
        Returns:
            Self for method chaining
        """
        self.add_module(VanillaSaber.create(name, with_trail))
        return self
    
    def build(self) -> SaberConfig:
        """
        Build and return the final SaberConfig.
        
        Returns:
            The configured SaberConfig instance
        """
        return self.config