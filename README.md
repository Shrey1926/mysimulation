# Young's Double-Slit Experiment Simulation

A comprehensive Python-based simulation of Young's double-slit experiment using NumPy and Matplotlib. This project creates realistic 2D interference patterns based on the wave equation, with full support for customizable parameters and animated visualizations.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Project Setup](#project-setup)
- [Usage](#usage)
- [Parameters](#parameters)
- [Output Files](#output-files)
- [Examples](#examples)
- [Physics Behind the Simulation](#physics-behind-the-simulation)
- [Troubleshooting](#troubleshooting)

## 🔬 Overview

This project simulates the classic Young's double-slit experiment, which demonstrates the wave nature of light through interference patterns. The simulation calculates the intensity distribution on a screen placed at a certain distance from two coherent light sources (slits) using the principles of wave superposition.

The experiment shows:
- **Constructive Interference**: Where waves from both slits are in phase, resulting in bright fringes
- **Destructive Interference**: Where waves are out of phase, resulting in dark fringes
- **Diffraction Effects**: How slit width affects the overall intensity envelope

## ✨ Features

- ✅ **2D Interference Pattern Calculation** - Based on wave equation and superposition principle
- ✅ **Customizable Parameters** - Wavelength, slit separation, slit width, screen distance
- ✅ **Static Visualizations** - High-quality plots of intensity patterns and cross-sections
- ✅ **3D Visualization** - Surface plots showing intensity distribution in 3D space
- ✅ **Animated Visualizations** - GIF animations showing parameter variations
- ✅ **Fringe Analysis** - Statistics on fringe spacing and intensity distribution
- ✅ **Phase Analysis** - Visualization of phase relationships
- ✅ **Diffraction Simulation** - Shows how slit width affects interference pattern

## 📦 Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Clone or Download the Project

```bash
cd /path/to/project
```

### Step 2: Install Required Dependencies

```bash
pip install numpy matplotlib scipy
```

Or install from requirements file:

```bash
pip install -r requirements.txt
```

### Step 3: Verify Installation

```bash
python -c "import numpy, matplotlib, scipy; print('All dependencies installed successfully!')"
```

## 🚀 Project Setup

### Directory Structure

```
youngs_double_slit_project/
├── youngs_double_slit.py           # Main simulation script
├── youngs_double_slit_analysis.py  # Advanced analysis and animations
├── README.md                        # This file
├── requirements.txt                 # Python dependencies
│
└── Output Files (Generated after running):
    ├── intensity_pattern.png        # 2D intensity heatmap
    ├── cross_sections.png           # Horizontal and vertical cross-sections
    ├── intensity_3d.png             # 3D surface plot
    ├── phase_analysis.png           # Phase pattern visualization
    ├── wavelength_comparison.png    # Comparison across wavelengths
    ├── wavelength_animation.gif     # Animated wavelength variation
    ├── slit_separation_animation.gif # Animated slit separation variation
    └── diffraction_comparison.gif   # Diffraction effect animation
```

## 💻 Usage

### Basic Usage

Run the main simulation:

```bash
python youngs_double_slit.py
```

Run the advanced analysis script:

```bash
python youngs_double_slit_analysis.py
```

### Customizing Parameters

Open `youngs_double_slit.py` and modify the simulation parameters in the main section:

```python
# Simulation parameters (in SI units where applicable)
wavelength = 0.5e-6           # Wavelength in meters (0.5 μm)
slit_separation = 50e-6       # Distance between slits in meters (50 μm)
slit_width = 40e-6            # Width of each slit in meters (40 μm)
distance_to_screen = 1.0      # Distance to screen in meters (1 m)
screen_width = 0.05           # Screen width in meters (50 mm)
screen_height = 0.05          # Screen height in meters (50 mm)
resolution = 400              # Number of points per dimension (400×400)
```

## 📊 Parameters

| Parameter | Description | Typical Range | Unit |
|-----------|-------------|----------------|------|
| **wavelength** | Wavelength of coherent light | 0.3-0.7 | μm |
| **slit_separation** | Distance between centers of two slits | 10-100 | μm |
| **slit_width** | Width of each individual slit | 1-100 | μm |
| **distance_to_screen** | Distance from slits to observation screen | 0.5-2.0 | m |
| **screen_width** | Width of observation region | 0.01-0.1 | m |
| **screen_height** | Height of observation region | 0.01-0.1 | m |
| **resolution** | Grid points per dimension | 200-600 | points |

### Parameter Effects on Output

- **↑ Wavelength**: Larger fringe spacing
- **↑ Slit Separation**: Smaller fringe spacing
- **↑ Distance to Screen**: Larger fringe spacing
- **↑ Slit Width**: Reduced overall intensity (diffraction effect)

## 📁 Output Files

### Static Visualizations

1. **intensity_pattern.png**
   - 2D heatmap of intensity distribution
   - Shows complete interference pattern
   - Useful for identifying bright and dark fringes

2. **cross_sections.png**
   - Horizontal intensity profile (top)
   - Vertical intensity profile (bottom)
   - Helps identify fringe spacing and intensity peaks

3. **intensity_3d.png**
   - 3D surface plot of intensity distribution
   - Provides perspective view of interference pattern
   - Shows intensity gradients clearly

4. **phase_analysis.png**
   - Phase difference visualization
   - Reveals phase relationships between wave components
   - Useful for understanding interference mechanism

5. **wavelength_comparison.png**
   - Comparison of patterns for wavelengths: 0.3 μm, 0.5 μm, 0.7 μm
   - Demonstrates wavelength dependence

### Animated Visualizations

1. **wavelength_animation.gif**
   - 20 frames showing variation from 0.3 μm to 0.7 μm
   - Smooth transition demonstrating wavelength effect

2. **slit_separation_animation.gif**
   - 20 frames showing variation in slit separation
   - Demonstrates inverse relationship with fringe spacing

3. **diffraction_comparison.gif**
   - 20 frames alternating between narrow and wide slits
   - Shows diffraction envelope effect

## 📈 Examples

### Example 1: Visible Light (Red)

```python
wavelength = 0.7e-6        # 700 nm (red light)
slit_separation = 50e-6    # 50 μm
slit_width = 40e-6         # 40 μm
distance_to_screen = 1.0   # 1 meter
```

**Expected Result**: Wide fringe spacing (~7 mm), clear interference pattern

### Example 2: Monochromatic UV

```python
wavelength = 0.3e-6        # 300 nm (UV)
slit_separation = 50e-6    # 50 μm
slit_width = 40e-6         # 40 μm
distance_to_screen = 1.0   # 1 meter
```

**Expected Result**: Narrow fringe spacing (~3 mm), more fringes visible

### Example 3: Tightly Spaced Slits

```python
wavelength = 0.5e-6        # 500 nm
slit_separation = 20e-6    # 20 μm (tighter spacing)
slit_width = 40e-6         # 40 μm
distance_to_screen = 1.0   # 1 meter
```

**Expected Result**: Wide fringe spacing (~25 mm), fewer fringes

## 🔬 Physics Behind the Simulation

### Wave Equation

The intensity at any point (x, y) on the screen is calculated as:

```
I(x,y) = |E₁(x,y) + E₂(x,y)|²
```

Where E₁ and E₂ are the electric field contributions from each slit.

### Fringe Spacing

The theoretical fringe spacing is given by:

```
Δy = λD / d

where:
  λ = wavelength
  D = distance to screen
  d = slit separation
```

### Intensity Formula

```
I ∝ sinc²(πa·sin(θ)/λ) · cos²(πd·sin(θ)/λ)

where:
  a = slit width
  d = slit separation
  θ = angle from center
```

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'numpy'"

**Solution**: Install dependencies
```bash
pip install numpy matplotlib scipy
```

### Issue: No output files generated

**Solution**: Ensure you have write permissions in the project directory
```bash
chmod +x /path/to/project
```

### Issue: Slow animation generation

**Solution**: Reduce resolution or number of frames in the script
```python
resolution = 300  # Lower than 400
num_frames = 10   # Lower than 20
```

### Issue: Patterns don't look right

**Solution**: Verify your parameters make physical sense:
- Check wavelength is very small (e.g., 0.5e-6 for 0.5 μm)
- Ensure slit_width < screen dimensions
- Verify distance_to_screen > 0

## 📝 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Feel free to:
- Modify parameters for different experimental setups
- Extend the code with additional physics (polarization, coherence, etc.)
- Generate publication-quality figures
- Create additional analysis scripts

## 📚 References

- Hecht, E. (2002). Optics (4th ed.)
- Born, M., & Wolf, E. (1999). Principles of Optics
- Feynman, R. P. (1963). The Feynman Lectures on Physics

## 📧 Support

For questions or issues, review the troubleshooting section or check the script comments for detailed explanations of the physics and numerical methods used.

---

**Last Updated**: May 24, 2026
**Version**: 1.0
