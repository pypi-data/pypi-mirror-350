from PySide6.QtCore import Qt, Signal,QRect
from PySide6.QtGui import QColor, QPainter, QBrush, QPen
from PySide6.QtWidgets import QWidget
import pyvisual as pv
from pyvisual.utils.helper_functions import add_shadow_effect, update_svg_color, draw_border



class PvSlider(QWidget):
    value_changed = Signal(int)

    def __init__(self, parent=None, x=100, y=100, width=200, height=30,
                 min_value=0, max_value=100, value=50,
                 track_color=(200, 200, 200, 255), track_border_color=(180, 180, 180, 255),
                 fill_color=(56, 182, 255, 255),
                 knob_color=(255, 255, 255, 255), knob_border_color=(245, 245, 245, 255),
                 hover_knob_color=None, disabled_knob_color=(150, 150, 150, 255),
                 track_corner_radius=0, knob_corner_radius=0,
                 knob_width=50, knob_height=30, is_disabled=False, opacity=1,
                 track_border_thickness=2, knob_border_thickness=2, on_change=None,
                 **kwargs):
        super().__init__(parent)
        self._width = width
        self._height = height
        self._min_value = min_value
        self._max_value = max_value
        self._value = value
        self._track_color = track_color
        self._track_border_color = track_border_color
        self._fill_color = fill_color
        self._knob_color = knob_color
        self._knob_border_color = knob_border_color
        self._hover_knob_color = hover_knob_color or knob_color
        self._disabled_knob_color = disabled_knob_color
        self._track_corner_radius = track_corner_radius
        self._knob_corner_radius = knob_corner_radius
        self._knob_width = knob_width
        self._knob_height = knob_height
        self._is_disabled = is_disabled
        self._opacity = opacity
        self._is_hovered = False
        self._track_border_thickness = track_border_thickness
        self._knob_border_thickness = knob_border_thickness
        self._on_change = on_change
        self.setGeometry(x, y, self._width, self._height)
        self.setMouseTracking(True)
        self._knob_padding = 3

        # Connect the `on_change` function to the `value_changed` signal if provided
        if callable(self._on_change):
            self.value_changed.connect(self._on_change)

        add_shadow_effect(self, "0 2 4 5 rgba(0,0,0,0.2)")

    def paintEvent(self, event):
        """Custom painting for the slider."""
        painter = QPainter(self)
        painter.setOpacity(self._opacity)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw track border
        track_rect = self.rect().adjusted(
            self._track_border_thickness // 2,
            (self._height - 10) // 2,
            -self._track_border_thickness // 2,
            -(self._height - 10) // 2
        )
        painter.setPen(QPen(QColor(*self._track_border_color), self._track_border_thickness))
        painter.setBrush(QBrush(QColor(*self._track_color)))
        painter.drawRoundedRect(track_rect, self._track_corner_radius, self._track_corner_radius)

        # Draw fill
        fill_width = self._knob_padding + int(
            (self._value - self._min_value) / (self._max_value - self._min_value) * (
                        self._width - self._knob_width - 2 * self._knob_padding))

        fill_rect = track_rect.adjusted(0, 0, fill_width, 0)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(*self._fill_color)))
        painter.drawRoundedRect(fill_rect, self._track_corner_radius, self._track_corner_radius)

        # Draw knob
        knob_x = fill_width
        knob_rect = QRect(
            knob_x,
            track_rect.center().y() - self._knob_height // 2,
            self._knob_width,
            self._knob_height
        )
        knob_color = self._knob_color if not self._is_disabled else self._disabled_knob_color
        if self._is_hovered and not self._is_disabled:
            knob_color = self._hover_knob_color

        # Draw knob border
        painter.setPen(QPen(QColor(*self._knob_border_color), self._knob_border_thickness))
        painter.setBrush(QBrush(QColor(*knob_color)))
        painter.drawRoundedRect(knob_rect, self._knob_corner_radius, self._knob_corner_radius)

    def update_value(self, x):
        """Update the slider value based on mouse position."""
        # Calculate the effective track width considering knob width
          # Increase this value for more padding
        effective_width = self._width - self._knob_width - (2 * self._knob_padding)

        # Clamp the x position so the knob stays within the effective track
        clamped_x = max(self._knob_padding, min(x - self._knob_width // 2, self._width - self._knob_width - self._knob_padding))

        # Map the clamped x position to the slider value
        new_value = self._min_value + (clamped_x / effective_width) * (self._max_value - self._min_value)

        # Update the slider value
        self._value = int(max(self._min_value, min(self._max_value, new_value)))
        self.value_changed.emit(self._value)
        self.update()

    def set_value(self, value):
        """Set the value of the slider."""
        self._value = max(self._min_value, min(self._max_value, value))
        self.update()

    def get_value(self):
        """Get the current value of the slider."""
        return self._value

    def mousePressEvent(self, event):
        """Handle mouse press events."""
        if event.button() == Qt.LeftButton and not self._is_disabled:
            self.update_value(event.x())

    def mouseMoveEvent(self, event):
        """Handle mouse move events."""
        if event.buttons() == Qt.LeftButton and not self._is_disabled:
            self.update_value(event.x())

    def enterEvent(self, event):
        """Handle mouse enter events."""
        super().enterEvent(event)
        self._is_hovered = True
        self.update()

    def leaveEvent(self, event):
        """Handle mouse leave events."""
        super().leaveEvent(event)
        self._is_hovered = False
        self.update()

    # def update_value(self, x):
    #     """Update the slider value based on mouse position."""
    #     # Calculate the effective track width considering knob size
    #     effective_width = self._width - self._knob_size
    #
    #     # Clamp the x position so the knob stays within the effective track
    #     clamped_x = max(0, min(x - self._knob_size // 2, effective_width))
    #
    #     # Map the clamped x position to the slider value
    #     new_value = self._min_value + (clamped_x / effective_width) * (self._max_value - self._min_value)
    #
    #     # Update the slider value
    #     self._value = int(max(self._min_value, min(self._max_value, new_value)))
    #     self.value_changed.emit(self._value)
    #     self.update()
    #
    # def set_value(self, value):
    #     """Set the value of the slider."""
    #     self._value = max(self._min_value, min(self._max_value, value))
    #     self.update()
    #
    # def get_value(self):
    #     """Get the current value of the slider."""
    #     return self._value


# Example Usage with PyVisual
if __name__ == "__main__":
    # Create PyVisual app
    app = pv.PvApp()

    # Create PyVisual window
    window = pv.PvWindow(title="PvSlider Example", is_resizable=True)

    # Add PvSlider to the window
    slider = PvSlider(
        window, x=50, y=50, width=300, height=40,
        track_color=(220, 220, 220, 1),
        track_border_color=(180, 180, 180, 255),
        fill_color=(70, 130, 180, 255),
        knob_color=(255, 255, 255, 255),
        knob_border_color=(100, 100, 100, 255)
    )


    # Show the window
    window.show()

    # Run the PyVisual app
    app.run()
