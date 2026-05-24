"""
Young's Double-Slit Experiment Simulation
==========================================

This script simulates the interference pattern created by coherent light
passing through two slits. It calculates the 2D intensity distribution
on a screen and provides both static and animated visualizations.

Physics Principles:
- Wave propagation from point sources
- Superposition principle
- Diffraction and interference
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LogNorm
import matplotlib.patches as patches


class DoubleSlitSimulation:
    """
    Simulates Young's double-slit experiment with coherent light.
    
    Parameters:
    -----------
    wavelength : float
        Wavelength of light in micrometers (λ)
    slit_separation : float
        Distance between the two slits in micrometers (d)
    slit_width : float
        Width of each slit in micrometers (w)
    screen_distance : float
        Distance from slits to screen in millimeters (L)
    screen_width : float
        Total width of the screen in millimeters
    screen_height : float
        Total height of the screen in millimeters
    resolution : int
        Number of points per dimension for the screen grid
    """
    
    def __init__(self, wavelength=0.5, slit_separation=50, slit_width=40,
                 screen_distance=1000, screen_width=50, screen_height=50,
                 resolution=300):
        """Initialize the double-slit simulation parameters."""
        self.wavelength = wavelength  # micrometers
        self.slit_separation = slit_separation  # micrometers
        self.slit_width = slit_width  # micrometers
        self.screen_distance = screen_distance  # millimeters
        self.screen_width = screen_width  # millimeters
        self.screen_height = screen_height  # millimeters
        self.resolution = resolution
        
        # Wavenumber k = 2π/λ
        self.k = 2 * np.pi / wavelength
        
        # Create screen coordinate system (convert to micrometers for consistency)
        self.x_screen = np.linspace(-screen_width / 2, screen_width / 2, resolution) * 1000
        self.y_screen = np.linspace(-screen_height / 2, screen_height / 2, resolution) * 1000
        self.X, self.Y = np.meshgrid(self.x_screen, self.y_screen)
        
        # Screen distance in micrometers
        self.z_screen = screen_distance * 1000
        
        # Slit positions (centered on y-axis)
        self.slit1_y = slit_separation / 2
        self.slit2_y = -slit_separation / 2
        self.slit1_x = 0
        self.slit2_x = 0
        
        print(f"Simulation Parameters:")
        print(f"  Wavelength: {wavelength} μm")
        print(f"  Slit Separation: {slit_separation} μm")
        print(f"  Slit Width: {slit_width} μm")
        print(f"  Screen Distance: {screen_distance} mm")
        print(f"  Screen Size: {screen_width} × {screen_height} mm")
        print(f"  Resolution: {resolution} × {resolution} points")
        print()
    
    def single_slit_amplitude(self, x, y, slit_x, slit_y, z):
        """
        Calculate amplitude from a single slit using Fresnel approximation.
        
        The single-slit diffraction pattern accounts for the finite width of each slit
        by integrating contributions from point sources across the slit width.
        
        Parameters:
        -----------
        x, y : 2D arrays
            Coordinates on the screen
        slit_x, slit_y : float
            Position of the slit center
        z : float
            Distance to screen
            
        Returns:
        --------
        amplitude : 2D complex array
            Complex amplitude at each point
        """
        # Distance from slit to screen point
        r = np.sqrt((x - slit_x)**2 + (y - slit_y)**2 + z**2)
        
        # Fraunhofer approximation: use average distance for amplitude
        # Fresnel zones for phase calculation
        phase = self.k * r
        
        # Single slit diffraction envelope (sinc function for rectangular slit)
        slit_width_rad = self.k * self.slit_width * (y - slit_y) / (2 * r)
        
        # Avoid division by zero
        sinc_arg = slit_width_rad
        with np.errstate(divide='ignore', invalid='ignore'):
            slit_envelope = np.sinc(sinc_arg / np.pi)
            slit_envelope[sinc_arg == 0] = 1.0
        
        # Complex amplitude
        amplitude = slit_envelope * np.exp(1j * phase) / r
        
        return amplitude
    
    def calculate_interference_pattern(self, use_diffraction=True):
        """
        Calculate the interference pattern on the screen.
        
        Combines amplitudes from both slits and calculates the resulting intensity.
        
        Parameters:
        -----------
        use_diffraction : bool
            If True, includes single-slit diffraction effects
            If False, uses point sources (interference only)
            
        Returns:
        --------
        intensity : 2D array
            Intensity pattern on the screen (normalized)
        """
        if use_diffraction:
            # Include single-slit diffraction
            amp1 = self.single_slit_amplitude(self.X, self.Y, self.slit1_x, self.slit1_y, self.z_screen)
            amp2 = self.single_slit_amplitude(self.X, self.Y, self.slit2_x, self.slit2_y, self.z_screen)
        else:
            # Point source approximation
            r1 = np.sqrt((self.X - self.slit1_x)**2 + (self.Y - self.slit1_y)**2 + self.z_screen**2)
            r2 = np.sqrt((self.X - self.slit2_x)**2 + (self.Y - self.slit2_y)**2 + self.z_screen**2)
            
            phase1 = self.k * r1
            phase2 = self.k * r2
            
            # Unit amplitude sources
            amp1 = np.exp(1j * phase1) / r1
            amp2 = np.exp(1j * phase2) / r2
        
        # Total amplitude (superposition)
        total_amp = amp1 + amp2
        
        # Intensity (square of amplitude magnitude)
        intensity = np.abs(total_amp)**2
        
        # Normalize
        intensity = intensity / np.max(intensity)
        
        return intensity
    
    def calculate_path_difference(self):
        """
        Calculate the path difference between rays from the two slits.
        
        Returns:
        --------
        path_diff : 2D array
            Path difference at each point on the screen (in wavelengths)
        """
        r1 = np.sqrt((self.X - self.slit1_x)**2 + (self.Y - self.slit1_y)**2 + self.z_screen**2)
        r2 = np.sqrt((self.X - self.slit2_x)**2 + (self.Y - self.slit2_y)**2 + self.z_screen**2)
        
        path_diff = (r2 - r1) / self.wavelength
        return path_diff
    
    def plot_intensity_pattern(self, use_diffraction=True, use_log_scale=False):
        """
        Create a static plot of the intensity pattern.
        
        Parameters:
        -----------
        use_diffraction : bool
            Include single-slit diffraction
        use_log_scale : bool
            Use logarithmic scale for intensity
        """
        intensity = self.calculate_interference_pattern(use_diffraction)
        path_diff = self.calculate_path_difference()
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # Plot 1: Intensity pattern
        norm = LogNorm(vmin=intensity[intensity > 0].min(), vmax=1) if use_log_scale else None
        im1 = axes[0].imshow(intensity, extent=[-self.screen_width/2, self.screen_width/2,
                                                   -self.screen_height/2, self.screen_height/2],
                            origin='lower', cmap='hot', norm=norm)
        axes[0].set_xlabel('Horizontal Position (mm)')
        axes[0].set_ylabel('Vertical Position (mm)')
        axes[0].set_title('Intensity Pattern on Screen\n(Young\'s Double-Slit Experiment)')
        cbar1 = plt.colorbar(im1, ax=axes[0])
        cbar1.set_label('Intensity (Normalized)')
        
        # Plot 2: Path difference
        im2 = axes[1].contourf(self.X / 1000, self.Y / 1000, path_diff, levels=20, cmap='viridis')
        axes[1].set_xlabel('Horizontal Position (mm)')
        axes[1].set_ylabel('Vertical Position (mm)')
        axes[1].set_title('Path Difference\n(in wavelengths)')
        cbar2 = plt.colorbar(im2, ax=axes[1])
        cbar2.set_label('Path Difference (λ)')
        
        # Add contour lines for constructive interference
        levels = np.arange(-5, 5, 1)
        axes[1].contour(self.X / 1000, self.Y / 1000, path_diff, levels=levels, colors='white', alpha=0.3, linewidths=0.5)
        
        plt.tight_layout()
        return fig, axes
    
    def plot_cross_section(self, use_diffraction=True):
        """
        Plot 1D cross-sections of the intensity pattern.
        
        Parameters:
        -----------
        use_diffraction : bool
            Include single-slit diffraction
        """
        intensity = self.calculate_interference_pattern(use_diffraction)
        
        # Get central row and column
        center_idx = self.resolution // 2
        horizontal = intensity[center_idx, :]
        vertical = intensity[:, center_idx]
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 4))
        
        x_axis = self.x_screen / 1000  # Convert to mm
        y_axis = self.y_screen / 1000  # Convert to mm
        
        # Horizontal cross-section
        axes[0].plot(x_axis, horizontal, linewidth=2, color='blue')
        axes[0].fill_between(x_axis, horizontal, alpha=0.3)
        axes[0].set_xlabel('Horizontal Position (mm)')
        axes[0].set_ylabel('Intensity (Normalized)')
        axes[0].set_title('Horizontal Cross-Section (Central Row)')
        axes[0].grid(True, alpha=0.3)
        
        # Vertical cross-section
        axes[1].plot(y_axis, vertical, linewidth=2, color='red')
        axes[1].fill_between(y_axis, vertical, alpha=0.3, color='red')
        axes[1].set_xlabel('Vertical Position (mm)')
        axes[1].set_ylabel('Intensity (Normalized)')
        axes[1].set_title('Vertical Cross-Section (Central Column)')
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig, axes
    
    def create_wavelength_animation(self, num_frames=20):
        """
        Create an animation showing how the pattern changes with wavelength.
        
        Parameters:
        -----------
        num_frames : int
            Number of frames in the animation
        """
        wavelengths = np.linspace(0.3, 0.8, num_frames)
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        def update_frame(frame):
            ax.clear()
            
            # Save original wavelength
            original_k = self.k
            original_wavelength = self.wavelength
            
            # Update wavelength
            self.wavelength = wavelengths[frame]
            self.k = 2 * np.pi / self.wavelength
            
            # Calculate pattern
            intensity = self.calculate_interference_pattern(use_diffraction=True)
            
            # Plot
            im = ax.imshow(intensity, extent=[-self.screen_width/2, self.screen_width/2,
                                              -self.screen_height/2, self.screen_height/2],
                           origin='lower', cmap='hot', vmin=0, vmax=1)
            ax.set_xlabel('Horizontal Position (mm)')
            ax.set_ylabel('Vertical Position (mm)')
            ax.set_title(f'Intensity Pattern - Wavelength: {self.wavelength:.2f} μm')
            
            # Restore original wavelength
            self.wavelength = original_wavelength
            self.k = original_k
            
            return [im]
        
        anim = FuncAnimation(fig, update_frame, frames=num_frames, blit=True, repeat=True)
        return fig, anim
    
    def create_slit_separation_animation(self, num_frames=20):
        """
        Create an animation showing how the pattern changes with slit separation.
        
        Parameters:
        -----------
        num_frames : int
            Number of frames in the animation
        """
        separations = np.linspace(10, 100, num_frames)
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        def update_frame(frame):
            ax.clear()
            
            # Save original separation
            original_sep = self.slit_separation
            
            # Update separation
            self.slit_separation = separations[frame]
            self.slit1_y = self.slit_separation / 2
            self.slit2_y = -self.slit_separation / 2
            
            # Calculate pattern
            intensity = self.calculate_interference_pattern(use_diffraction=True)
            
            # Plot
            im = ax.imshow(intensity, extent=[-self.screen_width/2, self.screen_width/2,
                                              -self.screen_height/2, self.screen_height/2],
                           origin='lower', cmap='hot', vmin=0, vmax=1)
            ax.set_xlabel('Horizontal Position (mm)')
            ax.set_ylabel('Vertical Position (mm)')
            ax.set_title(f'Intensity Pattern - Slit Separation: {self.slit_separation:.1f} μm')
            
            # Restore original separation
            self.slit_separation = original_sep
            self.slit1_y = self.slit_separation / 2
            self.slit2_y = -self.slit_separation / 2
            
            return [im]
        
        anim = FuncAnimation(fig, update_frame, frames=num_frames, blit=True, repeat=True)
        return fig, anim
    
    def print_fringe_statistics(self, use_diffraction=True):
        """
        Calculate and print statistics about the fringe pattern.
        
        Parameters:
        -----------
        use_diffraction : bool
            Include single-slit diffraction
        """
        intensity = self.calculate_interference_pattern(use_diffraction)
        path_diff = self.calculate_path_difference()
        
        print("Fringe Statistics:")
        print(f"  Maximum intensity: {np.max(intensity):.4f}")
        print(f"  Minimum intensity: {np.min(intensity):.4f}")
        print(f"  Mean intensity: {np.mean(intensity):.4f}")
        print(f"  Standard deviation: {np.std(intensity):.4f}")
        print()
        
        # Fringe spacing (Δy = λL/d)
        fringe_spacing = (self.wavelength * self.z_screen) / self.slit_separation
        print(f"Expected fringe spacing: {fringe_spacing:.4f} μm ({fringe_spacing/1000:.4f} mm)")
        
        # Find maxima
        from scipy import ndimage
        # Threshold to find peaks
        threshold = 0.9 * np.max(intensity)
        labeled, num_features = ndimage.label(intensity > threshold)
        print(f"Approximate number of bright fringes: {num_features}")
        print()


def main():
    """Main execution function."""
    
    print("=" * 60)
    print("Young's Double-Slit Experiment Simulation")
    print("=" * 60)
    print()
    
    # Create simulation with default parameters
    sim = DoubleSlitSimulation(
        wavelength=0.5,           # 500 nm (green light)
        slit_separation=50,       # 50 micrometers
        slit_width=40,            # 40 micrometers
        screen_distance=1000,     # 1000 mm (1 meter)
        screen_width=50,          # 50 mm wide screen
        screen_height=50,         # 50 mm tall screen
        resolution=400            # 400x400 pixel resolution
    )
    
    # Calculate and print statistics
    sim.print_fringe_statistics(use_diffraction=True)
    
    # 1. Static intensity pattern with path difference
    print("Creating intensity pattern plot...")
    fig1, _ = sim.plot_intensity_pattern(use_diffraction=True, use_log_scale=False)
    fig1.savefig('/Users/pradeep/Shreyashi/Projects/intensity_pattern.png', dpi=300, bbox_inches='tight')
    print("Saved: intensity_pattern.png")
    print()
    
    # 2. Cross-sections
    print("Creating cross-section plots...")
    fig2, _ = sim.plot_cross_section(use_diffraction=True)
    fig2.savefig('/Users/pradeep/Shreyashi/Projects/cross_sections.png', dpi=300, bbox_inches='tight')
    print("Saved: cross_sections.png")
    print()
    
    # 3. Wavelength animation
    print("Creating wavelength animation (this may take a moment)...")
    fig3, anim3 = sim.create_wavelength_animation(num_frames=20)
    anim3.save('/Users/pradeep/Shreyashi/Projects/wavelength_animation.gif', writer='pillow', fps=2)
    print("Saved: wavelength_animation.gif")
    print()
    
    # 4. Slit separation animation
    print("Creating slit separation animation (this may take a moment)...")
    fig4, anim4 = sim.create_slit_separation_animation(num_frames=20)
    anim4.save('/Users/pradeep/Shreyashi/Projects/slit_separation_animation.gif', writer='pillow', fps=2)
    print("Saved: slit_separation_animation.gif")
    print()
    
    # Show plots
    plt.show()
    
    print("=" * 60)
    print("Simulation complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()

