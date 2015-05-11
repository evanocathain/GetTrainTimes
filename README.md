# GetTrainTimes

This is a CLI to scrape the national rail website and quickly get journey
times. It is intended more as an experiment to learn about web scraping
rather than a serious project.

## Usage

A typical use case may be to look up trains from Basingstoke to Waterloo in
an hour. To do this we simply call:

    $ GetTrainTimes -f BSK -t WAT -d 60

This willl produce a table:

    Trains from BSK to WAT leaving after 10:18
    Departs   Arrives   Takes
    10:17     11:07     50
    10:24     11:36     72
    10:30     11:19     49
    10:35     11:20     45
    10:43     11:34     51

Nice and simple. For the input station names, you can use any format and an
attempt will be made. However, it is generally best to use the three letter
station code defined by national rail, since there could be more than one
station with a similar name. To aid with this we provide a helper function to
look up matched.  For example, if you wanted to know the station code for
waterloo:

    $ GetTrainTimes -g Waterloo

Then `GetTrainTimes` will return

    Best matches for input: waterloo
    london waterloo : WAT
    london waterloo east : WAE
    waterloo (merseyside) : WLO

This is a great example of why using the TLA (three letter acronym) is less
error prone. Note that using this function requires `numpy` to be installed
for the search, and `wget` to be instaled to download the station codes. The
former cannot be avoided, but you can avoid installing `wget` by downloading
the station codes manually from [here](http://www.nationalrail.co.uk/static/documents/content/station_codes.csv)
and placing the file `station_codes.csv` in this directory.

## Dependencies
The only non-standard library module that is required for normal operation is
[BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/). 

## Installation

### From source

Clone the repo and

    $ sudo python setup.py install


