import os
from urllib.request import urlopen
import ssl
import certifi
import json
import time

from src.NasdaqDataCollector.StockPolygon import StockStatePolygon


def get_fundamental_data(ticker):
    api_key = os.getenv("POLYGON_API_KEY")
    url = f"https://api.polygon.io/vX/reference/financials?ticker={ticker}&sort=filing_date&apiKey={api_key}"

    try:
        context = ssl.create_default_context(cafile=certifi.where())
        data = urlopen(url, context=context).read()

        # Parse the JSON object
        parsed_data = json.loads(data)
        # Extract the values of the 'basic_earnings_per_share' and 'net_income_loss' keys
        basic_earnings_per_share = \
            parsed_data['results'][0]['financials']['income_statement']['basic_earnings_per_share']['value']
        net_income_loss = parsed_data['results'][0]['financials']['income_statement']['net_income_loss']['value']
        return {
            "basic_earnings_per_share": basic_earnings_per_share,
            "net_income_loss": net_income_loss
        }
    except (KeyError, TypeError, json.JSONDecodeError):
        return None


def get_ticker_snapshot(ticker):
    api_key = os.getenv("POLYGON_API_KEY")
    url = f"https://api.polygon.io/v2/snapshot/locale/us/markets/stocks/tickers/{ticker}?apiKey={api_key}"

    try:
        context = ssl.create_default_context(cafile=certifi.where())
        data = urlopen(url, context=context).read()

        # Parse the JSON object
        ticker_data = json.loads(data)['ticker']
        print(ticker_data)
        stock_polygon = StockStatePolygon(
            ticker=ticker_data['ticker'],
            todays_change_percentage=ticker_data['todaysChangePerc'],
            todays_change=ticker_data['todaysChange'],
            updated=ticker_data['updated'],
            day_open=ticker_data['day']['o'],
            day_high=ticker_data['day']['h'],
            day_low=ticker_data['day']['l'],
            day_close=ticker_data['day']['c'],
            day_volume=ticker_data['day']['v'],
            day_vw=ticker_data['day']['vw'],
            minute_open=ticker_data['min']['o'],
            minute_high=ticker_data['min']['h'],
            minute_low=ticker_data['min']['l'],
            minute_close=ticker_data['min']['c'],
            minute_volume=ticker_data['min']['v'],
            minute_vw=ticker_data['min']['vw'],
            previous_day_open=ticker_data['prevDay']['o'],
            previous_day_high=ticker_data['prevDay']['h'],
            previous_day_low=ticker_data['prevDay']['l'],
            previous_day_close=ticker_data['prevDay']['c'],
            previous_day_volume=ticker_data['prevDay']['v'],
            previous_day_vw=ticker_data['prevDay']['vw']
        )

        return stock_polygon
    except Exception as e:
        print(f"Failed to retrieve data: {e}")
        return {"error": "Failed to retrieve data"}


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
    top_30 = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'GOOG', 'INTC', 'VZ', 'ADBE', 'CSCO', 'KO', 'T', 'PFE', 'WMT',
              'ABT', 'MRK',
              'CVX']
    for stock in top_30:
        try:
            print('Getting data for ' + stock)
            stocks_state_polygon = get_ticker_snapshot(stock)
            stocks_state_polygon.save_to_db()
            time.sleep(1)
        except Exception as e:
            print(f"Error processing {stock}: {e}")
            continue
