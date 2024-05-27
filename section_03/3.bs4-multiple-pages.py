from bs4 import BeautifulSoup
import requests

#####################################################
# Extracting links from pagination bar
#####################################################

# How To Get The HTML
root = 'https://subslikescript.com'  # this is the homepage of the website
website = f'{root}/movies_letter-X'  # concatenating the homepage with the movies "letter-X" section. You can choose any section (e.g., letter-A, letter-B, ...)
result = requests.get(website)
content = result.text
soup = BeautifulSoup(content, 'lxml')

# Locate the box that contains the pagination bar
pagination = soup.find('ul', class_='pagination')
pages = pagination.find_all('li', class_='page-item')
last_page = pages[-2].text  # this is the number of pages that the website has inside the movies "letter X" section

##################################################################################
# Extracting the links of multiple movie transcripts inside each page listed
##################################################################################

# Loop through all tbe pages and sending a request to each link
for page in range(1, int(last_page)+1):
    result = requests.get(f'{website}?page={page}')  # structure --> https://subslikescript.com/movies_letter-X?page=2
    content = result.text
    soup = BeautifulSoup(content, 'lxml')

    # Locate the box that contains a list of movies
    box = soup.find('article', class_='main-article')

    # Store each link in "links" list (href doesn't consider root aka "homepage", so we have to concatenate it later)
    links = []
    for link in box.find_all('a', href=True):  # find_all returns a list
        links.append(link['href'])

    #################################################
    # Extracting the movie transcript
    #################################################

    for link in links:
        try:  # "try the code below. if something goes wrong, go to the "except" block"
            result = requests.get(f'{root}/{link}')  # structure --> https://subslikescript.com/movie/X-Men_2-290334
            content = result.text
            soup = BeautifulSoup(content, 'lxml')

            # Locate the box that contains title and transcript
            box = soup.find('article', class_='main-article')
            # Locate title and transcript
            title = box.find('h1').get_text()
            transcript = box.find('div', class_='full-script').get_text(strip=True, separator=' ')

            # Exporting data in a text file with the "title" name
            with open(f'{title}.txt'.replace(':','_').replace('/', '_'), 'w', encoding='utf-8') as file:
                file.write(transcript)
        except Exception as e:  # "if something goes wrong, print the error message"
            print('------ Link not working -------')
            print(link, '\n\terror:\t', e)
