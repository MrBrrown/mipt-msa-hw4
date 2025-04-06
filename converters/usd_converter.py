from converters.currency_converter import CurrencyConverter

class USDConverter(CurrencyConverter):
    def __init__(self):
        super().__init__()
        self.API_URL = "https://api.exchangerate-api.com/v4/latest/USD"

     
    def convert(self, target_currency : str, amount : float) -> float:
        upper_target_currency = target_currency.upper()
        rates = self._get_actual_rates()
        if not rates:
            return None
         
        if upper_target_currency not in rates:
            return None
        
        return rates[upper_target_currency] * amount