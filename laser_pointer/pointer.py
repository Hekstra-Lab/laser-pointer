
import matplotlib.pyplot as plt
from datetime import datetime
from .clicking import click_handler
from mpl_interactions import zoom_factory, panhandler
from IPython import embed


class pointer:
    def __init__(self, image, radius=5, color='red', alpha=.5):
        """
        image_path : str | array
            Path to the image to use
        """
        self.fig, self.ax = plt.subplots()
        if isinstance(image, str):
            image = plt.imread(image)
        self.im = self.ax.imshow(image)
        zoom_factory(self.ax)
        if hasattr(self.fig.canvas, 'capture_scroll'):
            self.fig.canvas.capture_scroll = True
        self.click_handler = click_handler(self.fig, self.ax, radius=radius, color=color, alpha=alpha)
        self.ph = panhandler(self.fig,button=3) # gotta assign to avoid garbage collection
        self.fig.canvas.mpl_connect('close_event', self._handle_close)
        plt.show()
        
    def _handle_close(self, event):
        self.click_handler.save()
    def save(self, filename):
        self.click_handler.save(filename)

if __name__ == '__main__':
#     lp = laser_pointer('example-image.jpg')
    embed(colors='neutral')