#!/usr/bin/env python3
"""
xPOURY4 Recon - Elite Cyber Intelligence & Digital Forensics Platform
Main entry point for the package
"""

import sys
import os
import argparse
from pathlib import Path

# Add the parent directory to the path to import the main module
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import main as original_main

def main():
    """Main entry point for the xPOURY4 Recon package."""
    try:
        original_main()
    except KeyboardInterrupt:
        print("\n[!] Operation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"[!] Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 