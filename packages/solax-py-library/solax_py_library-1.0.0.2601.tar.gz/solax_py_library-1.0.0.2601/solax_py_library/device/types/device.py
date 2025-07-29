from enum import IntEnum


class DeviceType(IntEnum):
    EMS_TYPE = 100
    PCS_TYPE = 1
    BMS_TYPE = 2  # 电池簇
    ELM_TYPE = 3
    EVC_TYPE = 4
    IO_TYPE = 5
    ESS_TYPE = 6  # 机柜
    CELL_TYPE = 7  # 单体
    AIRCONDITIONER_TYPE = 501
    FIRE_SAFETY_TYPE = 502
    COLD_TYPE = 503
    DEHUMIDIFY_TYPE = 504
