import csv
import random

MINIMUM_TEAM_SIZE = 2
MAXIMUM_TEAM_SIZE = 4

if not MINIMUM_TEAM_SIZE or not MAXIMUM_TEAM_SIZE or MINIMUM_TEAM_SIZE > MAXIMUM_TEAM_SIZE:
    print("Wrong team size specification")
    exit()

names = []
with open('names.txt') as f:
    names = f.read().splitlines()
if not names:
    print("No names specified")
    exit()
random.shuffle(names)

total_names = len(names)
if MINIMUM_TEAM_SIZE > len(names):
    print("Team sizes are too large or there are too few names")
    exit()

print(f"Total:\t{total_names} names")
print(f"Sizes:\t{MINIMUM_TEAM_SIZE}-{MAXIMUM_TEAM_SIZE} people")

def distribute_teams(names):
    team_sizes = list(range(MAXIMUM_TEAM_SIZE, MINIMUM_TEAM_SIZE - 1, -1))
    teams = {size: [] for size in team_sizes}
    for size in team_sizes:
        while names and len(names) >= size:
            team = [names.pop() for _ in range(size)]
            teams[size].append(team)
    for name in names:
        smallest_team_size = min(teams.keys())
        teams[smallest_team_size].append([name])
    return teams

teams = distribute_teams(names)

if names:
    print(f"\nTeams have been generated but there are players left.\nRemaining names: {names}")
else:
    print(f"\nAll names have been successfully distributed")

with open('teams.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['Team', 'Size', '1', '2', '3', '4'])
    index = 1
    for size, team_list in teams.items():
        for i, team in enumerate(team_list, start=1):
            writer.writerow([f'{index}', len(team), *team])
            index += 1

    if names:
        writer.writerow(['Remaining names', '', *names])
