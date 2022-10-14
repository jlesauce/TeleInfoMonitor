class TeleInfoData:

    def __init__(self):
        self.meter_identifier = 0
        self.subscription_type = 0
        self.subscription_power_in_a = 0
        self.total_base_index_in_wh = 0
        self.current_pricing_period = ''
        self.instantaneous_intensity_in_a = 0
        self.intensity_max_in_a = 0
        self.power_consumption_in_va = 0
        self.off_peak_index = ''
        self.meter_state_code = '000000'

    def __int__(self, teleinfo_tags_as_list: list[str]):
        pass
