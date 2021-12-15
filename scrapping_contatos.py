from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
from threading import Thread
import re
from colorama import Fore
from time import sleep


class Crawler:
    site = 'https://www.guiamais.com.br/encontre?searchbox=true&what=XXXX&where=ZZZ%2C+ZZ'
    base = 'https://www.guiamais.com.br'
    

    def __init__(self, cidade, estado, pesquisa):
        """Informe a cidade-estado e o que está buscando"""
        self.__cidade = cidade
        self.__estado = estado
        self.__pesquisa = pesquisa
        
   
    @property
    def cidade(self):
        return self.__cidade

    @property
    def estado(self):
        return self.__estado

    @property
    def pesquisa(self):
        return self.__pesquisa

    @cidade.setter
    def cidade(self, nova_cidade):
        self.__cidade = nova_cidade


    def parse_html(self):
        try:
            search1 = Crawler.site.replace('XXXX', self.__pesquisa)
            search2 = search1.replace('ZZZ', self.__cidade).replace(' ', '+')
            search3 = search2.replace('ZZ', self.__estado)
            req = urlopen(search3)
        except HTTPError as HTTP:
            print(Fore.RED + "Erro no servidor do site, ou na sua rede")
            print(HTTP)
        except URLError as URL:
            print(Fore.RED + "Url incorreta, verifique o endereço")
            print(URL)
        else:
            bs = BeautifulSoup(req, 'html.parser')
            t = []
            tel = []
            ende = []
            # titulo dos médicos
            div = bs.find_all('div', {'class': 'left'})
            for titulo in div:
                texto = titulo.find('h2').find('a')
                link = texto.attrs
                buscar = urlopen(Crawler.base + link['href'])
                bs1 = BeautifulSoup(buscar, 'html.parser')
                tel.append(Crawler.busca_telefone(bs1))
                if 'href' in texto.attrs:
                    if texto.text.lstrip() not in t:
                        t.append(texto.text.lstrip())

            with open("pesquisa_contatos.txt", 'a') as f:
                for i in range(len(t)):
                    if tel[i] != []:
                        f.writelines(f"PESQUISA: {t[i]} ------ CONTATO:  {tel[i]}\n")


    @staticmethod
    def busca_telefone(obj):
        lista = obj.find_all('li', {'class': 'detail'})
        telefones = []
        t = []
        for tel in lista:
            telefone = tel.find('p')
            telefones.append(telefone.text.lstrip())
        for tel in telefones:
            telefone = str(tel)
            formato = re.compile("(\(?\d{2}\)?\s)?(\d{4,5}\-\d{4})")  # regex telefone e celular
            try:
                t.append(formato.search(telefone).group(0))
            except AttributeError:
                pass
        return t


if __name__ == '__main__':
    sleep(1)
    cidade = input(Fore.GREEN + "Informe a cidade, por exemplo, Sete Lagoas: ")
    estado = input("Informe o estado, por exemplo, MG: ")
    pesquisa = input("Informe o que quer, por exemplo, medicos: ")
    crawler = Crawler(cidade, estado, pesquisa)
    thread = Thread(target=crawler.parse_html, args=())
    thread.start()
    thread.join()
    print(Fore.LIGHTCYAN_EX + "\nCreated By Marcus-V@outlook.com")

# criado por Marcus Vinícius: https://github.com/PyMarcus/
