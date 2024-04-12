# routes/scraper.py
from flask import Blueprint, render_template, jsonify
import requests
from bs4 import BeautifulSoup
import re

def scrape_nzs_tekme():
    url = "https://www.nzs.si/reprezentanca/?action=tekme&id_menu=11"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    tekme = []
    for tekma in soup.select('table.tekme tr.hidden-xs'):
        rezultat_raw = tekma.select_one('td.rezultat span').get_text() if tekma.select_one('td.rezultat span') else None
        rezultat = obdelaj_rezultat(rezultat_raw)

        tekme.append({
            'home_team': tekma.select_one('td:nth-child(2)').get_text().strip(),
            'away_team': tekma.select_one('td:nth-child(6)').get_text().strip(),
            'result': rezultat,
            'datetime': tekma.select_one('td:nth-child(7)').get_text().strip(),
            'competition_type': tekma.select_one('td:nth-child(8)').get_text().strip(),
        })

    return tekme

def obdelaj_rezultat(rezultat_raw):
    if rezultat_raw:
        return rezultat_raw.strip().replace(':', 'vs.')
    return rezultat_raw


scraper_bp = Blueprint('scraper_bp', __name__)

@scraper_bp.route('/scrape')
def scrape_page():
    return render_template('scrape.html')

@scraper_bp.route('/scrape-matches', methods=['GET'])
def get_scraped_matches():
    scraped_matches = scrape_nzs_tekme()
    return jsonify(scraped_matches)
