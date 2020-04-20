import time
import pandas as pd
import numpy as np
import datetime as dt

###########################################################################
###########################################################################
###########################################################################
## The datasets to select from
CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

# Additional global variables for selection
cities = CITY_DATA.keys()
months = ['All', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
weekdays = ['All', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']

###########################################################################
###########################################################################
###########################################################################
## An interactive function to get data filters

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!\n')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("We have data for Chicago, New York City, and Washington. Which one would you like? \n")
    city = city.title() # just in case
    while city not in cities:
        city = input("Invalid input. Please try again: ")
        city = city.title()

    print("\nOK, let's look at {}. \n".format(city), )

    # TO DO: get user input for month (all, january, february, ... , june)
    month = input("Which month would you like to see? (Select from: all, Jan, Feb, Mar, Apr, May, or Jun)\n")
    month = month.title()
    while month not in months:
        month = input("Invalid input. Please try again: ")
        month = month.title()

    if month == 'All':
        print("\nOK, let's look at {} in all months. \n".format(city))
    else:
        print("\nOK, let's look at {} in {}. \n".format(city, month))

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    weekday = input("And, pick a weekday? (Select from All, Mo, Tu, We, Th, Fr, Sa or Su)\n")
    weekday = weekday.title()
    while weekday not in weekdays:
        weekday = input("Invalid input. Please try again: ")
        weekday = weekday.title()

    print("\nOK, let's look at \n-city: {}\n-month: {}\n-day: {}".format(city, month, weekday))

    print('-'*40)
    return city, month, weekday

###########################################################################
###########################################################################
###########################################################################
## A function to prep the data for analyses (including filters from user input)

def load_data(city, month, weekday):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) weekday - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    print("\nPreping the dataset based on your selection...")

    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Weekday'] = df['Start Time'].dt.day_name()

    # filter month if not 'All'
    if month != 'All':
        month = months.index(month)
        df = df[df['Month'] == month]

    # filter weekday if not "All"
    if weekday != 'All':
        df = df[df['Weekday'].str[:2] == weekday]

    print("\nOK, we can find {} records.".format(df.shape[0]))
    return df

###########################################################################
###########################################################################
###########################################################################
## A function for analyzing the temporal patterns

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...')
    start_time = time.time()

    # TO DO: display the most common month
    if len(df['Month'].unique()) > 1:
        peak_month = months[df['Month'].mode()[0]]
        print("\nThe month with the most trips: {}.".format(peak_month))

    # TO DO: display the most common day of week
    if len(df['Weekday'].unique()) > 1:
        peak_weekday = df['Weekday'].mode()[0]
        print("The day (of week) with the most trips: {}".format(peak_weekday))

    # TO DO: display the most common start hour
    df['Start Hour'] = df['Start Time'].dt.hour
    peak_hour = df['Start Hour'].mode()[0]
    print('The hour with the most trips is between {}:00 and {}:00'.format(peak_hour, peak_hour+1))

    print("\nRun time: %s seconds." % (time.time() - start_time))
    print('-'*40)

###########################################################################
###########################################################################
###########################################################################

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...')
    start_time = time.time()

    # TO DO: display most commonly used start station
    top_start = df['Start Station'].mode()[0]
    print('\nThe most popular starting station: ', top_start)

    top_5start = input("\nThere might be ties. Would you like to see the top five? (Enter yes or no)\n")
    if top_5start.lower() == 'yes':
        top_5start = df.groupby('Start Station').size()
        top_5start = top_5start.sort_values(ascending=False)[:5]
        print(top_5start.to_string())

    # TO DO: display most commonly used end station
    top_end = df['End Station'].mode()[0]
    print('\nThe most popular ending station: ', top_end)

    top_5end = input("\nThere might be ties. Would you like to see the top five? (Enter yes or no)\n")
    if top_5end.lower() == 'yes':
        top_5end = df.groupby('End Station').size()
        top_5end = top_5end.sort_values(ascending=False)[:5]
        print(top_5end.to_string())

    # TO DO: display most frequent combination of start station and end station trip
    count_combo = df.groupby(['Start Station', 'End Station']).size()
    count_combo = count_combo.sort_values(ascending=False)
    top_combo = count_combo.index[0]
    print('\nThe most popular start-end combination: {} to {}'.format(top_combo[0], top_combo[1]))

    top_5combo = input("\nThere might be ties. Would you like to see the top five? (Enter yes or no)\n")
    if top_5combo.lower() == 'yes':
        print(count_combo[:5].to_string())

    print("\nRun time: %s seconds." % (time.time() - start_time))
    print('-'*40)

###########################################################################
###########################################################################
###########################################################################

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...')
    start_time = time.time()

    # TO DO: display total travel time
    total = dt.timedelta(seconds=int(df['Trip Duration'].sum()))
    print('\nTotal travel time: ', total)

    # TO DO: display mean travel time
    mean = dt.timedelta(seconds=int(df['Trip Duration'].mean()))
    print('Average travel time: ', mean)

    print("\nRun time: %s seconds." % (time.time() - start_time))
    print('-'*40)

###########################################################################
###########################################################################
###########################################################################

def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...')
    start_time = time.time()

    # TO DO: Display counts of user types
    type_count = df.groupby('User Type').size().to_string()
    print("\nThere are {} types of users: \n{}".format(len(type_count), type_count))

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        gender_count = df.groupby('Gender').size().to_string()
        print("\nThe gender distribution of the users: \n{}".format(gender_count))
    else:
        print("\nThere are no user gender data available for {}.".format(city))

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        birth_mode = int(df['Birth Year'].mode()[0])
        birth_old = int(df['Birth Year'].min())
        birth_young = int(df['Birth Year'].max())
        print("\nThe youngest user was born in {} and oldest in {}, with {} being the most common birth year".format(birth_young, birth_old, birth_mode))
    else:
        print("\nThere are no data about user birth years for {}.".format(city))

    print("\nRun time: %s seconds." % (time.time() - start_time))
    print('-'*40)

###########################################################################
###########################################################################
###########################################################################

def main():
    while True:
        city, month, weekday = get_filters()
        df = load_data(city, month, weekday)

       ## Show raw data if the user wishes to see them
        q0 = input("\nWould you like to see a few lines of the data? (Enter yes or no.)\n")
        if q0.lower() == 'yes':
            i = 0
            print(df[i:(i+5)])
            while i <= (df.shape[0]-5):
                q0a = input("\n would you like to see more? (Enter yes or no)")
                if q0a.lower() == 'yes':
                    i += 5
                    print(df[i:(i+5)])
                else: 
                    break

        ## Statistic summaries of the data
        q1 = input("\nWould you like to see the most common date/time of travel? (Enter yes or no.)\n")
        if q1.lower() == 'yes':
            time_stats(df)
        q2 = input("\nWould you like to see the most common stations? (Enter yes or no.)\n")
        if q2.lower() == 'yes':
            station_stats(df)
        q3 = input("\nWould you like to see a summary of travel time? (Enter yes or no.)\n")
        if q3.lower() == 'yes':
            trip_duration_stats(df)
        q4 = input("\nWould you like to see a summary of user types? (Enter yes or no.)\n")
        if q4.lower() == 'yes':
            user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('\nThank you! See you next time.\n')
            break

###########################################################################
###########################################################################
###########################################################################

if __name__ == "__main__":
	main()
