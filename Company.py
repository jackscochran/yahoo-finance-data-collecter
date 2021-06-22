import requests
import json
import pandas as pd

class Company():

    def __init__(self, ticker, key):
        
        self.ticker = ticker
        self.data = {}
        self.key = key
    
    def load_data(self):

        # ------- get Financail API ------#
        url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-financials"
    
        querystring = {"symbol": self.ticker}
        
        headers = {
            'x-rapidapi-key': self.key,
            'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
        }
        
        response = requests.request("GET", url, headers=headers, params=querystring).text
        response = json.loads(response)

        #----------get EPS from summary ---------#

        url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-summary"

        summary_response = requests.request("GET", url, headers=headers, params=querystring).text
        summary_response = json.loads(summary_response)

        # ----------Extract data --------------#
        for years_ago in range(3):

            self.data[years_ago] = {}

            adresses = {
                'financialAPI': {
                    'sharePrice': ['price', 'regularMarketPrice', 'raw'],
                    'marketCap': ['price', 'marketCap', 'raw'],
                    'totalRevenue': ['incomeStatementHistory', 'incomeStatementHistory', years_ago, 'totalRevenue', 'raw'],
                    'grossProfit': ['incomeStatementHistory', 'incomeStatementHistory', years_ago, 'grossProfit', 'raw'],
                    'operatingIncome': ['incomeStatementHistory', 'incomeStatementHistory', years_ago, 'operatingIncome', 'raw'],
                    'netIncome': ['incomeStatementHistory', 'incomeStatementHistory', years_ago, 'netIncome', 'raw'],
                    'ebit': ['incomeStatementHistory', 'incomeStatementHistory', years_ago, 'ebit', 'raw'],

                    # ------------Balance Sheet Stock Info------------ #

                    'netReceivables': ['balanceSheetHistory', 'balanceSheetStatements', years_ago, 'netReceivables', 'raw'],
                    'inventory': ['balanceSheetHistory', 'balanceSheetStatements', years_ago, 'inventory', 'raw'],
                    'currentAssets': ['balanceSheetHistory', 'balanceSheetStatements', years_ago, 'totalCurrentAssets', 'raw'],
                    'totalAssets': ['balanceSheetHistory', 'balanceSheetStatements', years_ago, 'totalAssets', 'raw'],
                    'currentLiabilities': ['balanceSheetHistory', 'balanceSheetStatements', years_ago, 'totalCurrentLiabilities', 'raw'],
                    'longTermDebt': ['balanceSheetHistory', 'balanceSheetStatements', years_ago, 'longTermDebt', 'raw'], 
                    'totalLiabilities': ['balanceSheetHistory', 'balanceSheetStatements', years_ago, 'totalLiab', 'raw'],
                    'retainedEarnings': ['balanceSheetHistory', 'balanceSheetStatements', years_ago, 'retainedEarnings', 'raw'],
                    'liabilitiesAndEquity': ['balanceSheetHistory', 'balanceSheetStatements', years_ago, 'totalAssets', 'raw'],

                    # ------------Statement of Cash Flow Stock Info------------ #

                    'dividends': ['cashflowStatementHistory', 'cashflowStatements', years_ago, 'dividendsPaid', 'raw'],
                    'shareIssuance': ['cashflowStatementHistory', 'cashflowStatements', years_ago, 'issuanceOfStock', 'raw'],
                    'shareBuyback': ['cashflowStatementHistory', 'cashflowStatements', years_ago, 'repurchaseOfStock', 'raw'],
                    'operatingCashFlow': ['cashflowStatementHistory', 'cashflowStatements', years_ago, 'totalCashFromOperatingActivities', 'raw'],
                    'capitalExpenditure': ['cashflowStatementHistory', 'cashflowStatements', years_ago, 'capitalExpenditures', 'raw'],

                    'depreciation': ['cashflowStatementHistory', 'cashflowStatements', years_ago, 'depreciation', 'raw']

                },
                'eps': ['defaultKeyStatistics', 'trailingEps', 'raw']
            }


            #-------get financial API data-------#

            for item in adresses['financialAPI']:

                filtered_response = response

                for pointer in adresses['financialAPI'][item]:
                    try:
                        filtered_response = filtered_response[pointer]
                    except:
                        filtered_response = 1
                        break

                self.data[years_ago][item] = filtered_response     


        for pointer in adresses['eps']:
            
            try:
                summary_response = summary_response[pointer]
            except KeyError or IndexError:
                summary_response = 1
                break

        self.data[0]['eps'] = summary_response
        self.data[1]['eps'] = summary_response  
        self.data[2]['eps'] = summary_response 

    def reload(self, new_ticker):
        self.ticker = new_ticker
        self.load_data()

    def get_data(self, data_point):
        return self.data.get(data_point, None)


    def get_data(self):
        return self.data


    def to_dataframe(self):
        df = pd.DataFrame(self.data)

        return df

    