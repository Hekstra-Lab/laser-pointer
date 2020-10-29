from scipy.stats import linregress
import numpy as np
import matplotlib.pyplot as plt


def fit_transform_pointers(lp_bf, lp_rm, plot=True):
    """
    convenience method that allows passing pointers to
    fit_transform

    Usage
    -----
    transform_pointer, bfx_to_rmx, bfy_to_rmy, inverse_x, inverse_y = fit_transform
    """
    bf_x = np.asarray(lp_bf.click_handler.Xs)
    bf_y = np.asarray(lp_bf.click_handler.Ys)
    rm_x = np.asarray(lp_rm.click_handler.Xs)
    rm_y = np.asarray(lp_rm.click_handler.Ys)
    bf_coords = np.hstack([bf_x[:, None], bf_y[:, None]])
    rm_coords = np.hstack([rm_x[:, None], rm_y[:, None]])
    return fit_transform(bf_coords, rm_coords, plot=plot)


def fit_transform(bf_coords, rm_coords, plot=True):
    """

    transform_pointer, bfx_to_rmx, bfy_to_rmy, inverse_x, inverse_y = fit_transform
    """
    bf_x = bf_coords[:, 0]
    bf_y = bf_coords[:, 1]
    rm_x = rm_coords[:, 0]
    rm_y = rm_coords[:, 1]
    slope_x, intercept_x, r_value, p_value, std_err = linregress(bf_x, rm_x)
    slope_y, intercept_y, r_value, p_value, std_err = linregress(bf_y, rm_y)

    def bfx_to_rmx(x):
        x = np.asarray(x)
        return slope_x * x + intercept_x

    def bfy_to_rmy(y):
        y = np.asarray(y)
        return slope_y * y + intercept_y

    def inverse_x(x):
        x = np.asanyarray(x)
        return (x - intercept_x) / slope_x

    def inverse_y(y):
        y = np.asanyarray(y)
        return (y - intercept_y) / slope_y

    def transform_pointer(pointer, stack=True):
        """
        Parameters
        ----------
        pointer : laser_pointer.pointer
        stack : bool
            If True retun as a single array with shape (2, N). Otherwise return x, y
        """
        xs = bfx_to_rmx(pointer.click_handler.Xs)
        ys = bfx_to_rmx(pointer.click_handler.Ys)
        if stack:
            return np.vstack([xs[None, :], ys[None, :]])
        else:
            return xs, ys

    if plot:
        plt.figure()
        plt.plot(bf_x, rm_x, "o", label="x")
        plt.plot(bf_y, rm_y, "o", label="y")

        x_ = np.linspace(np.min(bf_x), np.max(bf_x))
        y_ = np.linspace(np.min(bf_y), np.max(bf_y))

        plt.plot(x_, slope_x * x_ + intercept_x, label="x fit")
        plt.plot(y_, slope_y * y_ + intercept_y, label="y fit")
        plt.xlabel("Bright Field coord")
        plt.ylabel("Galvo voltage")
        plt.legend()
        plt.show()
    return transform_pointer, bfx_to_rmx, bfy_to_rmy, inverse_x, inverse_y