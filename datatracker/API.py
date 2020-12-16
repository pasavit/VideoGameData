import json
import requests


from types import SimpleNamespace
from re import search
from flask import Flask, jsonify, request, redirect, flash, render_template, url_for, Blueprint
bp = Blueprint('home', __name__)


@bp.route('/test')
def test():
    return "All good!"


def get_api_data():
    api_request = requests.get('https://api.dccresource.com/api/games')
    api_data = json.loads(api_request.content, object_hook=lambda d: SimpleNamespace(**d))
    return api_data


@bp.route('/home')
def populate_game_chart():
    api_data = get_api_data()
    list_games = list(filter(lambda g: str(g.year) == '2017', api_data))
    headings = ('Title', 'Platform', 'Year', 'Genre', 'Publisher', 'Sales(mil)')
    return render_template('home/index.html', headings=headings, data=list_games)


def filter_by_year():
    api_data = get_api_data()
    year = input()
    list_games = list(filter(lambda g: str(g.year) == year, api_data))
    headings = ('Title', 'Platform', 'Year', 'Genre', 'Publisher', 'Sales(mil)')
    return render_template('home/index.html', headings=headings, data=list_games)


def filter_by_console():
    api_data = get_api_data()
    console = input()
    list_games = list(filter(lambda g: str(g.paltform) == console, api_data))
    headings = ('Title', 'Platform', 'Year', 'Genre', 'Publisher', 'Sales(mil)')
    return render_template('home/index.html', headings=headings, data=list_games)


@bp.route('/title', methods=['POST'])
def filter_by_title():
    api_data = get_api_data()
    title = request.form.get('title')
    list_games = []
    for item in api_data:
        if search(title.casefold(), item.name.casefold()):
            list_games.append(item)
    headings = ('Title', 'Platform', 'Year', 'Genre', 'Publisher', 'Sales(mil)')
    return render_template('home/title.html', headings=headings, data=list_games)


def find_games(games_list):
    print("please enter a title to search for")
    result = []
    titleSearch = input()
    for item in games_list:
        if search(titleSearch.casefold(), item.name.casefold()):
            result.append(item)
    return result


@bp.route('/name/<name>', methods=['GET', 'POST'])
def select_game(name):
    result = []
    title = name
    api_data = get_api_data()
    # name = request.form.get('name')
    headings = ('Title', 'Platform', 'Year', 'Genre', 'Publisher', 'Sales(mil)')
    for item in api_data:
        if item.name == title:
            result.append(item)
    return render_template('home/name.html', headings=headings, data=result)


def get_genre(games_list):
    genre = []
    for item in games_list:
        if item.genre not in genre:
         genre.append(item.genre)
    return genre

def sales_platform(result):
    sales = []
    regionSales = []
    totalSales = 0
    naSalesTotal = 0
    euSales = 0
    jpSales = 0
    otherSales = 0
    globalSales = 0
    for item in result:
        totalSales = totalSales + item.globalSales
        naSalesTotal = naSalesTotal + item.naSales
        sales.append({item.platform, item.globalSales})
        regionSales.append({item.platform,item.naSales})
        


def get_platform(games_list):
    console = []
    for item in games_list:
        if item.platform not in console:
            console.append(item.platform)
    return console


@bp.route('/consoles', methods=['GET', 'POST'])
def sales_by_console():
    games_list = get_api_data()
    console_list = get_platform(games_list)
    consoleData = []
    for console in console_list:
        totalnasales = 0
        totaleusales = 0
        totaljpsales = 0
        totalothersales = 0
        totalGlobalSales = 0
        for game in games_list:
            if game.platform == console:
                totalnasales += game.naSales
                totaleusales += game.euSales
                totaljpsales += game.jpSales
                totalothersales += game.otherSales
                totalGlobalSales += game.globalSales
        consoleData.append({'console' : console, 'naSales': round(totalnasales,2), 'euSales': round(totaleusales,2),
                            'jpSales': round(totaljpsales,2), 'otherSales': round(totalothersales,2), 'globalSales': round(totalGlobalSales,2)})

    # consoleSales = json.dumps(consoleData)
    headings = ('Console Name', 'North American Sales', 'European Sales', 'Japanese Sales', 'ROW Sales', 'Global Sales')
    return render_template('home/consoles.html', headings=headings, data=consoleData)

    # return consoleSales


def sales_by_genre(genre_list, games_list):
    genreSales = []
    for genre in genre_list:
        totalnasales = 0
        totaleusales = 0
        totaljpsales = 0
        totalothersales = 0
        for game in games_list:
            if game.genre == genre:
                totalnasales += game.naSales
                totaleusales += game.euSales
                totaljpsales += game.jpSales
                totalothersales += game.otherSales
        genreSales.append(
            {'Genre' : genre, 'naSales': totalnasales, 'euSales': totaleusales, 'jpSales': totaljpsales, 'otherSales': totalothersales})

    return genreSales