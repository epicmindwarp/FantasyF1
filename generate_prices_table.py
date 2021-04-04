import json
import urllib.request
from datetime import datetime as dt

URL_API_F1 = 'https://fantasy-api.formula1.com/partner_games/f1/players'


def get_json_data():

    # Read the contents of the URL
    web_page_data = urllib.request.urlopen(URL_API_F1).read()

    # Convert the url data into JSON 
    data_json = json.loads(web_page_data)

    # Sort players by field
    data_players = data_json
    data_teams = data_json
    data_players['players'] = sorted(data_players['players'], key=lambda k: k['price'], reverse=True)
    data_teams['players'] = sorted(data_teams['players'], key=lambda k: k['price'], reverse=True)

    return data_players, data_teams


def get_player_data(data_players):

    # Generates player level data from the JSON output

    # Table title
    table_player = '# Current Driver Prices and Changes\n'

    # Table header
    table_player += 'Driver|Team|Current Price|Weekly Price Change|Chance of Price ↑|Chance of Price ↓\n'

    # Table header seperator
    table_player += '--|--|--|--|--|--|--'

    # Capture the length of the header, for comparison later
    len_header = len(table_player)

    # Get all the player data
    for player in data_players['players']:
        
        if player['position'] == 'Driver':
        
            row_player = player['first_name'] + ' ' + player['last_name'] + '|'
            row_player = row_player + player['team_name'] + '|'
            row_player = row_player + f'{player["price"]}' + '|'
            row_player = row_player + f'{round(player["weekly_price_change"],2)}' + '|'
            row_player = row_player + str(player['current_price_change_info']['probability_price_up_percentage']) + '%' + '|'
            row_player = row_player + str(player['current_price_change_info']['probability_price_down_percentage']) +'%'

            # Add the details to the table in the end
            table_player = table_player + '\n' + row_player

    # If information was added
    if len(table_player) > len_header:
        table_player = table_player + '\n----\n'
        print(table_player)
        return table_player
    else:
        print('\t### No player data found!')
        return False



def get_team_data(data_teams):

    table_team = '# Current Team Prices and Changes\n'
    table_team += 'Team|Current Price|Weekly Price Change|Chance of Price ↑|Chance of Price ↓\n'
    table_team += '--|--|--|--|--|--'

    # Capture the length of the header, for comparison later
    len_header = len(table_team)

    for team in data_teams['players']:

        if team['position'] == 'Constructor':
            
            row_team = team['team_name'] + '|'
            row_team += f'{team["price"]}' + '|'
            row_team += f'{round(team["weekly_price_change"],2)}' + '|'
            row_team += str(team['current_price_change_info']['probability_price_up_percentage'])+'%' + '|'
            row_team += str(team['current_price_change_info']['probability_price_down_percentage'])+'%'

            # Add the details to the table in the end
            table_team += '\n' + row_team

    # If information was added
    if len(table_team) > len_header:
        table_team += f'\nPrices as at {dt.now().strftime("%Y-%m-%d %H:%M:%S")} (UK Time)'
        print(table_team)
        return table_team
    else:
        print('\t### No team data found!')
        return False


#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------

data_players, data_teams = get_json_data()

get_player_data(data_players=data_players)

get_team_data(data_teams=data_teams )