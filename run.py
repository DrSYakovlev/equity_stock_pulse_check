import yfinance as yf
import numpy as np


def access_data():
    """
    This function accesses the current share price of Ilica plc.
    """
    
    ticker = yf.Ticker('IKA.L').info    
    current_price = ticker['regularMarketPreviousClose']
    print(f'Current Ilika share price is...{current_price} p')
    return current_price

def historical_data():
    """
    This function extracts the historical share price on the day of acquisition.
    """
    print ('Enter the day of stock aquisition.\nThe day must be provided in a format  YYYY-MM-DD (e.g. 2024-01-05)')
    acquisition_day = input()
    print('Retrieving current data info...')
    acuisition_day_price = yf.download("IKA.L", 2010-5-14, acquisition_day)
    csv_export = acuisition_day_price.tail()
    print(csv_export)    
    csv_export.to_csv("ilika.csv")
    #open('ilika.csv')
    with open("ilika.csv", "r", encoding="utf-8", errors="ignore") as temp:
        final_line = temp.readlines()[-1]
        print(final_line)
        print(type(final_line))
        final_line = final_line.split(",")
        historical_share_price = float(final_line[5])
        print(historical_share_price)
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
        print("The sell would be profitable, but do not forget to add the broker\'s commission to the bill\n")
    return return_on_investment

def data_for_lin_fit():
    """
    The function selects the historical range of share price data for futher linear regression analysis.
    """
    while True:
        print("Enter the first (the earliest) date in the period you want to analyse. The date bust be entered in format yyyy-mm-dd (e.g. 2020-05-15)\n")
        date1 = input()
        print("Enter the second (the latest) date in the period you want to analyse. The date bust be entered in format yyyy-mm-dd (e.g. 2020-05-15)\n")
        date2 = input()
        days = np.busday_count(date1, date2)

        if validate_period(days):
            break
    if days < 5:
        print("The period is less than 5 days. The data is not enough for and the analysis may be unreliable. Suitable range is between 5 and 15 working days.\n")
    if days > 20:
        print("The selected period is long. The linear model may be disrupted by unpredictable events, such as dividend payment, company announcement, change of CEO and other major changes (consult www.ilika.com for the details).\n")
    else:
        print('Number of business days is:', days)
        print("")
        print ("Retrieving share price and volume data for the selected period...\n")
    historical_range_close = yf.download("IKA.L", date1, date2, interval="1d")['Close']
    historical_range_volume = yf.download("IKA.L", date1, date2, interval="1d")['Volume']
    historical_range_close.to_csv('ilika_selected_range_close.csv')
    historical_range_volume.to_csv('ilika_selected_range_volume.csv')

def validate_period(time_span):
    """
    The function generates an error message if the number of working days in a required period is 0 or negative.
    """
    try:
        if time_span <= 0:        
            raise ValueError(f'Check your input. The number of working days in the period is 0 or negative')
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False
    return True    

def main():
    """
    Run all program functions
    """
    current_price = access_data()
    historical_share_price = historical_data()
    calculate_ROI(current_price, historical_share_price)
    data_for_lin_fit()

print("Welcome to the 'Equity Stock Pulse Check' project.\nThis little tool will calculate Return on Investment (ROI) for your Ilika Technologies Ltd share stock based on the date of acquisition and current share price.\nIt will also suggest cell/buy strategy deduced from historical data range (defined by the user) of share price and traded volume extrapolation.\nDISCLAIMER: The algorithm does not take into account unpredictable events, such as breaking news or paiment of dividends.\nTHE RESULTS CANNOT BE TREATED AS A LEGAL FINANCIAL ADVICE.\n")


print('Press Enter to continue...')

input()

main()

