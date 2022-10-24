class TeleInfoData:

    def __init__(self, teleinfo_tags_as_dict: dict[str]):
        self._update_data(teleinfo_tags_as_dict)

    def _update_data(self, teleinfo_data: dict[str]):
        self.meter_identifier = teleinfo_data['ADCO']
        self.subscription_type = teleinfo_data['OPTARIF']
        self.subscription_power_in_a = int(teleinfo_data['ISOUSC'])
        self.total_base_index_in_wh = int(teleinfo_data['BASE'])
        self.current_pricing_period = teleinfo_data['PTEC']
        self.instantaneous_intensity_in_a = int(teleinfo_data['IINST'])
        self.intensity_max_in_a = int(teleinfo_data['IMAX'])
        self.power_consumption_in_va = int(teleinfo_data['PAPP'])
        self.off_peak_index = teleinfo_data['HHPHC']
        self.meter_state_code = teleinfo_data['MOTDETAT']

    def __str__(self):
        return '{\n' \
               f'\tADCO: {self.meter_identifier}\n' \
               f'\tOPTARIF: {self.subscription_type}\n' \
               f'\tISOUSC: {self.subscription_power_in_a} A\n' \
               f'\tBASE: {self.total_base_index_in_wh} W.h\n' \
               f'\tPTEC: {self.current_pricing_period}\n' \
               f'\tIINST: {self.instantaneous_intensity_in_a} A\n' \
               f'\tIMAX: {self.intensity_max_in_a} A\n' \
               f'\tPAPP: {self.power_consumption_in_va} V.A\n' \
               f'\tHHPHC: {self.off_peak_index}\n' \
               f'\tError Code: {self.meter_state_code}\n' \
               '}'
