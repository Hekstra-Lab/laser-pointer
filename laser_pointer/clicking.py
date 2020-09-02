import numpy as np
from datetime import datetime
import matplotlib.patches as patches
from scipy.spatial.distance import cdist

class click_handler:
    def __init__(self, fig, ax, radius=5, color='red', alpha = .5):
        self.fig = fig
        self.ax = ax
        self.x_max = self.ax.get_xlim()[1]
        self.y_max = self.ax.get_ylim()[0]
        print(self.y_max)
        self.callback_id = fig.canvas.mpl_connect('button_press_event', self.callback)
        self.alpha = alpha
        self.radius = radius
        self.color = color
        self.Xs = []
        self.Ys = []
        self._circles = []
        
    def callback(self, event):
        if event.button== 1:
            if event.xdata is not None and event.ydata is not None:
                if  (0 < event.xdata < self.x_max) and  (0 < event.ydata < self.y_max):
                    self.Xs.append(event.xdata)
                    self.Ys.append(event.ydata)
                    self._circles.append(patches.Circle((event.xdata, event.ydata), radius = self.radius,alpha=self.alpha, color = self.color))
                    self.ax.add_artist(self._circles[-1])
                    self.fig.canvas.draw_idle()
        # elif event.button == 3:
        #     # right click - remove closest point
        #     if len(self.Xs)>0:
        #         points = np.vstack([self.Xs, self.Ys]).T
        #         dists = cdist(points,[[event.xdata, event.ydata]])
        #         idx = np.argmin(dists)
        #         self.Xs.pop(idx)
        #         self.Ys.pop(idx)
        #         self._circles.pop(idx).remove()
        #         self.fig.canvas.draw_idle()
    def save(self, filename=None):
        if filename is None:
            now = datetime.now().isoformat('-','seconds').replace(':','-')
            filename = f'laser-positions-{now}.csv'
        print(f'saving as: {filename}')
        np.savetxt(filename, np.column_stack([self.Xs,self.Ys]), fmt='%s\t%s',header='x\ty')
