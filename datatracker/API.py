import json
import requests


from types import SimpleNamespace
from re import search
from flask import Flask, jsonify, request, redirect, flash, render_template, url_for, Blueprint
from flask_bootstrap import Bootstrap
bp = Blueprint('home', __name__)


# class API:
#     def __init__(self):
api_request = requests.get('https://api.dccresource.com/api/games')


@bp.route('/test')
def test():
    return "All good!"

@bp.route('/home')
def request_list_games():
    response = api_request
    game_data = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
    list_games = list(filter(lambda g: str(g.year) == '1985', game_data))
    headings = ('Title', 'Platform', 'Year', 'Genre', 'Publisher', 'Sales')
    return render_template('home/index.html', headings=headings, data=list_games)


# def filter_to_dict(list_games):
#     results = []
#     game_dict = {'PSV': {'name', 'platform', 'year', 'genre', 'publisher', 'globalSales'},
#                 'PS4': {'name', 'platform', 'year', 'genre', 'publisher', 'globalSales'}}
#     for game in list_games:
#         game_dict[game.]



def find_game(games_list):
    print("please enter a title to search for")
    result = []
    titleSearch = input()
    for item in games_list:
        if search(titleSearch.casefold(), item.name.casefold()):
            result.append(item)
    return result


def sales_platform(result):
    sales = []
    regionSales = []
    totalSales = 0
    naSalesTotal = 0
    for item in result:
        totalSales = totalSales + item.globalSales
        naSalesTotal = naSalesTotal + item.naSales
        sales.append({item.platform, item.globalSales})
        regionSales.append({item.platform,item.naSales})
        print(f"{item.name}\n  Platform: {item.platform}\n North American Sales: {item.naSales}"
              f"\n Total Sales: {item.globalSales} \n")
    print(f"{item.name} had sales across all platforms of\n North America: {round(naSalesTotal,2)}"
          f"\n Globally: {totalSales}")


def get_platform(games_list):
    console = []
    for item in games_list:
        if item.platform not in console:
            console.append(item.platform)
    return console


def sales_by_console(games_list, console_list):
    consoleSales = []
    for console in console_list:
        sales = 0
        for game in games_list:
            if game.platform == console:
                sales = sales + game.globalSales
        consoleSales.append({'console' : console, 'sales' : sales})
    return consoleSales