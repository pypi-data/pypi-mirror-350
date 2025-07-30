import requests as rq 
from bs4 import BeautifulSoup as bs 
from .currency import USD


def BTC(toman=True, beauty=False):
    """
    if toman is False, then BTC Price is in $
    """
    url = 'https://www.tgju.org/profile/crypto-bitcoin'
    response = rq.get(url)
    soup = bs(response.text, 'html.parser')
    price = soup.find('span', {'data-col': 'info.last_trade.PDrCotVal'}).text
    if price:
        gh = str(price).replace(',', '')
        if beauty:
            if toman:
                dollar_price = USD(toman=True)
                final_price = int(float(gh) * dollar_price)
                return f'{int(final_price) // 10:,}'
            else:
                return f'{float(gh):,}'
        else:
            return float(gh)

    else:
        return 'BTC price not found.'
    
def DOGE(toman=True, beauty=False):
    """
    if toman is False, then DOGE Price is in $
    """
    url = 'https://www.tgju.org/profile/crypto-dogecoin'
    response = rq.get(url)
    soup = bs(response.text, 'html.parser')
    price = soup.find('span', {'data-col': 'info.last_trade.PDrCotVal'}).text
    if price:
        gh = str(price).replace(',', '')
        if beauty:
            if toman:
                dollar_price = USD(toman=True)
                final_price = int(float(gh) * dollar_price)
                return f'{int(final_price) // 10:,}'
            else:
                return f'{float(gh):,}'
        else:
            return float(gh)

    else:
        return 'DOGE price not found.'
    
def ETH(toman=True, beauty=False):
    """
    if toman is False, then Ethereum Price is in $
    """
    url = 'https://www.tgju.org/profile/crypto-ethereum'
    response = rq.get(url)
    soup = bs(response.text, 'html.parser')
    price = soup.find('span', {'data-col': 'info.last_trade.PDrCotVal'}).text
    if price:
        gh = str(price).replace(',', '')
        if beauty:
            if toman:
                dollar_price = USD(toman=True)
                final_price = int(float(gh) * dollar_price)
                return f'{int(final_price) // 10:,}'
            else:
                return f'{float(gh):,}'
        else:
            return float(gh)

    else:
        return 'Ethereum price not found.'
    
def SOL(toman=True, beauty=False):
    """
    if toman is False, then Solana Price is in $
    """
    url = 'https://www.tgju.org/profile/crypto-solana'
    response = rq.get(url)
    soup = bs(response.text, 'html.parser')
    price = soup.find('span', {'data-col': 'info.last_trade.PDrCotVal'}).text
    if price:
        gh = str(price).replace(',', '')
        if beauty:
            if toman:
                dollar_price = USD(toman=True)
                final_price = int(float(gh) * dollar_price)
                return f'{int(final_price) // 10:,}'
            else:
                return f'{float(gh):,}'
        else:
            return float(gh)

    else:
        return 'Solana price not found.'