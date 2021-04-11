from datetime import datetime as dt

AUTHOR_NAME = 'epicmindwarp'

URL_API_F1 = 'https://fantasy-api.formula1.com/partner_games/f1/players'



def get_json_data():

    import json
    import urllib.request
    
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
        print(table_team)
        return table_team
    else:
        print('\t### No team data found!')
        return False



def reddit_login():

    import praw

    # File with dictionary with creds
    import config

    print('Connecting to reddit...')

    client_id       = config.reddit_ccb['client_id']
    client_secret   = config.reddit_ccb['client_secret']
    username        = config.reddit_ccb['username']
    password        = config.reddit_ccb['password']

    try:
        reddit = praw.Reddit(   client_id= client_id,
                                client_secret= client_secret,
                                user_agent=f'/r/FantasyF1 Price Changes Bot - v0.1, by /u/{AUTHOR_NAME}',
                                username=username,
                                password=password)

    except Exception as e:
        print(f'\t### ERROR - Could not login to reddit\n\t{e}')
        return False

    # Ensure it's usable
    if not reddit.read_only:
        print(f'Logged in as: {reddit.user.me()}')
        return reddit
    else:
        print('\t### Error - a usable reddit object was not returned!')
        return False


def submit_to_sub(as_at_date, header, table_player, table_team, footer):

    r = reddit_login()

    if not r:
        return False

    subreddit_name = 'fantasyf1'

    # Prepare post contents
    title = f'{as_at_date} - Latest Prices and Changes'
    selftext = header + table_player + table_team + footer

    # Submit the post
    new_post = r.subreddit(subreddit_name).submit(title, selftext=selftext, send_replies=False)

    # Always place at top
    new_post.mod.distinguish(how='yes', sticky=True)

    # Set the flair to Price changes
    new_post.mod.flair(text="Price Changes", flair_template_id="377b8eec-bb89-11ea-b523-0ef7de3e98b9")

    # Confirmation output
    print(f'\t#{dt.now().strftime("%Y-%m-%d %H:%M:%S")} - Succesfully posted: {title} at ')


#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------

def get_latest_prices():

    as_at_date = dt.now().strftime('%Y-%m-%d')

    data_players, data_teams = get_json_data()

    table_player = get_player_data(data_players=data_players)

    table_team = get_team_data(data_teams=data_teams)

    # Add footer
    header = f'Prices as at {dt.now().strftime("%Y-%m-%d %H:%M:%S")} (UK Time)\n'
    footer = f'\nSource: formula1.com'

    # Upload to the subreddit
    submit_to_sub(as_at_date, header, table_player, table_team, footer)



if __name__ == '__main__':

    try:
        get_latest_prices()
    except Exception as e:

        import os
        
        if os.name == 'nt':
            raise
        else:
            print(f'\t### ERROR - ABORTED - {e}')