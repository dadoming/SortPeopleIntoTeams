import csv
import random

MINIMUM_TEAM_SIZE = 4
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


# Begin of Added features
saveNames = []
divisor = ','
i = 0
fullLen = 0

header = names[0].split(divisor)
tolerances = names[len(names) - 1].split(divisor)
names.pop(0)
names.pop()

for element in names:
	saveNames.append(element)
	value = element.split(divisor)
	if len(value) > fullLen:
		fullLen = len(value)

vals = [[0] * fullLen for _ in range(len(names))]

i = 0
for element in names:
	vals[i] = element.split(divisor)
	i += 1
# End of added features


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


# Begin of Added features

def check_differences(iter, array, threshold):
	differences = []
	dict_values = {}

	for size, arr in array.items():
		for i, team in enumerate(arr):
			dict_values[size] = team

	for i in dict_values:
		for j in dict_values:
			if i < j and abs(dict_values[i] - dict_values[j]) > threshold:
				return 1
	return 0

def check_distribution(teams, fieldCol, threshold, exact):
	score = {}
	k = 0
	for size, team_list in teams.items():
		for i, team in enumerate(team_list, start=0):
			score[k] = set()
			j = 0
			sum = 0
			while j < len(team):
				values = team[j].split()
				val = values[0]
				for iter in vals:
					if val[0] == iter[0]:
						if not exact:
							sum += int(iter[fieldCol])
						else:
							if exact == int(iter[fieldCol]):
								sum += 1
				j += 1
			score[k].add(sum)
			k += 1
	return score

def remove_quotes(string):
    return string.replace('"', '').replace("'", '')

def get_tolerance(limitType):
	head = []
	tol = []
	limit = 0
	j = 1
	while (j < len(header)):
		if (header[j].find(limitType) == -1):
			j += 1
			continue
		if header[j].find("|") != -1:
			head = header[j].split('|')
			tol = tolerances[j].split('|')
			f = 0
			while f < len(head) and remove_quotes(str(head[f])) != remove_quotes(str(limitType)):
				f += 1
			limit = int(tol[f])
		else:
			limit = int(tolerances[j])
		j += 1
	return limit

def check_limiters(limiter, limitType, tolerance):
	j = 0
	position = 0
	while (j < len(header)):
		position = header[j].find(limitType, position)
		limit = 0
		if (position != -1):
			limiter[j] = set()
			if limitType == "RANGE":
				limiter[j] = check_distribution(teams, j, tolerance, 0)
			elif limitType == "FLAG":
				limiter[j].add(check_differences(j, check_distribution(teams, j, tolerance, 0), tolerance))
			else:
				k = 0
				sum = 0
				while(k <= 6):
					sum += check_differences(j, check_distribution(teams, j, tolerance, 0), tolerance)
					k += 1
				limiter[j].add(sum)
		else:
			position = 0
		j += 1
	return limiter

def check_values(array, tolerance, flag):
	differences = []
	dict_values = {}

	for size, arr in array.items():
		for i, team in enumerate(arr):
			dict_values[size] = team
			
	for j in dict_values:
		if flag:
			for i in dict_values:
				if i < j and abs(dict_values[i] - dict_values[j]) >= tolerance:
					return 1
		else:
			if dict_values[j] > tolerance:
				return 1
	return 0


j = 0
position = 0
ranges = {}
flags = {}
values = {}

ranges = check_limiters(ranges, "RANGE", get_tolerance("RANGE"))
flags = check_limiters(flags, "FLAG", get_tolerance("FLAG"))
values = check_limiters(values, "VALUES", get_tolerance("VALUES"))

while (check_values(ranges, get_tolerance("RANGE"), 1) or check_values(flags, get_tolerance("FLAG"), 0) or check_values(values, get_tolerance("VALUES"), 0)):
	for element in saveNames:
		names.append(element)
	teams.clear()
	random.shuffle(names)
	teams = distribute_teams(names)
	ranges.clear()
	flags.clear()
	values.clear()
	ranges = check_limiters(ranges, "RANGE", get_tolerance("RANGE"))
	flags = check_limiters(flags, "FLAG", get_tolerance("FLAG"))
	values = check_limiters(values, "VALUES", get_tolerance("VALUES"))

print(teams)
# End of Added features


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