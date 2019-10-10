import pandas_datareader as web
import datetime
import stock.analysis.preprocess as prep


# 时间跨度
end = datetime.datetime.now()
start = end - 10 * datetime.timedelta(days=360)

# 十年之内的交易数据
df1 = web.DataReader('MSFT', 'yahoo', start, end)
df2 = web.DataReader('AAPL', 'yahoo', start, end)
# print(df1)
arg = 'Close'

anl = prep.Analysis('2018', df1, df2)
result = anl.prePro(start, end)
param = 'Close'
# anl.showComp(arg, 'microsoft', 'apple')
anl.showStock(result[0])
# anl.showKChart(result[0])
# anl.showDayCloseBarChart(result[0])
# anl.tradingStrategy(result[0])
# anl.buySale(result[0])

