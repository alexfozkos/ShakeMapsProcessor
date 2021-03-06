# code from Impactutils/colors/cpalette.py and Shakemap/mapping/mapmaker.py
# Used so I can use the Shakemap colormap for mmi values and plot the legend as well for mmi
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
from matplotlib.font_manager import FontProperties
from matplotlib import patches
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import pandas as pd
MMI = {'z0': np.arange(0, 10),
       'z1': np.arange(1, 11),
       'rgb0': [(255, 255, 255),
                (255, 255, 255),
                (191, 204, 255),
                (160, 230, 255),
                (128, 255, 255),
                (122, 255, 147),
                (255, 255, 0),
                (255, 200, 0),
                (255, 145, 0),
                (255, 0, 0)],
       'rgb1': [(255, 255, 255),
                (191, 204, 255),
                (160, 230, 255),
                (128, 255, 255),
                (122, 255, 147),
                (255, 255, 0),
                (255, 200, 0),
                (255, 145, 0),
                (255, 0, 0),
                (200, 0, 0)],
       'nan_color': (0, 0, 0, 0),
       'resolution': 0.1}

POP = {'z0': [0, 4, 49, 99, 499, 999, 4999, 9999],
       'z1': [4, 49, 99, 499, 999, 4999, 9999, 50000],
       'rgb0': [(255, 255, 255),
                (191, 191, 191),
                (159, 159, 159),
                (127, 127, 127),
                (95, 95, 95),
                (63, 63, 63),
                (31, 31, 31),
                (0, 0, 0)],
       'rgb1': [(255, 255, 255),
                (191, 191, 191),
                (159, 159, 159),
                (127, 127, 127),
                (95, 95, 95),
                (63, 63, 63),
                (31, 31, 31),
                (0, 0, 0)],
       'nan_color': (0, 0, 0, 0),
       'resolution': 1.0}


TOPO = {'z0': [-100, 0, 50, 350, 1000, 1800, 2300, 2600, 4000, 9000, 9100],
        'z1': [0, 50, 350, 1000, 1800, 2300, 2600, 4000, 9000, 9200],
        'rgb0': [(195, 255, 193),
                 (110, 135, 80),
                 (120, 160, 90),
                 (230, 220, 110),
                 (210, 170, 80),
                 (195, 140, 100),
                 (100, 80, 70),
                 (60, 60, 60),
                 (255, 255, 255),
                 (255, 255, 255),
                 (255, 128, 0)],
        'rgb1': [(110, 135, 80),
                 (120, 160, 90),
                 (230, 220, 110),
                 (210, 170, 80),
                 (195, 140, 100),
                 (100, 80, 70),
                 (60, 60, 60),
                 (255, 255, 255),
                 (255, 255, 255),
                 (255, 128, 0),
                 (255, 0, 0)],
        'nan_color': (128, 128, 128, 0),
        'resolution': 1.0}

PALETTES = {'mmi': MMI,
            'pop': POP,
            'shaketopo': TOPO}

DEFAULT_NCOLORS = 256

class ColorPalette(object):
    def __init__(self, name, z0, z1, rgb0, rgb1,
                 resolution=None, nan_color=0, is_log=False):
        """Construct a DataColorMap from input Z values and RGB specs.
        Args:
            name: Name of colormap.
            z0: Sequence of z0 values.
            z1: Sequence of z1 values.
            rgb0: Sequence of RGB triplets (values between 0-255).
            rgb1: Sequence of RGB triplets (values between 0-255).
            resolution: Desired Resolution of the data values in data units.
                For example, the preset population color map has a resolution
                of 1.0, meaning that we want to be able to distinguish between
                color values associated with a difference of 1 person. This
                sets the number of colors to be:
                    `max(256,int((max(z1)-min(z0))/resolution))`
            nan_color: Either 0 or RGBA quadruplet (A is for Alpha, where 0 is
                transparent, and 255 is opaque.)
        """

        self._is_log = is_log
        z0 = np.array(z0)
        z1 = np.array(z1)
        self._vmin = z0.min()
        self._vmax = z1.max()
        if isinstance(nan_color, int):
            nan_color = [nan_color] * 4
        self.nan_color = np.array(nan_color) / 255.0

        # Change the z values to be between 0 and 1
        adj_z0 = (z0 - self._vmin) / (self._vmax - self._vmin)
        # should this be z0 - vmin?
        adj_z1 = (z1 - self._vmin) / (self._vmax - self._vmin)

        # loop over the sequences, and construct a dictionary of red, green,
        # blue tuples
        B = -.999 * 255
        # this will mark the y0 value in the first row (isn't used)
        E = .999 * 255
        # this will mark the y1 value in the last row (isn't used)

        # if we add dummy rows to our rgb sequences, we can do one simple loop
        # through.
        rgb0_t = rgb0.copy()
        rgb1_t = rgb1.copy()
        # append a dummy row to the end of RGB0
        rgb0_t.append((E, E, E))
        # prepend a dummy row to the beginning of RGB1
        rgb1_t.insert(0, (B, B, B))
        # Make the column of x values have the same length as the rgb sequences
        x = np.append(adj_z0, adj_z1[-1])

        cdict = {'red': [],
                 'green': [],
                 'blue': []
                 }

        for i in range(0, len(x)):
            red0 = rgb1_t[i][0] / 255.0
            red1 = rgb0_t[i][0] / 255.0
            green0 = rgb1_t[i][1] / 255.0
            green1 = rgb0_t[i][1] / 255.0
            blue0 = rgb1_t[i][2] / 255.0
            blue1 = rgb0_t[i][2] / 255.0
            cdict['red'].append((x[i], red0, red1))
            cdict['green'].append((x[i], green0, green1))
            cdict['blue'].append((x[i], blue0, blue1))

        self._cdict = cdict.copy()
        # choose the number of colors to store the colormap
        # if we choose too low, then there may not be enough colors to
        # accurately capture the resolution of our data.
        # this isn't perfect
        numcolors = DEFAULT_NCOLORS
        if resolution is not None:
            ncolors_tmp = np.ceil((self._vmax - self._vmin) / resolution)
            numcolors = max(DEFAULT_NCOLORS, ncolors_tmp)

        self._cmap = LinearSegmentedColormap(name, cdict, N=numcolors)
        self._cmap.set_bad(self.nan_color)

    @classmethod
    def fromPreset(cls, preset):
        """Construct a ColorPalette from one of several preset color maps.
        Args:
            preset: String to represent one of the preset color maps (see
                getPresets()).
        Returns:
            ColorPalette object.
        """

        z0 = PALETTES[preset]['z0'].copy()
        z1 = PALETTES[preset]['z1'].copy()
        rgb0 = PALETTES[preset]['rgb0'].copy()
        rgb1 = PALETTES[preset]['rgb1'].copy()
        nan_color = PALETTES[preset]['nan_color']
        resolution = None
        if 'resolution' in PALETTES[preset]:
            resolution = PALETTES[preset]['resolution']
        return cls(preset, z0=z0, z1=z1, rgb0=rgb0, rgb1=rgb1,
                   nan_color=nan_color, resolution=resolution)

    @property
    def vmin(self):
        """Property accessor for vmin.
        Returns:
            Minimum data value for ColorPalette.
        """
        return self._vmin

    @vmin.setter
    def vmin(self, value):
        """Property setter for vmin.
        Args:
            value: Float data value to which vmin should be set.
        """
        self._vmin = value

    @property
    def vmax(self):
        """Property accessor for vmax.
        Returns:
            Maximum data value for ColorPalette.
        """
        return self._vmax

    @vmax.setter
    def vmax(self, value):
        """Property setter for vmax.
        Args:
            value: Float data value to which vmax should be set.
        """
        self._vmax = value

    @property
    def cmap(self):
        """
        Property accessor for the Matplotlib colormap contained within the
        ColorPalette object.
        Returns:
            Matplotlib colormap object.
        """
        return self._cmap

    def getDataColor(self, value, color_format='mlab'):
        """Get the RGB color associated with a given data value.
        Args:
            value: Data value for which color should be retrieved.
            color_format: Output format for color specification.  Choices are:
                - 'mlab' Return a 4 element tuple of (R,G,B,A) with float
                  values between 0 and 1.
                - '255' Return a 4 element tuple of (R,G,B,A) with integer
                  values betwen 0 and 255.
                - 'hex' Return an HTML-style hex color specification (#RRGGBB).
                - 'array' Return an RGBA array of the same 1 or 2D dimensions
                   as value.
        Returns:
            The color value associated with the input data value.
        Raises:
            AttributeError when color_format is not recognized.
        """
        if self._is_log:
            value = np.log(value)
        normvalue = (value - self.vmin) / (self.vmax - self.vmin)
        color = self.cmap(normvalue)
        if color_format == 'mlab':
            return color
        elif color_format == '255':
            color255 = tuple([int(c * 255) for c in color])
            return color255
        elif color_format == 'array':
            rgba = np.uint8(color * 255)
            return rgba
        elif color_format == 'hex':
            color255 = [int(c * 255) for c in color]
            str_fmt = f'#{color255[0]:02x}{color255[1]:02x}{color255[2]:02x}'
            hexcolor = (str_fmt).upper()
            return hexcolor
        else:
            raise AttributeError(
                f'Color format {color_format} is not supported.')

mmimap = ColorPalette.fromPreset('mmi')
mmi_cmap = mmimap.cmap

def draw_colorbar(fig, mmimap, tdict):
    """Draw an MMI colorbar in a separate axis from the map.
    Args:
        fig (Figure): Matplotlib Figure object.
        mmimap (ColorPalette): Impactutils MMI ColorPalette instance.
        tdict (dict): Dictionary containing the text strings in the user's
            choice of language.
    """
    # making up our own colorbar object here because the default
    # pyplot functionality doesn't seem to do the job.
    cax = fig.add_axes([0.1, 0.035, 0.8, 0.035])
    cax.get_yaxis().set_visible(False)
    cax_xmin, cax_xmax = cax.get_xlim()
    bottom, top = cax.get_ylim()
    plt.xlim(cax_xmin, cax_xmax)
    plt.ylim(bottom, top)
    nsteps = 200
    left = 0
    rights = np.arange(1 / nsteps, 1 + (1 / nsteps), 1 / nsteps)
    mmis = np.linspace(1, 10, nsteps)
    for mmi, right in zip(mmis, rights):
        px = [left, right, right, left, left]
        py = [top, top, bottom, bottom, top]
        mmicolor = mmimap.getDataColor(mmi, color_format="hex")
        left = right
        plt.fill(px, py, mmicolor, ec=mmicolor)

    start_loc = (1 / nsteps) - (1 / nsteps) / 2
    end_loc = 1 - (1 / nsteps) / 2
    locs = np.linspace(start_loc, end_loc, 10)

    # plt.xticks(locs, tdict["mmi_scale"]["mmi_colorbar_labels"])
    plt.xticks(locs, ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X+'])
