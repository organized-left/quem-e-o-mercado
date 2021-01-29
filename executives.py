
'''
Get The excutives names from a list of Tickers

# Setup
pip install pandas
pip install numpy
python3 -m pip install googlesearch-python
'''

import pandas as pd
from googlesearch import search
import yfinance as yf
import yaml
import numpy as np
import json


def get_executives(symbol):
    # search on yahoo finances for executive names
    url = f'https://finance.yahoo.com/quote/{symbol}/profile?p={symbol}'
    print(f'>> loading ${symbol} from ${url}')
    profile = pd.read_html(url)
    df = profile[0]
    df = df.replace(np.nan, 0)

    executives = []
    for i in df.index:
        name = df['Name'][i].replace("Mr. ", '')  # removing all the "Mr."
        name = name.replace("Ms. ", '')  # removing all the "Ms."
        title = df['Title'][i]
        year_born = df['Year Born'][i]
        if pd.isna(year_born):
            year_born = -1

        age2021 = 2021 - df['Year Born'][i]
        pay = df["Pay"][i]
        if pd.isna(pay):
            pay = -1
        else:
            pay = float(pay)
        google_links = search(name)
        profile = {}

        for link in google_links:
            if "bloomberg.com/profile/person/" in link:
                profile["bloomberg"] = link
            if "wikipedia.org/wiki/" in link:
                profile["wikipedia"] = link
            if "wsj.com/market-data/quotes/ITUB/company-people/executive-profile/" in link:
                profile["wsj"] = link
            if "theofficialboard.com/biography/" in link:
                profile["biography"] = link

        person = {
            "name": name,
            "title": title,
            "year_born": int(year_born),
            "age2021": int(age2021),
            "pay": pay,
            "profile": profile
        }
        executives.append(person)

    return executives


if __name__ == "__main__":
    companies = [
        {
            "name": "Petrobras",
            "symbol": "PETR4.SA",
        },
        {
            "name": "Itau Unibanco Holding SA",
            "symbol": "ITUB4.SA"
        },
        {
            "name": "Banco Bradesco S.A.",
            "symbol": "BBDC4.SA"
        },
        {
            "name": "Banco do Brasil S.A.",
            "symbol": "BBAS3.SA"
        },
        {
            "name": "JBS",
            "symbol": "JBSS3.SA"
        },
        {
            "name": "Vale S.A.",
            "symbol": "VALE"
        },
        {
            "name": "Eletrobrás",
            "symbol": "ELET3.SA"
        },
        {
            "name": "Banco BTG Pactual",
            "symbol": "BPAC11.SA"
        },
        {
            "name": "B3 S.A. - Brasil, Bolsa, Balcão",
            "symbol": "B3SA3.SA"
        },
        {
            "name": "Suzano Papel e Celulose",
            "symbol": "SUZ"
        },
        {
            "name": "CPFL Energia S.A.",
            "symbol": "CPFE3.SA"
        },
        {
            "name": "Braskem S.A.",
            "symbol": "BRKM5.SA"
        },
        {
            "name": "WEG S.A.",
            "symbol": "WEGE3.SA"
        },
        {
            "name": "Companhia Energética de Minas Gerais ",
            "symbol": "CMIG4.SA"
        },
        {
            "name": "Ultrapar Participações S.A.",
            "symbol": "UGPA3.SA"
        },
        {
            "name": "Companhia Brasileira de Distribuição",
            "symbol": "CBD"
        },
        {
            "name": "Magazine Luiza S.A.",
            "symbol": "MGLU3.SA"
        },
    ]

    result = []

    for company in companies:
        try:
            company["executives"] = get_executives(company['symbol'])
            result.append(company)

        except(RuntimeError, TypeError, NameError):
            print(f'can\'t load company {company["name"]}')
            print(RuntimeError)
            continue

    # exporting yaml
    with open(r'excutives.yaml', 'w') as file:
        documents = yaml.dump(result, file, sort_keys=False)

    # export json
    with open(r'executives.json', 'w') as file:
        json.dump(result, file, sort_keys=False)
