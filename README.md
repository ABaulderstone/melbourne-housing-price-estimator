# Melbourne House Price Estimator

## Purpose

Machine Learning and Data Engineering are relatively foregin concepts to me, so I wanted to develop some understanding of these concepts with some data that I was reasonably familiar with. This application builds a small model based on some Melbourne house sales data, and provides an API and front end to access that predictive model.

## Running the app.

This application is built with Python and React. Docker config has been provided for ease of setup. Assuming you have Docker on your machine running the app is as simple as

```bash
docker compose up --build
```

On first run the python script will build the model, on subsequent runs it will skip straight to starting the Flask API

## Caveats

- The sale data is from 2016, the market has undergone significant growth since then so price estimates may be unreasonably low
- Converting suburb to numerical data may not be most optimal way to create a prediction, particularly if some suburbs are underrepresented in the data set. Perhaps using latitude/longitude or distance from CBD would yield better results
- Linear Regression also might not be the best way to predict data, the relationship between bedrooms and price is often not Linear
- I am not trained in data engineering or machine learning. This represents a couple days of scrappy self teaching. There could be other gaps in my knowledge contributing to inaccurate estimates
