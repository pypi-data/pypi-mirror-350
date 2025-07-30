"""
Cinder - ML model debugging and analysis dashboard
"""
__version__ = "1.0.6"

import sys
import os
from typing import Any, Dict, Optional, Union

# Try to add the parent directory to the path
parent_dir = os.path.dirname(os.path.dirname(__file__))
if parent_dir not in sys.path and os.path.exists(os.path.join(parent_dir, 'backend')):
    sys.path.insert(0, parent_dir)

# Define a placeholder/fallback ModelDebugger class
class ModelDebugger:
    """Placeholder ModelDebugger class for when backend is not available."""
    
    def __init__(self, model: Any = None, dataset: Any = None, name: Optional[str] = None):
        self.model = model
        self.dataset = dataset
        self.name = name
        print("Warning: Using placeholder ModelDebugger. Backend module not found.")
    
    def analyze(self) -> Dict[str, Any]:
        """Placeholder analyze method."""
        print("Warning: analyze() not implemented in placeholder ModelDebugger.")
        return {"accuracy": 0.0, "error_analysis": {"error_count": 0, "error_rate": 0.0}}
    
    def launch_dashboard(self, port: int = 8000) -> None:
        """Placeholder dashboard launcher."""
        print(f"Warning: Cannot launch dashboard - backend module not found.")
        print(f"This is a placeholder implementation. Please make sure the backend module is installed.")

# Try to import the real ModelDebugger
try:
    # If backend module is available, replace our placeholder
    from backend.model_interface.connector import ModelDebugger as BackendModelDebugger
    # Use the backend version
    ModelDebugger = BackendModelDebugger
except ImportError:
    # Keep using our placeholder defined above
    pass

# Export ModelDebugger
__all__ = ["ModelDebugger"]