import sys
import os

# Append the root/scripts folder to the system path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts"))
)
