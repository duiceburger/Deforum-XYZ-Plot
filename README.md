# Deforum-XYZ-Plot

A browser-based tool for generating batches of Deforum settings files with parametric variations for animation experiments.

## Overview

Deforum-XYZ-Plot is a utility that enables Stable Diffusion animation creators to easily experiment with different parameter combinations in Deforum. Instead of manually creating dozens of settings files, this tool allows you to:

1. Define parameter ranges on X, Y, and optionally Z axes
2. Automatically generate all parameter combinations
3. Download the resulting settings files individually or as a batch
4. Maintain proper prompt handling including global positive prompts and keyframed animation prompts

## Live Application on Gihhub

### **Basic Version**
[Deforum-XYZ-Plot Basic](https://duiceburger.github.io/Deforum-XYZ-Plot/deforum-xyz-simple.html)
- Simpler interface
- Parameter X/Y/Z plotting only
- No prompt management

### **Full-Featured Version**
[Deforum-XYZ-Plot Advanced](https://duiceburger.github.io/Deforum-XYZ-Plot/deforum-xyz-advanced.html)
- Complete interface
- Global positive prompts support
- Keyframe animation prompts
- Parameter X/Y/Z plotting
- Enhanced settings management

## Features

- **Parameter Selection**: Choose any parameters from Deforum settings to vary
- **Flexible Value Ranges**: Define values as exact numbers, ranges, or incremental sequences
- **Global Positive Prompts**: Set common positive prompts that apply to all frames
- **Keyframed Animation Prompts**: Maintain frame-specific prompts for animation
- **Batch Download**: Get all generated settings as a ZIP file organized by parameter values
- **3D Parameter Space**: Optionally add a Z-axis parameter for complete experimentation

## How to Use

### Step 1: Upload Deforum Settings

Start by uploading an existing Deforum settings file (TXT format). This will serve as the base for all the variations.

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

## Example Use Cases

- Test different strength values with different CFG scales
- Compare different noise schedules across various animation modes
- Find the optimal combination of motion parameters
- Experiment with different sampler+steps combinations

## Technical Details

This tool runs entirely in your browser - no data is sent to any server. Your settings and prompts remain private and secure.

## Contributing

Contributions are welcome!

## Acknowledgments

- The [Deforum team](https://github.com/deforum-art/deforum-stable-diffusion) for creating the amazing animation system
- The Stable Diffusion community for continuous innovation in AI art generation
