import pandas as pd
from yahoo_earnings_calendar import YahooEarningsCalendar
from Company import Company
import datetime
from openpyxl import load_workbook


def generate_ticker_list(start_date, end_date):
        # collect all companies included on yahoo's earnings calender for the given range

        # adapt inputs into datatime objects
        date_from = datetime.datetime(*start_date, 0, 0, 1)
        date_to = datetime.datetime(*end_date, 23, 59, 59)

        companies = pd.DataFrame(YahooEarningsCalendar().earnings_between(date_from, date_to))

        # create new excel file
        writer = pd.ExcelWriter("output/report.xlsx")

        #write this list into a sheet on excel file
        companies.to_excel(writer, 'Stocks Found')

        writer.save()

        return [ticker for ticker in companies['ticker']]


def save_sheet(ticker, key):


        # create company object to collect data
        company = Company(ticker, key)
        
        print("\n" + ticker + "\n")

        # create excel writer on existing sheet
        book = load_workbook("output/report.xlsx")
        writer = pd.ExcelWriter("output/report.xlsx", engine='openpyxl')
        writer.book = book

        company.load_data()
        df = company.to_dataframe()
        df.columns = ['Current', '1YA', '2YA']
        df.to_excel(writer, ticker)

        writer.save()