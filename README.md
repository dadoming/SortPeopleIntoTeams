# Sort People into teams

1. Go into main.py and set the minimum and maximum team sizes.
2. Create a file named names.txt and put the names of the people you want to sort into teams in it, one name per line.
3. Run main.py and it will create a file named teams.csv with the teams in it.

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
```bash
git clone https://github.com/dadoming/SortPeopleIntoTeams.git
```
```bash
cd SortPeopleIntoTeams
```
```bash
python3 main.py
```
```bash
csvtool readable teams.csv
```

### To add:
- Add a way if there are 6 people, for example, make it sort into 2 teams of 3 instead of 3 teams of 2.
- Add a way to insert remaining people into teams with less people.
