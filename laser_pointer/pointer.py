import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.patches as patches
from .clicking import click_handler
from mpl_interactions import zoom_factory, panhandler
import numpy as np


def make_overlay(bf_shape, inverse_x, inverse_y):
    """
    make an overlay to show which regions are accesible to the laser
    """
    x_ = np.arange(bf_shape[0])
    y_ = np.arange(bf_shape[1])
    Xs, Ys = np.meshgrid(x_, y_)
    overlay = np.zeros((*bf_shape, 4), dtype=np.float)
    overlay[:, :, -1] = 0.75
    xlims = inverse_x([-0.3, 0.3])
    ylims = inverse_y([-0.3, 0.3])
    idx_x = (Xs < xlims.max()) & (Xs > xlims.min())
    idx_y = (Ys < ylims.max()) & (Ys > ylims.min())
    idx = idx_x & idx_y
    overlay[idx] = 0.0
    return overlay


class pointer:
    def __init__(
        self, image, ax=None, X=None, Y=None, radius=5, color="red", alpha=0.5
    ):
        """
        image_path : str | array
            Path to the image to use
        """
        if ax is None:
            self.fig, self.ax = plt.subplots()
        else:
            self.ax = ax
            self.fig = ax.get_figure()
        if isinstance(image, str):
            image = plt.imread(image)
        self._image = image
        self._X = X
        self._Y = Y
        if X is None or Y is None:
            self.im = self.ax.imshow(self._image)
        else:
            self.im = self.ax.pcolormesh(X, Y, image, shading="nearest")

        zoom_factory(self.ax)
        if hasattr(self.fig.canvas, "capture_scroll"):
            self.fig.canvas.capture_scroll = True

        self.callback_id = self.fig.canvas.mpl_connect(
            "button_press_event", self._callback
        )
        self.alpha = alpha
        self.radius = radius
        self.color = color
        self.Xs = []
        self.Ys = []
        self._circles = []

        self.ph = panhandler(
            self.fig, button=3
        )  # gotta assign to avoid garbage collection
        self.fig.canvas.mpl_connect("close_event", self._handle_close)
        plt.show()

    def _add_point(self, x, y):
        self.Xs.append(x)
        self.Ys.append(y)
        self._circles.append(
            patches.Circle(
                (x, y), radius=self.radius, alpha=self.alpha, color=self.color
            )
        )
        self.ax.add_artist(self._circles[-1])

    def add_points(self, Xs, Ys):
        for x, y in zip(Xs, Ys):
            self._add_point(x, y)
        self.fig.canvas.draw_idle()

    def _callback(self, event):
        if event.button == 1:
            if (
                event.xdata is not None
                and event.ydata is not None
                and event.inaxes is self.ax
            ):
                # if  (self.xlims[0] < event.xdata < self.x_lims) and  (0 < event.ydata < self.y_max):
                self._add_point(event.xdata, event.ydata)
                self.fig.canvas.draw_idle()

    def _handle_close(self, event):
        self.save()

    def save(self, filename=None):
        if filename is None:
            now = datetime.now().isoformat("-", "seconds").replace(":", "-")
            filename = f"laser-positions-{now}"
        print(f"saving as: {filename}")
        np.savez_compressed(
            filename,
            image=self._image,
            X=self._X,
            Y=self._Y,
            Xs=np.array(self.Xs),
            Ys=np.array(self.Ys),
        )


def load_pointer(filename, ax=None, **kwargs):
    """
    Parameters
    ----------
    filename : str
    ax : matplotlib Axis
        Optional axis for the pointer to use
    **kwargs :
        Passed through to the pointer init function

    Returns
    -------
    laser_pointer.pointer
        Loaded with the contents of the file
    """
    arr = np.load(filename, allow_pickle=True)
    X = arr["X"]
    Y = arr["Y"]
    if X == np.array(None):
        X = None
    if Y == np.array(None):
        Y = None
    p = pointer(arr["image"], X=X, Y=Y, ax=ax, **kwargs)
    p.add_points(arr["Xs"], arr["Ys"])
    return p
