import datetime
from DecisionTreeModel import StockDecisionTree
from NeuralNetworkModel import NeuralNetworkModel
from RandomForestModel import RandomForestModel
from GBDTModel import GBDTModel
from DataBuilder import DataBuilder
from NasdaqDataCollector.StockPredictor import StockPredictor

######
# This class calculates the predictions for the model over a period of 7 days and 30 days for all the stocks
# and compares those predictions with the values from the actual world
# It calculates the mean squared error on the diff between the values

class ModelMetricsCalculator:
    @staticmethod
    def calculateMeanSquaredError(start_date = datetime.date(2017, 8, 30),
                                  predict_range=7):
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
                          "DHR","EW","HOLX","IDXX","JNJ","MDT","PKI","RMD","SYK","TMO","VAR","ZBH","DVA","HCA","UHS",
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

        # get the predictions for the stocks
        stock_predictions = {}
        for i, stock in enumerate(all_stock_list):
            print i
            stock_predictions[stock] = StockPredictor.predict_stock2(stock, start_date, predict_range)

        end_date = start_date + datetime.timedelta(days=predict_range)
        # get the actual values
        dc = DataBuilder()
        actual_data = dc.get_price_diff_data(start_date, end_date)
	
	for i, stock in enumerate(all_stock_list):
            print str(stock) + " Predictions : " + str(stock_predictions[stock]) + ", Actual : " + str(actual_data[stock])

        #calculate the mean squared error
        error = [stock_predictions[stock]-actual_data[stock] if ((stock_predictions[stock]>0 and actual_data[stock]<0) or (stock_predictions[stock]<0 and actual_data[stock]>0)) else 0 for stock in all_stock_list]
        mean_squared_error = sum(map(lambda x:x*x,error))/(len(error))

        return mean_squared_error

print "Mean Squared Error" + str(ModelMetricsCalculator.calculateMeanSquaredError(datetime.date(2017, 9, 1),30))
