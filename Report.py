import pandas as pd
from yahoo_earnings_calendar import YahooEarningsCalendar
from Company import Company
import datetime

class Report():

    def __init__(self, start_date, end_date):

        # create excel writer that will track changes
        self.writer = pd.ExcelWriter("output/report.xlsx")
        self.start_date = start_date
        self.end_date = end_date

        #generate and save ticker list from earnings calender

        self.tickers = self.generate_ticker_list()


    def generate_ticker_list(self):
        # collect all companies included on yahoo's earnings calender for the given range

        # adapt inputs into datatime objects
        date_from = datetime.datetime(*self.start_date, 0, 0, 1)
        date_to = datetime.datetime(*self.end_date, 23, 59, 59)

        companies = pd.DataFrame(YahooEarningsCalendar().earnings_between(date_from, date_to))

        #write this list into a sheet on excel file
        companies.to_excel(self.writer, 'Stocks Found')

        company_data = {}

        #format data 

        tickers = companies['ticker']
        shortNames = companies['companyshortname']
        dates = companies['startdatetime']

        for i in range(len(tickers)):
            company_data[tickers[i]] = {'shortName': shortNames[i], 'date': dates[i][:10:]}

        return company_data


    def produce_excel(self, key):
        # create one company object and keep reloading data save on memory

        company = Company('', key)
        for ticker in self.tickers:
            print("\n" + ticker + "\n")

            # generate header with basic data
            header = pd.DataFrame(
                {
                    'Stock': [self.tickers[ticker]['shortName']],
                    'Ticker': [ticker],
                    'Date': [self.tickers[ticker]['date']]
                } 
            )

            header.to_excel(self.writer, ticker, index=False)

            company.reload(ticker)
            df = company.to_dataframe()
            df.columns = ['Current', '1YA', '2YA']
            df.to_excel(self.writer, ticker, startrow=3)

        self.writer.save()
            
        