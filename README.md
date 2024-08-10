# ODMD Data Science Project

This project is focused on extracting data from the Otomotiv Distribütörleri Mobilite Derneği (ODMD) website using Selenium, followed by performing Exploratory Data Analysis (EDA) and implementing time series prediction models. The goal is to analyze the automotive industry trends and make accurate forecasts based on historical data.

## Table of Contents

- [Introduction](#introduction)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Data Collection](#data-collection)
- [Exploratory Data Analysis](#exploratory-data-analysis)
- [Time Series Prediction](#time-series-prediction)
- [Results](#results)

## Introduction

This project aims to analyze and predict trends in the automotive industry by leveraging data from the ODMD website. The project is divided into three main stages: web scraping, exploratory data analysis (EDA), and time series prediction. Additionally, economic variables from the Electronic Data Delivery System (EVDS) have been incorporated to enhance the accuracy of vehicle sales predictions.

## Project Structure

### Data Collection
Data is scraped from the ODMD website using Selenium (undetected_selenium_scraper.py). Which automates the downloading of various data files from the website.


### Exploratory Data Analysis
The exploratory data analysis is performed in Jupyter notebooks located in the notebooks/ directory. This step involves:

* Cleaning and preprocessing the data
* Visualizing key metrics and trends in the automotive industry
* Identifying patterns and anomalies in the data

### Time Series Prediction
Time series models are implemented to predict future trends in the automotive industry. The following steps are included:

* Data preparation for time series modeling
* Incorporation of economic variables from EVDS (Electronic Data Delivery System) to enhance prediction accuracy
* Implementation of various time series models (e.g., ARIMA, Prophet, CatBoostRegressor)
* Model evaluation and selection based on performance metrics


### Results

The project demonstrates the ability to predict future automotive industry trends based on historical data and economic indicators. Key insights and model performance metrics are discussed in the notebooks.

