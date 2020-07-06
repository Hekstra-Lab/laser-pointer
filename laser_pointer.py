
import matplotlib.pyplot as plt
from skimage import data
from ipywidgets import Output
import matplotlib.patches as patches
from scipy.spatial.distance import cdist
import numpy as np
from matplotlib.widgets import Button
from datetime import datetime

class click_handler:
    Xs = []
    Ys = []
    _circles = []
    radius = 10
    def __init__(self, fig, ax, alpha = .5):
        self.fig = fig
        self.ax = ax
        self.callback_id = fig.canvas.mpl_connect('button_press_event', self.callback)
        self.alpha = alpha
        
    def callback(self, event):
        if event.button== 1:
            if event.xdata is not None and event.ydata is not None:
                self.Xs.append(event.xdata)
                self.Ys.append(event.ydata)
                self._circles.append(patches.Circle((event.xdata, event.ydata), radius = self.radius,alpha=self.alpha))
                self.ax.add_artist(self._circles[-1])
                self.fig.canvas.draw_idle()
        elif event.button == 3:
            # right click - remove closest point
            if len(self.Xs)>0:
                points = np.vstack([self.Xs, self.Ys]).T
                dists = cdist(points,[[event.xdata, event.ydata]])
                idx = np.argmin(dists)
                self.Xs.pop(idx)
                self.Ys.pop(idx)
                self._circles.pop(idx).remove()
                self.fig.canvas.draw_idle()
    def save(self, filename=None):
        if filename is None:
            now = datetime.now().isoformat('-','seconds').replace(':','-')
            filename = f'laser-positions-{now}.csv'
        np.savetxt(filename, np.column_stack([self.Xs,self.Ys]), fmt='%s\t%s',header='x\ty')
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)
im = ax.imshow(data.astronaut())
ch = click_handler(fig, ax)
def handle_close(evt):
    ch.save()
    print('Closed Figure!')

fig.canvas.mpl_connect('close_event', handle_close)
plt.show()