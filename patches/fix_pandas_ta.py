#!/usr/bin/env python3
"""
This script patches the pandas_ta package to fix the numpy NaN import issue.
Run this script after installing pandas_ta to fix the compatibility issue with newer numpy versions.
"""

import os
import sys
from pathlib import Path

def find_pandas_ta_dir():
    """Find the pandas_ta package directory."""
    for path in sys.path:
        momentum_dir = Path(path) / 'pandas_ta' / 'momentum'
        if momentum_dir.exists():
            return momentum_dir
    return None

def patch_squeeze_pro():
    """Patch the squeeze_pro.py file to use numpy.nan instead of NaN."""
    momentum_dir = find_pandas_ta_dir()
    if not momentum_dir:
        print("Could not find pandas_ta package directory.")
        return False
    
    squeeze_pro_path = momentum_dir / 'squeeze_pro.py'
    if not squeeze_pro_path.exists():
        print(f"Could not find {squeeze_pro_path}")
        return False
    
    with open(squeeze_pro_path, 'r') as f:
        content = f.read()
    
    # Replace 'from numpy import NaN as npNaN' with 'from numpy import nan as npNaN'
    patched_content = content.replace('from numpy import NaN as npNaN', 'from numpy import nan as npNaN')
    
    with open(squeeze_pro_path, 'w') as f:
        f.write(patched_content)
    
    print(f"Successfully patched {squeeze_pro_path}")
    return True

if __name__ == "__main__":
    if patch_squeeze_pro():
        print("Patch applied successfully!")
    else:
        print("Failed to apply patch.") 