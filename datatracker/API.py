import json
import requests


from types import SimpleNamespace
from re import search
from flask import Flask, jsonify, request, redirect, flash, render_template, url_for, Blueprint
from flask_bootstrap import Bootstrap
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


def filter_by_title():
    api_data = get_api_data()
    title = input()
    list_games = []
    for item in api_data:
        if search(title.casefold(), item.name.casefold()):
            list_games.append(item)
    headings = ('Title', 'Platform', 'Year', 'Genre', 'Publisher', 'Sales(mil)')
    return render_template('home/index.html', headings=headings, data=list_games)


def find_games(games_list):
    print("please enter a title to search for")
    result = []
    titleSearch = input()
    for item in games_list:
        if search(titleSearch.casefold(), item.name.casefold()):
            result.append(item)
    return result

def select_game(games_list, name):
    result = []
    for item in games_list:
        if item.name == name:
            result.append(item)
    return result


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