# Chess openings statistics

## Description

This project is an interactive web application that allows users to explore statistics about popular chess openings. The data is obtained from the [Lichess API](https://lichess.org/api). The application is written in [Python](https://www.python.org/) using the [Dash](https://dash.plotly.com/) framework.

## Usage

### Prerequisites

The application was developed using Python 3.10. It is recommended to use a virtual environment to install the required packages.
Install the required packages using the following command:

```bash
pip install -r requirements.txt
```

### Collecting statistics data

To collect the statistics from openings specified in `data/openings.csv`, run:

```bash
python collect_stats.py
```

The data file `data/openings_stats.csv` will be created.

### Running the application

Launch the application using:

```bash
python app.py
```
