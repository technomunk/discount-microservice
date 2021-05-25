# Discount Microservice

A proof of concept implementation of a discount code microservices.

## Setup

- Get [python 3](https://www.python.org/).
- (optional) Set up virtual environment: `python -m venv venv`.
	+ Once set up, activate the environment: `venv/Scripts/activate`.
- Install dependencies: `python -m pip install -r requirements.txt`.

## Running

To run the application locally:

- (optional) Make sure the virtual environment is active.
- Set `FLASK_APP=src/pages` environmental variable.
- Run Flask: `flask run`.
- Go to [localhost:5000](http://localhost:5000/).

## Testing

As the program is a proof of concept there are 3 pages of interest:

- [Generating discount codes as a brand](http://localhost:5000/generate?brandId=Billogram).
- [Checking discount codes as a brand](http://localhost:5000/list?brandId=Billogram).
- [Fetching discount codes as a user](http://localhost:5000/fetch?userId=Technomunk).

The brands and the user is hard-coded, as those entries would be handled by other parts of the full
service. The available brands are *TechnoInc* and *Billogram*. The only user is *Technomunk*.
