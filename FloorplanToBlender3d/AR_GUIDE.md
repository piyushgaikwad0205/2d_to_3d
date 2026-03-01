# AR-Compatible FloorplanToBlender3d

## 🚀 Quick Start

Run the interactive script:
```bash
python run_auto.py
```

## 📱 AR-Compatible Formats

### 1. GLTF (.gltf) - Best for Web AR
- **Use for:** Web-based AR, mobile browsers
- **Compatible with:** 
  - Model Viewer (https://modelviewer.dev)
  - AR.js
  - A-Frame
  - Three.js
  - WebXR

**Quick AR Preview:**
1. Select format `2` (GLTF) in the script
2. Upload the generated `.gltf` file to https://modelviewer.dev/editor/
3. Use "View in AR" button on your phone
4. Point your camera at a flat surface

### 2. FBX (.fbx) - Best for Game Engines
- **Use for:** Unity, Unreal Engine
- **Compatible with:**
  - Unity with AR Foundation
  - Unreal Engine with AR Kit/AR Core
  - 8th Wall
  - Vuforia

**Unity AR Setup:**
1. Select format `3` (FBX) in the script
2. Import `.fbx` file into Unity
3. Add AR Foundation package
4. Use AR Session Origin with the model

### 3. OBJ (.obj) - Universal Format
- **Use for:** General 3D applications
- Compatible with most 3D software

## 🎯 Workflow

1. **Run the script:**
   ```bash
   python run_auto.py
   ```

2. **Select AR format:**
   - Option 2: GLTF (Web AR)
   - Option 3: FBX (Unity/Unreal)

3. **Choose a floorplan:**
   - Select 1-6 for example images
   - Press Enter for default

4. **Get your AR-ready file:**
   - File saved in `Target/` folder
   - BLEND file also created for editing in Blender

## 📲 Mobile AR Viewers

### iOS:
- USDZ Viewer (built-in)
- AR Quick Look
- Sketchfab app

### Android:
- Scene Viewer (built-in)
- Google Arts & Culture
- Sketchfab app

### Cross-Platform:
- Model Viewer (web)
- Sketchfab (web/app)

## 🔧 Advanced: Edit in Blender

All exports also create a `.blend` file that you can:
1. Open in Blender
2. Edit materials, lighting, textures
3. Re-export in any format
4. Add animations for interactive AR

## 📦 Output Files

After running, you'll find in `Target/` folder:
- `floorplanX.blend` - Blender native file
- `floorplanX.gltf` (if selected) - AR web format
- `floorplanX.fbx` (if selected) - AR game engine format
- `floorplanX.obj` (if selected) - Universal format

## 🌐 Web AR Example

For GLTF files, use this HTML:
```html
<model-viewer src="floorplan.gltf" 
              ar 
              ar-modes="webxr scene-viewer quick-look"
              camera-controls 
              poster="poster.png"
              shadow-intensity="1">
</model-viewer>
```

## 🎮 Unity AR Example

1. Create new Unity project
2. Install AR Foundation package
3. Import FBX file
4. Add to AR Session Origin
5. Build for iOS/Android

## ✨ Tips

- **GLTF** is smaller and loads faster for web AR
- **FBX** preserves more detail for game engines
- Always test on actual devices, not just emulators
- Optimize models for mobile (reduce polygons if needed)
- Add good lighting in Blender before export

## 🐛 Troubleshooting

**Model not showing in AR?**
- Check file size (keep under 10MB for mobile)
- Ensure proper lighting in Blender
- Verify format compatibility with your platform

**Export failed?**
- Update Blender to latest version
- Check Python environment
- Try BLEND format first, then export manually from Blender

## 📚 Resources

- Model Viewer: https://modelviewer.dev/
- AR Foundation: https://unity.com/unity/features/arfoundation
- AR.js: https://ar-js-org.github.io/AR.js-Docs/
- Blender Manual: https://docs.blender.org/

---

**Enjoy creating AR floorplans!** 🏠📱✨
