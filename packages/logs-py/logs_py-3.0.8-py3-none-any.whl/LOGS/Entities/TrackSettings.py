from typing import Optional

from LOGS.Entities.AxisNaming import AxisNaming
from LOGS.Entity.SerializableContent import SerializableContent


class TrackSettings(SerializableContent):
    """LOGS general Track settings"""

    _color: Optional[str] = None
    _axisUnits: Optional[AxisNaming] = None
    _axisLabels: Optional[AxisNaming] = None

    @property
    def color(self) -> Optional[str]:
        return self._color

    @color.setter
    def color(self, value):
        self._color = self.checkAndConvertNullable(value, str, "color")

    @property
    def axisUnits(self) -> Optional[AxisNaming]:
        return self._axisUnits

    @axisUnits.setter
    def axisUnits(self, value):
        self._axisUnits = self.checkAndConvertNullable(value, AxisNaming, "axisUnits")

    @property
    def axisLabels(self) -> Optional[AxisNaming]:
        return self._axisLabels

    @axisLabels.setter
    def axisLabels(self, value):
        self._axisLabels = self.checkAndConvertNullable(value, AxisNaming, "axisLabels")
