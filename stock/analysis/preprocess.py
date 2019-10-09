import pandas_datareader as web
import datetime
import matplotlib.pyplot as plt
from mpl_finance import candlestick2_ohlc as ohlc


def isNull(df):
    if df.isnull().values.sum():
        return False
    return True


# 数据清洗
def dataClean(df):
    pass


# 数据规范化
def dataNorm(df):
    return (df - df.min())/(df.max() - df.min())


def prePro(start_date, end_date):
    # 十年之内的交易数据
    df1 = web.DataReader('MSFT', 'yahoo', start_date, end_date)
    df2 = web.DataReader('AAPL', 'yahoo', start_date, end_date)

    #  是否存在缺失值
    if isNull(df1):
        dataClean(df1)
    if isNull(df2):
        dataClean(df2)

    return df1, df2


# 两个股票的比较
def showComp(arg, *df):
    #  查看股票价格走势
    plt.figure(figsize=(18.5, 8.6))  # 设置图片大小
    # plot画图
    l1, = plt.plot(df[0][arg], 'b')
    l2, = plt.plot(df[1][arg], 'r')
    # 添加标题
    plt.title(f"comparison of {arg}", fontsize='15')
    plt.xlabel('year')  # 添加x轴图标
    plt.ylabel('dollar')  # 添加y轴图标
    # 设置图例
    plt.legend(handles=[l1, l2,], labels=['micro', 'apple'], loc='best')
    plt.show()


#展示股票所有参数
def showStock(df):
    df = dataNorm(df)
    plt.style.use("seaborn-whitegrid")
    plt.figure(figsize=(18.5, 8.5))

    plt.plot(df)
    plt.legend(labels=['High', 'Low', 'Open', 'Close', 'Volume', 'Adj-close'], loc='best')
    plt.show()


# 展示股票k线图
def showKChart(df):
    year_2018 = df['2018-01-01':'2018-12-31']
    fig, ax = plt.subplots(figsize=(18.5, 8.5))
    ohlc(ax, year_2018.Open, year_2018.High, year_2018.Low, year_2018.Close,
         width=0.5, alpha=0.6, colorup='r', colordown='g')
    plt.show()


if __name__ == '__main__':
    # 时间跨度
    end = datetime.datetime.now()
    start = end - 10 * datetime.timedelta(days=360)
    df1, df2 = prePro(start, end)
    arg = 'Close'
    # showComp(arg, df1, df2)
    # showStock(df1)
    showKChart(df1)