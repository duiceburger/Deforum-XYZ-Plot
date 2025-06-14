# Deforum-XYZ-Plot

A browser-based tool for generating batches of Deforum settings files with parametric variations for animation experiments.

## Overview

Deforum-XYZ-Plot is a utility that enables Stable Diffusion animation creators to easily experiment with different parameter combinations in Deforum. Instead of manually creating dozens of settings files, this tool allows you to:

1. Define parameter ranges on X, Y, and optionally Z axes
2. Automatically generate all parameter combinations
3. Download the resulting settings files individually or as a batch
4. Maintain proper prompt handling including global positive prompts and keyframed animation prompts

https://github.com/user-attachments/assets/1a46209c-7a08-4ed1-99e7-40b5dbbf03ee

## Live Application on Gihhub

### **Basic Fixed Version Name and Output**
[Deforum XYZ PLOT V2](https://duiceburger.github.io/Deforum-XYZ-Plot/deforum_xyz_enhanced-batchname.html)
- Simpler interface
- Parameter X/Y/Z plotting only
- fixed 0: X issue

## Features

- **Parameter Selection**: Choose any parameters from Deforum settings to vary
- **Flexible Value Ranges**: Define values as exact numbers, ranges, or incremental sequences
- **Batch Download**: Get all generated settings as a ZIP file organized by parameter values
- **optional 3rd value**: Optionally add a Z-axis parameter for massive batches

## How to Use

### Step 1: Upload Deforum Settings

Start by uploading an existing Deforum settings file (TXT format). This will serve as the base for all the variations.
[Deforum XYZ PLOT V2](https://duiceburger.github.io/Deforum-XYZ-Plot/deforum_xyz_enhanced-batchname.html)

### Step 2: Configure Prompts

- Set your **Global Positive Prompt** that applies to all frames
- Set a **Negative Prompt** for exclusions across all frames
- Add **Keyframed Prompts** with specific frame numbers for animation

### Step 3: Choose Parameters to Vary

Select which parameters you want to vary on each axis:
- **X-Axis Parameter**: Required
- **Y-Axis Parameter**: Required
- **Z-Axis Parameter**: Optional (enables 3D parameter space)

### Step 4: Define Value Ranges

For each parameter, define the values or ranges you want to test:

Supported formats include:
- Simple value: `0.5`
- Simple range: `1-5` (produces 1, 2, 3, 4, 5)
- Range with increment: `0-1 (+0.2)` (produces 0, 0.2, 0.4, 0.6, 0.8, 1)
- Range with count: `0-1 [6]` (produces 0, 0.2, 0.4, 0.6, 0.8, 1)

### Step 5: Generate and Download

Click "Generate Plot Settings" to create all parameter combinations. You can then:
- Download all settings as a ZIP file
- Download individual settings files
- If using Z-axis, download specific Z-groups


### Step 6: Run in Deofrum

Run all your [Deforum](https://github.com/deforum-art/deforum-stable-diffusion) settings files using Batch Mode!
- Enable Batch mode in Deforum
- Drag and drop outputs to Batch Mode
- Render!

## Example Use Cases

- Test different strength values with different CFG scales
- Compare different noise schedules across various animation modes
- Find the optimal combination of motion parameters
- Experiment with different sampler+steps combinations

## Fixing File output
# Deforum Video Renamer

A simple utility to automatically rename Deforum video outputs to match their descriptive folder names, making batch experiments easier to organize and identify.

 Simple Batch File (Windows - Recommended)

1. Download both files:  https://github.com/duiceburger/Deforum-XYZ-Plot/tree/9c270cb2e6e23691d611738fd96a420ade89b068/batch-renamer
   - `deforum_video_renamer.py`
   - `rename_deforum_videos.bat`

2. Place both files in your Deforum output directory

3. Double-click `rename_deforum_videos.bat`

4. Review the dry-run results and confirm to proceed

## Technical Details

This tool runs entirely in your browser - no data is sent to any server. Your settings and prompts remain private and secure.

## Contributing

Contributions are welcome!

## Acknowledgments

- The [Deforum team](https://github.com/deforum-art/deforum-stable-diffusion) for creating the amazing animation system
- The Stable Diffusion community for continuous innovation in AI art generation
