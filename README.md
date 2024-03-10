# Sort People into teams

1. Go into the sort .py file and set the minimum and maximum team sizes.

2. Create a file and put the names of the people you want to sort into teams in it, one name per line.
    - names.txt for random_sort.py (normal names)
    - names_42.txt for by_level_sort.py (sort by 42 rank given usernames)
3. Running the script will create a csv file.

### Requirements:
- Python 3.8
- csvtool (optional, to make the teams.csv file more readable on the terminal)

```bash
sudo apt-get update && sudo apt-get upgrade
```
```bash
sudo apt-get install python3.8
```
```bash
sudo apt-get install csvtool
```

## To Run:
Clone the repository:
```bash
git clone https://github.com/dadoming/SortPeopleIntoTeams.git
```
Install the requirements:
```bash
cd SortPeopleIntoTeams && pip install -r requirements.txt
```
Run the normal name script:
```bash
python3 normal_sort.py
```
Run the intra names script:
```bash
python3 by_level_sort.py
```
For more readability of the csv on the terminal:
```bash
csvtool readable teams.csv
```

### To add:
- Add a way if there are 6 people, for example, make it sort into 2 teams of 3 instead of 3 teams of 2.
- Add a way to insert remaining people into teams with less people.
- Eventually add an Intra API setting to sort people into teams based on their levels.
- Improve intra username sorting, very bad right now.
