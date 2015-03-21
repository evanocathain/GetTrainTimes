# GetTrainTimes

This is a CLI to scrape the national rail website to quickly get journey
times. It is intended more as an experiment to learn about web scraping
rather than a serious project.

## Usage

A typical use case may be to look up trains from Basinstoke to Waterloo in
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

Nice and simple.
