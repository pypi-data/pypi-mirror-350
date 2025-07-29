from enum import Enum
from typing import Any, Optional

from mantarix.core.constrained_control import ConstrainedControl
from mantarix.core.control import OptionalNumber

class LightSensor(ConstrainedControl):
    def __init__(
        self,
        opacity: OptionalNumber = None,
        tooltip: Optional[str] = None,
        visible: Optional[bool] = None,
        data: Any = None,
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        expand: Optional[bool] = None,
    ):
        ConstrainedControl.__init__(
            self,
            tooltip=tooltip,
            opacity=opacity,
            visible=visible,
            data=data,
            left=left,
            top=top,
            right=right,
            bottom=bottom,
            expand=expand,
            width=width,
            height=height
        )

    def _get_control_name(self):
        return "light_sensor"
    
    def value(self, comment: str = "", wait_timeout: Optional[float] = 25):
        out = self.invoke_method(
            "get_sensor_value",
            {"comment": comment},
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return str(out)
    
    def on(self, comment: str = "", wait_timeout: Optional[float] = 25):
        out = self.invoke_method(
            "on",
            {"comment": comment},
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return str(out)
    
    def off(self, comment: str = "", wait_timeout: Optional[float] = 25):
        out = self.invoke_method(
            "off",
            {"comment": comment},
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return str(out)