# overwatch_skills

Scraper using BeautifulSoup to scrape the ability information from the 
Overwatch wiki.
https://overwatch.fandom.com/wiki/

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
