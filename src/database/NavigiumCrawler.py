import socket
import requests
from time import perf_counter
from bs4 import BeautifulSoup as soup

class NavigiumCrawler():

    @staticmethod
    def check_connection():
        try:
            socket.setdefaulttimeout(2)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
            connectivity = True
        except socket.error as ex:
            connectivity = False
        return connectivity

    @staticmethod
    def search(word):
        if not NavigiumCrawler.check_connection():
            print('No Internet connection')
            return ''

        url = f"https://www.navigium.de/latein-woerterbuch.html?form={word}&wb=gross&nr=1"
        navigium_html = requests.get(url)
        navigium_soup = soup(navigium_html.content, 'lxml')
        ausgabe_soup = navigium_soup.find(id='ausgabe')

        html = ''
        if ausgabe_soup:
            results = []
            for elem in ausgabe_soup.contents:
                if elem.attrs['class'][0] == 'margin-top-50':
                    break
                if elem.attrs['class'][0] == 'result':
                    results.append(elem)

            for result in results:
                word_soup = result.find("div", {"class": "latein"})
                if word_soup:
                    word = word_soup.text.rstrip()
                form_soup = result.find("div", {"class": "formen"})
                if form_soup:
                    form = form_soup.text.rstrip()
                    beds = result.find_all("div", {"class": "bed"})
                meanings = []
                if beds:
                    for bed in beds:
                        meanings.append(bed.text.rstrip())

                html += '<b style="color: #b85">' + word + '</b><br>'
                html += '<i style="color: #b85">' + form + '</i>'
                html += '<ol>'
                for mean in (meanings):
                    html = html + '<li>' + mean + '</li>'
                html += '</ol><br>'
        return html