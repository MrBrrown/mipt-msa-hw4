from converters import *


def convert(target_currency : str, amount : float, converter : CurrencyConverter):
    res = converter.convert(target_currency, amount)
    if not res:
        print(f"Error to convert from USD to {target_currency.upper()}, see log file")
    else:
        print(f"{amount} USD to {target_currency.upper()}: {res:.3f}")

def main():    
    amount = float(input('Введите значение в USD: \n'))
    converter = USDConverter()

    convert("RUB", amount, converter)
    convert("EUR", amount, converter)
    convert("GBP", amount, converter)
    convert("CNY", amount, converter)

if __name__ == "__main__":
    main()