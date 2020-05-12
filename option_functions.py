import pandas as pd

def choose_chart():
    '''
    Allowing user to choose data type

        return: chart number (1=total_cases, 2=total_deaths, 3=new_cases, 4=new_deaths,)
    '''
    print("Options:\n\n1: Total cases\n2: Total deaths\n3: New cases\n4: New deaths\n")
    while True:
        chart = input("Choose statistics number: ")
        if chart != '1' and chart != '2' and chart != '3' and chart != '4':
            print("\nERROR: Invalid number. Try again.")
            continue
        else:
            break
    return chart

def choose_country(countries):
    '''
    Allowing user to choose country data

        param: countries (list of all the countries)
        type: ndarray
        return: country name in lower case 
    '''
    while True:
        new_country = input("\nEnter country name or hit Enter to continue: ").lower()
        if not new_country:
            break
        elif new_country in countries:
            print("\nAdded ", new_country.title())
            break
        else:
            print(f"\nERROR: Country '{new_country}' doesn't exist. Try again.")
            continue
    return new_country

def choose_time_period(youngest):
    '''
    Allowing user to choose time period

        param: youngest (newest date)
        type: datetime.date object
        return: startdate (youngest - time period)
    '''
    print("\nOptions:\n\n1: One month\n2: Three months\n3: Five months\n")
    while True:
        try:
            period = int(input("Choose period number: "))
        except ValueError:
            print("\nERROR: Input not number. Try again.")
            continue
        if period != 1 and period !=2 and period !=3:
            print("\nERROR: Invalid number. Try again.")
            continue
        else:
            break
    if period != 1:
        period = 3 if period == 2 else 5
    startdate = pd.to_datetime(youngest, format="%Y-%m-%d") - pd.DateOffset(months=period)
    return startdate
