# overwatch_skills

Scraper using BeautifulSoup to scrape the ability information from the 
Overwatch wiki.
https://overwatch.fandom.com/wiki/

# Design Goals
Core goal is to provide a simple interface that gives recommendations to an Overwatch player
about which character to select based on the current map, team composition, enemy
composition, and game mode.
Since the player will be using and updating the tool during the match,
it needs to be easy and quick to enter in information, and the
recommendations need to be concise.
But, we also want to provide as much information as possible,
without it becoming cluttered.

# Data Sources
Primary data source for start is the Overwatch wiki.
Data on abilities is collected via a BeautifulSoup scraper.
This data is used to determine the strength and weaknesses
of each character.

# Setup

## Python Setup
Recommended to use Anaconda for environment setup.
https://www.anaconda.com/download

Create the environment with:
conda env create -f overwatch_skills.env

Problems? Maybe try this instead:
conda create bs4 requests jupyter -n overwatch_skills

## Jupyter Notebook
Activate the environment with:
conda activate overwatch_skills

Start the jupyter notebook with:
jupyter notebook

With the abilities_scraper.ipynb open, you can Shift+Enter through it to
execute the cells and display the scraped data.
