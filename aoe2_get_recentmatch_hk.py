import urllib.request as urlimport
import pandas as pd
from datetime import datetime, time
from colorama import Style
from colorama import Fore

win_time_period = {'Morning': 0, 'Afternoon': 0, 'Night': 0}
lose_time_period = {'Morning': 0, 'Afternoon': 0, 'Night': 0}

def check_win_time(hour):
    if(12 >= hour and hour >= 6):
        #print('Morning')
        win_time_period['Morning'] += 1
    elif(18 >= hour and hour >= 13):
        #print('Afternoon')
        win_time_period['Afternoon'] += 1
    else:    
        #print('Night')
        win_time_period['Night'] += 1
def check_lose_time(hour):
    if(12 >= hour and hour >= 6):
        #print('Morning')
        lose_time_period['Morning'] += 1
    elif(18 >= hour and hour >= 13):
        #print('Afternoon')
        lose_time_period['Afternoon'] += 1
    else:    
        #print('Night')
        lose_time_period['Night'] += 1

api_url = "https://aoe2.net/api/player/ratinghistory?game=aoe2de&leaderboard_id=3&steam_id=76561198324387591&count=200"
with urlimport.urlopen(api_url) as url:
    match_history = url.read().decode()
    #Get pd json
    df = pd.DataFrame(eval(match_history))
    #Get datetime
    d = pd.to_datetime(df['timestamp'], unit='s')
    hktime = d.dt.tz_localize("GMT").dt.tz_convert('Hongkong').dt.tz_localize(None)
    #calcuate win/or/lose
    lose, win, draw = 0, 0, 0
    previous_elo = 0
    for m, d in zip(df['rating'], df['timestamp']):
        current_elo = m
        normaltime = pd.to_datetime(d, unit='s')
        hktime = normaltime.tz_localize("GMT").tz_convert('Hongkong').tz_localize(None)
        if(current_elo > previous_elo):
            print(f"LOSE {current_elo} -> {previous_elo}, {hktime} ")
            lose += 1
            previous_elo = m
            check_lose_time(hktime.hour)

        elif (current_elo == previous_elo):
            print(f"DRAW {current_elo} -> {previous_elo}, {hktime}")
            draw += 1
            previous_elo = m
        else :
            print(f'WIN {current_elo} -> {previous_elo}, {hktime}')
            win += 1
            previous_elo = m
            check_win_time(hktime.hour)
    #print Win / Lose / Draw Data
    print(f"win: {win}, lose: {lose}, draw: {draw}")
    print(f"{Fore.GREEN}WIN~~~Morning: {win_time_period['Morning']}, Afternoon:{win_time_period['Afternoon']}, Night: {win_time_period['Night']}{Style.RESET_ALL}")
    print(f"{Fore.RED}LOSE~~~Morning: {lose_time_period['Morning']}, Afternoon:{lose_time_period['Afternoon']}, Night: {lose_time_period['Night']}{Style.RESET_ALL}")
        