# Import the PyArmor runtime first
try:
    # Add the obfuscated directory to the path
    import sys
    import os
    
    # Get the directory containing the obfuscated code
    obfuscated_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'obfuscated')
    
    # Add it to the path if not already there
    if obfuscated_dir not in sys.path:
        sys.path.insert(0, obfuscated_dir)
    
    # Import the runtime and obfuscated module
    from pyarmor_runtime_000000.pyarmor_runtime import __pyarmor__
    from addition import add
    
    # Clean up the path
    if obfuscated_dir in sys.path:
        sys.path.remove(obfuscated_dir)
        
except ImportError as e:
    # If we can't import the obfuscated version, raise a clear error
    raise ImportError(
        f"Failed to import obfuscated module: {str(e)}. "
        "Make sure you have built the package correctly with PyArmor."
    ) from e

__version__ = '0.1.1'
