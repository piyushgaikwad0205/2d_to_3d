import bpy
import sys

# Get arguments after "--"
args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []

if len(args) < 2:
    print("Usage: blender --background --python export_glb.py -- input.blend output.glb")
    sys.exit(1)

input_file = args[0]
output_file = args[1]

print(f"Opening: {input_file}")
print(f"Exporting to: {output_file}")

# Open the blend file
bpy.ops.wm.open_mainfile(filepath=input_file)

# Count meshes
mesh_count = sum(1 for obj in bpy.data.objects if obj.type == 'MESH')
print(f"Found {mesh_count} mesh objects")

# Export to GLB (binary GLTF)
bpy.ops.export_scene.gltf(
    filepath=output_file,
    export_format='GLB',  # Binary format - single file
    use_selection=False,
    export_apply=True,
    export_yup=True,
    export_materials='EXPORT',
    export_extras=True,
    export_cameras=False,
    export_lights=False
)

print(f"\n✓ GLB export successful!")
print(f"✓ Created: {output_file}")
print("Done!")
