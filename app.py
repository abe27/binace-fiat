import requests
import psycopg2

fiatList = ["AUD", "BRL", "EUR", "GBP", "RUB",
            "TRY", "UAH", "ZAR", "IDRT", "PLN", "RON", "ARS"]

crytoList = ['BTC', 'ETH', 'ADA', 'USDT', 'XRP', 'LINK', 'MANA', 'XLM', 'BNB', 'DOGE', 'TRX', 'ALGO', 'BUSD', 'ENJ', 'DOT', 'NEAR', 'UNI',
             'SAND', 'GRT', 'MATIC', 'AXS', 'IMX', 'GALA', 'CHZ', 'SOL', 'AVAX', 'FTM', 'APE', 'GAL', 'OP', 'ATOM', 'ARB', 'ID']
advCash = ["RUB", "EUR"]

# Replace the placeholders with your actual database connection details
host = 'localhost'
database = 'arbitragedb'
user = 'postgres'
password = 'admin@1234'


def lastPricePerTHB(currency):
    response = requests.request(
        "GET", f"https://api.exchangerate-api.com/v4/latest/{currency}")
    obj = response.json()
    data = obj["rates"]
    return float(data["THB"])


def main():
    conn = psycopg2.connect(host=host, database=database,
                            user=user, password=password)
    # Create a cursor object to interact with the database
    cursor = conn.cursor()
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
                cursor.execute(
                    f"select * from tbt_assets where symbol='{symbol}' and pair='{currency}'")

                sql = f"update public.tbt_assets set symbol='{symbol}', pair='{currency}', price={float(obj['price']) * thbPrice}, lastupdate=CURRENT_TIMESTAMP where symbol='{symbol}' and pair='{currency}'"
                if cursor.fetchone() == None:
                    sql = f"insert into public.tbt_assets(symbol,pair,price,lastupdate)values('{symbol}', '{currency}',{float(obj['price']) * thbPrice},CURRENT_TIMESTAMP)"

                cursor.execute(sql)
        print(f"---------------------------")

    conn.commit()
    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
