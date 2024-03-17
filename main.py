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

for element in names:
	saveNames.append(element)
	value = element.split(divisor)
	if len(value) > fullLen:
		fullLen = len(value)
# End of added features

random.shuffle(names)
random.shuffle(saveNames)

total_names = len(names)
if MINIMUM_TEAM_SIZE > len(names):
	print("Team sizes are too large or there are too few names")
	exit()

print(f"Total:\t{total_names} names")
print(f"Sizes:\t{MINIMUM_TEAM_SIZE}-{MAXIMUM_TEAM_SIZE} people")

def distribute_teams(names, newSize):	
	if newSize == 0:
		team_sizes = list(range(MAXIMUM_TEAM_SIZE, MINIMUM_TEAM_SIZE - 1, -1))
	else:
		team_sizes = list(range(newSize, newSize - 1, -1))
	teams = {size: [] for size in team_sizes}
	for size in team_sizes:
		while len(names) >= size:
			team = [names.pop() for _ in range(size)]
			teams[size].append(team)
	for name in names:
		smallest_team_size = min(teams.keys())
		teams[smallest_team_size].append([name])
	return teams


teams = distribute_teams(names, 0)


# Begin of Added features

# Main Sort Utilities

def custom_sort_key(item):
    return tuple(item.split(','))

def trim_set(listing, seen):
	newListing = sorted(listing, key=lambda x: x[0], reverse=True)
	finalListing = []
	i = 0
	for entry in newListing:
		count = newListing.count(entry)
		if count == math.ceil(len(listing) // MAXIMUM_TEAM_SIZE) and entry not in seen:
			seen.add(entry)
		i += 1
	finalListing = [x for x in newListing if x not in seen]
	random.shuffle(finalListing)
	return finalListing


#Getting All Differences

def check_limiters(team, tolerance):
	j = 1
	position = 0
	limiter = []
	while (j < len(header)):
		limiter.append(check_mid_differences(check_distribution(team, j - 1), tolerance[j - 1]))
		j += 1
	return limiter

def check_distribution(teams, fieldCol):
	score = []
	k = 0
	listing = []
	for name in saveNames:
		sname = name.find(',')
		if sname != -1:
			sname += 1
			listing.append(name[sname:])
	for size, team_list in teams.items():
		for i, team in enumerate(team_list, start=0):
			j = 0
			sums = 0
			while j < len(team):
				val = team[j]
				f = 0
				for iters in listing:
					if iters == val:
						iteration = iters.split(divisor)
						sums += int(iteration[fieldCol])
						listing.pop(f)
						break
					f += 1
				j += 1
			score.append(sums)
			k += 1
	return score


# Check Differences

def check_mid_differences(array, threshold):
	if max(array) - min(array) > threshold:
		return 1
	return 0

def check_final_differences(array, tolerance):
	i = 0
	while i < len(array):
		if array[i] > tolerance[i]:
			return 1
		i += 1
	return 0


# Tolerance Management

def init_tolerances(listing, sizes):
	tol = []
	j = 0
	f = 0
	sums = 0
	while j < len(header) - 1:
		sums = 0
		for name in listing:
			sname = name.split(',')
			sums += int(sname[j])
		j += 1
		sums = (sums % sizes)
		tol.append(math.floor(sums))
	return tol

def get_diff_tolerances(possibilities):
	length = len(possibilities)

	for perm in permutations(possibilities, length):
		if perm not in seen_combinations:
			seen_combinations.add(perm)
			return perm

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

def updateTolerances():
	curTol = []
	curTol = get_diff_tolerances(tolerances)
	if curTol == None:
		icr_tolerances(tolerances)
		curTol = get_diff_tolerances(tolerances)
	return curTol

seen_combinations = set()



# Main Sorting Function

def gen_result(perm, allSet, teamSizes, seenElements):
	team = {}
	allNames = []
	finalTeam = []
	t = 0
	i = 0
	for name in allSet:
		allNames.append(name)
	maxSize = len(allNames) // MAXIMUM_TEAM_SIZE

	while t < maxSize:
		for s in seenElements:
			j = 0
			for name in allNames:
				sname = name.find(',')
				if sname != -1:
					sname += 1
					if s == name[sname:]:
						finalTeam.append(name)
						allNames.pop(j)
						break
				j += 1
		f = 0
		while f < teamSizes:
			j = 0
			for name in allNames:
				sname = name.find(',')
				if sname != -1:
					sname += 1
					if perm[i] == name[sname:]:
						finalTeam.append(name)
						allNames.pop(j)
						break
				j += 1
			i += 1
			f += 1
		t += 1
	team.clear()
	team = distribute_teams(finalTeam, 0)
	return team

def get_diff_arrangement():
	team = {}
	seen_arrangements = set()
	seenElements = set()
	newList = []
	newNames = []
	allNames = []

	for name in saveNames:
		allNames.append(name)
		sname = name.find(',')
		if sname != -1:
			newNames.append(name[:sname])
			sname += 1
			newList.append(name[sname:])
	newList = trim_set(newList, seenElements)

	teamSizes = len(newList) // (MAXIMUM_TEAM_SIZE - len(seenElements))
	tolerances = init_tolerances(newList, teamSizes)
	curTol = get_diff_tolerances(tolerances)

	allPerm = permutations(newList)
	valid_permutations = []
	seenSets = set()
	for perm in allPerm:
		valid = False
		i = 0
		newTeamSet = []
		while i < len(perm):
			sums = 0
			newTeam = []
			while len(newTeam) < teamSizes:
				newTeam.append(perm[i])
				newTeam = sorted(newTeam, key=custom_sort_key)
				i += 1
			newTeamSet.append(tuple(newTeam))
		if tuple(newTeamSet) not in seenSets:
			seenSets.add(tuple(newTeamSet))
			valid = True
		if valid:
			valid_permutations.append(perm)
			team.clear()
			team = distribute_teams(list(perm), MAXIMUM_TEAM_SIZE - len(seenElements))
			if not check_final_differences(check_limiters(team, curTol), curTol):
				return gen_result(perm, allNames, teamSizes, seenElements)
	curTol = updateTolerances()
	while True:
		print(f"Tolerances: {curTol}")
		seen_arrangements.clear()
		for perm in valid_permutations:
			if perm not in seen_arrangements:
				seen_arrangements.add(perm)
			else:
				continue
			team.clear()
			team = distribute_teams(list(perm), MAXIMUM_TEAM_SIZE - len(seenElements))
			if not check_final_differences(check_limiters(team, curTol), curTol):
				return gen_result(perm, allNames, teamSizes, seenElements)
		curTol = updateTolerances()


if not names:
	teams.clear()
	teams = get_diff_arrangement()

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
