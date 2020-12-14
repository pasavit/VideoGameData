pass
# import json
# import requests
#
#
# from types import SimpleNamespace
#
#
# api_request = requests.get('https://api.dccresource.com/api/games')
#
# def request_list_games():
#     response = api_request
#     game_data = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
#     list_games = list(filter(lambda g: str(g.year) == '2013', game_data))
#     return list_games
#
#
# print(request_list_games())




