# Equity Stock Pulse Check Project

## Introduction

Welcome to the Equity Stock Pulse Check Project. This CLI-based program extracts current share price from yfinance external sourse. It also asks the user to provide the day of the equity purchase, obtains historical share price and calculates ROI (Return on Investment). As an example to work with I took Ilika Technologies Ltd (the author was an employee there for many years and is familiar with current and historical trends). Based on ROI, the program suggests if it would be profitable to sell your shares today. The programme will also prompt you to enter starting and final dates of the period of time (not necessarily the most recent), run linear regression analysis and conclude if the market was bearish or bullish. It will also check an applicability of the linear model and warn the user if the results can be trusted.

![Introduction](./images/intro.jpg "Introduction_message")

## How to use

1. Hit Enter when asked.

The program will immediately show the most recent available share price. I took the value, corresponding to closure of the latest trading session.

![Current_share_price](./images/current_share_price.jpg "Current_share_price")

2. Enter the date of the equity acquisition when prompted.

![Date_of_equity_acquisition](./images/roi_and_hist_share_price.jpg "Enter_equity_acquisition_date")

The program will print an extra message from the external yfinance library, historical share price and return on investment (ROI) if you were to decide cell today.

3. Enter the starting and ending dates of the period you want to analise.

The dates must be provided in the required format (also in step 2). The program will generate an error message if you provide beginning and ending days in a different order.

![Enter_dates_error_message](./images/error_message.jpg "Enter_dates_error_message")

If the dates enterred in a correct order, the program will run linear regression analysis and print outcome.

![Analysis](./images/analysis.jpg "Analysis")

4. Choose if you want to quit or continue.

## Future features

1. Add possibility to select various tickers (other stock portfolia)
2. Add possibility to select share price form "open", "high", "low" and "closure" for more accurate short-term data analysis.
3. Validate date format.
4. Add possibility to compile imported data and analysis results into a single spreadsheet (e.g. *.xlsx).

## Data structure

In this project, I used a set of defined functions, each with unique task to perform and single return. The flow runs through several if-else structures, selecting appropriate outcome. The functions are assembled in main() function, which is called at the end of code. The program uses several external libraries.

![external](./images/libraries.jpg "external")

The program creates *.csv files in working directory and use them to store imported data.

## Testing

The code was manually tested by providint different dates and monitoring if the generated outcome is appropriate.

The code was supplied to PEP8 validator. The validator indicates few issues with the code which the author is completely aware of:

1. The first print() command appears above import block. It is done on purpose. It takes a while to retrieve the data from yfinance library. The user may get an impression the the code is frozen or stuck. I wanted to print the message that the step could take few seconds.
2. Some strings in printed messages are two long. I supplied enough of "new line" characters to prevent broken words and keep text tidy.

## Remaining bugs

The main bug the author could not fix in the context of this work is date format validation. There is an error message generator only testing the validity of time interval (period, e.g. negative number of business days). It seems that used library (yfinance) strictly adheres to its own format YYYY-MM-DD and generates an error if it is wrong. The warning message was added, but the program tend to restart if the date format is incorrect.

## Plagiarism

The author confirms that the project represents an origional work.

## Development and deployment

## Credits

Deployment terminal and project template were provided by Code Institute.











