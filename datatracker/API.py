import json
import requests
from types import SimpleNamespace
from re import search

class API:
    def __init__(self):
        self.api_request = requests.get('https://api.dccresource.com/api/games')

    def request_list_games(self, api_request):
        response = api_request
        game_data = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
        list_games = list(filter(lambda g: str(g.year) == '2013', game_data))
        return list_games

    def find_game(self, games_list):
        print("please enter a title to search for")
        result = []
        titleSearch = input()
        for item in games_list:
            if search(titleSearch.casefold(), item.name.casefold()):
                result.append(item)
        return result

    def sales_platform(self, result):
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
