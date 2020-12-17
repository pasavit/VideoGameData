import json
import requests

from types import SimpleNamespace
from re import search
from flask import Flask, jsonify, request, redirect, flash, render_template, url_for, Blueprint
bp = Blueprint('home', __name__)


@bp.route('/test')
def test():
    return "All good!"


@bp.route('/us')
def us():
    return render_template('home/us.html')


def get_api_data():
    api_request = requests.get('https://api.dccresource.com/api/games')
    api_data = json.loads(api_request.content, object_hook=lambda d: SimpleNamespace(**d))
    return api_data


def get_new_data():
    api_request = requests.get('https://api.dccresource.com/api/games')
    api_data = json.loads(api_request.content, object_hook=lambda d: SimpleNamespace(**d))
    list_games = list(filter(lambda d: str(d.year) == '2013' or str(d.year) == '2014' or str(d.year) == '2015' or str(d.year) == '2016' or str(d.year) == '2017', api_data))
    return list_games


@bp.route('/home')
def populate_game_chart():
    api_data = get_api_data()
    list_games = list(filter(lambda g: str(g.year) == '2017', api_data))
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


@bp.route('/name/<name>', methods=['GET', 'POST'])
def select_game(name):
    result = []
    label = []
    series = []
    title = name
    api_data = get_api_data()
    headings = ('Title', 'Platform', 'Year', 'Genre', 'Publisher', 'Sales(mil)')
    for item in api_data:
        if item.name == title:
            result.append(item)
            label.append(item.platform)
            series.append(item.globalSales)
    return render_template('home/name.html', headings=headings, data=result, series=series, label=label)


@bp.route('/consoles', methods=['GET', 'POST'])
def sales_by_console():
    games_list = get_new_data()
    console_list = get_platform(games_list)
    console_data = []
    x_axis = []
    y_axis = []
    for console in console_list:
        x_axis.append(console)
        total_na_sales = 0
        total_eu_sales = 0
        total_jp_sales = 0
        total_other_sales = 0
        total_global_sales = 0
        for game in games_list:
            if game.platform == console:
                total_na_sales += game.naSales
                total_eu_sales += game.euSales
                total_jp_sales += game.jpSales
                total_other_sales += game.otherSales
                total_global_sales += game.globalSales
        console_data.append({'console': console, 'naSales': round(total_na_sales, 2), 'euSales': round(total_eu_sales, 2), 'jpSales': round(total_jp_sales, 2), 'otherSales': round(total_other_sales, 2), 'globalSales': round(total_global_sales, 2)})
        y_axis.append(round(total_global_sales, 2))
    headings = ('Console', 'NA Sales', 'EU Sales', 'Japan Sales', 'ROW Sales', 'Global Sales')
    return render_template('home/consoles.html', headings=headings, data=console_data, x_axis=x_axis, y_axis=y_axis)


@bp.route('/genres', methods=['GET', 'POST'])
def sales_by_genre():
    games_list = get_api_data()
    genre_list = get_genre(games_list)
    genre_sales = []
    series = []
    for genre in genre_list:
        total_na_sales = 0
        total_eu_sales = 0
        total_jp_sales = 0
        total_other_sales = 0
        total_global_sales = 0
        for game in games_list:
            if game.genre == genre:
                total_na_sales += game.naSales
                total_eu_sales += game.euSales
                total_jp_sales += game.jpSales
                total_other_sales += game.otherSales
                total_global_sales += game.globalSales
        genre_sales.append({'genre': genre, 'naSales': round(total_na_sales, 2), 'euSales': round(total_eu_sales, 2), 'jpSales': round(total_jp_sales, 2), 'otherSales': round(total_other_sales, 2), 'globalSales': round(total_global_sales, 2)})
        series.append([round(total_na_sales, 2),round(total_eu_sales, 2),round(total_jp_sales),round(total_other_sales, 2)])
    headings = ('Genre', 'North American Sales', 'European Sales', 'Japanese Sales', 'ROW Sales', 'Global Sales')
    header = ('North American Sales', 'European Sales', 'Japanese Sales', 'ROW Sales')
    return render_template('home/genres.html', headings=headings, data=genre_sales, genre=genre_list, series=series, header=header)


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
        regionSales.append({item.platform, item.naSales})


def get_platform(games_list):
    console = []
    for item in games_list:
        if item.platform not in console:
            console.append(item.platform)
    return console


def find_games(games_list):
    print("please enter a title to search for")
    result = []
    title_search = input()
    for item in games_list:
        if search(title_search.casefold(), item.name.casefold()):
            result.append(item)
    return result


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

