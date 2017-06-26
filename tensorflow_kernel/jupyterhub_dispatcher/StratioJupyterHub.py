#!/usr/bin/env python3
from jupyterhub import app
import sys
import warnings
from handlers.TensorflowHandler import TensorflowHandler


class StratioJupyterHub(app.JupyterHub):

    name = 'StratioJupyterHub'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def init_handlers(self):
        super().init_handlers()
        self.add_handlers([
             ('/hub/tensorflow', TensorflowHandler)
        ])

    def add_handlers(self, handlers, replace_existing=True):
        """Add new handlers.

        Parameters
        ----------
        handlers : list-like
            Contains tuples representing handlers: (url, handler[, init_args]).
        replace_existing : bool, optional(True)
            If True, old handlers will be overwritten by new ones on overlapping urls.
        """

        self.log.info("add new Handler")
        existing_handler_indices = {handler[0]: i for i, handler in enumerate(self.handlers)}
        for handler in handlers:
            existing_handler_index = existing_handler_indices.get(handler[0])
            if existing_handler_index is None:
                # must be inserted before the pattern '(.*)', which is the last one
                self.handlers.insert(-1, handler)
            elif replace_existing:
                self.handlers[existing_handler_index] = handler
            else:
                warnings.warn('Custom handler for url {} was not added'.format(handler[0]),
                              RuntimeWarning)


main = StratioJupyterHub.launch_instance

if __name__ == "__main__":
    main(sys.argv)
