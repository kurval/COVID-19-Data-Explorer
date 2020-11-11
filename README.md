![Build Status](https://travis-ci.com/kurval/COVID-19-Data-Explorer.svg?branch=master)

# Covid-19 Data Explorer
App is live at: https://www.covid19dataexplorer.com/

# About
Covid-19 Data Explorer -app allows user to compare and explore different corona statistics from over 200 countries.
This python based project was created with Streamlit’s open-source app framework.
Using Alrair library for building interactive charts that are displayd with Vega-Lite. Data is **updated daily**.

# Statistics
**These statistics includes:**
* Total confirmed cases
* Total deaths
* Total cases per million  
* Total deaths per million
* New confirmed cases
* New deaths

# Using:
* python3
* streamlit, altair, pandas
* data.world's REST API
* Travis CI
* selenium

# Running with Docker
You can run this app with Dockerfile  

# Testautomation  
I have automated UI tests using Selenium library and Travis CI.  
Travis-CI is a continuous integration tool that will run tests for a GitHub repository every time commits are pushed.  
I'm running tests with both Firefox and Chrome in the headless mode, which is suitable for driving browser-based tests using Selenium and other tools.  
After tests are executed I can check my Travis CI build status page to see if my build passes or fails according to the return status of the build command.  
You can also get the status by e-mail after execution.

Build the container:  
```docker build -t st-app .```  

And run it:  
```docker run -p 8501:8501 --name st-app -it --rm st-app```  

Container is now available on:  
```http://<your docker-machine ip>:8501/```  

Data is originally sourced from: https://ourworldindata.org/coronavirus-source-data  
More information about this dataset: https://github.com/owid/covid-19-data/tree/master/public/data

