# Importing necessary modules and libraries:
import yfinance as yf
import numpy as np
import pandas
import sys
from scipy import stats


def access_data():
    """
    This function accesses the current share price of Ilica plc.
    """
    ticker = yf.Ticker('IKA.L').info
    current_price = ticker['regularMarketPreviousClose']
    print(f'Current Ilika share price is...{current_price} p\n')
    return current_price


def historical_data():
    """
    This function extracts a historical share price on the day of acquisition.
    """
    confirm = None
    while confirm != "y":
        print('Enter the date of stock aquisition.\n')
        print('Date format is YYYY-MM-DD (e.g. 2024-01-05).\n')
        acquisition_day = input("\n")
        print(f"Is the date {acquisition_day} correct? y/n\n")
        confirm = input("\n")
    print("Retrieving share price on that day...\n")
    acuisition_day_price = yf.download("IKA.L", 2010-5-14, acquisition_day)
    csv_export = acuisition_day_price.tail()
    csv_export.to_csv("ilika.csv")
    with open("ilika.csv", "r", encoding="utf-8", errors="ignore") as temp:
        final_line = temp.readlines()[-1]
    final_line = final_line.split(",")
    historical_share_price = float(final_line[5])
    print(f"Share price on {acquisition_day} is:\n")
    print(f"{int(historical_share_price)} p.\n")
    return historical_share_price


def calculate_ROI(current_price, historical_share_price):
    """
    The function calculates return on investment (ROI)
    from share price on the day of acquisition and todays price.
    """
    return_on_investment = int((current_price -
                                historical_share_price) * 100
                               / historical_share_price)
    print(f'Today\'s ROI would be {return_on_investment}%\n')
    if return_on_investment <= 0:
        print('\n')
        print('You are loosing money.\n')
        print('ROI is below 0, not a good day to sell.\n')
    else:
        print('\n')
        print('The sell would be profitable.\n')
        print('Do not forget to add broker\'s commission to the bill.\n')


def data_for_lin_fit():
    """
    The function selects the historical range of share price
    data for futher linear regression analysis.
    """
    while True:
        confirm = None
        while confirm != 'y':
            print('Enter the starting date in a period you want to check.\n')
            print('Date format is yyyy-mm-dd (e.g. 2020-05-15).\n')
            print('The program will issue an error message\n')
            print('if you enter the latest date first.\n')
            date1 = input('\n')
            print(f'Is the date {date1} correct? y/n')
            confirm = input('\n')
        print('\n')
        confirm = None
        while confirm != 'y':
            print('Enter the ending date in the period you want to check.\n')
            print('Date format is yyyy-mm-dd (e.g. 2020-05-15).\n')
            print('The program will issue an error message\n')
            print('if you enter the starting or earlier date instead.\n')
            date2 = input("\n")
            print(f"Is the date {date2} correct? y/n")
            confirm = input("\n")
        days = np.busday_count(date1, date2)
        print('\n')
        print(f'Specified period includes {days} market days.\n')
        if validate_period(days):
            break
    if days < 5:
        print('The period is less than 5 days. Not enough data.\n')
        print('Suitable range is between 5 and 15 working days.\n')
        print('The linear analysis may be unreliable.\n')
    if days > 20:
        print('The selected period is long.\n')
        print('Suitable range is between 5 and 15 working days.\n')
        print('The linear model may be disrupted by unpredictable events\n')
        print('such as dividend payment, company announcements,\n')
        print('missed financial targets or change of CEO.\n')
        print('(consult www.ilika.com for updates).\n')
    else:
        print('\n')
        print('Retrieving historical share price for the selected period...\n')
    historical_range_close = yf.download("IKA.L", date1,
                                         date2, interval="1d")['Close']
    historical_range_close.to_csv('ilika_selected_range_close.csv')


def validate_period(time_span):
    """
    The function generates an error message if the number
    of working days in a required period is 0 or negative.
    """
    try:
        if time_span <= 0:
            raise ValueError('The number of market days is 0 or negative.\n')
    except ValueError as e:
        print(f'Invalid data: {e}, please try again.\n')
        return False
    return True


def linear_regr():
    """
    The function accesses file closure share price for the period defined
    in function data_for_lin_fit() and converts it into the list format
    suitable for linear regression analysis.
    """
    close = pandas.read_csv("ilika_selected_range_close.csv", header=0)
    list_close = list(close.Close)
    i = 0
    day_number = []
    while i < len(list_close):
        i = i + 1
        day_number.append(i)
    print('Running linear fit...\n')
    slope_close, intercept_close, r_close, p_close, \
        std_err_close = stats.linregress(day_number, list_close)
    print('Checking applicability of linear model for selected range...\n')
    r_close_abs = abs(r_close)
    if r_close_abs >= 0.7:
        print(f'Correlation coefficient is {r_close_abs}.\n')
        print('For numbers above 0.7 the model can be trusted.\n')
        print('Extracting model parameters...\n')
        if slope_close <= 0:
            print('The market is bearish. Buying is not recommended.\n')
        else:
            print('The market is bullish. Selling is not recommended\n')
    else:
        print('Correlation coefficient is below 0.7.\n')
        print('Linear correlation is poor. Proceed with caution.\n')
        if slope_close <= 0:
            print('The market is bearish.\n')
            print('Buying is not advised, but the model is not suitable.\n')
            print('Other parameters must be checked.\n')
        else:
            print('The market is bullish.\n')
            print('Selling is not advised, but the model is not suitable\n')
            print('Other parameters must be checked.\n')


def stay_or_exit():
    """
    Offers options: continue or leave program.
    """
    print('Would you like to contonue?\n')
    response = input('Type y or n and press ENTER...\n')
    if response == "y":
        main()
    elif response == "n":
        sys.exit('Exiting the code. See you later.\n')
    else:
        print('The answer is not recognised. The app will run again.\n')
        print('Abort by pressing Ctrl-C on Windows or Crts-Z on Linux.\n')
        main()


def main():
    """
    Run all program functions.
    """
    current_price = access_data()
    historical_share_price = historical_data()
    calculate_ROI(current_price, historical_share_price)
    data_for_lin_fit()
    linear_regr()
    stay_or_exit()


print('Welcome to the "Equity Stock Pulse Check2 project.\n')
print('This little tool will calculate Return on Investment (ROI)\n')
print('for your Ilika Technologies Ltd share stock\n')
print('based on the date of acquisition and current share price.\n')
print('It will also suggest sell/buy strategy.\n')
print('DISCLAIMER: The algorithm does not take into account unpredictable\n')
print('events, such as breaking news or paiment of dividends.\n')
print('THE RESULTS CANNOT BE TREATED AS A LEGAL FINANCIAL ADVICE.\n')

input('Press Enter to continue...\n')

print('Starting the program...\n')
print('Retrieving the latest share price of Ilika Technologies Ltd...\n')
print('This may take few seconds...\n')

main()
