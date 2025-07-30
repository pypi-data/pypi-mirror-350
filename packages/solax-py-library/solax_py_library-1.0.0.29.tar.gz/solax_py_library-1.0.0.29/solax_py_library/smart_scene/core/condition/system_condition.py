from solax_py_library.smart_scene.core.condition.base import BaseCondition
from solax_py_library.smart_scene.types.condition import (
    SystemConditionItemData,
    SystemConditionType,
    ConditionType,
)


class SystemCondition(BaseCondition):
    condition_type = ConditionType.systemCondition

    def __init__(self, update_value_function, **kwargs):
        super().__init__(update_value_function, **kwargs)

    def meet_func(self, data: SystemConditionItemData, ctx):
        if not self.value:
            return False
        child_data = data.childData
        function_value = child_data.function
        compare_value = None
        if data.childType == SystemConditionType.systemExportPower:
            compare_value = self.value.get("grid_active_power")
            if compare_value < 0:
                return False
        elif data.childType == SystemConditionType.systemImportPower:
            compare_value = self.value.get("grid_active_power")
            if compare_value > 0:
                return False
        elif data.childType == SystemConditionType.systemSoc:
            compare_value = self.value.get("system_soc")
        if compare_value is None:
            return False
        return function_value.function()(
            compare_value=abs(compare_value), base_value=child_data.data[0]
        )
