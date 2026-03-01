# Auto-run version with default values
import os
import sys
import subprocess
from FloorplanToBlenderLib import *

def create_blender_project(base_path, blender_path, program_path, output_format=".blend"):
    """Create blender project with the generated data files"""
    
    # Verify Blender exists
    if not blender_path or not os.path.exists(blender_path):
        print(f"\n❌ ERROR: Blender not found at: {blender_path}")
        sys.exit(1)
    
    if os.path.isdir(blender_path):
        print(f"\n❌ ERROR: Path is a directory, not the blender.exe file: {blender_path}")
        sys.exit(1)
    
    # Use provided output format
    outformat = output_format
    
    # Create target directory
    target_dir = os.path.abspath("./Target")
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    # Generate output filename
    existing_files = [f for f in os.listdir(target_dir) if f.startswith('floorplan') and f.endswith('.blend')]
    base_name = f"floorplan{len(existing_files) + 1}"
    target_path = f"/Target/{base_name}.blend"
    blend_file = os.path.join(target_dir, f"{base_name}.blend")
    
    print(f"\n{'='*70}")
    print("CREATING BLENDER PROJECT")
    print(f"{'='*70}")
    print(f"Blender path: {blender_path}")
    print(f"Target path: {target_path}")
    print(f"Base data path: {base_path}")
    
    # Use the correct Blender script
    blender_script = './Blender/floorplan_to_3dObject_in_blender.py'
    if not os.path.exists(blender_script):
        print(f"❌ ERROR: Blender script not found: {blender_script}")
        sys.exit(1)
    
    cmd_create = [
        blender_path,
        '-noaudio',
        '--background',
        '--python', blender_script,
        program_path,  # program path
        target_path,   # target file
        base_path      # data path
    ]
    
    print("\n⏳ Creating blend file...")
    print(f"Command: {' '.join([str(x) for x in cmd_create])}")
    
    try:
        result = subprocess.check_output(cmd_create, stderr=subprocess.STDOUT)
        print(f"✓ Blend file created: {blend_file}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating blend file:")
        if e.output:
            print(e.output.decode())
        raise
    
    # Verify the blend file was created
    if not os.path.exists(blend_file):
        print(f"❌ ERROR: Blend file was not created at {blend_file}")
        return
    
    # If we need to export to another format
    if outformat != ".blend":
        output_file = os.path.join(target_dir, f"{base_name}{outformat}")
        print(f"\n⏳ Exporting to {outformat.upper()}...")
        
        # Create a Python script to export properly
        export_script_content = f"""import bpy
import sys

# Open the blend file
bpy.ops.wm.open_mainfile(filepath=r'{blend_file}')

# Select all objects
bpy.ops.object.select_all(action='SELECT')

# Export based on format
try:
"""
        
        # Add format-specific export commands
        if outformat == ".gltf":
            export_script_content += f"""    bpy.ops.export_scene.gltf(
        filepath=r'{output_file}',
        export_format='GLTF_SEPARATE',
        export_apply=True,
        export_materials='EXPORT',
        export_colors=True,
        use_selection=False,
        export_yup=True
    )
    print("GLTF export successful")
"""
        elif outformat == ".fbx":
            export_script_content += f"""    bpy.ops.export_scene.fbx(
        filepath=r'{output_file}',
        use_selection=False,
        apply_scale_options='FBX_SCALE_ALL',
        object_types={{'MESH'}}
    )
    print("FBX export successful")
"""
        elif outformat == ".obj":
            export_script_content += f"""    bpy.ops.wm.obj_export(
        filepath=r'{output_file}',
        export_selected_objects=False,
        apply_modifiers=True,
        export_materials=True
    )
    print("OBJ export successful")
"""
        
        export_script_content += """    sys.exit(0)
except Exception as e:
    print(f"Export error: {{e}}")
    sys.exit(1)
"""
        
        # Write export script to temporary file
        temp_export_script = os.path.join(target_dir, "_temp_export.py")
        with open(temp_export_script, 'w') as f:
            f.write(export_script_content)
        
        # Run export
        cmd_export = [
            blender_path,
            '-noaudio',
            '--background',
            '--python', temp_export_script
        ]
        
        try:
            # Python 3.6 compatible version
            result = subprocess.run(cmd_export, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            
            # Clean up temp script
            if os.path.exists(temp_export_script):
                os.remove(temp_export_script)
            
            if result.returncode != 0:
                print(f"Export error: {result.stderr}")
                print(f"Export output: {result.stdout}")
            else:
                # Verify export file exists and has content
                if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
                    print(f"✓ Export successful: {output_file}")
                    print(f"✓ File size: {os.path.getsize(output_file) / 1024:.1f} KB")
                    
                    # Show AR usage instructions
                    if outformat in [".gltf", ".fbx"]:
                        print(f"\n{'='*70}")
                        print("📱 AR READY!")
                        print(f"{'='*70}")
                        if outformat == ".gltf":
                            print("To view in AR:")
                            print("1. Upload to: https://modelviewer.dev/editor/")
                            print("2. Click 'View in AR' on your mobile device")
                            print("3. Or use in web apps with AR.js, A-Frame, or Three.js")
                        elif outformat == ".fbx":
                            print("To use in AR:")
                            print("1. Import into Unity (AR Foundation)")
                            print("2. Or import into Unreal Engine (AR Kit/Core)")
                            print("3. Or use with 8th Wall for web AR")
                        print(f"{'='*70}\n")
                else:
                    print(f"❌ Export file was not created or is empty")
                    print(f"Note: You can manually export from the BLEND file: {blend_file}")
        except Exception as e:
            print(f"❌ Export failed: {e}")
            print(f"Note: You can still use the BLEND file: {blend_file}")
    
    print(f"\n{'='*70}")
    print("✓ BLENDER PROJECT CREATED SUCCESSFULLY!")
    print(f"{'='*70}\n")
    
    # Open the created file in Blender
    print("🚀 Opening Blender with the created file...\n")
    try:
        subprocess.Popen([blender_path, blend_file])
        print(f"✓ Blender launched with: {blend_file}")
    except Exception as e:
        print(f"❌ Could not open Blender: {e}")
        print(f"You can manually open: {blend_file}")

# Main execution
if __name__ == "__main__":
    print("\n" + "="*70)
    print("FLOORPLAN TO BLENDER 3D - INTERACTIVE (AR COMPATIBLE)")
    print("="*70)
    
    # Set Blender path
    blender_path = "P:\\blender\\blender.exe"
    program_path = os.path.dirname(os.path.realpath(__file__))
    
    # Check if Blender exists
    if not os.path.exists(blender_path):
        print(f"\n❌ ERROR: Blender not found at: {blender_path}")
        print("\nPlease install Blender or update the blender_path in this script")
        sys.exit(1)
    
    print(f"\n✓ Found Blender at: {blender_path}")
    print(f"✓ Program path: {program_path}")
    
    # Select output format
    print(f"\n{'='*70}")
    print("SELECT OUTPUT FORMAT")
    print(f"{'='*70}")
    print("1. BLEND - Blender native format")
    print("2. GLTF - AR compatible (Web AR, Model Viewer)")
    print("3. FBX - AR compatible (Unity, Unreal Engine)")
    print("4. OBJ - Universal 3D format")
    print(f"{'='*70}")
    
    while True:
        format_choice = input("\nSelect format (1-4) or press Enter for BLEND: ").strip()
        
        if format_choice == "" or format_choice == "1":
            output_format = ".blend"
            format_name = "BLEND"
            break
        elif format_choice == "2":
            output_format = ".gltf"
            format_name = "GLTF (AR Compatible)"
            break
        elif format_choice == "3":
            output_format = ".fbx"
            format_name = "FBX (AR Compatible)"
            break
        elif format_choice == "4":
            output_format = ".obj"
            format_name = "OBJ"
            break
        else:
            print("❌ Please enter 1, 2, 3, or 4")
    
    print(f"✓ Selected format: {format_name}\n")
    
    # Show available example images
    examples_dir = "./Images/Examples"
    if os.path.exists(examples_dir):
        example_files = [f for f in os.listdir(examples_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        if example_files:
            print(f"\n{'='*70}")
            print("AVAILABLE EXAMPLE FLOORPLANS")
            print(f"{'='*70}")
            for i, filename in enumerate(example_files, 1):
                print(f"{i}. {filename}")
            print(f"{'='*70}")
            
            # Get user selection
            while True:
                try:
                    choice = input(f"\nSelect a floorplan (1-{len(example_files)}) or press Enter for default: ").strip()
                    
                    if choice == "":
                        # Use default config
                        config_path = "./Configs/default.ini"
                        selected_image = None
                        print(f"✓ Using default config: {config_path}")
                        break
                    
                    choice_num = int(choice)
                    if 1 <= choice_num <= len(example_files):
                        selected_image = os.path.join(examples_dir, example_files[choice_num - 1])
                        config_path = "./Configs/default.ini"
                        print(f"\n✓ Selected: {example_files[choice_num - 1]}")
                        print(f"✓ Image path: {selected_image}")
                        break
                    else:
                        print(f"❌ Please enter a number between 1 and {len(example_files)}")
                except ValueError:
                    print("❌ Please enter a valid number")
        else:
            print("\n⚠ No example images found, using default config")
            config_path = "./Configs/default.ini"
            selected_image = None
    else:
        print("\n⚠ Examples directory not found, using default config")
        config_path = "./Configs/default.ini"
        selected_image = None
    
    print(f"✓ Using config: {config_path}\n")
    
    # Create floorplan object
    print("⏳ Initializing floorplan...")
    floorplan_obj = floorplan.new_floorplan(config_path)
    
    # Override image path if user selected one
    if selected_image:
        floorplan_obj.image_path = selected_image
        print(f"✓ Using selected image: {selected_image}")
    
    # Generate data files
    print("⏳ Generating data files...")
    try:
        base_path = execution.simple_single(floorplan_obj, show=False)
        print(f"✓ Data files generated at: {base_path}\n")
        
        # Create Blender project
        create_blender_project(base_path, blender_path, program_path, output_format)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    print("\n" + "="*70)
    print("✓ ALL DONE! Have a nice day!")
    print("="*70)
