# Create a new main file with absolute paths
import os
import sys
import subprocess
from FloorplanToBlenderLib import * # floorplan to blender library
from pathlib import Path

def create_blender_project(data_paths, blender_path=None):
    """Create blender project with the generated data files"""
    
    # Get paths from data_paths
    paths = data_paths[0]  # Assuming single floorplan
    
    # Get config values
    if not blender_path:
        blender_path = config.get_default_blender_installation_path()
    
    # Verify Blender exists
    if not blender_path or not os.path.exists(blender_path):
        print(f"\n❌ ERROR: Blender not found at: {blender_path}")
        print("\nPlease install Blender from: https://www.blender.org/download/")
        print("Or provide the correct path when prompted.")
        sys.exit(1)
    
    # Verify it's an executable file, not a directory
    if os.path.isdir(blender_path):
        print(f"\n❌ ERROR: Path is a directory, not the blender.exe file: {blender_path}")
        print("Please provide the full path to blender.exe")
        print("Example: C:\\Program Files\\Blender Foundation\\Blender 3.6\\blender.exe")
        sys.exit(1)
    
    # Get outformat without default parameter
    try:
        outformat = config.get(const.SYSTEM_CONFIG_FILE_NAME, "SYSTEM", "out_format")
    except:
        outformat = "BLEND"  # Default if not found
    
    # Create target directory if it doesn't exist
    target_dir = os.path.abspath("./Target")
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    # Generate output filename
    existing_files = [f for f in os.listdir(target_dir) if f.startswith('floorplan') and f.endswith('.blend')]
    base_name = f"floorplan{len(existing_files) + 1}"
    blend_file = os.path.join(target_dir, f"{base_name}.blend")
    
    if outformat.upper() == "BLEND":
        output_file = blend_file
    else:
        output_file = os.path.join(target_dir, f"{base_name}.{outformat.lower()}")
    
    print(f"\nCreates blender project")
    print(f"Blender path: {blender_path}")
    print(f"Output file: {output_file}")
    print(f"Blend file: {blend_file}")
    
    # Convert all data paths to absolute
    abs_paths = {}
    for key, path in paths.items():
        if os.path.exists(path):
            abs_paths[key] = os.path.abspath(path)
        else:
            abs_paths[key] = path
    
    # First create the blend file
    # Use the correct Blender script name
    blender_script = './Blender/floorplan_to_3dObject_in_blender.py'
    if not os.path.exists(blender_script):
        print(f"❌ ERROR: Blender script not found: {blender_script}")
        sys.exit(1)
    
    cmd_create = [
        blender_path,
        '-noaudio',
        '--background',
        '--python', blender_script,
        '--',
        abs_paths['floor_verts'], abs_paths['floor_faces'],
        abs_paths['wall_vertical_verts'], abs_paths['wall_vertical_faces'],
        abs_paths['wall_horizontal_verts'], abs_paths['wall_horizontal_faces'],
        abs_paths['room_verts'], abs_paths['room_faces'],
        abs_paths['window_vertical_verts'], abs_paths['window_vertical_faces'],
        abs_paths['window_horizontal_verts'], abs_paths['window_horizontal_faces'],
        abs_paths['door_vertical_verts'], abs_paths['door_vertical_faces'],
        abs_paths['door_horizontal_verts'], abs_paths['door_horizontal_faces'],
        blend_file,
        abs_paths['transform']
    ]
    
    print("\nCreating blend file...")
    print(f"Command: {' '.join(cmd_create[:5])}...")  # Show first few args
    print(f"Working directory: {os.getcwd()}")
    
    try:
        result = subprocess.check_output(cmd_create, stderr=subprocess.STDOUT, shell=False)
        print(f"Blend file created: {blend_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error creating blend file: {e.output.decode() if e.output else 'Unknown error'}")
        raise
    
    # Verify the blend file was created
    if not os.path.exists(blend_file):
        print(f"ERROR: Blend file was not created at {blend_file}")
        return
    
    # If we need to export to another format
    if outformat.upper() != "BLEND":
        print(f"\nExporting to {outformat}...")
        cmd_export = [
            blender_path,
            '-noaudio',
            '--background',
            '--python', './Blender/blender_export_any.py',
            '--',
            output_file,
            outformat,
            blend_file  # Pass the absolute path
        ]
        
        try:
            result = subprocess.run(cmd_export, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Export error: {result.stderr}")
                print(f"Export output: {result.stdout}")
                raise subprocess.CalledProcessError(result.returncode, cmd_export)
            print(f"Export successful: {output_file}")
        except Exception as e:
            print(f"Export failed: {e}")
            raise
    
    print("\n✓ Blender project created successfully!")

# Main execution
if __name__ == "__main__":
    print("...")  # ASCII art here
    
    print("\n----- CREATE BLENDER PROJECT FROM FLOORPLAN WITH DIALOG -----")
    print("Welcome to this program. Please answer the questions below to progress.")
    print("Remember that you can change data more efficiently in the config file.\n")
    
    # Get user input (simplified for testing)
    print("=" * 70)
    print("BLENDER INSTALLATION CHECK")
    print("=" * 70)
    
    blender_path_input = input("\nPlease enter your blender installation path\n[Press Enter to skip if not installed]: ").strip()
    
    # Use provided path or try to detect
    if blender_path_input:
        if not os.path.exists(blender_path_input):
            print(f"\n❌ ERROR: Blender not found at: {blender_path_input}")
            sys.exit(1)
        if os.path.isdir(blender_path_input):
            print(f"\n❌ ERROR: That's a directory. Please provide the full path to blender.exe")
            sys.exit(1)
        blender_path = blender_path_input
    else:
        # Try to detect or use default
        blender_path = config.get_default_blender_installation_path()
        if not blender_path or not os.path.exists(blender_path):
            print("\n" + "=" * 70)
            print("❌ BLENDER NOT FOUND!")
            print("=" * 70)
            print("\nThis project requires Blender to create 3D models.")
            print("\nTo install Blender:")
            print("1. Visit: https://www.blender.org/download/")
            print("2. Download Blender (latest version)")
            print("3. Install it")
            print("4. Note the installation path (usually:")
            print("   C:\\Program Files\\Blender Foundation\\Blender X.X\\blender.exe)")
            print("5. Run this script again and provide the path")
            print("\n" + "=" * 70)
            sys.exit(1)
    
    print(f"\n✓ Using Blender: {blender_path}")
    print("=" * 70 + "\n")
    
    build_type = input("Do you want to build from StackingFile or ConfigFile list ? [default = ConfigFile]: ")
    config_files = input("Use default config or import from file paths separated by space [default = ./Configs/default.ini]: ")
    set_images = input("Do you want to set images to use in each config file? [N/y]: ")
    proceed = input("\nThis program is about to run and create blender3d project, continue? : ")
    
    if proceed.lower() == 'n':
        print("Exiting...")
        sys.exit(0)
    
    print("\nGenerate datafiles in folder: Data\n")
    print("Clean datafiles\n")
    
    clear_cache = input("Clear all cached data before run: [default = yes] : ")
    
    # build a list of floorplan objects
    floorplans = []
    if build_type.lower().startswith("stack"):
        stacking_path = config_files or "./Stacking/all_separated_example.txt"
        floorplans = stacking.parse_stacking_file(stacking_path)
    else:
        cfgs = config_files.split() if config_files else ["./Configs/default.ini"]
        floorplans = [floorplan.new_floorplan(c) for c in cfgs]

    if set_images.lower() == 'y' and floorplans:
        for f in floorplans:
            default_img = getattr(f, 'image_path', '')
            var = input(f"For config file {f.conf} write path for image to use [Default={default_img}]: ")
            if var:
                f.image_path = var

    # generate data files and create blender projects
    data_paths = []
    try:
        for f in floorplans:
            gen = execution.simple_single(f, show=False)
            base = gen[0] if isinstance(gen, (tuple, list)) else gen
            data_paths.append({
                'floor_verts': os.path.join(base, 'floor_verts.txt'),
                'floor_faces': os.path.join(base, 'floor_faces.txt'),
                'wall_vertical_verts': os.path.join(base, 'wall_vertical_verts.txt'),
                'wall_vertical_faces': os.path.join(base, 'wall_vertical_faces.txt'),
                'wall_horizontal_verts': os.path.join(base, 'wall_horizontal_verts.txt'),
                'wall_horizontal_faces': os.path.join(base, 'wall_horizontal_faces.txt'),
                'room_verts': os.path.join(base, 'room_verts.txt'),
                'room_faces': os.path.join(base, 'room_faces.txt'),
                'window_vertical_verts': os.path.join(base, 'window_vertical_verts.txt'),
                'window_vertical_faces': os.path.join(base, 'window_vertical_faces.txt'),
                'window_horizontal_verts': os.path.join(base, 'window_horizontal_verts.txt'),
                'window_horizontal_faces': os.path.join(base, 'window_horizontal_faces.txt'),
                'door_vertical_verts': os.path.join(base, 'door_vertical_verts.txt'),
                'door_vertical_faces': os.path.join(base, 'door_vertical_faces.txt'),
                'door_horizontal_verts': os.path.join(base, 'door_horizontal_verts.txt'),
                'door_horizontal_faces': os.path.join(base, 'door_horizontal_faces.txt'),
                'transform': os.path.join(base, 'transform.txt'),
            })

        if len(data_paths) == 1:
            create_blender_project(data_paths, blender_path)
        else:
            for paths in data_paths:
                create_blender_project([paths], blender_path)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    print("\n✓ Done, Have a nice day!")
