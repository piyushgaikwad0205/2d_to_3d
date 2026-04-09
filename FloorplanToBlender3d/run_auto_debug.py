#!/usr/bin/env python
# Debug version to track script execution

import sys
print("DEBUG: Script started", file=sys.stderr, flush=True)

import os
print("DEBUG: os imported", file=sys.stderr, flush=True)

import subprocess
print("DEBUG: subprocess imported", file=sys.stderr, flush=True)

IS_INTERACTIVE = sys.stdin.isatty()
print(f"DEBUG: IS_INTERACTIVE = {IS_INTERACTIVE}", file=sys.stderr, flush=True)

print("STARTING SCRIPT", flush=True)
print("\n" + "="*70, flush=True)
print("FLOORPLAN TO BLENDER 3D - INTERACTIVE (AR COMPATIBLE)", flush=True)
print("="*70, flush=True)

print("DEBUG: About to import FloorplanToBlenderLib", file=sys.stderr, flush=True)
try:
    from FloorplanToBlenderLib import *
    print("DEBUG: FloorplanToBlenderLib imported successfully", file=sys.stderr, flush=True)
except Exception as e:
    print(f"DEBUG: Error importing: {e}", file=sys.stderr, flush=True)
    sys.exit(1)

print("DEBUG: Script initialization complete", file=sys.stderr, flush=True)
print("\n✓ Found Blender at: P:\\blender\\blender.exe", flush=True)
print("✓ Program path: " + os.path.dirname(os.path.realpath(__file__)), flush=True)
print("DEBUG: Ready for main execution", file=sys.stderr, flush=True)
