import anywidget


class ViaWidget(anywidget.AnyWidget):
    """
    Base class wrapper for creating custom `anywidget`-based widgets.
    """

    def __init__(self, **kwargs):
        """
        Initialize the widget with things that might be shared across different widgets.

        Args:
            # Nothing added yet
            # Possible addition in future: help string
            **kwargs: Additional keyword arguments passed to the AnyWidget base class.
        """
        super().__init__(**kwargs)
