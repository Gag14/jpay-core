import requests

def get_crypto_to_fiat_rate(crypto, fiat):
    url = f"https://min-api.cryptocompare.com/data/price?fsym={crypto}&tsyms={fiat}"
    print(crypto, fiat)
    headers = {
        "Authorization": "Apikey YOUR_API_KEY"  # Only if needed
    }
    response = requests.get(url, headers=headers)
    return response.json().get(fiat)

# rate = get_crypto_to_fiat_rate("BTC", "EUR")
# print("BTC to EUR:", rate)
