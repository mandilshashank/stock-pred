from urllib.request import urlopen
import json
import datetime
from random import randint
import mysql.connector
from sklearn import preprocessing
import os
import pickle

def getStocksData(data_date):
    cnx = mysql.connector.connect(user='root', database='stock_data', password='root')
    cursor = cnx.cursor()

    query = ("SELECT * FROM stocks_snaps where date_snap = '{}'")

    stocks_date = data_date
    final_query = query.format(stocks_date)
    cursor.execute(final_query)

    ret_data={}
    for (id, symbol, date_snap, previous_close, dividend_yield, dividend_per_share,
         one_yr_target_price, f2_wk_high, f2_wk_low, eps, book_value, price_per_sales,
         price_per_book, pe, peg, short_ratio) in cursor:

        final_previous_close = 0 if previous_close.find('N') > -1 else float(previous_close)
        ret_data[symbol]=final_previous_close


    cursor.close()
    cnx.close()

    return ret_data

if __name__ == '__main__':
    all_stock_list = ["IPG","OMC","FL","GPS","LB","ROST","TJX","COH","HBI","KORS","NKE","RL","PVH","TIF","UA","UAA","VFC",
                      "BWA","DLPH","F","GM","AAP","CBS","CHTR","CMCSA","DISCA","DISCK","DISH","SNI","TWX","VIAB","DIS",
                      "MGM","WYNN","BBY","GRMN","M","JWN","LKQ","DG","DLTR","KSS","TGT","LEG","MHK","HD","LOW","DHI",
                      "LEN","PHM","CCL","HLT","MAR","RCL","WYN","SNA","SWK","WHR","NWL","AMZN","EXPE","PCLN","TRIP",
                      "HAS","MAT","HOG","NWSA","NWS","FOXA","FOX","CMG","DRI","MCD","SBUX","YUM","AZO","KMX","GPC",
                      "ORLY","SIG","SPLS","TSCO","ULTA","GT","ADM","TAP","BF.B","STZ","CVS","WBA","SYY","KR","WFM","CHD",
                      "CLX","CL","KMB","COST","WMT","CPB","CAG","GIS","HSY","HRL","SJM","K","KHC","MKC","MDLZ","TSN",
                      "COTY","EL","PG","KO","DPS","MNST","PEP","MO","PM","CVX","XOM","HES","HP","BHGE","HAL","NOV","SLB",
                      "FTI","APC","APA","COG","CHK","XEC","CXO","COP","DVN","EOG","EQT","MRO","NFX","NBL","OXY","PXD","RRC",
                      "ANDV","MPC","PSX","VLO","KMI","OKE","WMB","AMG","AMP","BK","BLK","BEN","IVZ","NTRS","STT","TROW",
                      "AXP","HRB","COF","DFS","NAVI","SYF","BAC","C","CMA","JPM","USB","WFC","CBOE","CME","ICE","MCO",
                      "NDAQ","SPGI","AON","AJG","MMC","WLTW","SCHW","ETFC","GS","MS","RJF","AFL","BHF","MET","PFG","PRU",
                      "TMK","UNM","AIZ","LNC","L","BRK.B","LUK","ALL","AIG","CB","CINF","HIG","PGR","TRV","XL","BBT","CFG",
                      "FITB","HBAN","KEY","MTB","PNC","RF","STI","ZION","RE","PBCT","ALXN","AMGN","BIIB","CELG","GILD",
                      "INCY","REGN","VRTX","ABC","BMY","CAH","ESRX","HSIC","MCK","WAT","ABT","A","BCR","BAX","BDX","BSX",
                      "DHR","EW","HOLX","IDXX","ISRG","JNJ","MDT","PKI","RMD","SYK","TMO","VAR","ZBH","DVA","HCA","UHS",
                      "EVHC","LH","DGX","ALGN","COO","XRAY","PDCO","CERN","ILMN","MTD","AET","ANTM","CNC","CI","HUM","UNH",
                      "ABBV","AGN","LLY","MRK","MYL","PRGO","PFE","ZTS","ARNC","BA","GD","LLL","LMT","NOC","RTN","COL",
                      "TXT","TDG","UTX","DE","CHRW","EXPD","FDX","UPS","ALK","AAL","DAL","LUV","UAL","ALLE","AOS","FAST",
                      "FBHS","JCI","MAS","FLR","JEC","PWR","CAT","PCAR","CTAS","AYI","AME","ETN","EMR","ROK","RSG","SRCL",
                      "WM","RHI","MMM","GE","HON","ROP","CMI","DOV","FLS","FTV","GWW","ITW","IR","PH","PNR","XYL","CSX",
                      "KSU","NSC","UNP","EFX","INFO","NLSN","VRSK","URI","JBHT","ADBE","ANSS","ADSK","ORCL","SYMC","SNPS",
                      "CSCO","FFIV","HRS","JNPR","MSI","ADS","GPN","PYPL","APH","GLW","FLIR","TEL","ATVI","EA","AKAM",
                      "GOOGL","GOOG","ADP","CTXS","EBAY","FB","FIS","FISV","INTU","MA","NTAP","NFLX","PAYX","CRM","TSS",
                      "VRSN","V","WU","ACN","CTSH","CSRA","DXC","IT","IBM","AMAT","KLAC","LRCX","AMD","ADI","AVGO","INTC",
                      "MCHP","MU","NVDA","QRVO","QCOM","SWKS","TXN","XLNX","CA","MSFT","RHT","AAPL","HPE","HPQ","STX","WDC",
                      "XRX","MLM","VMC","FCX","DOW","DD","EMN","CF","FMC","MON","MOS","NEM","APD","PX","BLL","AVY","IP",
                      "PKG","SEE","WRK","ALB","ECL","IFF","LYB","PPG","SHW","NUE","HCP","VTR","HCN","HST","DRE","PLD","ARE",
                      "BXP","SLG","VNO","CBG","AIV","AVB","EQR","ESS","MAA","UDR","FRT","GGP","KIM","MAC","O","REG","SPG",
                      "AMT","CCI","DLR","EQIX","EXR","IRM","PSA","WY","LVLT","T","CTL","VZ","LNT","AEP","ED","D","DUK",
                      "EIX","ETR","FE","PPL","PEG","SO","WEC","AES","NRG","AEE","CNP","CMS","DTE","ES","EXC","NEE","NI",
                      "PCG","PNW","SCG","SRE","XEL","AWK"]

    some_stocks_list = ["AZO","KMX","GPC","ORLY","SIG","SPLS","TSCO","ULTA",]

    for stock in some_stocks_list:
        stock_data = getStocksData(datetime.date(2017, 10, 5))
        url = "http://e2delivery.com:5000/prediction/{}/5/10/2017/30".format(stock)
        data = json.loads(urlopen(url).read())
        print(stock + ":" + str(data["prediction"]) + ":" + str(stock_data[stock]))