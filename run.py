# Importing necessary modules and libraries:
from datetime import datetime, date
from dateutil.parser import parse
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
    print('Enter the date of stock aquisition.\n')
    return current_price

def date_input_validate():
    """
    Get the data from the user.
    Validate data: i) check date format is correct
    ii)  check if the date of the stock acquisition is in a correct period
    (i.e. not before the IPO and not in the future). 
    """    
    ipo = '2010-05-17'
    while True:
        print('Date format is YYYY-MM-DD (e.g. 2024-01-05):\n')
        date = input('\n')
        print('\n')
        try:
            parse(date, fuzzy=False, yearfirst=True, dayfirst=False)
            days = np.busday_count(date, datetime.today().strftime('%Y-%m-%d'))
            range = np.busday_count(ipo, datetime.today().strftime('%Y-%m-%d'))
            if days > 0 and days < range:
                break
            else:
                print('Check the date format and period of acquisition.\n')
                print('Must be between IPO and the most\n')
                print('recent closed market day.\n')
        except ValueError:
            print('Invalid input. Try again.\n')
        next_step = input('Enter y to continue, or any other key to quit.\n')
        if next_step == 'y':
            print('...\n')
        else:
            exit('Program stopped.\n')
    return date


def historical_data(date):
    """
    This function extracts a historical share price on the day of acquisition.
    """
    print("Retrieving historical share price...\n")
    acquisition_date_price = yf.download("IKA.L", 2010-5-17, date, progress=False)
    csv_export = acquisition_date_price.tail()
    csv_export.to_csv("ilika.csv")
    with open("ilika.csv", "r", encoding="utf-8", errors="ignore") as temp:
        final_line = temp.readlines()[-1]
    final_line = final_line.split(",")
    historical_share_price = float(final_line[5])
    print('========================================\n')
    print(f'Share price on {date} is: {int(historical_share_price)} p.\n')
    return historical_share_price


def calculate_ROI(current_price, historical_share_price):
    """
    The function calculates return on investment (ROI)
    from share price on the day of acquisition and todays price.
    """
    return_on_investment = int((current_price -
                                historical_share_price) * 100
                               / historical_share_price)
    print(f'Today\'s ROI would be: {return_on_investment}%\n')
    if return_on_investment <= 0:
        print('You are loosing money.\n')
        print('ROI is below 0, not a good day to sell.\n')
    else:
        print('The sell would be profitable.\n')
        print('Do not forget to add broker\'s commission to the bill.\n')
    print('----------------------------------------\n')
    input('Press Enter to continue...\n')


def data_for_lin_fit():
    """
    The function selects the historical range of share price
    data for futher linear regression analysis.
    """
    print('You can now apply the linear regression fit\n')
    print('to analyse stock behaviour in a specified period.\n')
    print('The most reliable period duration is 5 to 15 market days')
    print('----------------------------------------\n')
    input('Press Enter to continue...\n')
    while True:
        print('Enter an initial date of period\n')
        print('you want to analyse.\n')        
        date_init = date_input_validate()
        print('Enter a final date of period\n')
        print('you want to analyse.\n')        
        date_end = date_input_validate()        
        days = np.busday_count(date_init, date_end)    
        print(f'Specified period includes {days} market days.\n')
        if validate_period(days):
            break
    if days < 5:
        print('The period is less than 5 days. Not enough data.\n')
        print('Suitable range is between 5 and 15 working days.\n')
        print('The linear analysis may be unreliable.\n')
    elif days > 20:
        print('The selected period is long.\n')
        print('Suitable range is between 5 and 15 working days.\n')
        print('The linear model may be disrupted by unpredictable events\n')
        print('such as dividend payment, company announcements,\n')
        print('missed financial targets or change of CEO.\n')
        print('(consult www.ilika.com for updates).\n')
    else:
        print('Retrieving historical share price for the selected period...\n')
    historical_range_close = yf.download("IKA.L", date_init,
                                         date_end, interval="1d", progress=False)['Close']
    historical_range_close.to_csv('ilika_selected_range_close.csv')


def validate_period(time_span):
    """
    The function generates an error message if the number
    of working days in a required period is 0 or negative.
    """
    try:
        if time_span <= 1:
            raise ValueError('The number of market days is 1 or 0 or negative,\n')
    except ValueError as e:
        print(f'Invalid data: {e} please try again.\n')
        return False
    return True


def linear_regr():
    """
    The function accesses file closure share price for the period defined
    in function data_for_lin_fit() and converts it into the list format
    suitable for linear regression analysis.
    """
    print('========================================\n')
    input('Press Enter to continue...\n')
    close = pandas.read_csv("ilika_selected_range_close.csv", header=0)
    list_close = list(close.Close)
    i = 0
    day_number = []
    while i < len(list_close):
        i = i + 1
        day_number.append(i)
    print('Running linear fit...\n')
    slope_close, intercept_close, r_close, p_close, std_err_close = stats.linregress(day_number, list_close)
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
    date_of_acquisition = date_input_validate()
    historical_share_price = historical_data(date_of_acquisition)
    calculate_ROI(current_price, historical_share_price)
    data_for_lin_fit()
    linear_regr()
    stay_or_exit()


print('Welcome to the "Equity Stock Pulse Check" project.\n')
print('This little tool will calculate Return on Investment (ROI)\n')
print('for your Ilika Technologies Ltd share stock\n')
print('based on the date of acquisition and current share price.\n')

input('Press Enter to continue...\n')

print('It will also suggest sell/buy strategy.\n')
print('DISCLAIMER: The algorithm uses linear regression and\n')
print('does not take into account unpredictable\n')
print('events, such as breaking news or payment of dividends.\n')
print('THE RESULTS CANNOT BE TREATED AS A LEGAL FINANCIAL ADVICE.\n')

input('Press Enter to continue...\n')

print('Starting the program...\n')
print('Retrieving the latest share price of Ilika Technologies Ltd...\n')
print('This may take few seconds...\n')

main()
