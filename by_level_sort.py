import csv
import random
from os import getenv
from dotenv import load_dotenv
import requests
import time
from pprint import pprint as pp

CAMPUS_ID = 38 # Lisboa
# lisboa = "/v2/campus/{CAMPUS_ID}"

## Insert values based on your needs here ##
MINIMUM_TEAM_SIZE = 2
MAXIMUM_TEAM_SIZE = 4

if (
	not MINIMUM_TEAM_SIZE
	or not MAXIMUM_TEAM_SIZE
	or MINIMUM_TEAM_SIZE > MAXIMUM_TEAM_SIZE
):
	print("Wrong team size specification")
	exit()

load_dotenv()
client_id = getenv("UID_KEY")
client_secret = getenv("SECRET_KEY")

def post42(url, payload):
	url = "https://api.intra.42.fr" + url
	payload = payload
	headers = {"Content-Type": "application/x-www-form-urlencoded"}
	response = requests.request("POST", url, headers=headers, data=payload)
	return response.json()


def get42(url, payload):
	url = "https://api.intra.42.fr" + url
	payload = payload
	headers = {"Content-Type": "application/x-www-form-urlencoded"}
	response = requests.request("GET", url, headers=headers, data=payload)
	return response.json()

wtoken = post42(
	"/oauth/token",
	{
		"grant_type": "client_credentials",
		"client_id": client_id,
		"client_secret": client_secret,
	},
)

if "error" in wtoken:
	print("Error: ", wtoken["error_description"])
	exit()

with open("names_42.txt") as f:
	names = f.read().splitlines()
	if not names:
		print("No names specified")
		exit()

def getUserInfo(username):
	username = f"/v2/users/{username}/quests_users"
	user = get42(username, {"access_token": wtoken["access_token"]})
	# pp(user)
	return user

# Load users
user_dict = {}
for name in names:
	user = getUserInfo(name)
	if user:
		user_dict[name] = 0
	all_slugs = []
	for info in user:
		all_slugs.append(info["quest"]["slug"])
	if all_slugs:
		user_dict[name] = int(max(all_slugs).split("-")[3][1])
	else:
		user_dict[name] = "ERROR"
	time.sleep(1)

pp(user_dict)

# Remove users with no quests
error_usernames = []
for user in user_dict:
	if user_dict[user] == "ERROR":
		print(f"User {user} has no quests")
		error_usernames.append(user)
		del user_dict[user]

total_names = len(user_dict)
print(f"Total:\t{total_names} names")
if MINIMUM_TEAM_SIZE > total_names:
	print("Team sizes are too large or there are too few names")
	exit()
print(f"Sizes:\t{MINIMUM_TEAM_SIZE}-{MAXIMUM_TEAM_SIZE} people")


WEIGHTS = {
	0: 1,
	1: 3,
	2: 6,
	3: 10,
	4: 20,
	5: 25,
	6: 35,
}
def sort_users_by_rank(user_dict):
    sorted_users = sorted(
        user_dict.items(), key=lambda x: x[1]
    )
    return sorted_users

# Sort users by rank
sorted_users = sort_users_by_rank(user_dict)

# Get the total weight of all users
total_sum_of_weights = 0
for user in sorted_users:
	total_sum_of_weights += WEIGHTS[user[1]]

# Calculate the number of teams
number_of_teams = total_names // MAXIMUM_TEAM_SIZE
if total_names % MAXIMUM_TEAM_SIZE:
	number_of_teams += 1

# Calculate the number of users in each team
team_sizes = [MAXIMUM_TEAM_SIZE] * number_of_teams
remaining = total_names % MAXIMUM_TEAM_SIZE
for i in range(remaining):
	team_sizes[i] = MINIMUM_TEAM_SIZE

# Generate teams according to weights and team sizes
teams = []
for size in team_sizes:
	team = []
	while len(team) < size:
		team_weight = 0
		for user in sorted_users:
			if user[0] not in team:
				team_weight += WEIGHTS[user[1]]
		if not team_weight:
			break
		random_number = random.randint(1, team_weight)
		for user in sorted_users:
			if user[0] not in team:
				random_number -= WEIGHTS[user[1]
				]
				if random_number <= 0:
					team.append(user[0])
					break
	for user in team:
		sorted_users.remove((user, user_dict[user]))
	teams.append(team)

if sorted_users:
	for user in sorted_users:
		min_team = min(teams, key=lambda x: len(x))
		min_team_index = teams.index(min_team)
		if len(teams[min_team_index]) < MAXIMUM_TEAM_SIZE:
			teams[min_team_index].append(user[0])

for team in teams:
	for user in team:
		if user in user_dict:
			del user_dict[user]

for i, team in enumerate(teams, 1):
    print(f"Team {i}: {team}")

if user_dict:
    print(
        f"\nTeams have been generated but there are players left.\nRemaining names: {user_dict.keys()}"
    )
else:
    print(f"\nAll names have been successfully distributed")

with open("teams.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(
		["Team", "Size"] + [str(i) for i in range(1, MAXIMUM_TEAM_SIZE + 1)]
	)
    index = 1
    for team in teams:
        writer.writerow([f"{index}", len(team), *team])
        index += 1

    if user_dict:
        writer.writerow(["Remaining names: ", user_dict.keys()])
