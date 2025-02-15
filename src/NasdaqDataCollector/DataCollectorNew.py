import time
from urllib.request import urlopen
import ssl
import certifi
import datetime
import json
import Stock

attributes_map = {
    "previous_close": "p",
    "dividend_yield": "y",
    "dividend_per_share": "d",
    "one_yr_target_price": "t8",
    "f2_wk_high": "k",
    "f2_wk_low": "j",
    "eps": "e",
    "book_value": "b4",
    "price_per_sales": "p5",
    "price_per_book": "p6",
    "pe": "r",
    "peg": "r5",
    "short_ratio": "s7"
}

attributes_list = "pydt8kjeb4p5p6rr5s7"


def getFundamentalUrl(stock):
    return "https://www.alphavantage.co/query?function=OVERVIEW&symbol={}&apikey={}".format(stock, "A5ZQ7ESZOUG7B3TU")


def getDataUrl(stock):
    return "https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={}&apikey={}".format(stock,
                                                                                                                "A5ZQ7ESZOUG7B3TU")


def getStockData(stock):
    url = getDataUrl(stock)
    fundamental_url = getFundamentalUrl(stock)

    context = ssl.create_default_context(cafile=certifi.where())
    fundamental_data = urlopen(fundamental_url, context=context).read()
    data = urlopen(url, context=context).read()

    # Get today's date
    todays_date = '2025-02-14'  # 'datetime.date.today()

    # Convert the data to json dict
    stock_data = json.loads(data.decode('utf-8'))
    stock_state = json.loads(fundamental_data.decode('utf-8'))

    # Extract the fields from the data
    dividend_yield = extract_stock_state(stock_state, 'DividendYield')
    dividend_per_share = extract_stock_state(stock_state, 'DividendPerShare')
    one_yr_target_price = extract_stock_state(stock_state, 'AnalystTargetPrice')
    f2_wk_high = stock_state['52WeekHigh']
    f2_wk_low = stock_state['52WeekLow']
    eps = stock_state['EPS']
    book_value = stock_state['BookValue']
    price_per_sales = stock_state['PriceToSalesRatioTTM']
    price_per_book = stock_state['PriceToBookRatio']
    pe = stock_state['PERatio']
    peg = stock_state['PEGRatio']
    short_ratio = 0
    previous_close = stock_data['Monthly Adjusted Time Series'][str(todays_date)]['4. close']

    return Stock.StockState(stock, todays_date, previous_close, dividend_yield, dividend_per_share, one_yr_target_price,
                            f2_wk_high, f2_wk_low, eps, book_value, price_per_sales, price_per_book, pe, peg,
                            short_ratio)


def extract_stock_state(stock_state, key):
    try:
        return stock_state[key]
    except:
        print(stock_state)
        return 'NAN'


if __name__ == '__main__':
    all_stock_list = ["OMC", "FL", "GPS", "LB", "ROST", "TJX", "COH", "HBI", "KORS", "NKE", "RL", "PVH", "TIF",
                      "UA", "UAA", "VFC",
                      "BWA", "DLPH", "F", "GM", "AAP", "CBS", "CHTR", "CMCSA", "DISCA", "DISCK", "DISH", "SNI", "TWX",
                      "VIAB", "DIS",
                      "MGM", "WYNN", "BBY", "GRMN", "M", "JWN", "LKQ", "DG", "DLTR", "KSS", "TGT", "LEG", "MHK", "HD",
                      "LOW", "DHI",
                      "LEN", "PHM", "CCL", "HLT", "MAR", "RCL", "WYN", "SNA", "SWK", "WHR", "NWL", "AMZN", "EXPE",
                      "PCLN", "TRIP",
                      "HAS", "MAT", "HOG", "NWSA", "NWS", "FOXA", "FOX", "CMG", "DRI", "MCD", "SBUX", "YUM", "AZO",
                      "KMX", "GPC",
                      "ORLY", "SIG", "SPLS", "TSCO", "ULTA", "GT", "ADM", "TAP", "BF.B", "STZ", "CVS", "WBA", "SYY",
                      "KR", "WFM", "CHD",
                      "CLX", "CL", "KMB", "COST", "WMT", "CPB", "CAG", "GIS", "HSY", "HRL", "SJM", "K", "KHC", "MKC",
                      "MDLZ", "TSN",
                      "COTY", "EL", "PG", "KO", "DPS", "MNST", "PEP", "MO", "PM", "CVX", "XOM", "HES", "HP", "BHGE",
                      "HAL", "NOV", "SLB",
                      "FTI", "APC", "APA", "COG", "CHK", "XEC", "CXO", "COP", "DVN", "EOG", "EQT", "MRO", "NFX", "NBL",
                      "OXY", "PXD", "RRC",
                      "ANDV", "MPC", "PSX", "VLO", "KMI", "OKE", "WMB", "AMG", "AMP", "BK", "BLK", "BEN", "IVZ", "NTRS",
                      "STT", "TROW",
                      "AXP", "HRB", "COF", "DFS", "NAVI", "SYF", "BAC", "C", "CMA", "JPM", "USB", "WFC", "CBOE", "CME",
                      "ICE", "MCO",
                      "NDAQ", "SPGI", "AON", "AJG", "MMC", "WLTW", "SCHW", "ETFC", "GS", "MS", "RJF", "AFL", "BHF",
                      "MET", "PFG", "PRU",
                      "TMK", "UNM", "AIZ", "LNC", "L", "BRK.B", "LUK", "ALL", "AIG", "CB", "CINF", "HIG", "PGR", "TRV",
                      "XL", "BBT", "CFG",
                      "FITB", "HBAN", "KEY", "MTB", "PNC", "RF", "STI", "ZION", "RE", "PBCT", "ALXN", "AMGN", "BIIB",
                      "CELG", "GILD",
                      "INCY", "REGN", "VRTX", "ABC", "BMY", "CAH", "ESRX", "HSIC", "MCK", "WAT", "ABT", "A", "BCR",
                      "BAX", "BDX", "BSX",
                      "DHR", "EW", "HOLX", "IDXX", "ISRG", "JNJ", "MDT", "PKI", "RMD", "SYK", "TMO", "VAR", "ZBH",
                      "DVA", "HCA", "UHS",
                      "EVHC", "LH", "DGX", "ALGN", "COO", "XRAY", "PDCO", "CERN", "ILMN", "MTD", "AET", "ANTM", "CNC",
                      "CI", "HUM", "UNH",
                      "ABBV", "AGN", "LLY", "MRK", "MYL", "PRGO", "PFE", "ZTS", "ARNC", "BA", "GD", "LLL", "LMT", "NOC",
                      "RTN", "COL",
                      "TXT", "TDG", "UTX", "DE", "CHRW", "EXPD", "FDX", "UPS", "ALK", "AAL", "DAL", "LUV", "UAL",
                      "ALLE", "AOS", "FAST",
                      "FBHS", "JCI", "MAS", "FLR", "JEC", "PWR", "CAT", "PCAR", "CTAS", "AYI", "AME", "ETN", "EMR",
                      "ROK", "RSG", "SRCL",
                      "WM", "RHI", "MMM", "GE", "HON", "ROP", "CMI", "DOV", "FLS", "FTV", "GWW", "ITW", "IR", "PH",
                      "PNR", "XYL", "CSX",
                      "KSU", "NSC", "UNP", "EFX", "INFO", "NLSN", "VRSK", "URI", "JBHT", "ADBE", "ANSS", "ADSK", "ORCL",
                      "SYMC", "SNPS",
                      "CSCO", "FFIV", "HRS", "JNPR", "MSI", "ADS", "GPN", "PYPL", "APH", "GLW", "FLIR", "TEL", "ATVI",
                      "EA", "AKAM",
                      "GOOGL", "GOOG", "ADP", "CTXS", "EBAY", "FB", "FIS", "FISV", "INTU", "MA", "NTAP", "NFLX", "PAYX",
                      "CRM", "TSS",
                      "VRSN", "V", "WU", "ACN", "CTSH", "CSRA", "DXC", "IT", "IBM", "AMAT", "KLAC", "LRCX", "AMD",
                      "ADI", "AVGO", "INTC",
                      "MCHP", "MU", "NVDA", "QRVO", "QCOM", "SWKS", "TXN", "XLNX", "CA", "MSFT", "RHT", "AAPL", "HPE",
                      "HPQ", "STX", "WDC",
                      "XRX", "MLM", "VMC", "FCX", "DOW", "DD", "EMN", "CF", "FMC", "MON", "MOS", "NEM", "APD", "PX",
                      "BLL", "AVY", "IP",
                      "PKG", "SEE", "WRK", "ALB", "ECL", "IFF", "LYB", "PPG", "SHW", "NUE", "HCP", "VTR", "HCN", "HST",
                      "DRE", "PLD", "ARE",
                      "BXP", "SLG", "VNO", "CBG", "AIV", "AVB", "EQR", "ESS", "MAA", "UDR", "FRT", "GGP", "KIM", "MAC",
                      "O", "REG", "SPG",
                      "AMT", "CCI", "DLR", "EQIX", "EXR", "IRM", "PSA", "WY", "LVLT", "T", "CTL", "VZ", "LNT", "AEP",
                      "ED", "D", "DUK",
                      "EIX", "ETR", "FE", "PPL", "PEG", "SO", "WEC", "AES", "NRG", "AEE", "CNP", "CMS", "DTE", "ES",
                      "EXC", "NEE", "NI",
                      "PCG", "PNW", "SCG", "SRE", "XEL", "AWK"]

    # 'TSLA', 'JPM', 'JNJ', 'V', 'PG', 'UNH', 'NVDA', 'HD', 'MA', 'PYPL', 'BAC', 'DIS',
    top_30 = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'GOOG', 'INTC', 'VZ', 'ADBE', 'CSCO', 'KO', 'T', 'PFE', 'WMT', 'ABT', 'MRK',
              'CVX']

    for stock in top_30:
        print('Getting data for ' + stock)
        getStockData(stock).save_to_db()
        time.sleep(30)
