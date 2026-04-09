
import os
import sys
from FloorplanToBlenderLib import *

def test_debug():
    print("STEP 1: Checking Blender path")
    blender_path = "P:\\blender\\blender.exe"
    if not os.path.exists(blender_path):
        print(f"Blender NOT found at {blender_path}")
    else:
        print(f"Blender found at {blender_path}")

    print("STEP 2: Initializing floorplan")
    config_path = "./Configs/default.ini"
    if not os.path.exists(config_path):
        print(f"Config NOT found at {config_path}")
        return
    
    try:
        fp = floorplan.new_floorplan(config_path)
        # Use a known example
        fp.image_path = "./Images/Examples/example.png"
        print(f"Floorplan initialized for {fp.image_path}")

        print("STEP 3: Running execution.simple_single")
        # We'll try to see if it reaches inside generate_all_files
        from FloorplanToBlenderLib import execution
        base_path = execution.simple_single(fp, show=False)
        print(f"Data generated at: {base_path}")
    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_debug()
