import requests
from datetime import datetime, timedelta
import csv
r = requests.get("https://lichess.org/api/player/top/5/classical")
player_users = []

dt = datetime.now() - timedelta(29)
csv_data = []
headers = ["username"]
for i in range(30):
	nedt = dt + timedelta(i)
	headers.append(f"{nedt.year}-{nedt.month}-{nedt.day}")
csv_data.append(headers)
print(dt.year, dt.day, dt.month)

for itm in r.json()["users"]:
	username = itm["username"]
	data = requests.get(f"https://lichess.org/api/user/{username}/rating-history")
	hist_data = data.json()
	ratings_d = {}
	for game in hist_data:
		if game["name"] == "Classical":
			for rating in game["points"]:
				if (rating[0] >= dt.year and rating[1] >= (dt.month - 1) and rating[2] >= dt.day) or ((rating[0] >= dt.year and rating[1] >= dt.month)):
					ratings_d[(rating[0], rating[1], rating[2])] = rating[3]
	time_correct_ratings = [username]
	for i in range(30):
		nedt = dt + timedelta(i)
		o = ratings_d.get((nedt.year, nedt.month - 1, nedt.day))
		if o:
			time_correct_ratings.append(o)
		else:
			time_correct_ratings.append(None)

	csv_data.append(time_correct_ratings)
	player_users.append(itm["username"])

with open("out.csv", "w+") as f:
	writer = csv.writer(f)
	writer.writerows(csv_data)


