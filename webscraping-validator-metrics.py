import csv
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import numpy as np

url = 'https://stakeview.app/good.html'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

req = Request(url, headers=headers)
webpage = urlopen(req).read()

soup = BeautifulSoup(webpage, "html.parser")

rows = soup.find_all('tr')

with open('validators.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Validator', 'Vote Account', 'Stake (SOL)', 'VL', 'LLV', 'CV', 'VO'])

    for row in rows[1:]:  
        columns = row.find_all('td')
        if columns:
            validator = columns[0].text.strip().replace('\xa0', '').replace('&nbsp', '')
            vote_account = columns[1].text.strip()
            stake = columns[2].text.strip()
            vl = columns[3].text.strip()
            llv = columns[4].text.strip()
            cv = columns[5].text.strip()
            vo = columns[6].text.strip()
            writer.writerow([validator, vote_account, stake, vl, llv, cv, vo])

validators = []

with open('validators.csv', mode='r') as file:
    reader = csv.reader(file)
    next(reader)  
    for row in reader:
        try:
            vl = float(row[3])
            validators.append((row[0], vl))
        except ValueError:
            continue

validators.sort(key=lambda x: x[1])

vl_values = [v[1] for v in validators]
percentiles = [np.percentile(vl_values, i) for i in range(101)]

def get_percentile(vl):
    return next(i for i, p in enumerate(percentiles) if vl <= p)

print("\nTop 10 Validators by Smallest VL Value:\n")
for rank, (validator, vl) in enumerate(validators[:10], start=1):
    percentile = get_percentile(vl)
    print(f"{rank:<3} | {validator:<30} | VL: {vl:.3f} | Percentile: {percentile}%")

print("\nTop 30 Validators by Largest VL Value:\n")
for rank, (validator, vl) in enumerate(validators[-30:], start=1):
    percentile = get_percentile(vl)
    print(f"{rank:<3} | {validator:<30} | VL: {vl:.3f} | Percentile: {percentile}%")