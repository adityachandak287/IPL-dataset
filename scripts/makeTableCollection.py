from pymongo import MongoClient
import json
client = MongoClient("mongodb://localhost:27017")

db = client.ipl
matchesCollection = db.matches

matchData = list(matchesCollection.find())

result = {}
seasonFirstMatchId = {}
seasonMatchTotal = {
    '2008': 58,
    '2009': 57,
    '2010': 60,
    '2011': 73,
    '2012': 74,
    '2013': 76,
    '2014': 60,
    '2015': 59,
    '2016': 60
}
for match in matchData:
    season = str(match['season'])
    if season not in result:
        result[season] = {}
        seasonFirstMatchId[season] = match['id']

    team1 = match['team1']
    team2 = match['team2']

    defaultTeamObject = {
        'points': 0,
        'wins': 0,
        'losses': 0,
        'matches': 0
    }
    if team1 not in result[season]:
        result[season][team1] = defaultTeamObject.copy()
    if team2 not in result[season]:
        result[season][team2] = defaultTeamObject.copy()

    # matchId = int(match['id']) - int(seasonFirstMatchId[season]) + 1
    # if matchId <= (seasonMatchTotal[season]-4):
    if match['result'] == 'normal':
        if team1 == match['winner']:
            result[season][team1]['wins'] += 1
            result[season][team1]['points'] += 2

            result[season][team2]['losses'] += 1
        elif team2 == match['winner']:
            result[season][team2]['wins'] += 1
            result[season][team2]['points'] += 2

            result[season][team1]['losses'] += 1
    elif match['result'] in ['tie', 'no result']:
        result[season][team1]['points'] += 1
        result[season][team2]['points'] += 1

    result[season][team1]['matches'] += 1
    result[season][team2]['matches'] += 1

tempSeason = {}


resultList = {}
for season in result:
    resultList[str(season)] = []
    for team in result[season]:
        tempTeam = result[season][team].copy()
        tempTeam['team'] = team
        resultList[season].append(tempTeam)


def getKey(team):
    return team['points']


tableList = []
for season in resultList:
    print(season, "-----------------")
    tempSeason = resultList[season].copy()
    tempSeason.sort(key=getKey, reverse=True)
    resultList[season] = tempSeason.copy()
    tableList.append({
        'season': season,
        'table': tempSeason
    })
    # for team in resultList[season]:
    #     tempRecord = team.copy()
    #     tempRecord['season'] = int(season)
    #     tableList.append(tempRecord)

for record in tableList:
    print(record)
print(len(tableList))


print(db.tables.insert(tableList))


'''
table {
    '2018' : [
        'rank' : {
            'team' : 'Mumbai Indians',
            'points' : ,
            'wins' : ,
            'losses' : ,
            'matches':
        }
    ]
}

result:
normal
tie
no result
'''
