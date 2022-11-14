import time as tm
import pandas as pd
import numpy as np
import pprint as pp

# link input cities to their csv file names
cities_csv = {'chicago' : 'chicago.csv',
              'new york' : 'new_york_city.csv',
              'washington' : 'washington.csv'}

# convert month name to month int
month_conversion = {'january' : 1,
                    'february' : 2,
                    'march' : 3,
                    'april': 4,
                    'may' : 5,
                    'june' : 6,
                    'all' : [1, 2, 3, 4, 5, 6]}

# convert month int to month name
month_reverse_conversion = {1 : 'january',
                            2 : 'february',
                            3 : 'march',
                            4 : 'april',
                            5 : 'may',
                            6 : 'june'}

#convert day of the week name to int
dow_conversion = {'monday' : 0,
                          'tuesday' : 1,
                          'wednesday' : 2,
                          'thursday' : 3,
                          'friday' : 4,
                          'saturday' : 5,
                          'sunday' : 6,
                          'all' : [0, 1, 2, 3, 4, 5, 6]}

# convert day of the week int to name
dow_reverse_conversion = {0 : 'monday',
                                  1 : 'tuesday',
                                  2 : 'wednesday',
                                  3 : 'thursday',
                                  4 : 'friday',
                                  5 : 'saturday',
                                  6 : 'sunday'}

def reader(city):

    """ Takes a city and returns a dataframe of that city's information """

    if city == 'chicago':
        reader = pd.read_csv(cities_csv['chicago'])
        data = pd.DataFrame(reader)

    elif city == 'washington':
        reader = pd.read_csv(cities_csv['washington'])
        data = pd.DataFrame(reader)

    elif city == 'new york':
        reader = pd.read_csv(cities_csv['new york'])
        data = pd.DataFrame(reader)
    return data

def get_filters():

    """ Gets the filters from the user and returns the city month and day """

    # Loop to ask city
    while True:
        city = input('\nWhat city would you like to analyze? Chicago, New York, or Washington? \n').lower().strip()
        if city in ['chicago', 'new york', 'washington']:
            break
        print('\nSorry, it looks like you did not select one of these cities, lets try again!')
        continue
    # Loop to ask whether or not to filter
    time_filter_q = input(f'\nGreat! Lets look at {city.title()}! Would you like to filter the data by time?\nYes or No\n').lower().strip()
    while time_filter_q not in ['yes', 'no']:
        time_filter_q = input('\nSlow down partner, you\'re not reading the prompt! Want to filter by time? yes or no\n').lower().strip()


    # Loop to get the specific filter
    while True:
        if time_filter_q == 'yes':
            while True:
                month = input('\nAlright which month? January, February, March, April, May, June, or all?\n').lower().strip()
                if month in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
                    while True:
                        day = input('\nAlright which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or all?\n').lower().strip()
                        if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
                            print('\nOnward we go!')
                            print('-'*80)
                            return city, month, day
                        else:
                            print('\nWe can do this all day... (just don\'t press ctrl C)')
                            continue
                else:
                    print('\nNow I can tell you\'re just stress testing.')
                    continue
        if time_filter_q == 'no':
            month = None
            day = None
            print('\nOnward we go!')
            print('-'*80)
            return city, month, day

def group_filter(data, month_name, day_name):

    """ Takes a dataframe, month, and day filters, and returns a filtered dataframe """

    # create empty dataframe to enter the filtered data into
    filteredDF = pd.DataFrame([])
    # turn the start time into a usable datetime
    data['Start Time'] = pd.to_datetime(data['Start Time'])
    # add a column of the month number
    data['Month'] = pd.DatetimeIndex(data['Start Time']).month
    # add a column of the day number
    data['DoW'] = pd.DatetimeIndex(data['Start Time']).dayofweek
    # apply the month filter
    if month_name == 'all':
        emptydf = data[data.Month.isin(month_conversion[month_name])]
    elif month_name == None:
        emptydf = data
    else:
        emptydf = data[data.Month == month_conversion[month_name]]
        # apply the day filter
    if day_name == 'all':
        emptydf = emptydf[emptydf.DoW.isin(dow_conversion[day_name])]
    elif day_name == None:
        emptydf = emptydf
    else:
        emptydf = emptydf[emptydf.DoW == dow_conversion[day_name]]

    # returns the filtered dataframe
    return emptydf

def time_stats(data):

    """ Takes a filtered dataframe and prints time statistics """

    data['Hour'] = pd.DatetimeIndex(data['Start Time']).hour

    start_time = tm.time()

    print('-'*80)
    print('Popular times of travel:')
    print('\nThe most common month was:', month_reverse_conversion[data['Month'].mode()[0]].title())
    print('The most common day of the week was:', dow_reverse_conversion[data['DoW'].mode()[0]].title())
    print('The most common hour of day was:', data['Hour'].mode()[0])

    print("\nThis took %s seconds." % (tm.time() - start_time))
    print('-'*80)

def station_stats(data):

    """ Takes a filtered dataframe and prints station data """

    data['Trip'] = data['Start Station'] + ' and ' + data['End Station']

    start_time = tm.time()

    print('-'*80)
    print('Popular stations and trip:')
    print('\nThe most common start station was:', data['Start Station'].mode()[0])
    print('The most common end station was:', data['End Station'].mode()[0])
    print('The most common trip from start to end was:', data['Trip'].mode()[0])

    print("\nThis took %s seconds." % (tm.time() - start_time))
    print('-'*80)

def trip_stats(data):

    """ Takes a filtered dataframe and prints travel time data """

    start_time = tm.time()

    print('-'*80)
    print('Trip duration:')
    print('\nTotal travel time was:', data['Trip Duration'].sum(), 'seconds')
    print('The average trip duration was:', data['Trip Duration'].mean(), 'seconds')

    print("\nThis took %s seconds." % (tm.time() - start_time))
    print('-'*80)

def user_stats(data, city):

    """ Takes a filtered dataframe, and the city name and prints user information """

    start_time = tm.time()

    # assure that the user type and count correspond reguardless of which has more
    # if it was only by index there was a chance of me misslabeling it
    user_types = data['User Type'].value_counts()
    type1 = user_types.index[0]
    count1 = user_types[0]
    type2 = user_types.index[1]
    count2 = user_types[1]
    print(type1, count1, type2, count2)


    print('-'*80)
    print('User Info:')
    print(f'\nThere were {count1} {type1}s and {count2} {type2}s')

    if city != 'washington':
        # assure that the user type and count correspond reguardless of which has more
        # if it was only by index there was a chance of me misslabeling it
        user_gender = data['Gender'].value_counts()
        gender1 = user_gender.index[0]
        gender_count1 = user_gender[0]
        gender2 = user_gender.index[1]
        gender_count2 = user_gender[1]
        print(gender1, gender_count1, gender2, gender_count2)

        print(f'There were {gender_count1} {gender1}s and {gender_count2} {gender2}s')
        print('Earliest year of birth:', int(data['Birth Year'].min()))
        print('Most recent year of birth:', int(data['Birth Year'].max()))
        print('Most common year of birth:', int(data['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (tm.time() - start_time))
    print('-'*80)

def show_data(data):

    """ Takes a dataframe and prompts the user to show five rows at a time """

    check = input('\nWould you like to see the raw data?\n').lower().strip()

    # This while loop filters any response that isn't yes or no
    while check not in ['yes', 'no']:
        check = input('Sorry, either yes or no\n').lower().strip()

    # Don't show any data and continue to main
    if check == 'no':
        return
    else:
        # Remove the columns added for calculations
        data.drop(['DoW', 'Month', 'Hour', 'Trip'], axis = 1, inplace = True)
        # starting place for the data
        counter = 5
        start = 0
        while check == 'yes':
            print(data[start: counter])
            check = input('\nWant to see more?\n').lower().strip()
            while check not in ['yes', 'no']:
                check = input('Sorry, either yes or no\n').lower().strip()
            counter += 5
            start += 5
            if counter > data.shape[0]:
                print('\nWoah, that must have taken a while, thats all the data')
                return


def main():

    """ main loop to run the program """

    while True:
        # Get the filters
        city_raw, month, day = get_filters()
        # Convert city into data for the city
        city = reader(city_raw)
        # Count total time elpased
        start_time = tm.time()
        # Gather the filtered dataframe
        data = group_filter(city, month, day)
        # Pass filtered dataframe into calculators
        time_stats(data)
        station_stats(data)
        trip_stats(data)
        user_stats(data, city_raw)

        print(f'Above is the info for {city_raw.title()} within your time filter')
        print("\nTotal time elapsed: %s seconds." % (tm.time() - start_time))

        show_data(data)

        again = input('\nWant to start over?\n').lower().strip()
        # This input check method is great and I should have used it earlier
        while again not in ['yes', 'no']:
            again = input('That wasn\'t a yes or no, try again\n').lower().strip()
        if again == 'no':
            print('Thank you for testing out my program!')
            break

if __name__ == "__main__":
	main()














































# Scroll Saver
