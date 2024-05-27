from bs4 import BeautifulSoup
import requests

#####################################################
# Extracting the links of multiple movie transcripts
#####################################################

# How To Get The HTML
root = 'https://subslikescript.com'  # this is the homepage of the website
website = f'{root}/movies'  # concatenating the homepage with the movies section
result = requests.get(website)
content = result.text
soup = BeautifulSoup(content, 'lxml')
# print(soup.prettify())  # prints the HTML of the website

# Locate the box that contains a list of movies
box = soup.find('article', class_='main-article')

# Store each link in "links" list (href doesn't consider root aka "homepage", so we have to concatenate it later)
links = []
for link in box.find_all('a', href=True):  # find_all returns a list
    links.append(link['href'])

#################################################
# Extracting the movie transcript
#################################################

# Loop through the "links" list and sending a request to each link
for link in links:
    result = requests.get(f'{root}/{link}')
    content = result.text
    soup = BeautifulSoup(content, 'lxml')

    # Locate the box that contains title and transcript
    box = soup.find('article', class_='main-article')
    # Locate title and transcript
    title = box.find('h1').get_text()
    title = ''.join(title.split('/'))
    transcript = box.find('div', class_='full-script').get_text(strip=True, separator=' ')

    # Exporting data in a text file with the "title" name
    with open(f'{title}.txt', 'w', encoding='utf-8') as file:
        file.write(transcript)