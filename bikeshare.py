import time
import pandas as pd
import numpy as np
import calendar

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def raw_data(df):
    view_raw_data = input('Would you like to view 5 rows of individual trip data? Enter yes/y or no/n? ').lower()
    data_ptr = 0
    while view_raw_data not in ['yes', 'y', 'no', 'n']:
        print('You provided an invalid response')
        view_raw_data = input('Would you like to view 5 rows of individual trip data? Enter yes/y or no/n? ').lower()
    while view_raw_data == 'yes' or view_raw_data == 'y':
        print(df.iloc[data_ptr:data_ptr + 5])
        data_ptr += 5
        more_raw_data = input('Do you wish to see five more rows?: Enter yes/y or no/n? ').lower()
        if more_raw_data == 'no' or more_raw_data == 'n':
            print('Have a great day!')
            break

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('enter chicago/c, new york city/ny, washington/w:\n').lower()
    while city not in ['washington', 'w', 'new york city', 'ny', 'chicago', 'c']:
        print('You provided an invalid city selection')
        city = input('enter chicago, new york city, washington:\n').lower()
    if city == 'w':
        city = 'washington'
    elif city == 'ny':
        city = 'new york city'
    elif city == 'c':
        city = 'chicago'

    # TO DO: get user input for month (all, january, february, ... , june)
    month = input('enter a month selection from january-june or all:\n').lower()
    while month not in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
        print('You provided invalid month')
        month = input('enter a month selection from january-june or all:\n').lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('enter a day selection from monday-sunday or all:\n').lower()
    while day not in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
        print('You provided invalid day')
        day = input('enter a day selection from monday-sunday or all:\n').lower()

    print('-'*40)
    
    print('\nCity:', city)
    print('Month:', month)
    print('Day:', day)
    
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
    
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day)
        df = df[df['day_of_week'] == day]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = calendar.month_name[df['month'].mode()[0]]
    print('The most common month is:', common_month)

    # TO DO: display the most common day of week
    common_day = calendar.day_name[df['day_of_week'].mode()[0]]
    print('The most common day of week is:', common_day)

    # TO DO: display the most common start hour
    common_hour = df['hour'].mode()[0]

    if (common_hour >= 1) and (common_hour <= 11):
        print('The most common start hour is: %iAM' % common_hour)
    elif (common_hour == 12):
        print('The most common start hour is: %iPM' % common_hour)
    elif (common_hour == 24):
        common_hour_temp = common_hour - 12
        print('The most common start hour is: %iAM' % common_hour_temp)
    else:
        common_hour_temp = common_hour - 12
        print('The most common start hour is: %iPM' % common_hour_temp)
    
    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station is:', common_start_station)
    
    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('The most commonly used end station is:', common_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    df['Combination'] = df['Start Station'] + ' to ' + df['End Station']
    common_combination = df['Combination'].mode()[0]
    print('The most common combination of start and end stations is:', common_combination)

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    # TO DO: display total travel time
    total_time = df['Trip Duration'].sum()
    print('Total travel time is: ', total_time, 'seconds.')
    
    # TO DO: display mean travel time
    average_time = df['Trip Duration'].mean()
    print('The average trip lasts: ', average_time, 'seconds.')

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    try:
        user = df['User Type'].value_counts(dropna=False)
        print('\nSubscribers:', user.loc['Subscriber'])
        user_temp = user.sum() - user.loc['Subscriber']
        print('Customers:', user.loc['Customer'])
        user_temp -= user.loc['Customer']
        print('Dependent:', user.loc['Dependent'])
        user_temp -= user.loc['Dependent']
    except KeyError:
        print('User Type does not appear in the dataframe')
        
    print('Not Specified:', user_temp)

    # TO DO: Display counts of gender
    try:
        gender = df['Gender'].value_counts(dropna=False)
        print('\nMale:', gender.loc['Male'])
        gender_temp = gender.sum() - gender.loc['Male']
        print('Female:', gender.loc['Female'])
        gender_temp -= gender.loc['Female']
        print('Not Specified:', gender_temp)
    except KeyError:
        print('\nGender does not appear in the dataframe')

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        year = df['Birth Year']
        print('\nEarliest year of birth:', int(year.min()))
        print('Most recent year of birth:', int(year.max()))
        print('Most common year of birth:', int(year.mode()[0]))
    except KeyError:
        print('\nBirth Year does not appear in the dataframe')

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() not in ['yes', 'y']:
            break


if __name__ == "__main__":
	main()
