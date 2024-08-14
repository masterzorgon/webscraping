import requests
from bs4 import BeautifulSoup

url = 'https://coinmarketcap.com/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

# Find the rows containing the cryptocurrency data
rows = soup.find_all('tr')[:5]  # We are assuming that the top 5 rows correspond to the top 5 cryptos

top_cryptos = []

for row in rows:
    name = row.find('p', class_="coin-item-symbol").text if row.find('p', class_="coin-item-symbol") else "No Name"
    symbol = row.find('p', class_="coin-item-symbol").text if row.find('p', class_="coin-item-symbol") else "No Symbol"
    price_container = row.find('div', class_="sc-500f568e-0 ejtlWy")
    price_link = price_container.find('a', class_="cmc-link") if price_container else None
    price_text = price_link.find('span').text if price_link and price_link.find('span') else "No Price"
    
    # Removing dollar sign and commas before converting to float
    price = float(price_text.replace('$', '').replace(',', '')) if "No Price" not in price_text else 0

    percent_change_text = row.find('span', class_="sc-6a54057-0 YXxPZ").text if row.find('span', class_="sc-6a54057-0 YXxPZ") else "0%"
    # Removing the percent sign and converting to float
    percent_change = float(percent_change_text.replace('%', '').replace(',', '')) if "No Change" not in percent_change_text else 0

    # Calculating corresponding price
    corresponding_price = price / (1 + (percent_change / 100))

    top_cryptos.append({
        'Name': name,
        'Symbol': symbol,
        'Current Price': f'${price:.2f}',
        'Change in 24h': f'{percent_change:.2f}%',
        'Corresponding Price 24h Ago': f'${corresponding_price:.2f}'
    })

# Print the data
for crypto in top_cryptos:
    print(f"\nName: {crypto['Name']}, Symbol: {crypto['Symbol']}, Current Price: {crypto['Current Price']}, Change in 24 hrs: {crypto['Change in 24h']}, Corresponding Price 24h Ago: {crypto['Corresponding Price 24h Ago']}")
