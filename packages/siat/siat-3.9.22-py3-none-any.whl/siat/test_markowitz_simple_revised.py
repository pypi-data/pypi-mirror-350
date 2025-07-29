# -*- coding: utf-8 -*-

#==============================================================================
%matplotlib inline

# 小函数，使得过程逻辑更加清晰
def gen_weights(n):
    """
    产生投资组合各个成分股的随机权重
    """
    import numpy as np
    w=np.random.rand(n)
    return w /sum(w)

def port_ret(w,r_annual):
    """
    计算投资组合的年化收益率
    """
    import numpy as np
    return np.sum(w*r_annual)

def port_std(w,log_r):
    """
    计算投资组合的年化标准差
    """
    import numpy as np
    return np.sqrt((w.dot(log_r.cov()*250).dot(w.T)))


def gen_ports(n,times,log_r,r_annual):
    #生成若干投资组合的收益和风险
    for _ in range(times):#生成不同的组合
        w=gen_weights(n)#每次生成不同的权重
        yield (port_std(w,log_r),port_ret(w,r_annual),w)#计算风险和期望收益 以及组合的权重情况

#------------------------------------------------------------------------------

if __name__=='__main__':
    components = {
        'AAPL':'苹果',
        'AMZN':'亚马逊',
        'GOOGL':'谷歌',
        'BABA':'阿里巴巴'
        }

    start='2016-1-1'    
    end='2017-12-31'
    
    rf=0.015
    simulation=25000
    trend=True
    ef=True
    MSR=True
    CML=True
    
    markowitz_simple(components,start,end)
    
def markowitz_simple(components,start,end,rf=0.015,simulation=25000, \
               trend=True,ef=True,MSR=True,CML=False):
    """
    马科维茨有效投资投资边界的基本思想
    通过对资产组合当中不同资产的配置情况进行调整，达到在既定风险水平下的收益最大化，
    或者既定收益水平下的风险最小化。
    """

    from datetime import date
    import pandas_datareader.data as web
    import matplotlib.pyplot as plt
    import numpy as np 
    import seaborn as sns
    import warnings
    warnings.filterwarnings("ignore")
    
    # 步骤1：获取股价
    tickers=list(components)
    stock_data=get_prices(tickers,start,end)['Close']
    stock_data.rename(columns=components,inplace=True)
    stock_data=stock_data.iloc[::-1]
 
    #画出收盘价走势图
    if trend:
        sns.set_style("whitegrid")#横坐标有标线，纵坐标没有标线，背景白色
        sns.set_style("darkgrid") #默认，横纵坐标都有标线，组成一个一个格子，背景稍微深色
        sns.set_style("dark")#背景稍微深色，没有标线线
        sns.set_style("white")#背景白色，没有标线线
        sns.set_style("ticks")#xy轴都有非常短的小刻度
        sns.despine(offset=30,left=True)#去掉上边和右边的轴线，offset=30表示距离轴线（x轴）的距离,left=True表示左边的轴保留
        sns.set(font='SimHei',rc={'figure.figsize':(10,6)})# 图片大小和中文字体设置

        # 图形展示
        # stock_data.iloc[0]含有字样Symbols
        (stock_data/stock_data.iloc[0]).plot()

#------------------------------------------------------------------------------
    # 步骤2：计算股票的收益率和风险，假定每年有250个交易日
    # 收益率
    R=stock_data/stock_data.shift(1)-1
    
    # 对数收益率 
    log_r=np.log(stock_data/stock_data.shift(1))
    
    # 年化收益率 
    r_annual=np.exp(log_r.mean()*250)-1
    
    # 风险
    std = np.sqrt(log_r.var() * 250)#假设协方差为0

#------------------------------------------------------------------------------
    # 步骤3：投资组合的收益和风险
 
    n=len(list(tickers))
    w=gen_weights(n)
    #list(zip(r_annual.index,w))
 
    import pandas as pd 
    # 投资组合模拟次数
    df=pd.DataFrame(gen_ports(n,simulation,log_r,r_annual),columns=["std","ret","w"])

#------------------------------------------------------------------------------

    # 步骤4：画出投资有效边界，假设无风险利率为rf
    # 引入夏普比率
    df['sharpe'] = (df['ret'] - rf) / df['std']#定义夏普比率
    fig, ax = plt.subplots()
    df.plot.scatter('std', 'ret', c='sharpe',s=30, alpha=0.3, cmap='cool',marker='o', ax=ax)
    plt.style.use('ggplot')
    plt.rcParams['axes.unicode_minus'] = False# 显示负号
 
    #list(zip(r_annual.index, df.loc[df.sharpe.idxmax()].w))


    import scipy.optimize as opt
    frontier=pd.DataFrame(columns=['std','ret'])

    # std的范围：0.16,0.25 
    std_min=round(df['std'].min(),2)
    std_max=round(df['std'].max(),2)
    #for std in np.linspace(0.16,0.25):
    for std in np.linspace(std_min,std_max):    
        res=opt.minimize(lambda x:-port_ret(x,r_annual),
                    x0=((1/n),)*n,
                    method='SLSQP',
                    bounds=((0,1),)*n,
                    constraints=[
                       {"fun":lambda x:port_std(x,log_r)-std,"type":"eq"},
                       {"fun":lambda x:(np.sum(x)-1),"type":"eq"}
                    ])
        if res.success:
            frontier=frontier.append({"std":std,"ret":-res.fun},ignore_index=True)
    
    if ef:
        frontier.plot('std','ret',lw=3,c='blue',ax=ax)
        fig

#------------------------------------------------------------------------------
    # 步骤5：计算最优资产配置情况
    
    res=opt.minimize(lambda x:-((port_ret(x,r_annual)-0.03)/port_std(x,log_r)),
                    x0=((1/n),)*n,
                    method='SLSQP',
                    bounds=((0,1),)*n,
                    constraints={"fun":lambda x:(np.sum(x)-1), "type":"eq"})
     
    print(res.x.round(3))
    
    if MSR:
        ax.scatter(port_std(res.x,log_r),port_ret(res.x,r_annual),marker="*",c="black",s=300)
        fig

#------------------------------------------------------------------------------
    # 步骤6：绘制资本市场线CML=Capital Market Line
    if CML:
        ax.plot((0,.27),(.03,-res.fun*.27+.03))
        fig

    """
    在上图的所示资本市场线上，星号左边表示将资本用于投资一部分无风险资产和一部分风险资产组合，
    而在星号处代表将所有的资本都用于投资风险资产组合，
    星号右边意味着借入无风险资产并投资于风险资产组合，可以在相同的风险水平下获得更高的收益。
    
    """
    
    return


#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------



















