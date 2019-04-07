import numpy as np
import matplotlib.pyplot as plt

# toolkit of useful functions
# -----------------------------------------------------------------------------------------------------------------


def find_nearest(array, value):
    idx = (np.abs(array - value)).argmin()
    return idx, array[idx]


def cart2pol(x, y):
    rho = np.sqrt(x ** 2 + y ** 2)
    phi = np.arctan2(y, x)
    return rho, phi


def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return x, y


# nan-seg interp (interpret nan's found in an array...does not deal with a nan segment that ends an array)
def nanseg_interp(xx, y):
    n = len(y)
    iv = np.where(np.isnan(y))[0]  # index of NaN values in y
    diffiv = np.diff(iv)
    nb = np.size(np.where(diffiv > 1)[0]) + 1  # number of blocks of NaNs to be interpolated
    yi = y.copy()

    if len(iv) < 1:
        b = 23
    else:
        if iv[0] == 0:
            ing = np.where(np.isfinite(y))[0][0]
            yi[0:ing] = y[ing]
            nb = nb - 1

        for jj in range(nb):
            ilg = np.where(np.isnan(yi))[0][0] - 1  # index of last y value before first NaN
            if np.sum(np.isfinite(yi[(ilg + 1):n])) > 0:
                ing = np.where(np.isfinite(yi[(ilg + 1):n]))[0][0] + ilg + 1
                yi[(ilg + 1):ing] = np.interp(xx[(ilg + 1):ing], [xx[ilg], xx[ing]], [y[ilg], y[ing]])
    return yi


def group_consecutives(vals, step=1):
    """Return list of consecutive lists of numbers from vals (number list)."""
    run = []
    result = [run]
    expect = None
    for v in vals:
        if (v == expect) or (expect is None):
            run.append(v)
        else:
            run = [v]
            result.append(run)
        expect = v + step
    return result


def plot_pro(ax):
    ax.grid()
    plt.show(block=False)
    plt.pause(0.1)
    return ()
# -----------------------------------------------------------------------------------------------------------------