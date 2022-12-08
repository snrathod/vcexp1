import bs4
import urllib.request
import json

def soup_function(url):
    sauce = urllib.request.urlopen(url).read()
    soup = bs4.BeautifulSoup(sauce, 'lxml')
    return soup

def all_links():
    urls = list()
    all_movies = list()
    soup = soup_function('https://www.imdb.com/chart/top/')
    for i in soup.find_all('a'):
        links = i.get('href')
        urls.append(links)
    
    urls = ['https://imdb.com'+x.strip() for x in urls if x is not None and x.startswith('/title/tt')]
    for links in urls:
        if links not in all_movies:
            all_movies.append(links)
    return all_movies


def movie_information():
    data_list = list()
    all_movies = all_links()
    for i in all_movies:
        soup = soup_function(i)
        title = soup.find('meta', property = 'og:title')
        movie_name = title['content']
        image = soup.find('meta', property = 'og:image')
        movie_image = image['content']
        genre = soup.find('div', {'class':'subtext'})
        movie_genre = genre.find('a').text
        director = soup.find('div', {'class':'credit_summary_item'})
        movie_director = director.find('a').text
        data = {
            "movie_name" : movie_name,
            "movie_image" : movie_image,
            "movie_genre" : movie_genre,
            "movie_director" : movie_director
        }
        data_list.append(data)
    
    json_file = open('data.json', 'w')
    json.dump(data_list, json_file)

if __name__ == '__main__':
    movie_information()