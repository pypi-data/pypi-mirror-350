import numpy as np
import matplotlib.pyplot as plt
from scipy.special import hermite
from mpl_toolkits.mplot3d import Axes3D

class TEM:
    """
    Model and visualize Transvers Electro Magnetic (TEM) Gaussian-Hermite (LASER) beam modes.
    
    The beam is characterized by its Gaussian profile, Hermite polynomial mode structure,
    and propagation-dependent parameters such as beam width, curvature, and Gouy phase.
    """
    def __init__(self, w0, l):
        """
        Initialize the Gaussian-Hermite beam model.
        
        Parameters:
            w0 (float):
                Beam waist. This is the smallest radius of the beam.
            l (float):
                Wavelength
        """
        self.w0 = w0  
        self.l = l
        self.zR = np.pi * (self.w0**2) / self.l  # Rayleigh range
        self.k = 2 * np.pi / self.l              # Wave number
        self.w = lambda z: self.w0 * np.sqrt(1 + (z / self.zR) ** 2)
        self.R = lambda z: np.inf if z == 0 else z * (1 + (self.zR / z) ** 2)
        self.zeta = lambda z: np.arctan(z / self.zR)

    def field(self, x, y, z, n, m):
        """
        Calculate the complex electric field of a TEM mode in the z-plane.
        
        Parameters:
            x (numpy array or float):
                The x-coordinates
            y (numpy array or float):
                The y-coordinates
            z (float):
                The z-coordinate
            n (int):
                x-direction mode index (Hermite order)
            m (int):
                y-direction mode index (Hermite order)
        
        Returns:
            (numpy array of ) complex:
                Complex field values at given coordinates
        """
        w_z = self.w(z)
        R_z = self.R(z)
        zeta_z = self.zeta(z)

        # Hermite polynomials
        Hn = hermite(n)
        Hm = hermite(m)

        # Normalized coordinates
        x_norm = np.sqrt(2) * x / w_z
        y_norm = np.sqrt(2) * y / w_z

        # Field calculation
        amplitude = (1 / w_z) * Hn(x_norm) * Hm(y_norm)
        gaussian_envelope = np.exp(-(x**2 + y**2) / w_z**2)
        phase = np.exp(-1j * (
            self.k * z +
            self.k * (x**2 + y**2) / (2 * R_z) -
            (n + m + 1) * zeta_z
        ))

        return amplitude * gaussian_envelope * phase
    def wavelength_to_RGB(self):
        """
        Convert wavelength in nm to a RGB color approximation.
        """
        wavelength = self.l * 1e9
        gamma = 0.8
        intensity_max = 1
        factor = 0.0
        R = G = B = 0.0 
        if 380 <= wavelength < 440:
            R = -(wavelength - 440) / (440 - 380)
            B = 1.0
        elif 440 <= wavelength < 490:
            G = (wavelength - 440) / (490 - 440)
            B = 1.0
        elif 490 <= wavelength < 510:
            G = 1.0
            B = -(wavelength - 510) / (510 - 490)
        elif 510 <= wavelength < 580:
            R = (wavelength - 510) / (580 - 510)
            G = 1.0
        elif 580 <= wavelength < 645:
            R = 1.0
            G = -(wavelength - 645) / (645 - 580)
        elif 645 <= wavelength <= 750:
            R = 1.0
        else:
            return (0, 0, 0) 
        
        if 380 <= wavelength < 420:
            factor = 0.3 + 0.7 * (wavelength - 380) / (420 - 380)
        elif 420 <= wavelength < 645:
            factor = 1.0
        elif 645 <= wavelength <= 750:
            factor = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
        
        R = (R * factor) ** gamma
        G = (G * factor) ** gamma
        B = (B * factor) ** gamma
        return (R, G, B)
    def plot_mode(self, n, m, z, size=2e-3, resolution=500, surf=True, contour=False):
        """
        Plot the intensity distribution of the TEM mode at given z-position.
        
        Parameters:
            n (int):
                x-direction mode index (Hermite order)
            m (int):
                y-direction mode index (Hermite order)
            z (float):
                Propagation distance along z-axis
            size (optional float):
                Half-width of the plot window (default 2e-3)
            resolution (int):
                Number of grid points in each spatial dimension (default 500)
            surf (bool):
                Show the 3D surface plot of the intensity distribution (default True)
            contour (bool):
                Show the 2D contour plot of the intensity distribution (default False)
        Note:
            If the beams wavelength is in the visible range, approx 380 to 750 nm,
            the color of the surface plot corrensponds to
            the percieved color of that light.
            Otherwise, the default colormap is used.
        """
        x = np.linspace(-size, size, resolution)
        y = np.linspace(-size, size, resolution)
        X, Y = np.meshgrid(x, y)
        Xmm, Ymm = X * 1e3, Y * 1e3

        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')
        plt.subplots_adjust(bottom=0.2)

        u = self.field(X, Y, z, n, m)
        I = np.abs(u)**2
        
        rgb_color = self.wavelength_to_RGB()
        if surf:
            if rgb_color == (0, 0, 0):
                surface = ax.plot_surface(Xmm, Ymm, I, cmap='inferno', linewidth=0, antialiased=True, alpha = 0.95)
            else:
                facecolors = np.empty((*I.shape,4))
                facecolors[..., :3] = rgb_color
                facecolors[..., 3] = 0.95
                surface = ax.plot_surface(Xmm, Ymm, I, facecolors=facecolors, linewidth=0, antialiased=True, alpha=0.95)
        if contour:
            contour = ax.contour(Xmm, Ymm, I, zdir='z', offset=0, cmap='gray', linewidths=1)

        ax.set_xlabel('x (mm)')
        ax.set_ylabel('y (mm)')
        ax.set_zlabel('Intensity (a.u.)')
        ax.set_zlim(0, np.max(I)*1.1)
        ax.set_title(f"Hermite-Gaussian Mode TEM$_{{{n},{m}}}$ at z = {z*100:.1f} cm", fontsize=14)


        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    # === HeNe beam ===
    tem = TEM(w0=1e-3, l=632.8e-9)  # 1 mm waist, 632.8 nm wavelength
    tem.plot_mode(1, 1, 1e-3, surf=True, contour=False)