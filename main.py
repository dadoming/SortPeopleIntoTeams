import csv
import random

# Begin of Added features
import math
from itertools import permutations
# End of Added features

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
names.pop(0)

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
random.shuffle(saveNames)

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
		while len(names) >= size:
			team = [names.pop() for _ in range(size)]
			teams[size].append(team)
	for name in names:
		smallest_team_size = min(teams.keys())
		teams[smallest_team_size].append([name])
	return teams


teams = distribute_teams(names)


# Begin of Added features

def check_differences(array, threshold, limitType):
	differences = []

	for s, arr in array.items():
		for a in arr:
	 	   differences.append(a)
	if max(differences) - min(differences) > threshold:
		return 1
	return 0

def check_distribution(teams, fieldCol, exact):
	score = {}
	k = 0
	newNames = []
	for name in saveNames:
		newNames.append(name)
	for size, team_list in teams.items():
		for i, team in enumerate(team_list, start=0):
			score[k] = set()
			j = 0
			sums = 0
			while j < len(team):
				value = team[j].split()
				val = value[0]
				f = 0
				for iters in newNames:
					if iters == val:
						iteration = iters.split(divisor)
						if exact == 0:
							sums += int(iteration[fieldCol])
						else:
							if exact == int(iteration[fieldCol]):
								sums += 1
						newNames.pop(f)
					f += 1
				j += 1
			score[k].add(sums)
			k += 1
	return score

def remove_quotes(string):
	return string.replace('"', '').replace("'", '')

def get_diff_tolerances(possibilities):
	length = len(tolerances)

	for perm in permutations(possibilities, length):
		if perm not in seen_combinations:
			seen_combinations.add(perm)
			return perm

def get_diff_arrangement(currentTol):
	team = {}
	while True:
		print(f"Tolerances: {currentTol}")
		for perm in permutations(saveNames, len(saveNames)):
			team.clear()
			team = distribute_teams(list(perm))
			ranges = check_limiters(team, {}, "RANGE", get_tolerance("RANGE"))
			flags = check_limiters(team, {}, "FLAG", get_tolerance("FLAG"))
			values = check_limiters(team, {}, "VALUE", get_tolerance("VALUE"))
			if not check_values(ranges, get_tolerance("RANGE"), "RANGE") and not check_values(flags, get_tolerance("FLAG"), "FLAG") and not check_values(values, get_tolerance("VALUE"), "VALUE"):
				return team
		currentTol = get_diff_tolerances(tolerances)
		if currentTol == None:
			icr_tolerances(tolerances)
			currentTol = get_diff_tolerances(tolerances)



def icr_tolerances(tols):
	j = 0
	i = 0
	newTol = tols
	while True:
		j = 0
		while j < len(tols):
			if newTol[j] == i:
				newTol[j] = i + 1
				return newTol
			j += 1
		i += 1

def init_tolerances():
	head = []
	tol = []
	j = 1
	f = 0
	sums = 0
	while j < len(header):
		sums = 0
		for name in saveNames:
			sname = name.split(',')
			sums += int(sname[j])
		sums = (sums % (math.ceil(len(saveNames) // MAXIMUM_TEAM_SIZE)))
		if header[j].find("RANGE") != -1:
			tol.append(math.floor(sums))
		if header[j].find("VALUE") != -1:
			k = 1
			allsum = []
			while k <= 6:
				sums = 0
				for name in saveNames:
					sname = name.split(',')
					if int(sname[j]) == k:
						sums += 1
				newsum = sums % (math.ceil(len(saveNames) // MAXIMUM_TEAM_SIZE))
				if newsum > 0:
					allsum.append(1)
				k += 1
			t = 0
			tol.append(sum(allsum) % (math.ceil(len(saveNames) // MAXIMUM_TEAM_SIZE)))
		if header[j].find("FLAG") != -1:
			tol.append(math.floor(sums))
		j += 1
	return tol

def get_tolerance(limitType):
	head = []
	limit = 0
	j = 1
	curlim = 0
	while (j < len(header)):
		if header[j].find(limitType) == -1:
			j += 1
			continue
		if header[j].find("|") != -1:
			head = header[j].split('|')
			if (len(head) > 1):
				curlim = len(head) - 1
			f = 0
			while f < len(head) and remove_quotes(str(head[f])) != remove_quotes(str(limitType)):
				f += 1
			limit = int(currentTol[f])
		else:
			limit = int(currentTol[j - 1 + curlim])
		j += 1
	return limit

def check_limiters(team, limiter, limitType, tolerance):
	j = 1
	position = 0
	while (j < len(header)):
		position = header[j].find(limitType, position)
		limit = 0
		if (position != -1):
			limiter[j] = set()
			if limitType == "RANGE":
				limiter[j] = check_distribution(team, j, 0)
			elif limitType == "FLAG":
				limiter[j].add(check_differences(check_distribution(team, j, 0), tolerance, limitType))
			else:
				k = 1
				sums = 0
				while(k <= 6):
					sums = check_differences(check_distribution(team, j, k), tolerance, limitType)
					k += 1
				limiter[j].add(sums)
		else:
			position = 0
		j += 1
	return limiter

def check_values(teams, tolerance, limitType):
	array = []

	for key, inner_dict in teams.items():
		if (limitType == "RANGE"):
			for inner_key, set_value in inner_dict.items():
				for v in set_value:
					array.append(v)
		else:
			for set_value in inner_dict:
				array.append(set_value)
	if len(array) > 1 and limitType == "RANGE":
		if max(array) - min(array) > tolerance:
			return 1
	else:
		for f in array:
			if f > tolerance:
				return 1
	return 0


j = 0
position = 0
arrange = 0

seen_combinations = set()
tolerances = init_tolerances()
currentTol = get_diff_tolerances(tolerances)

if not names:
	teams.clear()
	teams = get_diff_arrangement(currentTol)

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
