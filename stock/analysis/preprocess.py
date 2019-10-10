import numpy as np
import matplotlib.pyplot as plt
from mpl_finance import candlestick2_ohlc as ohlc


class Analysis:
    def __init__(self, year, *df):
        self.df = df
        self.year = year
        self.whole_year = self.df[0][(self.year + '-01-01'):(self.year + '-12-31')]

    def isNull(self):
        for k in self.df:
            if k.isnull().values.sum():
                return False
            return True

    # 数据清洗
    def dataClean(self):
        pass

    # 数据规范化
    def dataNorm(self, df):
        return (df - df.min()) / (df.max() - df.min())

    def prePro(self, start_date, end_date):

        #  是否存在缺失值
        if self.isNull():
            self.dataClean()

        return self.df

    # 两个股票的比较
    def showComp(self, arg, name1, name2):
        #  查看股票价格走势
        plt.figure(figsize=(18.5, 8.6))  # 设置图片大小
        # plot画图
        l1, = plt.plot(self.df[0][arg], 'b')
        l2, = plt.plot(self.df[1][arg], 'r')
        # 添加标题
        plt.title(f"comparison of {arg}", fontsize='15')
        plt.xlabel('year')  # 添加x轴图标
        plt.ylabel('dollar')  # 添加y轴图标
        # 设置图例
        plt.legend(handles=[l1, l2, ], labels=[f'{name1}', f'{name2}'], loc='best')
        plt.show()

    # 展示股票所有参数
    def showStock(self, df):
        # 归一化
        df = self.dataNorm(df)
        plt.style.use("seaborn-whitegrid")
        plt.figure(figsize=(18.5, 8.5))

        plt.plot(df)
        plt.legend(labels=['High', 'Low', 'Open', 'Close', 'Volume', 'Adj-close'], loc='best')
        plt.show()

    # 展示股票k线图
    def showKChart(self, df):
        fig, ax = plt.subplots(figsize=(18.5, 8.5))
        ohlc(ax, self.whole_year.Open, self.whole_year.High, self.whole_year.Low, self.whole_year.Close,
             width=0.5, alpha=0.6, colorup='r', colordown='g')
        plt.show()

    # 当日价格相对变化
    def showDayCloseLineChart(self, df):
        year_arg = self.whole_year.Close
        log_change = np.log(year_arg) - np.log(year_arg.shift(1))

        fig, ax = plt.subplots(figsize=(18.5, 8.5))
        ax.plot(log_change, ".-")
        ax.axhline(y=0, color='red', lw=1)
        plt.show()

    def showDayCloseBarChart(self, df):
        year_arg = self.whole_year.Close
        log_change = np.log(year_arg) - np.log(year_arg.shift(1))

        # 柱状图
        fig, ax = plt.subplots(figsize=(30, 9))
        log_change.plot(kind='bar')
        plt.show()

    # 股票交易策略
    '''
    而长期和短期变化曲线的交点，往往就是我们购入或卖出股票的时间点。如果我们是短期投资者，就可以建立一个交易策略。
    当短期变化曲线从上方交与长期变化曲线，说明股票短期看跌，则卖出。
    当短期变化曲线从下方交与长期变化曲线，说明股票长期看涨，则买入。
    '''

    def tradingStrategy(self, df):
        year_arg = self.whole_year.Close
        # 短期和长期的平均变化
        short_rolling = year_arg.rolling(window=5).mean()
        long_rolling = year_arg.rolling(window=15).mean()

        fig, ax = plt.subplots(figsize=(16, 9))
        ax.plot(year_arg.index, year_arg, label=f'{year} close')
        ax.plot(short_rolling.index, short_rolling, label='5 days rolling')
        ax.plot(long_rolling.index, long_rolling, label='20 days rolling')

        ax.set_xlabel('Date')
        ax.set_ylabel('Closing price ($)')

        ax.legend(fontsize='large')
        plt.show()

    def buySale(self, df):
        year_arg = self.whole_year.Close
        # 短期和长期的平均变化
        short_rolling = year_arg.rolling(window=5).mean()
        long_rolling = year_arg.rolling(window=15).mean()

        fig, ax = plt.subplots(figsize=(16, 9))
        short_long = np.sign(short_rolling - long_rolling)
        buy_sell = np.sign(short_long - short_long.shift(1))
        buy_sell.plot(ax=ax)
        ax.axhline(y=0, color='red', lw=2)
        plt.show()

        # 适合买入点
        buy_sell[buy_sell == 1]
        # 适合卖出点
        buy_sell[buy_sell == -1]

        print(year_arg[(self.year + '-05-16')] - year_arg[(self.year + '-05-13')])
