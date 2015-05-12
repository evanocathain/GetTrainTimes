from setuptools import setup

setup(name='GetTrainTimes',
      packages=[''],
      version='1.0',
      description="CLI to scrape the National Rail website",
      author="Greg Ashton",
      install_requires = ['BeautifulSoup'],
      entry_points={'console_scripts': ['GetTrainTimes = GetTrainTimes:main']}
      )
