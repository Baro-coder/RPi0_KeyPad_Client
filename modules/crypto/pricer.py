#!/usr/bin/python
# -- KeyPad_Client/modules/crypto: pricer.py --

from bs4 import BeautifulSoup
import requests


URL = 'https://e-kursy-walut.pl/'

URL_PATHS = {
    'BTC' : 'kurs-bitcoin/',
    'ETH' : 'kurs-ethereum/'
}

CURRENCY = 'USD'

PTRS = {
    'INC' : '↑',
    'DEC' : '↓',
    'EQL' : '-'
}


def get_BTC_price():
    url = URL + URL_PATHS['BTC']
    
    try: 
        html_doc = requests.get(url)
        
    except Exception as e:
        return None
    
    soup = BeautifulSoup(html_doc.content, 'html.parser')
    
    sections = soup.find_all('small')
    
    price = str(sections[1].get_text())
    
    price = price.replace(' ', '')[:-3]
    price = price.replace(',', '.')
    price = float(price)
    price = round(price, 2)
    
    out = f'BTC:{(19 - (len(price) + len(CURRENCY))) * " "}{price} {CURRENCY}'
    
    return out

def get_ETH_price():
    url = URL + URL_PATHS['ETH']
    
    try: 
        html_doc = requests.get(url)
        
    except Exception as e:
        return None
    
    soup = BeautifulSoup(html_doc.content, 'html.parser')
    
    sections = soup.find_all('small')
    
    price = str(sections[1].get_text())
    
    price = price.replace(' ', '')[:-3]
    price = price.replace(',', '.')
    price = float(price)
    price = round(price, 2)
    
    out = f'ETH:{(19 - (len(price) + len(CURRENCY))) * " "}{price} {CURRENCY}'
    
    return out