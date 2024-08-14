from urllib.request import urlopen, Request
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go

url = 'http://quotes.toscrape.com/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

req = Request(url, headers=headers)
webpage = urlopen(req).read()
soup = BeautifulSoup(webpage, "html.parser")
print(soup.title.text)

# step 1. scrape the first 10 pages of quotes
quotes = []

for i in range(1, 11):
    res = requests.get(url.format(i), headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    quote_data = soup.findAll('div', attrs={"class": "quote"})

    for quote in quote_data:
        text = quote.find('span', class_='text').get_text()
        author = quote.find('small', class_='author').get_text()
        tags = [tag.get_text() for tag in quote.find_all('a', class_='tag')]
        quotes.append((text, author, tags))

# step 2. Count the number of quotes by each author
author_quote_count = {}

for _, author, _ in quotes:
    if author not in author_quote_count:
        author_quote_count[author] = 0
    author_quote_count[author] += 1

# step 3. Find the author with the most and least quotes
most_quotes_author = max(author_quote_count, key=author_quote_count.get)
least_quotes_author = min(author_quote_count, key=author_quote_count.get)

print(f"\nMost prolific author: {most_quotes_author} with {author_quote_count[most_quotes_author]} quotes.")
print(f"\nLeast prolific author: {least_quotes_author} with {author_quote_count[least_quotes_author]} quotes.")

# step 4. Determine the average length of quotes
total_length = sum(len(text) for text, _, _ in quotes)
average_length = total_length / len(quotes)
print(f"\nAverage length of quotes: {average_length:.2f} characters.")

# step 5. Identify the longest and shortest quotes
sorted_quotes = sorted(quotes, key=lambda x: len(x[0]))
longest_quote = sorted_quotes[-1][0]
shortest_quote = sorted_quotes[0][0]

print(f"\nLongest quote: \"{longest_quote}\"")
print(f"\nShortest quote: \"{shortest_quote}\"")

# step 6. If there are tags associated with each quote, analyze the distribution of tags
tag_distr = {}

for _, _, tags in quotes:
    for tag in tags:
        if tag not in tag_distr:
            tag_distr[tag] = 0
        tag_distr[tag] += 1

# step 7. What is the most popular tag?
most_popular_tag = max(tag_distr, key=tag_distr.get)
print(f"\nMost popular tag: {most_popular_tag} used {tag_distr[most_popular_tag]} times.")

# step 8. How many total tags were used across all quotes?
total_tags = sum(tag_distr.values())
print(f"\nTotal number of tags used: {total_tags}")


# step 9. Create a visualization using plotly to represent the top 10 authors and their corresponding number of quotes with the highest number first
top_authors = sorted(author_quote_count.items(), key=lambda x: x[1], reverse=True)[:10]
fig_authors = go.Figure([go.Bar(x=[author for author, _ in top_authors], y=[count for _, count in top_authors])])
fig_authors.update_layout(title='Top 10 Authors by Number of Quotes', xaxis_title='Author', yaxis_title='Number of Quotes')
fig_authors.show()

# step 10. Create a visualization using plotly to represent the top 10 tags based on popularity
top_tags = sorted(tag_distr.items(), key=lambda x: x[1], reverse=True)[:10]
fig_tags = go.Figure([go.Bar(x=[tag for tag, _ in top_tags], y=[count for _, count in top_tags])])
fig_tags.update_layout(title='Top 10 Tags by Popularity', xaxis_title='Tag', yaxis_title='Count')
fig_tags.show()