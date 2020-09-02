import matplotlib.pyplot as plt
class panhandler:
    """
    enable right click to pan image
    this doesn't set up the eventlisteners, whatever calls this needs to do
    fig.mpl_connect('button_press_event', panhandler.press)
    fig.mpl_connect('button_release_event', panhandler.release)
    
    or somehitng 
    """
    def __init__(self, fig, button=2):
        self.fig = fig
        self._id_drag = None
        self.button = button
        cid = self.fig.canvas.mpl_connect('button_press_event', self.press)
        self.fig.canvas.mpl_connect('button_release_event', self.release)

    def _cancel_action(self):
        self._xypress = []
        if self._id_drag:
            self.fig.canvas.mpl_disconnect(self._id_drag)
            self._id_drag = None
        
    def press(self, event):
        print(event.button)
        print(event.button==2)
        if event.button != self.button:
            self._cancel_action()
            return

        x, y = event.x, event.y

        self._xypress = []
        for i, a in enumerate(self.fig.get_axes()):
            if (x is not None and y is not None and a.in_axes(event) and
                    a.get_navigate() and a.can_pan()):
                a.start_pan(x, y, event.button)
                self._xypress.append((a, i))
                self._id_drag = self.fig.canvas.mpl_connect(
                    'motion_notify_event', self._mouse_move)
    def release(self, event):
        self._cancel_action()
        self.fig.canvas.mpl_disconnect(self._id_drag)


        for a, _ind in self._xypress:
            a.end_pan()
        if not self._xypress:
            self._cancel_action()
            return
        self._cancel_action()

    def _mouse_move(self, event):
        for a, _ind in self._xypress:
            # safer to use the recorded button at the _press than current
            # button: # multiple button can get pressed during motion...
            a.drag_pan(1, event.key, event.x, event.y)
        self.fig.canvas.draw_idle()