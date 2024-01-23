import yfinance as yf
#import csv

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
        print('You are loosing money, ROI is below 0, not a good day to sell')
    else:
        print("The sell would be profitable, but do not forget to add the broker\'s commission to the bill")
    return return_on_investment

def access_month_back():
    one_month_historical_close = yf.download("IKA.L", period="1mo")['Close']
    one_month_historical_volume = yf.download("IKA.L", period="1mo")['Volume']
    print(one_month_historical_close)
    print(one_month_historical_volume)
    return one_month_historical_close, one_month_historical_volume

def linear_extrapolation():
    """
    The function extrapolates linearly one-month (from now) share price and traded volume data and shows the trend (bullish or bearish).
    """


def main():
    """
    Run all program functions
    """
    current_price = access_data()
    historical_share_price = historical_data()
    calculate_ROI(current_price, historical_share_price)
    linear_extrapolation(access_month_back())


print("Welcome to the 'Equity Stock Pulse Check' project.\nThis little tool will calculate Return on Investment (ROI) for your share stock based on the date of acquisition and current share price.\nIt will also suggest cell/buy strategy deduced from five-day (tail) share price and traded volume extrapolation.\nDISCLAIMER: The algorithm does not take into account unpredictable events, such as breaking news or paiment of dividends.\nTHE RESULTS CANNOT BE TREATED AS A LEGAL FINANCIAL ADVICE.\n")


print('Press Enter to continue...')

input()

main()

