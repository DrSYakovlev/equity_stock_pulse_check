import yfinance as yf
import csv

def access_data():
    """
    This function accesses the current share price of Ilica plc.
    """
    
    ticker = yf.Ticker('IKA.L').info    
    current_price = ticker['regularMarketPreviousClose']
    print(f'Current Ilika share price is...{current_price} p')
    return current_price

def estimate_ROI ():
    """
    This function calculates the current return-on-investment (ROI) calculated from the day of the stock acquisition.
    """
    print ('Enter the day of stock aquisition.\nThe day must be provided in a format  YYYY-MM-DD (e.g. 2024-01-05)')
    acquisition_day = input()
    print('Retrieving current data info...')
    acuisition_day_price = yf.download("IKA.L", 2010-5-14, acquisition_day)
    csv_export = acuisition_day_price.tail()
    print(csv_export)    
    csv_export.to_csv("ilika.csv")
    file = open('ilika.csv')
    with open("ilika.csv", "r", encoding="utf-8", errors="ignore") as scraped:
        final_line = scraped.readlines()[-1]
        print(final_line)
        print(type(final_line))
        #final_line = final_line.split
        historicac_share_price = final_line[5]
        print(historicac_share_price)

        


def main():
    """
    Run all program functions
    """
    access_data()
    estimate_ROI()



print("Welcome to the 'Equity Stock Pulse Check' project.\nThis little tool will calculate Return on Investment (ROI) for your share stock based on the date of acquisition and current share price.\nIt will also suggest cell/buy strategy deduced from five-day (tail) share price and traded volume extrapolation.\nDISCLAIMER: The algorithm does not take into account unpredictable events, such as breaking news or paiment of dividends.\nTHE RESULTS CANNOT BE TREATED AS A LEGAL FINANCIAL ADVICE.\n")

print('Press Enter to continue...')

input()

main()

