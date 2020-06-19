from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017")

db = client.ipl
matchesCollection = db.matches

# matchData = []
matchData = list(matchesCollection.find({'$or': [{'team1': 'Mumbai Indians'}, {'team2': 'Mumbai Indians'}]
                                         }))

result = {}
count = 0
total = 0
for match in matchData:
    print(count, "-------------------------------------")
    count += 1
    print(match)
print(len(matchData))
