import requests
from bs4 import BeautifulSoup
import re
from flask import Flask, jsonify

def parser(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    return soup

def scraper(search_term):
    soup = parser(f"https://www.1377x.to/search/{search_term}/1/")
    containers = soup.findAll("tbody")

    link_lst = []
    names_lst = []
    sizes_lst = []
    for container in containers:
        temp_link = container.findAll("td", {"class": "name"})
        sizes = container.findAll("td", {"class": "size"})
        
        for link in temp_link:
            names_lst.append(link.findAll('a')[1].text)
            
            l = [a['href'] for a in link.findAll('a', href=True)]
            link_lst.append(l[1])

        for size in sizes:
            sizes_lst.append(size.text)
    
                    
    modded_lst = []  
    for link in link_lst:
        first_link = "https://www.1377x.to"
        modded_link = first_link + link
        modded_lst.append(modded_link)
        

    movie_dict = {}        
    for i in range(0, len(link_lst), 1):
        # print(f"[{i+1}]  " + names_lst[i] + "----->" + sizes_lst[i])
        movie_dict[i] = {"name": names_lst[i],
                        "size": sizes_lst[i],
                        "link": modded_lst[i]}
        
    return movie_dict


app = Flask(__name__)

@app.route('/')
def index():
    return '''<html><h1>The API is running</h1></html>'''

@app.route('/<query>')
def home(query):
    diction = scraper(query)
    return jsonify(diction)

if __name__ == "__main__":
    app.debug = True
    app.run(host='localhost', port=5000)
    
    
    
# magnet_links = []
# def fun(movie_link):
#     soup = parser(movie_link)
#     containers = soup.findAll("div", {"class": "box-info"})
    
#     for container in containers:
#         t=0
#         for link in container.findAll("li"):
        
#             l = [a['href'] for a in link.findAll('a', href=True)]
#             return l[0]
                

# ch = 2
# movie_link = movie_dict[ch]["link"]
# l = fun(movie_link)
# print(l)