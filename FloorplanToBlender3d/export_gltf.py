import bpy
import sys
import os

print(f"All arguments: {sys.argv}")

# Arguments after -- are what we need
# Find the -- separator
try:
    separator_index = sys.argv.index('--')
    args = sys.argv[separator_index + 1:]
except ValueError:
    # No -- separator, use last two args
    args = sys.argv[-2:]

if len(args) < 2:
    print("Error: Need blend_file and output_file arguments")
    print("Usage: blender --background --python export_gltf.py -- input.blend output.gltf")
    sys.exit(1)

blend_file = args[0]
output_file = args[1]

print(f"Opening: {blend_file}")
print(f"Exporting to: {output_file}")

# Open the blend file
bpy.ops.wm.open_mainfile(filepath=blend_file)

# Get all mesh objects
mesh_objects = [obj for obj in bpy.data.objects if obj.type == 'MESH']
print(f"Found {len(mesh_objects)} mesh objects")

if len(mesh_objects) == 0:
    print("ERROR: No mesh objects found in blend file!")
    sys.exit(1)

# Select all objects
bpy.ops.object.select_all(action='SELECT')

# Export to GLTF with proper settings
try:
    bpy.ops.export_scene.gltf(
        filepath=output_file,
        export_format='GLTF_SEPARATE',
        use_selection=False,
        export_apply=True,
        export_yup=True,
        export_materials='EXPORT',
        export_extras=True,
        export_cameras=False,
        export_lights=False
    )
    print("✓ GLTF export successful!")
    
    # Check if files were created
    if os.path.exists(output_file):
        file_size = os.path.getsize(output_file)
        print(f"✓ Created: {output_file} ({file_size} bytes)")
        
        # Check for .bin file
        bin_file = output_file.replace('.gltf', '.bin')
        if os.path.exists(bin_file):
            bin_size = os.path.getsize(bin_file)
            print(f"✓ Created: {bin_file} ({bin_size} bytes)")
    else:
        print("ERROR: Output file not created!")
        sys.exit(1)
        
except Exception as e:
    print(f"ERROR during export: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("Done!")
sys.exit(0)
