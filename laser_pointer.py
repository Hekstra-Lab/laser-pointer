
import matplotlib.pyplot as plt
from datetime import datetime
from zooming import zoom_factory
from panning import panhandler
from clicking import click_handler
from IPython import embed

class laser_pointer:
    def __init__(self, image_path, radius=5, color='red', alpha=.5):
        """
        image_path : str
            Path to the image to use
        """
        self.fig, self.ax = plt.subplots()
        im = plt.imread(image_path)
        self.im = self.ax.imshow(im)
        zoom_factory(self.ax)
        self.click_handler = click_handler(self.fig, self.ax, radius=radius, color=color, alpha=alpha)
        self.ph = panhandler(self.fig) # gotta assign to avoid garbage collection
        self.fig.canvas.mpl_connect('close_event', self._handle_close)
        plt.show()
        
    def _handle_close(self, event):
        self.click_handler.save()
    def save(self, filename):
        self.click_handler.save(filename)

if __name__ == '__main__':
#     lp = laser_pointer('example-image.jpg')
    embed(colors='neutral')