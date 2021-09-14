import csv;
import pandas;
import requests;
import numpy;
import matplotlib.pyplot as plt;
import matplotlib;
#download csv files from online
countyurl = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv';
stateurl = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv';
r1 = requests.get(countyurl, allow_redirects=True);
r2 = requests.get(stateurl, allow_redirects=True);
open('us-counties.csv', 'wb').write(r1.content);
open('us-states.csv', 'wb').write(r2.content);
#file opening data
filename = "us-states.csv";
#row and column names
stateFields = [];
countyFields = [];
stateData = [];
countyData = [];

def getData():
	# coviData = open(filename);
	# covidReader = csv.reader(coviData);
	# stateFields = next(covidReader);
	with open('us-states.csv', 'r') as coviData:
		covidReader = csv.reader(coviData);
		for x in range(1):
			stateFields.append(next(covidReader));

		for row in covidReader:
			stateData.append(row);

	with open('us-counties.csv', 'r') as coviData:
		covidReader = csv.reader(coviData);
		for x in range(1):
			countyFields.append(next(covidReader));

		for row in covidReader:
			countyData.append(row);

def getTotalCases():
	total = 0;
	size = len(stateData)-1;
	for x in range(size-54, size):
		total += int(stateData[x][3]);
	return "{:,}".format(total);

def getTotalDeaths():
	total = 0;
	size = len(stateData)-1;
	for x in range(size-54, size):
		total += int(stateData[x][4]);
	return "{:,}".format(total);

def getStateDeaths(state):
	size = len(stateData)-1;
	for x in reversed(range(0, size)):
		stateName = stateData[x][1];
		if stateName.lower() == state.lower():
			deaths = int(stateData[x][4]);
			return "{:,}".format(deaths);
	return "state not found";

def getStateCases(state):
	size = len(stateData)-1;
	for x in reversed(range(0, size)):
		stateName = stateData[x][1];
		if stateName.lower() == state.lower():
			cases = int(stateData[x][3]);
			return "{:,}".format(cases);
	return "state not found";

def getCountyCases(county, state):
	size = len(countyData)-1;
	for x in reversed(range(0, size)):
		countyName = countyData[x][1];
		stateName = countyData[x][2];
		if stateName.lower() == state.lower() and countyName.lower() == county.lower():
			cases = int(countyData[x][4]);
			return "{:,}".format(cases);
	return "county not found";

def getCountyDeaths(county, state):
	size = len(countyData)-1;
	for x in reversed(range(0, size)):
		countyName = countyData[x][1];
		stateName = countyData[x][2];
		if stateName.lower() == state.lower() and countyName.lower() == county.lower():
			deaths = int(countyData[x][5]);
			return "{:,}".format(deaths);
	return "county not found";

def makeGraph(county, state):
	#create arrays
	dates = [];
	monthCases = [];
	monthDeaths = [];
	size = len(countyData)-1;
	upperLimit = 30;
	#iterate through array
	for x in reversed(range(0, size)):
		if upperLimit == 0:
			break;
		else:
			countyName = countyData[x][1];
			stateName = countyData[x][2];
			if stateName.lower() == state.lower() and countyName.lower() == county.lower():
				dates.append(str(countyData[x][0]));
				monthCases.append(countyData[x][4]);
				monthDeaths.append(countyData[x][5]);
				upperLimit -= 1;
	#plot data
	dates.reverse();
	monthCases.reverse();
	monthDeaths.reverse();
	#convert dates
	x_values = [datetime.datetime.strptime(d,"%m/%d/%Y").date() for d in dates];
	ax = plt.gca();
	formatter = mdates.DateFormatter("%Y-%m-%d");
	ax.xaxis.set_major_formatter(formatter);

	locator = mdates.DayLocator();
	ax.xaxis.set_major_locator(locator);
	#create canvas
	plt.figure(figsize=(9, 3));
	#plot cases
	plt.subplot(131);
	plt.plot(x_values, monthCases);
	plt.ylabel('Cases in %s County, %s\n' % (county, state));
	#plot deaths
	plt.subplot(133);
	plt.plot(x_values, monthDeaths);
	plt.ylabel('Deaths in %s County, %s\n' % (county, state))
	plt.show();


def main():
	#instance varaible
	total = 0;
	getData();
	#header
	print ("Welcome To GIAH COVIDCOPIA\n")
	#print cases and deaths
	print ("Current Number of Cases Today: %s" % (getTotalCases()));
	print ("Current Number of Deaths Today: %s\n" % (getTotalDeaths()));
	#get state
	state = raw_input("What state would you like to know more about >>> ");
	print ("Current Number of Cases in %s Today: %s" % (state, getStateCases(state)));
	print ("Current Number of Deaths in %s Today: %s\n" % (state, getStateDeaths(state)));
	#get county
	county = raw_input("Which county are you looking for >>> ");
	print ("Current Number of Cases in %s County, %s Today: %s" % (county, state, getCountyCases(county, state)));
	print ("Current Number of Deaths in %s County, %s Today: %s\n" % (county, state, getCountyDeaths(county, state)));
	#show cases
	showGraph = raw_input("Would you like to see graph for %s County, %s >>> " % (county, state));
	if showGraph.lower() == "yes":
		makeGraph(county, state);
	else:
		print("Good Bye!");



if __name__ == "__main__":
	main();
