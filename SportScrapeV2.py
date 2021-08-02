import requests
import json
from prettytable import PrettyTable


scoreboardPage = requests.get('https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard')
standingsPage = requests.get('https://site.api.espn.com/apis/v2/sports/baseball/mlb/standings')
standingsDict = json.loads(standingsPage.text)
scoreboardDict = json.loads(scoreboardPage.text)


def teamMatches():
    count = 0
    list_dict = {}
    for i in range(len(scoreboardDict['events'])):
        list_dict.setdefault(i, [])
        list_dict[i].append('Name: ' + scoreboardDict['events'][i]['name']) #name
        list_dict[i].append(scoreboardDict['events'][i]['competitions'][0]['status']['type']['detail'])
        if 'weather' in scoreboardDict['events'][i]:
            list_dict[i].append('Weather: ' + scoreboardDict['events'][i]['weather']['displayValue']) #weather
            list_dict[i].append('Temperature: ' + str(scoreboardDict['events'][i]['weather']['temperature'])) #temperature
        list_dict[i].append('Event Suspended: ' + str(scoreboardDict['events'][i]['competitions'][0]['wasSuspended'])) #event suspended
        list_dict[i].append('Indoor: ' + str(s`coreboardDict['events'][i]['competitions'][0]['venue']['indoor'])) #indoor/outdoor
        list_dict[i].append('State: ' + scoreboardDict['events'][i]['status']['type']['state']) #state
        count += 1
    return list_dict

def probable_pitchers():
    pitcher_list = {}
    for i in range(len(scoreboardDict['events'])):
        if 'probables' in scoreboardDict['events'][i]['competitions'][0]['competitors'][0]:
            home_pitcher_name = scoreboardDict['events'][i]['competitions'][0]['competitors'][0]['probables'][0]['athlete']['displayName']
            home_pitcher_id = scoreboardDict['events'][i]['competitions'][0]['competitors'][0]['probables'][0]['athlete']['id']
            away_pitcher_name = scoreboardDict['events'][i]['competitions'][0]['competitors'][1]['probables'][0]['athlete']['displayName']
            away_pitcher_away = scoreboardDict['events'][i]['competitions'][0]['competitors'][1]['probables'][0]['athlete']['id']
            pitcher_list.setdefault(i, [])
            pitcher_list[i].append('Probable Home Pitcher: ' + home_pitcher_name)
            pitcher_list[i].append('Probable Away Pitcher: ' + away_pitcher_name)
        else:
            pitcher_list.setdefault(i, [])
            pitcher_list[i].append('no data')
    return pitcher_list


def tableKeys():
    statName = []
    for x in range(len(standingsDict['children'][0]['standings']['entries'][0]['stats'])):
        if standingsDict['children'][0]['standings']['entries'][0]['stats'][x]['type'] not in statName:
            statName.append(standingsDict['children'][0]['standings']['entries'][1]['stats'][x]['type'])
    return statName


def makeTable(team):
    table = PrettyTable()
    master = {}
    playoffTeam = team.split()
    currentT1 = []
    currentT2 = []
    for i in range(len(standingsDict['children'][0]['standings']['entries'])): #American League
        if playoffTeam[0] == standingsDict['children'][0]['standings']['entries'][i]['team']['abbreviation']:
            for x in range(len(standingsDict['children'][0]['standings']['entries'][i]['stats'])):
                currentT1.append(standingsDict['children'][0]['standings']['entries'][i]['stats'][x]['displayValue'])
        if playoffTeam[1] == standingsDict['children'][0]['standings']['entries'][i]['team']['abbreviation']:
            for x in range(len(standingsDict['children'][0]['standings']['entries'][i]['stats'])):
                currentT2.append(standingsDict['children'][0]['standings']['entries'][i]['stats'][x]['displayValue'])
        else:
            pass
    for i in range(len(standingsDict['children'][1]['standings']['entries'])): #National League
        if playoffTeam[0] == standingsDict['children'][1]['standings']['entries'][i]['team']['abbreviation']:
            for x in range(len(standingsDict['children'][1]['standings']['entries'][i]['stats'])):
                currentT1.append(standingsDict['children'][1]['standings']['entries'][i]['stats'][x]['displayValue'])
        elif playoffTeam[1] == standingsDict['children'][1]['standings']['entries'][i]['team']['abbreviation']:
            for x in range(len(standingsDict['children'][1]['standings']['entries'][i]['stats'])):
                currentT2.append(standingsDict['children'][1]['standings']['entries'][i]['stats'][x]['displayValue'])
        else:
            pass

    master[playoffTeam[0]] = currentT1
    master[playoffTeam[1]] = currentT2
    keys = tableKeys()
    table.add_column('keys', keys)
    count = 0
    for entry in master:
        table.add_column(entry, master[entry])
    print(table)

#def team_roster():


def main():
    matches = teamMatches()
    pitchers = probable_pitchers()
    shortNames = []
    count = 0
    for i in range(len(scoreboardDict['events'])):
        shortNames.append(scoreboardDict['events'][i]['shortName'])
    shortNames = [s.replace('@', '') for s in shortNames]
    for team in shortNames:
        print(matches[count])
        print(pitchers[count])
        makeTable(team)
        count += 1
    print('Number of games today: ', count )

main()