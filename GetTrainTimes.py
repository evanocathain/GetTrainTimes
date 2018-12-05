#!/usr/bin/python
""" Script to scrape the national rail website for train times """

import urllib2
from BeautifulSoup import BeautifulSoup
import datetime
import argparse
import os
from termcolor import colored


def strip_tags(item):
    return item.text


def stringtime_to_datetime(string):
    """ Convert 08:59 to datetime """
    now = datetime.datetime.now()
    [hour, minute] = string.split(":")
    return datetime.datetime(now.year, now.month, now.day,
                             hour=int(hour), minute=int(minute))


def journey_duration(dep, arr):
    dep_dt = stringtime_to_datetime(dep)
    arr_dt = stringtime_to_datetime(arr)
    dur_secs = (arr_dt - dep_dt).total_seconds()
    # Check if the arrival time is on the next day
    if dur_secs < 0:
        arr_dt = arr_dt + datetime.timedelta(days=1)
        dur_secs = (arr_dt - dep_dt).total_seconds()
    dur_mins = dur_secs / 60.0

    # Pretty print
    if dur_mins > 60:
        mins = dur_mins % 60
        hrs = (dur_mins - mins) / 60
        return "{} hrs {} mins".format(int(hrs), int(mins))
    else:
        return "{} mins".format(int(dur_mins))


def normalise_string(string):
    return string.replace('"', '').lower()


def get_station_name(station):
    """ Attempt to find the 3 letter station name from the string input

    This will normalise the input string, then use partial matching to identify
    a list of possible strings for the user.
    """

    import numpy as np

    station = normalise_string(station)
    file_name = "station_codes.csv"

    if not os.path.isfile(file_name):
        print("Attempting to download the list of station codes")
        try:
            import wget
            wget.download("http://www.nationalrail.co.uk/static/"
                          "documents/content/station_codes.csv")
            print("\nSuccess!")
        except IOError:
            raise IOError("Unable to download station codes")

    name, TLA = read_station_codes(file_name)
    idx = np.char.find(name, station)

    print("Best matches for input: {}".format(station))
    for i in np.arange(len(name))[idx > -1]:
        print("{} : {}".format(name[i], TLA[i]))


def read_station_codes(file_name):
    name, TLA = [], []
    with open(file_name) as f:
        for row in f:
            row = row.split(",")
            name.append(normalise_string("".join(row[:-1])))
            TLA.append(row[-1].rstrip("\r\n"))
    return name, TLA


def get_departures_and_arrivals(args):
    now = datetime.datetime.now()
    args.then = now + datetime.timedelta(minutes=args.TIME_OFFSET)

    string_time = "{:02.0f}{:02.0f}".format(args.then.hour, args.then.minute)

    URL = ('http://ojp.nationalrail.co.uk/service/timesandfares/' +
           '{}/{}/today/'.format(args.FROM_STATION, args.TO_STATION) +
           '{}/dep#outwardJump'.format(string_time))

    soup = BeautifulSoup(urllib2.urlopen(URL).read())

    departures = [strip_tags(i) for i in soup.findAll("td", {"class": "dep"})]
    arrivals = [strip_tags(i) for i in soup.findAll("td", {"class": "arr"})]

    return departures, arrivals


def print_departure_and_arrivals_table(args, departures, arrivals):
    print("Using time-delta {}".format(args.TIME_OFFSET))
    print("Trains from {} to {} leaving after {:02d}:{:02d}".format(
          colored(args.FROM_STATION, "red"),
          colored(args.TO_STATION, "red"),
          args.then.hour, args.then.minute))
    print(colored("Departs   Arrives   Takes", "green"))
    for dep, arr in zip(departures, arrivals):
        line = "{}     {}     {}".format(dep, arr, journey_duration(dep, arr))
        print(colored(line, "blue"))


def main():
    # Get command line arguments
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-d", dest="TIME_OFFSET",
                        help="The time delta at which to search for times",
                        default=-20, type=int)
    parser.add_argument("-t", "--to", dest="TO_STATION",
                        help="To station", default="MAN")
    parser.add_argument("-f", "--from", dest="FROM_STATION", default="EUS",
                        help="From station")
    parser.add_argument("-g", "--get", dest="GetStationName", default=None,
                        help="Get the 3 letter station name")
    args = parser.parse_args()

    if args.GetStationName:
        get_station_name(args.GetStationName)
    else:
        d, a = get_departures_and_arrivals(args)
        print_departure_and_arrivals_table(args, d, a)

if __name__ == "__main__":
    main()
