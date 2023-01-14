# Automated road accident casuality survey based on news articles

The system is designed to gather information on road accident casualties by searching for and collecting news articles containing the keyword "road accident" from online news portals. The collected data is then processed through a natural language processing (NLP) model to extract information such as the number of deaths, injuries, location, and vehicle type involved in the accidents.

## How to use

### Install the dependencies
Install all required python libraries by running `pip install -r requirements.txt`
It'll install the following requirements

- chromedriver_binary
- matplotlib==3.5.2
- nltk==3.7
- numpy==1.21.5
- pandas==1.4.3
- seaborn==0.11.2
- selenium==4.7.2
- word2number==1.1

### Scrape news articles
Collect news articles from [The Daily Star](https://www.thedailystar.net/) by running the following command
`python dailystar.py`
It'll open an automated google chrome window using chrome web driver and crawl through the website to collect news articles data and store them into `input.csv` file.

### Run the NLP model
`python model.py`
This command will pass the data from `input.txt` into the NLP model in order to extract the casuality data and put them into `output.csv`

### Data Visualization
Use the jupyter notebook `plots.ipynb` to visualized the data in the `output.csv` file.