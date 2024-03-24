import sys
import csv
import math
import random
from copy import deepcopy
from itertools import permutations


# All Utility functions

def custom_sort_key(item):
    return tuple(item.split(','))

def rotateThresholds(possibilities):
	length = len(possibilities)

	for perm in permutations(possibilities, length):
		if perm not in seen_combinations:
			seen_combinations.append(perm)
			return perm


def distribute_teams(entry, tnum, tsize):
	teams = ["" for j in range(0, tnum)]
	for i in range(0, tnum):
		team = []
		for t in range(0, tsize):
			team.append(entry[0])
			entry.pop(0)
		teams[i] = team
	return teams

def check_mid_differences(array, threshold):
	if max(array) - min(array) > threshold:
		return 1
	return 0

def check_distribution(curTeam, fieldCol):
	score = ["" for j in range(0, len(curTeam))]
	for i, team_list in enumerate(curTeam):
		sums = 0
		for team in team_list:
			sums += int(team[fieldCol])
		score[i] = sums
	return score

def check_limiters(curTeam):
	position = 0
	limiter = []
	for col in range(0, rowLen):
		limiter.append(check_mid_differences(check_distribution(curTeam, col), thresholds[col]))
	return limiter

def check_final_differences(thresholdArray):
	for i in range(0, len(thresholdArray)):
		if thresholdArray[i] > thresholds[i]:
			return 1
	return 0

# End of Utility functions


args = sys.argv

if len(args) != 3:
	print("Usage: python3 customSort.py [inputFileName].csv [intendedTeamSize]")
	sys.exit(1)

teamSize = int(args[2])

with open(args[1], newline='') as infile:
	input = csv.reader(infile)
	inputData = [row[1:] for row in input]
	inputSize = sum(1 for row in inputData)
	transposed = zip(*inputData)
	rowLen =  sum(1 for row in transposed)

if inputSize % teamSize != 0:
	print("Optimum sort option not available for the provided set and option")
	sys.exit(1)

copy = deepcopy(inputData)
seen = []

for entry in copy:
	count = copy.count(entry)
	if count == inputSize // teamSize and entry not in seen:
		seen.append(entry)
trimmed = [x for x in copy if x not in seen]
random.shuffle(trimmed)
trimmedSize = sum(1 for row in trimmed)

startThresholds = []

for i in range (0, rowLen):
	sums = 0
	for row in trimmed:
		sums += int(row[i])
	startThresholds.append(math.floor(sums % (teamSize - len(seen))))

seen_combinations = []
thresholds = rotateThresholds(startThresholds)
allPerms = list(permutations(trimmed))
valid_permutations = []
seenSets = []

for perm in allPerms:
	valid = False
	newTeamSet = []
	i = 0
	while i < len(perm):
		newTeam = []
		while len(newTeam) < (trimmedSize // (teamSize - len(seen))):
			newTeam.append(perm[i])
			i += 1
		newTeam = sorted(newTeam, key=lambda x: x[0], reverse=True)
		newTeamSet.append(newTeam)
	if newTeamSet not in seenSets:
		seenSets.append(newTeamSet)
		valid = True
	if valid:
		valid_permutations.append(perm)
		teams = distribute_teams(list(perm), (trimmedSize // (teamSize - len(seen))), teamSize - len(seen))
		if not check_final_differences(check_limiters(teams)):
			break
		teams.clear()

with open(args[1], newline='') as infile:
	input = csv.reader(infile)
	inputCopy = [row[:] for row in input]

finalTeams = []
i = 0
for t in range(0, inputSize // teamSize):
	for s in seen:
		for j, name in enumerate(inputCopy):
			if s == name[1:]:
				finalTeams.append(name)
				inputCopy.pop(j)
				break
	for f in range(0, teamSize):
		for j, name in enumerate(inputCopy):
			if perm[i] == name[1:]:
				finalTeams.append(name)
				inputCopy.pop(j)
				break
		i += 1

print(distribute_teams(finalTeams, inputSize // teamSize, teamSize))
