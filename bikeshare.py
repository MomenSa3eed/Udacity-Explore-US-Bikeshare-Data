# import packages
import time
import pandas as pd

# define variables
city_data = {"chicago": "chicago.csv",
             "new york city": "new_york_city.csv",
             "washington": "washington.csv"}
months = ["all", "january", "february", "march", "april", "may", "june"]
days = ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]


def percentage(df, x):
    """
    Calculate the percentage of a value from the total rounded to two decimal points
    Args:
        df - Pandas DataFrame containing the information
        (str) x - name of the value to calculate percentage for
    Returns:
        (float) perc - percentage of the value from the total
    """
    perc = round((df[x].value_counts().max() / df[x].value_counts().sum()) * 100.0, 2)
    return perc


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print("Hello! Let's explore some US bikeshare data!")

    # get user input for city (chicago, new york city, washington)
    while True:
        city = input("Please enter the name of the city to explore \n"
                     "(Chicago, New York City, Washington): ").strip().lower()
        if city not in city_data.keys():
            print("Sorry, Please enter a valid city name.")
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Please enter the name of the month to filter by (january, february, ... , june)\n"
                      "or enter 'all' to apply no month filter: ").strip().lower()
        if month not in months:
            print("Sorry, Please enter a valid month name.")
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Please enter the name of the day of week to filter by (monday, tuesday, ... , sunday)\n"
                    "or enter 'all' to apply no day filter: ").strip().lower()
        if day not in days:
            print("Sorry, Please enter a valid day name.")
        else:
            break

    print("-"*40)
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

    # load data file into a dataframe
    data = pd.read_csv(city_data[city])
    # take a copy the original data to preserve the integrety of the original data
    df = data.copy()

    """
    RECOMMENDATION: before we start analyzing the data, I think we should do the following tasks:
    (1) Rename the dataframe columns to avoid spaces in the column name. ex. Start_Time, Trip_Duration, ...etc.
    (2) Clean the Data by Delete/Estimate NAN values in the dataset. ex. Gender, Birth Year (70 NAN Each).
    """

    # convert the Start Time column to datetime
    df["Start Time"] = pd.to_datetime(df["Start Time"])

    # extract month and day of week from Start Time column and create new columns
    df["month"] = df["Start Time"].dt.month_name()
    df["day_of_week"] = df["Start Time"].dt.day_name()

    # filter the dataframe by month (if applicable)
    if month != "all":
        df = df[df["month"] == month.title()]

    # filter the dataframe by day of week (if applicable)
    if day != "all":
        df = df[df["day_of_week"] == day.title()]
    print("\nAlright! You filtered {} data by {} month(s) and by {} day(s), \n"
          "Here is your filtered data\n".format(city.title(), month.title(), day.title()))
    print(df)
    print("-"*40)
    return data, df


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.
    """

    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

    # display the most common month
    popular_month = df["month"].mode()[0]
    popular_month_perc = percentage(df, "month")
    print("The most common month of travel is: {}, recorded {}% of total."
          .format(popular_month, popular_month_perc))

    # display the most common day of week
    popular_day = df["day_of_week"].mode()[0]
    popular_day_perc = percentage(df, "day_of_week")
    print("\nThe most common day of week of travel is: {}, recorded {}% of total."
          .format(popular_day, popular_day_perc))

    # display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df["hour"] = df["Start Time"].dt.hour

    # find the most common hour (from 0 to 23)
    popular_hour = df["hour"].mode()[0]
    popular_hour_perc = percentage(df, "hour")
    print("\nThe most common hour of travel is: {}, recorded {}% of total."
          .format(popular_hour, popular_hour_perc))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-"*40)


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.
    """

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # display most commonly used start station
    popular_st_station = df["Start Station"].mode()[0]
    popular_st_station_perc = percentage(df, "Start Station")
    print("The most commonly used start station is: {}, recorded {}% of total."
          .format(popular_st_station, popular_st_station_perc))

    # display most commonly used end station
    popular_end_station = df["End Station"].mode()[0]
    popular_end_station_perc = percentage(df, "End Station")
    print("\nThe most commonly used end station is: {}, recorded {}% of total."
          .format(popular_end_station, popular_end_station_perc))

    # display most frequent combination of start station and end station trip
    # combine start station and end station to create a new column
    df["Start End Station"] = df["Start Station"] + " --- " + df["End Station"]

    popular_st_end = df["Start End Station"].mode()[0]
    popular_st_end_perc = percentage(df, "Start End Station")
    print("\nThe most commonly used start/end station is: {}, recorded {}% of total."
          .format(popular_st_end, popular_st_end_perc))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-"*40)


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.
    """

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    # display total travel time
    travel_time = df["Trip Duration"].sum()/3600.0
    print("The total trips travel time is: {} hours.".format(travel_time.round(2)))

    # display mean travel time
    mean_travel_time = df["Trip Duration"].mean()/60.0
    print("\nThe average trip travel time is: {} minutes.".format(mean_travel_time.round(2)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-"*40)


def user_stats(city, df):
    """
    Displays statistics on bikeshare users.
    """

    print("\nCalculating User Stats...\n")
    start_time = time.time()

    # display counts for each user type
    user_types = df["User Type"].value_counts()
    perc = percentage(df, "User Type")
    print("The counts for each user type are:\n{}"
          "\n{} recorded {}% of total, while {} recorded {}% of total."
          .format(user_types, user_types.index[0], perc, user_types.index[1], round((100 - perc), 2)))

    # display counts of gender
    if city != "washington":
        gender_types = df["Gender"].value_counts()
        perc = percentage(df, "Gender")
        print("\nThe counts for each gender are:\n{}"
              "\n{} recorded {}% of total, while {} recorded {}% of total."
              .format(gender_types, gender_types.index[0], perc, gender_types.index[1], round((100 - perc), 2)))
    else:
        print("\nThere is no available gender data for", city.title())

    # display earliest, most recent, and most common year of birth
    if city != "washington":
        early_yob = int(df["Birth Year"].min())
        recent_yob = int(df["Birth Year"].max())
        popular_yob = int(df["Birth Year"].mode()[0])

        # extract year from the Start Time column to calculate the age
        year = df["Start Time"].dt.year.mode()[0]

        print("\nThe oldest year of birth is: {}, with an Age of {} years at the trip time!"
              .format(early_yob, year - early_yob))
        print("\nThe youngest year of birth is: {}, with an Age of {} years at the trip time!"
              .format(recent_yob, year - recent_yob))
        print("\nThe most common year of birth is: {}, with an Age of {} years at the trip time!"
              .format(popular_yob, year - popular_yob))
    else:
        print("\nThere is no available birth year data for", city.title())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-"*40)


def raw_data(data):
    """
    Displays raw data upon request by the user.
    """

    for i in range(0, len(data), 5):
        display = input("Would you like to display 5 rows of raw data? yes/no \n")
        if display.lower() != "yes":
            break
        else:
            print(data[i:i+5])


def main():
    while True:
        city, month, day = get_filters()
        data, df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(city, df)
        raw_data(data)

        restart = input("\nWould you like to explore another city? yes/no \n")
        if restart.lower() != "yes":
            print("That was fun! Thank you.")
            break


if __name__ == "__main__":
    main()
