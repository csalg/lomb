import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy.spatial import cKDTree


def heatmap(xs, ys, neighbours=50):
    """
    Attribution: https://stackoverflow.com/questions/2369492/generate-a-heatmap-in-matplotlib-using-a-scatter-data-set/59920744#59920744
    """

    def data_coord2view_coord(p, resolution, pmin, pmax):
        dp = pmax - pmin
        dv = (p - pmin) / dp * resolution
        return dv

    resolution = 10

    extent = [np.min(xs), np.max(xs), np.float64(0), np.float64(1)]
    xv = data_coord2view_coord(xs, resolution, extent[0], extent[1])
    yv = data_coord2view_coord(ys, resolution, extent[2], extent[3])

    def kNN2DDens(xv, yv, resolution, neighbours, dim=2):
        """
        """
        # Create the tree
        tree = cKDTree(np.array([xv, yv]).T)
        # Find the closest nnmax-1 neighbors (first entry is the point itself)
        grid = np.mgrid[0:resolution, 0:resolution].T.reshape(resolution ** 2, dim)
        dists = tree.query(grid, neighbours)
        # Inverse of the sum of distances to each grid point.
        inv_sum_dists = 1. / dists[0].sum(1)

        # Reshape
        im = inv_sum_dists.reshape(resolution, resolution)
        return im

    fig, ax = plt.subplots()

    im = kNN2DDens(xv, yv, resolution, neighbours)

    ax.imshow(im, origin='lower', extent=extent, cmap=cm.terrain)
    ax.set_xlim(extent[0], extent[1])
    ax.set_ylim(extent[2], extent[3])
    ax.set_xscale('log')
    ax.set_aspect('auto')

    return fig, ax

