import time
import datetime
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTH = ['all','january','february','march','april','may','june']
DAY = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    #Get user input for city (chicago, new york city, washington) until a valid city is returned.
    while True:
        city = input('Which city would you like to explore? Chicago, New York City, Washington: \n').lower()
        if city in CITY_DATA.keys():
            break;
        else:
            print('Invalid City, please try again \n')

    #Get user input for month (all, january, february, ... , june)
    while True:
        month = input('Which month would you want to see data for? All, January, February, ... , June: \n').lower()
        if month in MONTH:
            break;
        else:
            print('Invalid Month, please try again \n')

    #Get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Which day would you want to see data for? All, Monday, Tuesday, ... , Sunday: \n').lower()
        if day in DAY:
            break;
        else:
            print('Invalid Day, please try again \n')


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    #Create a data frame from the city file name
    df = pd.read_csv(CITY_DATA[city])
    #Create a new column 'month' by extracting the month name from Start Time column
    df['month'] = pd.to_datetime(df['Start Time']).dt.month
    #Create a new column 'day' by extracting the day from Start Time column
    df['day'] = pd.to_datetime(df['Start Time']).dt.weekday
    #Create a new column 'hour' by extracting the hour from Start Time column
    df['hour'] = pd.to_datetime(df['Start Time']).dt.hour

    #Filter by selected month
    if month != 'all':
        df = df[df['month'] == MONTH.index(month)]
    #Filter by selected day
    if day != 'all':
        df = df[df['day'] == DAY.index(day)]

    return df


def time_stats(df, month = 'all', day = 'all'):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #Display the most common month in an year and common day of week
    if month == 'all' and day == 'all':
        print('{} had the most rentals monthly with count {}'.format(MONTH[df['month'].value_counts().index[0]], df['month'].value_counts().values[0]))
        print('{} had the most rentals daily with count {}'.format(DAY[df['day'].value_counts().index[0]], df['day'].value_counts().values[0]))
    elif month == 'all':
        print('{} had the most rentals on {} with count {}'.format(MONTH[df['month'].value_counts().index[0]], day, df['month'].value_counts().values[0]))
    elif day == 'all':
        print('{} had the most rentals in {} with count {}'.format(DAY[df['day'].value_counts().index[0]], month, df['day'].value_counts().values[0]))
    else:
        print('{}s in {} had {} rentals'.format(day, month, df['month'].count()))


    #Display the most common start hour
    print('{} was the most common start hour for rentals, count = {}'.format(df['hour'].value_counts().index[0], df['hour'].value_counts().values[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #Display most commonly used start station
    print('Station {} is the most commonly used start point {} times'.format(df['Start Station'].value_counts().index[0], df['Start Station'].value_counts().values[0]))

    #Display most commonly used end station
    print('Station {} is the most commonly used end point {} times'.format(df['End Station'].value_counts().index[0], df['End Station'].value_counts().values[0]))

    #Display most frequent combination of start station and end station trip
    common_startstop_stations = (df['Start Station'] + ' to ' + df['End Station']).value_counts()
    print('{} is the most common start stop combination used {} times'.format(common_startstop_stations.index[0], common_startstop_stations.values[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #Display total travel time
    total_time = str(datetime.timedelta(seconds = int(df['Trip Duration'].sum())))
    print('Total travel time of all rentals is {}'.format(total_time))

    #Display mean travel time
    mean_time = str(datetime.timedelta(seconds = int(df['Trip Duration'].mean())))
    print('Mean travel time of all rentals is {}'.format(mean_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    print('Types of users and their rental counts')
    print(df['User Type'].value_counts())

    #Display counts of gender, earliest, most recent, and most common year of birth for Chicago and NYC
    if city != 'washington':
        print('\nCount of male and female renters')
        print(df['Gender'].value_counts())

        print('\nThe most earliest year of birth among renters were {}'.format(int(df['Birth Year'].min())))

        print('The most recent year of birth among renters were {}'.format(int(df['Birth Year'].max())))

        print('{} was the most common year of birth among renters'.format(int(df['Birth Year'].mode().values[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def individual_trip_details(df):
    """Displays individual trip details for the filtered data using user input."""

    axes_index = 0
    while True:
        display_rows = input('\nDo you want to display individual entries? Enter yes or no. \n')
        if 'yes' == display_rows.lower():
            loop_count = 0
            #Loop until the axes is less than number of rows in the Data frame
            #Display only 5 entries at a time and keep track of the index
            while axes_index < df.shape[0] and loop_count < 5:
                print(df.iloc[axes_index])
                loop_count += 1
                axes_index += 1
                print('-'*40)
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        if df.size:
            time_stats(df, month, day)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df,city)
            individual_trip_details(df)
        else:
            print('No data available for {} during {} for {} days'.format(city,month,day))

        if input('\nWould you like to restart? Enter yes or no.\n').lower() != 'yes':
            break


if __name__ == "__main__":
	main()
