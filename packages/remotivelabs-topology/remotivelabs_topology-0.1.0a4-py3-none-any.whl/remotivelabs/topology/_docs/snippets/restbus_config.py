from remotivelabs.topology import RestbusConfig, filters

restbus_configs = RestbusConfig(
    restbus_filters=[filters.Sender(ecu_name="HazardLightControlUnit")],
    cycle_time_millis=20,  # Fixed cycle time of 0.02 seconds (50Hz)
    # and/or
    delay_multiplier=2,  # Scale database cycle times by factor 2
)
