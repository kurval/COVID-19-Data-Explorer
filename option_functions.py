import pandas as pd

def choose_chart():
    '''
    Allowing user to choose data type
    '''
    print("Options:\n\n1: Total cases\n2: Total deaths\n")
    while True:
        try:
            chart = int(input("Choose statistics number: "))
        except ValueError:
            print("\nERROR: Input not number. Try again.")
            continue
        if chart != 1 and chart !=2:
            print("\nERROR: Invalid number. Try again.")
            continue
        else:
            break
    return chart

def choose_country(countries):
    '''
    Allowing user to choose country data
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
    if period == 2:
        period = 3
    elif period == 3:
        period = 5
    startdate = pd.to_datetime(youngest, format="%Y-%m-%d") - pd.DateOffset(months=period)
    return startdate
