"""
lib-test-package - A test package
"""

__version__ = "1.0.3"

# Importez les fonctions/classes que vous voulez rendre disponibles
from .main import main

# Définissez ce qui sera importé avec "from lib_test_package import *"
__all__ = ["main"]
