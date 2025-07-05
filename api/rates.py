import requests
from bs4 import BeautifulSoup
from utils.logger import log_error

def get_rfr() -> float:
    """Scrape the 10-year Treasury yield from FRED."""
    try:
        url = 'https://fred.stlouisfed.org/series/DGS10'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, features='html.parser')
        span = (
            soup.find('div', id='container')
                .find('div', id='main-content-column')
                .find('div', class_='row series-attributes')
                .find('p', class_='mb-2')
                .find_next('span')
        )
        return float(span.text) / 100
    except Exception as e:
        print(f"[ERROR] Failed to fetch risk-free rate: {e}")
        log_error(e)
        return 0.05  # fallback rate