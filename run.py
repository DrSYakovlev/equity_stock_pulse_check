print("Starting the program...\n")
#Importing necessary modules and libraries:
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
    This function extracts the historical share price on the day of acquisition.
    """
    confirm = None
    while confirm != "y":
        print('Enter the date of stock aquisition.\nThe date must be provided in a format  YYYY-MM-DD (e.g. 2024-01-05).\nEnterringincorrect data may result in a program crash.\n')
        acquisition_day = input("\n")
        print(f"Is the date {acquisition_day} correct? y/n")
        confirm = input("\n")
    print("Retrieving share price on that day...\n")
    acuisition_day_price = yf.download("IKA.L", 2010-5-14, acquisition_day)
    csv_export = acuisition_day_price.tail()
    csv_export.to_csv("ilika.csv")
    with open("ilika.csv", "r", encoding="utf-8", errors="ignore") as temp:
        final_line = temp.readlines()[-1]
    final_line = final_line.split(",")
    historical_share_price = float(final_line[5])
    print(f"Share price on {acquisition_day} is {int(historical_share_price)} p.\n")
    return historical_share_price


def calculate_ROI(current_price, historical_share_price):
    """
    The function calculates return on investment (ROI) from share price on the day of acquisition and todays price
    """
    return_on_investment = int((current_price - historical_share_price) * 100 / historical_share_price)
    print(f'Today\'s ROI would be {return_on_investment}%')
    if return_on_investment <= 0:
        print("")
        print('You are loosing money, ROI is below 0, not a good day to sell.\n')
    else:
        print("")
        print("The sell would be profitable, but do not forget to add the broker\'s commission to the bill.\n")


def data_for_lin_fit():
    """
    The function selects the historical range of share price data for futher linear regression analysis.
    """
    while True:
        confirm = None
        while confirm != "y":
            print("Enter the first (the earliest) date in the period you want to analyse.\nThe date must be entered in format yyyy-mm-dd (e.g. 2020-05-15).\nEnterring incorrect date may result in a program crash.\nThe program will issue an error message if you enter the latest date first.")
            date1 = input("\n")
            print(f"Is the date {date1} correct? y/n")
            confirm = input("\n")
        print("")
        confirm = None
        while confirm != "y":
            print("Enter the second (the latest) date in the period you want to analyse.\nThe date must be entered in format yyyy-mm-dd (e.g. 2020-05-15).\nEnterring incorrect date may result in a program crash.\nThe program will issue an error message if you enter the starting date instead.")
            date2 = input("\n")
            print(f"Is the date {date2} correct? y/n")
            confirm = input("\n")
        days = np.busday_count(date1, date2)
        print("")
        print(f"Specified period includes {days} market days.\n")
        if validate_period(days):
            break
    if days < 5:
        print("The period is less than 5 days.\nThe data are not enough and the analysis may be unreliable.\nSuitable range is between 5 and 15 working days.\n")
    if days > 20:
        print("The selected period is long.\nThe linear model may be disrupted by unpredictable events,\nsuch as dividend payment, company announcements,\nchange of CEO and other major changes\n(consult www.ilika.com for the details).\n")
    else:
        print("")
        print("Retrieving share price and volume data for the selected period...\n")
    historical_range_close = yf.download("IKA.L", date1, date2, interval="1d")['Close']
    historical_range_close.to_csv('ilika_selected_range_close.csv')


def validate_period(time_span):
    """
    The function generates an error message if the number of working days in a required period is 0 or negative.
    """
    try:
        if time_span <= 0:
            raise ValueError('Check your input. The number of working days in the period is 0 or negative')
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False
    return True


def linear_regr():
    """
    The function accesses file closure share price for the period defined in function data_for_lin_fit() and converts it into the list format (suitable for linear regression analysis).
    """
    close = pandas.read_csv("ilika_selected_range_close.csv", header=0)
    list_close = list(close.Close)
    i = 0
    day_number = []
    while i < len(list_close):
        i = i + 1
        day_number.append(i)
    print("Running linear fit...\n")
    slope_close, intercept_close, r_close, p_close, std_err_close = stats.linregress(day_number, list_close)
    print("Checking applicability of linear model for selected range...\n")
    r_close_abs = abs(r_close)
    if r_close_abs >= 0.7:
        print(f"Correlation coefficient is {r_close_abs}.\nFor numbers above 0.7 the model can be trusted.\nExtracting model parameters...\n")
        if slope_close <= 0:
            print("The market is bearish.\nBuying is not recommended")
        else:
            print("The market is bullish.\nSelling is not recommended")
    else:
        print("Linear correlation is poor.\nCorrelation coefficient is below 0.7.\nThe results are not trustable.\nProceed with caution.\n")
        if slope_close <= 0:
            print("The market is bearish.\nBuying is not recommended,\nbut the linear model is not suitable\nand other parameters must be checked.\n")
        else:
            print("The market is bullish.\nSelling is not recommended,\nbut the linear model is not suitable\nand other parameters must be checked.\n")


def stay_or_exit():
    response = input("Would you like to contonue?\nType y or n and press ENTER...\n")
    if response == "y":
        main()
    elif response == "n":
        sys.exit("Exiting the code")
    else:
        print("An answer is not recognised. The app will run again.\nYou can abort an execution by pressing Ctrl-C on Windows or Crts-Z on Linux.\n")
        main()


def main():
    """
    Run all program functions
    """
    current_price = access_data()
    historical_share_price = historical_data()
    calculate_ROI(current_price, historical_share_price)
    data_for_lin_fit()
    linear_regr()
    stay_or_exit()


print("Welcome to the 'Equity Stock Pulse Check' project.\n")
print("This little tool will calculate Return on Investment (ROI)\n")
print("for your Ilika Technologies Ltd share stock\n")
print("based on the date of acquisition and current share price.\n")
print("It will also suggest cell/buy strategy.\n")
print("DISCLAIMER: The algorithm does not take into account unpredictable\n")
print("events, such as breaking news or paiment of dividends.\n")
print("THE RESULTS CANNOT BE TREATED AS A LEGAL FINANCIAL ADVICE.\n")

input('Press Enter to continue...\n')

print("Retrieving the latest share price of Ilika Technologies Ltd...\n")
print("This may take few seconds...\n")

main()
