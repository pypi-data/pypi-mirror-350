"""
Veeva Tools package for accelerating Veeva Systems internal tools development
"""

import sys
import os

# Add parent directory to path to make direct imports work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import modules to expose at the veevatools namespace level
from salesforce import Sf
import veevanetwork
import veevanitro
import veevavault
