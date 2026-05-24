"""
Enhanced Young's Double-Slit Experiment - Interactive Analysis Script
======================================================================

This script provides additional analysis and visualization capabilities
for the Young's double-slit experiment simulation, including:
- Interactive parameter adjustment
- Detailed fringe analysis
- 3D visualization
- Multiple simulation scenarios
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import sys

# Import the simulation class
sys.path.insert(0, '/Users/pradeep/Shreyashi/Projects')
from youngs_double_slit import DoubleSlitSimulation


def analyze_fringe_pattern(sim, use_diffraction=True):
    """
    Perform detailed analysis of the fringe pattern.
    
    Parameters:
    -----------
    sim : DoubleSlitSimulation
        The simulation object
    use_diffraction : bool
        Include single-slit diffraction
    """
    intensity = sim.calculate_interference_pattern(use_diffraction)
    
    # Get central horizontal line
    center_idx = sim.resolution // 2
    horizontal = intensity[center_idx, :]
    
    # Find local maxima (bright fringes)
    from scipy.signal import argrelextrema
    maxima_indices = argrelextrema(horizontal, np.greater, order=10)[0]
    
    print("Fringe Analysis:")
    print(f"  Number of detectable bright fringes: {len(maxima_indices)}")
    
    if len(maxima_indices) > 1:
        # Calculate spacing between adjacent maxima
        spacings = np.diff(maxima_indices)
        spacing_mm = spacings * (sim.screen_width / sim.resolution)
        
        print(f"  Average fringe spacing: {np.mean(spacing_mm):.4f} mm")
        print(f"  Min fringe spacing: {np.min(spacing_mm):.4f} mm")
        print(f"  Max fringe spacing: {np.max(spacing_mm):.4f} mm")
        print(f"  Fringe spacing std dev: {np.std(spacing_mm):.4f} mm")
        
        # Visibility (contrast)
        max_intensity = np.max(horizontal)
        min_intensity = np.min(horizontal)
        visibility = (max_intensity - min_intensity) / (max_intensity + min_intensity)
        print(f"  Visibility (contrast): {visibility:.4f}")
    print()


def plot_3d_intensity(sim, use_diffraction=True):
    """
    Create a 3D surface plot of the intensity pattern.
    
    Parameters:
    -----------
    sim : DoubleSlitSimulation
        The simulation object
    use_diffraction : bool
        Include single-slit diffraction
    """
    intensity = sim.calculate_interference_pattern(use_diffraction)
    
    # Downsample for faster plotting
    step = 4
    X_plot = sim.X[::step, ::step] / 1000
    Y_plot = sim.Y[::step, ::step] / 1000
    Z_plot = intensity[::step, ::step]
    
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')
    
    surf = ax.plot_surface(X_plot, Y_plot, Z_plot, cmap='hot', 
                           linewidth=0, antialiased=True, alpha=0.8)
    
    ax.set_xlabel('Horizontal Position (mm)')
    ax.set_ylabel('Vertical Position (mm)')
    ax.set_zlabel('Intensity (Normalized)')
    ax.set_title('3D Intensity Pattern - Young\'s Double-Slit Experiment')
    
    cbar = fig.colorbar(surf, ax=ax, pad=0.1)
    cbar.set_label('Intensity')
    
    return fig, ax


def plot_phase_pattern(sim):
    """
    Plot the phase pattern from both slits.
    
    Parameters:
    -----------
    sim : DoubleSlitSimulation
        The simulation object
    """
    # Calculate phases from both slits
    r1 = np.sqrt((sim.X - sim.slit1_x)**2 + (sim.Y - sim.slit1_y)**2 + sim.z_screen**2)
    r2 = np.sqrt((sim.X - sim.slit2_x)**2 + (sim.Y - sim.slit2_y)**2 + sim.z_screen**2)
    
    phase1 = (sim.k * r1) % (2 * np.pi)
    phase2 = (sim.k * r2) % (2 * np.pi)
    phase_diff = (phase2 - phase1) % (2 * np.pi)
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    
    # Phase from slit 1
    im1 = axes[0, 0].imshow(phase1, extent=[-sim.screen_width/2, sim.screen_width/2,
                                             -sim.screen_height/2, sim.screen_height/2],
                            origin='lower', cmap='hsv')
    axes[0, 0].set_title('Phase from Slit 1')
    axes[0, 0].set_xlabel('Horizontal Position (mm)')
    axes[0, 0].set_ylabel('Vertical Position (mm)')
    plt.colorbar(im1, ax=axes[0, 0], label='Phase (rad)')
    
    # Phase from slit 2
    im2 = axes[0, 1].imshow(phase2, extent=[-sim.screen_width/2, sim.screen_width/2,
                                             -sim.screen_height/2, sim.screen_height/2],
                            origin='lower', cmap='hsv')
    axes[0, 1].set_title('Phase from Slit 2')
    axes[0, 1].set_xlabel('Horizontal Position (mm)')
    axes[0, 1].set_ylabel('Vertical Position (mm)')
    plt.colorbar(im2, ax=axes[0, 1], label='Phase (rad)')
    
    # Phase difference
    im3 = axes[1, 0].imshow(phase_diff, extent=[-sim.screen_width/2, sim.screen_width/2,
                                                 -sim.screen_height/2, sim.screen_height/2],
                            origin='lower', cmap='hsv')
    axes[1, 0].set_title('Phase Difference (Slit 2 - Slit 1)')
    axes[1, 0].set_xlabel('Horizontal Position (mm)')
    axes[1, 0].set_ylabel('Vertical Position (mm)')
    plt.colorbar(im3, ax=axes[1, 0], label='Phase Difference (rad)')
    
    # Constructive/Destructive interference regions
    intensity = sim.calculate_interference_pattern(use_diffraction=False)
    im4 = axes[1, 1].imshow(intensity, extent=[-sim.screen_width/2, sim.screen_width/2,
                                                -sim.screen_height/2, sim.screen_height/2],
                            origin='lower', cmap='hot')
    axes[1, 1].set_title('Resulting Intensity Pattern')
    axes[1, 1].set_xlabel('Horizontal Position (mm)')
    axes[1, 1].set_ylabel('Vertical Position (mm)')
    plt.colorbar(im4, ax=axes[1, 1], label='Intensity')
    
    plt.tight_layout()
    return fig, axes


def create_comparison_animation(num_frames=15):
    """
    Create animation comparing different diffraction effects.
    
    Parameters:
    -----------
    num_frames : int
        Number of frames in animation
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    def update_frame(frame):
        # Vary slit width from very narrow to very wide
        slit_widths = np.linspace(5, 80, num_frames)
        
        for ax in axes:
            ax.clear()
        
        # Create simulations with different slit widths
        sim_with_diffraction = DoubleSlitSimulation(
            wavelength=0.5,
            slit_separation=50,
            slit_width=slit_widths[frame],
            screen_distance=1000,
            screen_width=50,
            screen_height=50,
            resolution=300
        )
        
        sim_no_diffraction = DoubleSlitSimulation(
            wavelength=0.5,
            slit_separation=50,
            slit_width=0.1,  # Very narrow
            screen_distance=1000,
            screen_width=50,
            screen_height=50,
            resolution=300
        )
        
        # Calculate patterns
        intensity_with_diff = sim_with_diffraction.calculate_interference_pattern(use_diffraction=True)
        intensity_no_diff = sim_no_diffraction.calculate_interference_pattern(use_diffraction=False)
        
        # Plot with diffraction
        im1 = axes[0].imshow(intensity_with_diff, 
                            extent=[-sim_with_diffraction.screen_width/2, sim_with_diffraction.screen_width/2,
                                   -sim_with_diffraction.screen_height/2, sim_with_diffraction.screen_height/2],
                            origin='lower', cmap='hot', vmin=0, vmax=1)
        axes[0].set_xlabel('Horizontal Position (mm)')
        axes[0].set_ylabel('Vertical Position (mm)')
        axes[0].set_title(f'With Diffraction (Slit Width: {slit_widths[frame]:.1f} μm)')
        plt.colorbar(im1, ax=axes[0], label='Intensity')
        
        # Plot without diffraction (point sources)
        im2 = axes[1].imshow(intensity_no_diff,
                            extent=[-sim_no_diffraction.screen_width/2, sim_no_diffraction.screen_width/2,
                                   -sim_no_diffraction.screen_height/2, sim_no_diffraction.screen_height/2],
                            origin='lower', cmap='hot', vmin=0, vmax=1)
        axes[1].set_xlabel('Horizontal Position (mm)')
        axes[1].set_ylabel('Vertical Position (mm)')
        axes[1].set_title('Without Diffraction (Point Sources)')
        plt.colorbar(im2, ax=axes[1], label='Intensity')
        
        return [im1, im2]
    
    anim = FuncAnimation(fig, update_frame, frames=num_frames, blit=True, repeat=True)
    return fig, anim


def visualize_diffraction_effects(wavelengths=[0.3, 0.5, 0.7]):
    """
    Show how different wavelengths affect the pattern.
    
    Parameters:
    -----------
    wavelengths : list
        List of wavelengths to compare in micrometers
    """
    n_plots = len(wavelengths)
    fig, axes = plt.subplots(1, n_plots, figsize=(5*n_plots, 5))
    
    if n_plots == 1:
        axes = [axes]
    
    for idx, wavelength in enumerate(wavelengths):
        sim = DoubleSlitSimulation(
            wavelength=wavelength,
            slit_separation=50,
            slit_width=40,
            screen_distance=1000,
            screen_width=50,
            screen_height=50,
            resolution=300
        )
        
        intensity = sim.calculate_interference_pattern(use_diffraction=True)
        
        im = axes[idx].imshow(intensity, 
                             extent=[-sim.screen_width/2, sim.screen_width/2,
                                    -sim.screen_height/2, sim.screen_height/2],
                             origin='lower', cmap='hot')
        axes[idx].set_xlabel('Horizontal Position (mm)')
        axes[idx].set_ylabel('Vertical Position (mm)')
        axes[idx].set_title(f'Wavelength: {wavelength} μm')
        
        plt.colorbar(im, ax=axes[idx], label='Intensity')
    
    plt.suptitle('Effect of Wavelength on Double-Slit Pattern', fontsize=14, y=1.02)
    plt.tight_layout()
    
    return fig, axes


def main():
    """Main execution for enhanced analysis."""
    
    print("=" * 70)
    print("Enhanced Young's Double-Slit Experiment Analysis")
    print("=" * 70)
    print()
    
    # Create main simulation
    sim = DoubleSlitSimulation(
        wavelength=0.5,
        slit_separation=50,
        slit_width=40,
        screen_distance=1000,
        screen_width=50,
        screen_height=50,
        resolution=400
    )
    
    # Fringe analysis
    print("Analyzing fringe pattern with diffraction...")
    analyze_fringe_pattern(sim, use_diffraction=True)
    
    print("Analyzing fringe pattern without diffraction...")
    analyze_fringe_pattern(sim, use_diffraction=False)
    
    # 3D visualization
    print("Creating 3D intensity surface plot...")
    fig_3d, _ = plot_3d_intensity(sim, use_diffraction=True)
    fig_3d.savefig('/Users/pradeep/Shreyashi/Projects/intensity_3d.png', dpi=300, bbox_inches='tight')
    print("Saved: intensity_3d.png")
    print()
    
    # Phase pattern analysis
    print("Creating phase pattern analysis...")
    fig_phase, _ = plot_phase_pattern(sim)
    fig_phase.savefig('/Users/pradeep/Shreyashi/Projects/phase_analysis.png', dpi=300, bbox_inches='tight')
    print("Saved: phase_analysis.png")
    print()
    
    # Wavelength comparison
    print("Creating wavelength comparison...")
    fig_wavelength, _ = visualize_diffraction_effects(wavelengths=[0.3, 0.5, 0.7])
    fig_wavelength.savefig('/Users/pradeep/Shreyashi/Projects/wavelength_comparison.png', dpi=300, bbox_inches='tight')
    print("Saved: wavelength_comparison.png")
    print()
    
    # Diffraction effect animation
    print("Creating diffraction effect animation...")
    fig_comp, anim_comp = create_comparison_animation(num_frames=15)
    anim_comp.save('/Users/pradeep/Shreyashi/Projects/diffraction_comparison.gif', writer='pillow', fps=1)
    print("Saved: diffraction_comparison.gif")
    print()
    
    plt.show()
    
    print("=" * 70)
    print("Enhanced analysis complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()

