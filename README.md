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

# Running app with Docker
You can run this app with Dockerfile  

Build the container:  
```docker build -t st-app .```  

And run it:  
```docker run -p 8501:8501 --name st-app -it --rm st-app```  

Container is now available on:  
```http://<your virtual machine ip>:8501/```  

# Testautomation  
I have automated UI tests using Selenium library and Travis CI.  

Travis-CI is a continuous integration tool that will run tests for a GitHub repository every time commits are pushed.
I'm running tests with both Firefox and Chrome in the headless mode, which is suitable for driving browser-based tests using Selenium and other tools.  

After all tests have finished I can check my Travis CI build status page to see if my build passes or fails according to the return status of the build command.
You can also get the status by e-mail after execution.  

I'm using Python unittest as my test runner so I can also run the specific test class from the command line for example:  
```python -m unittest tests.CompareCountries```  
or running a single test case:  
```python -m unittest tests.CompareCountries.test_check_chart```  

# Data Source  
Dataset: https://data.world/vale123/covid-19-complete-dataset  
Data is originally sourced from: https://ourworldindata.org/coronavirus-source-data  
More information about this dataset: https://github.com/owid/covid-19-data/tree/master/public/data

