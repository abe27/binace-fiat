import requests

fiatList = ["AUD", "BRL", "EUR", "GBP", "RUB",
            "TRY", "UAH", "ZAR", "IDRT", "NGN", "PLN", "RON", "ARS"]

crytoList = ['BTC', 'ETH', 'ADA', 'USDT', 'XRP', 'LINK', 'MANA', 'XLM', 'BNB', 'DOGE', 'TRX', 'ALGO', 'BUSD', 'ENJ', 'DOT', 'NEAR', 'UNI',
             'SAND', 'GRT', 'MATIC', 'AXS', 'IMX', 'GALA', 'CHZ', 'SOL', 'AVAX', 'FTM', 'APE', 'GAL', 'OP', 'ATOM', 'ARB', 'ID']
advCash = ["RUB", "EUR"]


def lastPricePerTHB(currency):
    response = requests.request(
        "GET", f"https://api.exchangerate-api.com/v4/latest/{currency}")
    obj = response.json()
    data = obj["rates"]
    return float(data["THB"])


def main():
    for symbol in crytoList:
        print(f"Start {symbol}:==>")
        for currency in fiatList:
            pair = f"{symbol}{currency}"
            res = requests.request(
                "GET", f"https://api.binance.com/api/v3/ticker/price?symbol={pair}")
            if res.status_code == 200:
                obj = res.json()
                thbPrice = lastPricePerTHB(currency)
                print(
                    f"{symbol}/{currency} ==> {res.status_code} price: {obj['price']} THB: {float(obj['price']) * thbPrice}")

        print(f"---------------------------")


if __name__ == "__main__":
    main()
