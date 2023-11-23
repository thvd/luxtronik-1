"""Luxtronik sensors definitions."""
# region Imports
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import (
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfFrequency,
    UnitOfPower,
    UnitOfPressure,
    UnitOfTemperature,
    UnitOfTime,
)
from homeassistant.helpers.entity import EntityCategory

from .const import (
    LUX_STATE_ICON_MAP,
    SECOUND_TO_HOUR_FACTOR,
    UPDATE_INTERVAL_NORMAL,
    UPDATE_INTERVAL_SLOW,
    UPDATE_INTERVAL_VERY_SLOW,
    DeviceKey,
    FirmwareVersionMinor,
    LuxCalculation as LC,
    LuxOperationMode,
    LuxParameter as LP,
    LuxStatus1Option,
    LuxStatus3Option,
    LuxSwitchoffReason,
    LuxVisibility as LV,
    SensorAttrFormat,
    SensorAttrKey as SA,
    SensorKey,
    UnitOfVolumeFlowRateExt,
)
from .model import (
    LuxtronikEntityAttributeDescription as attr,
    LuxtronikSensorDescription as descr,
    LuxtronikIndexSensorDescription as descr_index,
)

# endregion Imports

SENSORS_STATUS: list[descr] = [
    descr(
        key=SensorKey.STATUS,
        luxtronik_key=LC.C0080_STATUS,
        icon_by_state=LUX_STATE_ICON_MAP,
        device_class=SensorDeviceClass.ENUM,
        extra_attributes=[
            attr(SA.EVU_FIRST_START_TIME, LC.UNSET, None, True),
            attr(SA.EVU_FIRST_END_TIME, LC.UNSET, None, True),
            attr(SA.EVU_SECOND_START_TIME, LC.UNSET, None, True),
            attr(SA.EVU_SECOND_END_TIME, LC.UNSET, None, True),
        ],
        options=[e.value for e in LuxOperationMode],
        update_interval=UPDATE_INTERVAL_NORMAL,
    ),
]

SENSORS_INDEX: list[descr] = [
    descr_index(
        key=SensorKey.SWITCHOFF_REASON,
        luxtronik_key=LP.P0716_0720_SWITCHOFF_REASON,
        luxtronik_key_timestamp=LP.P0721_0725_SWITCHOFF_TIMESTAMP,
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:electric-switch",
        device_class=SensorDeviceClass.ENUM,
        options=[e.value for e in LuxSwitchoffReason],
    ),
]

SENSORS: list[descr] = [
    # region Main heatpump
    descr(
        key=SensorKey.STATUS_TIME,
        luxtronik_key=LC.C0120_STATUS_TIME,
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:timer-sand",
        native_unit_of_measurement=UnitOfTime.SECONDS,
        entity_registry_visible_default=False,
        native_precision=0,
        extra_attributes=[
            attr(SA.STATUS_TEXT, LC.C0120_STATUS_TIME, SensorAttrFormat.HOUR_MINUTE),
            attr(SA.TIMER_HEATPUMP_ON, LC.C0067_TIMER_HEATPUMP_ON),
            attr(SA.TIMER_ADD_HEAT_GENERATOR_ON, LC.C0068_TIMER_ADD_HEAT_GENERATOR_ON),
            attr(SA.TIMER_SEC_HEAT_GENERATOR_ON, LC.C0069_TIMER_SEC_HEAT_GENERATOR_ON),
            attr(SA.TIMER_NET_INPUT_DELAY, LC.C0070_TIMER_NET_INPUT_DELAY),
            attr(SA.TIMER_SCB_OFF, LC.C0071_TIMER_SCB_OFF),
            attr(SA.TIMER_SCB_ON, LC.C0072_TIMER_SCB_ON),
            attr(SA.TIMER_COMPRESSOR_OFF, LC.C0073_TIMER_COMPRESSOR_OFF),
            attr(SA.TIMER_HC_ADD, LC.C0074_TIMER_HC_ADD),
            attr(SA.TIMER_HC_LESS, LC.C0075_TIMER_HC_LESS),
            attr(SA.TIMER_TDI, LC.C0076_TIMER_TDI),
            attr(SA.TIMER_BLOCK_DHW, LC.C0077_TIMER_BLOCK_DHW),
            attr(SA.TIMER_DEFROST, LC.C0141_TIMER_DEFROST),
            attr(SA.TIMER_HOT_GAS, LC.C0158_TIMER_HOT_GAS),
        ],
    ),
    descr(
        key=SensorKey.STATUS_LINE_1,
        luxtronik_key=LC.C0117_STATUS_LINE_1,
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:numeric-1-circle",
        entity_registry_visible_default=False,
        device_class=SensorDeviceClass.ENUM,
        options=[e.value for e in LuxStatus1Option]
        # translation_key="status1",
    ),
    descr(
        key=SensorKey.STATUS_LINE_2,
        luxtronik_key=LC.C0118_STATUS_LINE_2,
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:numeric-2-circle",
        entity_registry_visible_default=False,
        device_class=SensorDeviceClass.ENUM,
        options=["since", "in"],
        # translation_key="status2",
    ),
    descr(
        key=SensorKey.STATUS_LINE_3,
        luxtronik_key=LC.C0119_STATUS_LINE_3,
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:numeric-3-circle",
        entity_registry_visible_default=False,
        device_class=SensorDeviceClass.ENUM,
        options=[e.value for e in LuxStatus3Option],
        # translation_key="status3",
    ),
    descr(
        key=SensorKey.HEAT_SOURCE_INPUT_TEMPERATURE,
        luxtronik_key=LC.C0204_HEAT_SOURCE_INPUT_TEMPERATURE,
        icon="mdi:thermometer",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        entity_registry_enabled_default=False,
        update_interval=UPDATE_INTERVAL_NORMAL,
    ),
    descr(
        key=SensorKey.OUTDOOR_TEMPERATURE,
        luxtronik_key=LC.C0015_OUTDOOR_TEMPERATURE,
        icon="mdi:thermometer",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        update_interval=UPDATE_INTERVAL_SLOW,
    ),
    descr(
        key=SensorKey.OUTDOOR_TEMPERATURE_AVERAGE,
        luxtronik_key=LC.C0016_OUTDOOR_TEMPERATURE_AVERAGE,
        icon="mdi:thermometer",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        entity_registry_enabled_default=False,
        update_interval=UPDATE_INTERVAL_VERY_SLOW,
    ),
    descr(
        key=SensorKey.COMPRESSOR1_IMPULSES,
        luxtronik_key=LC.C0057_COMPRESSOR1_IMPULSES,
        icon="mdi:pulse",
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
        native_unit_of_measurement="\u2211",
        entity_registry_enabled_default=False,
        visibility=LV.V0081_COMPRESSOR1_IMPULSES,
    ),
    descr(
        key=SensorKey.COMPRESSOR1_OPERATION_HOURS,
        luxtronik_key=LC.C0056_COMPRESSOR1_OPERATION_HOURS,
        icon="mdi:timer-sand",
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
        native_unit_of_measurement=UnitOfTime.HOURS,
        visibility=LV.V0080_COMPRESSOR1_OPERATION_HOURS,
        factor=SECOUND_TO_HOUR_FACTOR,
        native_precision=2,
        update_interval=UPDATE_INTERVAL_VERY_SLOW,
    ),
    descr(
        key=SensorKey.COMPRESSOR2_IMPULSES,
        luxtronik_key=LC.C0059_COMPRESSOR2_IMPULSES,
        icon="mdi:pulse",
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
        native_unit_of_measurement="\u2211",
        entity_registry_enabled_default=False,
        visibility=LV.V0084_COMPRESSOR2_IMPULSES,
    ),
    descr(
        key=SensorKey.COMPRESSOR2_OPERATION_HOURS,
        luxtronik_key=LC.C0058_COMPRESSOR2_OPERATION_HOURS,
        icon="mdi:timer-sand",
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
        native_unit_of_measurement=UnitOfTime.HOURS,
        visibility=LV.V0083_COMPRESSOR2_OPERATION_HOURS,
        factor=SECOUND_TO_HOUR_FACTOR,
        native_precision=2,
        update_interval=UPDATE_INTERVAL_VERY_SLOW,
    ),
    descr(
        key=SensorKey.OPERATION_HOURS,
        luxtronik_key=LC.C0063_OPERATION_HOURS,
        icon="mdi:timer-sand",
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
        native_unit_of_measurement=UnitOfTime.HOURS,
        factor=SECOUND_TO_HOUR_FACTOR,
        native_precision=2,
        update_interval=UPDATE_INTERVAL_VERY_SLOW,
    ),
    descr(
        key=SensorKey.HEAT_AMOUNT_COUNTER,
        luxtronik_key=LC.C0154_HEAT_AMOUNT_COUNTER,
        icon="mdi:lightning-bolt-circle",
        state_class=SensorStateClass.TOTAL_INCREASING,
        device_class=SensorDeviceClass.ENERGY,
        entity_category=EntityCategory.DIAGNOSTIC,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        native_precision=1,
        update_interval=UPDATE_INTERVAL_VERY_SLOW,
    ),
    descr(
        key=SensorKey.HEAT_AMOUNT_FLOW_RATE,
        luxtronik_key=LC.C0155_HEAT_AMOUNT_FLOW_RATE,
        device_key=DeviceKey.heating,
        icon="mdi:water-sync",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=None,  # SensorDeviceClass.WATER, <- There is no predefined device class for flow at the moment.
        entity_category=EntityCategory.DIAGNOSTIC,
        native_unit_of_measurement=UnitOfVolumeFlowRateExt.LITER_PER_HOUR,
        native_precision=1,
        update_interval=UPDATE_INTERVAL_NORMAL,
    ),
    descr(
        key=SensorKey.HEAT_SOURCE_FLOW_RATE,
        luxtronik_key=LC.C0173_HEAT_SOURCE_FLOW_RATE,
        device_key=DeviceKey.heating,
        icon="mdi:water-sync",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=None,  # SensorDeviceClass.WATER, <- There is no predefined device class for flow at the moment.
        entity_category=EntityCategory.DIAGNOSTIC,
        native_unit_of_measurement=UnitOfVolumeFlowRateExt.LITER_PER_HOUR,
        native_precision=1,
        update_interval=UPDATE_INTERVAL_NORMAL,
    ),
    descr(
        key=SensorKey.HOT_GAS_TEMPERATURE,
        luxtronik_key=LC.C0014_HOT_GAS_TEMPERATURE,
        icon="mdi:thermometer",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        visibility=LV.V0027_HOT_GAS_TEMPERATURE,
    ),
    descr(
        key=SensorKey.SUCTION_COMPRESSOR_TEMPERATURE,
        luxtronik_key=LC.C0176_SUCTION_COMPRESSOR_TEMPERATURE,
        icon="mdi:thermometer",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        visibility=LV.V0289_SUCTION_COMPRESSOR_TEMPERATURE,
    ),
    descr(
        key=SensorKey.SUCTION_EVAPORATOR_TEMPERATURE,
        luxtronik_key=LC.C0175_SUCTION_EVAPORATOR_TEMPERATURE,
        icon="mdi:thermometer",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        visibility=LV.V0310_SUCTION_EVAPORATOR_TEMPERATURE,
    ),
    descr(
        key=SensorKey.COMPRESSOR_HEATING_TEMPERATURE,
        luxtronik_key=LC.C0177_COMPRESSOR_HEATING_TEMPERATURE,
        icon="mdi:thermometer",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        visibility=LV.V0290_COMPRESSOR_HEATING,
    ),
    descr(
        key=SensorKey.OVERHEATING_TEMPERATURE,
        luxtronik_key=LC.C0178_OVERHEATING_TEMPERATURE,
        icon="mdi:thermometer",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.KELVIN,
        visibility=LV.V0291_OVERHEATING_TEMPERATURE,
    ),
    descr(
        key=SensorKey.OVERHEATING_TARGET_TEMPERATURE,
        luxtronik_key=LC.C0179_OVERHEATING_TARGET_TEMPERATURE,
        icon="mdi:thermometer",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.KELVIN,
        visibility=LV.V0291_OVERHEATING_TEMPERATURE,
    ),
    descr(
        key=SensorKey.HIGH_PRESSURE,
        luxtronik_key=LC.C0180_HIGH_PRESSURE,
        icon="mdi:gauge-full",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.PRESSURE,
        native_unit_of_measurement=UnitOfPressure.BAR,
        visibility=LV.V0292_LIN_PRESSURE,
    ),
    descr(
        key=SensorKey.LOW_PRESSURE,
        luxtronik_key=LC.C0181_LOW_PRESSURE,
        icon="mdi:gauge-low",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.PRESSURE,
        native_unit_of_measurement=UnitOfPressure.BAR,
        visibility=LV.V0292_LIN_PRESSURE,
    ),
    descr(
        key=SensorKey.ADDITIONAL_HEAT_GENERATOR_OPERATION_HOURS,
        luxtronik_key=LC.C0060_ADDITIONAL_HEAT_GENERATOR_OPERATION_HOURS,
        icon="mdi:timer-sand",
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
        native_unit_of_measurement=UnitOfTime.HOURS,
        visibility=LV.V0086_ADDITIONAL_HEAT_GENERATOR_OPERATION_HOURS,
        factor=SECOUND_TO_HOUR_FACTOR,
        native_precision=2,
        update_interval=UPDATE_INTERVAL_VERY_SLOW,
    ),
    descr(
        key=SensorKey.ADDITIONAL_HEAT_GENERATOR_AMOUNT_COUNTER,
        luxtronik_key=LP.P1059_ADDITIONAL_HEAT_GENERATOR_AMOUNT_COUNTER,
        icon="mdi:lightning-bolt-circle",
        state_class=SensorStateClass.TOTAL_INCREASING,
        device_class=SensorDeviceClass.ENERGY,
        entity_category=EntityCategory.DIAGNOSTIC,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        invisible_if_value=0.0,
        visibility=LV.V0324_ADDITIONAL_HEAT_GENERATOR_AMOUNT_COUNTER,
        factor=0.1,
        native_precision=1,
        update_interval=UPDATE_INTERVAL_VERY_SLOW,
    ),
    descr(
        key=SensorKey.ANALOG_OUT1,
        luxtronik_key=LC.C0156_ANALOG_OUT1,
        icon="mdi:alpha-v-circle-outline",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        visibility=LV.V0248_ANALOG_OUT1,
        entity_registry_enabled_default=False,
        factor=0.1,
    ),
    descr(
        key=SensorKey.ANALOG_OUT2,
        luxtronik_key=LC.C0157_ANALOG_OUT2,
        icon="mdi:alpha-v-circle-outline",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        visibility=LV.V0249_ANALOG_OUT2,
        entity_registry_enabled_default=False,
        factor=0.1,
    ),
    descr(
        key=SensorKey.CURRENT_HEAT_OUTPUT,
        luxtronik_key=LC.C0257_CURRENT_HEAT_OUTPUT,
        icon="mdi:lightning-bolt-circle",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.POWER,
        entity_category=EntityCategory.DIAGNOSTIC,
        native_unit_of_measurement=UnitOfPower.WATT,
        entity_registry_enabled_default=False,
        native_precision=0,
    ),
    descr(
        key=SensorKey.PUMP_FREQUENCY,
        luxtronik_key=LC.C0231_PUMP_FREQUENCY,
        icon="mdi:sine-wave",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.FREQUENCY,
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        entity_registry_enabled_default=False,
    ),
    descr(
        key=SensorKey.PUMP_FLOW_DELTA_TARGET,
        luxtronik_key=LC.C0239_PUMP_FLOW_DELTA_TARGET,
        icon="mdi:delta",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.KELVIN,
        factor=0.1,
        entity_registry_enabled_default=False,
    ),
    descr(
        key=SensorKey.PUMP_FLOW_DELTA,
        luxtronik_key=LC.C0240_PUMP_FLOW_DELTA,
        icon="mdi:delta",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.KELVIN,
        factor=0.1,
        entity_registry_enabled_default=False,
    ),
    descr(
        key=SensorKey.CIRCULATION_PUMP_DELTA_TARGET,
        luxtronik_key=LC.C0242_CIRCULATION_PUMP_DELTA_TARGET,
        icon="mdi:delta",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.KELVIN,
        factor=0.1,
        entity_registry_enabled_default=False,
    ),
    descr(
        key=SensorKey.CIRCULATION_PUMP_DELTA,
        luxtronik_key=LC.C0243_CIRCULATION_PUMP_DELTA,
        icon="mdi:delta",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.KELVIN,
        factor=0.1,
        entity_registry_enabled_default=False,
    ),
    descr(
        key=SensorKey.HEAT_SOURCE_OUTPUT_TEMPERATURE,
        luxtronik_key=LC.C0020_HEAT_SOURCE_OUTPUT_TEMPERATURE,
        icon="mdi:thermometer",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        entity_registry_enabled_default=False,
        invisible_if_value=-50.0,
        visibility=LV.V0291_OVERHEATING_TEMPERATURE,
    ),
    descr(
        key=SensorKey.ERROR_REASON,
        luxtronik_key=LC.C0100_ERROR_REASON,
        icon="mdi:alert",
        extra_attributes=[
            attr(SA.TIMESTAMP, LC.C0095_ERROR_TIME),
            attr(SA.CODE, LC.C0100_ERROR_REASON),
            attr(SA.CAUSE, LC.C0100_ERROR_REASON),
            attr(SA.REMEDY, LC.C0100_ERROR_REASON),
        ],
    ),
    # endregion Main heatpump
    # region Heating
    descr(
        key=SensorKey.FLOW_IN_TEMPERATURE,
        luxtronik_key=LC.C0010_FLOW_IN_TEMPERATURE,
        device_key=DeviceKey.heating,
        entity_category=None,
        icon="mdi:waves-arrow-right",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        extra_attributes=[
            attr(
                SA.MAX_ALLOWED,
                LP.P0149_FLOW_IN_TEMPERATURE_MAX_ALLOWED,
                SensorAttrFormat.CELSIUS_TENTH,
            ),
        ],
    ),
    descr(
        key=SensorKey.FLOW_OUT_TEMPERATURE,
        luxtronik_key=LC.C0011_FLOW_OUT_TEMPERATURE,
        device_key=DeviceKey.heating,
        entity_category=None,
        icon="mdi:waves-arrow-left",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
    descr(
        key=SensorKey.FLOW_OUT_TEMPERATURE_TARGET,
        luxtronik_key=LC.C0012_FLOW_OUT_TEMPERATURE_TARGET,
        device_key=DeviceKey.heating,
        entity_category=None,
        icon="mdi:thermometer",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        extra_attributes=[
            attr(
                SA.SWITCH_GAP,
                LC.C0011_FLOW_OUT_TEMPERATURE,
                SensorAttrFormat.SWITCH_GAP,
            ),
        ],
    ),
    descr(
        key=SensorKey.OPERATION_HOURS_HEATING,
        luxtronik_key=LC.C0064_OPERATION_HOURS_HEATING,
        device_key=DeviceKey.heating,
        icon="mdi:timer-sand",
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
        native_unit_of_measurement=UnitOfTime.HOURS,
        factor=SECOUND_TO_HOUR_FACTOR,
        native_precision=2,
        update_interval=UPDATE_INTERVAL_VERY_SLOW,
    ),
    descr(
        key=SensorKey.HEAT_AMOUNT_HEATING,
        luxtronik_key=LC.C0151_HEAT_AMOUNT_HEATING,
        device_key=DeviceKey.heating,
        icon="mdi:lightning-bolt-circle",
        state_class=SensorStateClass.TOTAL_INCREASING,
        device_class=SensorDeviceClass.ENERGY,
        entity_category=EntityCategory.DIAGNOSTIC,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        native_precision=1,
        update_interval=UPDATE_INTERVAL_VERY_SLOW,
    ),
    descr(
        key=SensorKey.HEAT_ENERGY_INPUT,
        luxtronik_key=LP.P1136_HEAT_ENERGY_INPUT,
        device_key=DeviceKey.heating,
        icon="mdi:circle-slice-3",
        state_class=SensorStateClass.TOTAL_INCREASING,
        device_class=SensorDeviceClass.ENERGY,
        entity_category=EntityCategory.DIAGNOSTIC,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        native_precision=2,
        factor=0.01,
        min_firmware_version_minor=FirmwareVersionMinor.minor_88,
        update_interval=UPDATE_INTERVAL_VERY_SLOW,
    ),
    descr(
        key=SensorKey.FLOW_OUT_TEMPERATURE_EXTERNAL,
        luxtronik_key=LC.C0013_FLOW_OUT_TEMPERATURE_EXTERNAL,
        device_key=DeviceKey.heating,
        entity_category=None,
        icon="mdi:waves-arrow-right",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        visibility=LV.V0024_FLOW_OUT_TEMPERATURE_EXTERNAL,
    ),
    descr(
        key=SensorKey.ROOM_THERMOSTAT_TEMPERATURE,
        luxtronik_key=LC.C0227_ROOM_THERMOSTAT_TEMPERATURE,
        device_key=DeviceKey.heating,
        entity_category=None,
        icon="mdi:thermometer",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        visibility=LV.V0122_ROOM_THERMOSTAT,
    ),
    descr(
        key=SensorKey.ROOM_THERMOSTAT_TEMPERATURE_TARGET,
        luxtronik_key=LC.C0228_ROOM_THERMOSTAT_TEMPERATURE_TARGET,
        device_key=DeviceKey.heating,
        entity_category=None,
        icon="mdi:thermometer",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        visibility=LV.V0122_ROOM_THERMOSTAT,
    ),
    # endregion Heating
    # region Domestic water
    descr(
        key=SensorKey.DHW_TEMPERATURE,
        luxtronik_key=LC.C0017_DHW_TEMPERATURE,
        device_key=DeviceKey.domestic_water,
        entity_category=None,
        icon="mdi:coolant-temperature",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
    descr(
        key=SensorKey.DHW_OPERATION_HOURS,
        luxtronik_key=LC.C0065_DHW_OPERATION_HOURS,
        device_key=DeviceKey.domestic_water,
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:timer-sand",
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=UnitOfTime.HOURS,
        factor=SECOUND_TO_HOUR_FACTOR,
        native_precision=2,
        update_interval=UPDATE_INTERVAL_VERY_SLOW,
    ),
    descr(
        key=SensorKey.DHW_HEAT_AMOUNT,
        luxtronik_key=LC.C0152_DHW_HEAT_AMOUNT,
        device_key=DeviceKey.domestic_water,
        icon="mdi:lightning-bolt-circle",
        state_class=SensorStateClass.TOTAL_INCREASING,
        device_class=SensorDeviceClass.ENERGY,
        entity_category=EntityCategory.DIAGNOSTIC,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        native_precision=1,
        update_interval=UPDATE_INTERVAL_VERY_SLOW,
    ),
    descr(
        key=SensorKey.DHW_ENERGY_INPUT,
        luxtronik_key=LP.P1137_DHW_ENERGY_INPUT,
        device_key=DeviceKey.domestic_water,
        icon="mdi:circle-slice-3",
        state_class=SensorStateClass.TOTAL_INCREASING,
        device_class=SensorDeviceClass.ENERGY,
        entity_category=EntityCategory.DIAGNOSTIC,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        native_precision=2,
        factor=0.01,
        min_firmware_version_minor=FirmwareVersionMinor.minor_88,
        update_interval=UPDATE_INTERVAL_VERY_SLOW,
    ),
    descr(
        key=SensorKey.SOLAR_COLLECTOR_TEMPERATURE,
        luxtronik_key=LC.C0026_SOLAR_COLLECTOR_TEMPERATURE,
        device_key=DeviceKey.domestic_water,
        entity_category=None,
        icon="mdi:solar-panel-large",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        visibility=LV.V0038_SOLAR_COLLECTOR,
    ),
    descr(
        key=SensorKey.SOLAR_BUFFER_TEMPERATURE,
        luxtronik_key=LC.C0027_SOLAR_BUFFER_TEMPERATURE,
        device_key=DeviceKey.domestic_water,
        entity_category=None,
        icon="mdi:propane-tank-outline",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        visibility=LV.V0039_SOLAR_BUFFER,
    ),
    descr(
        key=SensorKey.OPERATION_HOURS_SOLAR,
        luxtronik_key=LP.P0882_SOLAR_OPERATION_HOURS,
        device_key=DeviceKey.domestic_water,
        icon="mdi:timer-sand",
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
        native_unit_of_measurement=UnitOfTime.HOURS,
        factor=SECOUND_TO_HOUR_FACTOR,
        native_precision=2,
        visibility=LV.V0038_SOLAR_COLLECTOR,
        update_interval=UPDATE_INTERVAL_VERY_SLOW,
    ),
    # endregion Domestic water
    # region Cooling
    descr(
        key=SensorKey.OPERATION_HOURS_COOLING,
        luxtronik_key=LC.C0066_OPERATION_HOURS_COOLING,
        device_key=DeviceKey.cooling,
        icon="mdi:timer-sand",
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
        native_unit_of_measurement=UnitOfTime.HOURS,
        factor=SECOUND_TO_HOUR_FACTOR,
        native_precision=2,
        update_interval=UPDATE_INTERVAL_VERY_SLOW,
    ),
    # endregion Cooling
]
