# -*- coding: utf-8 -*-

import os; os.chdir("S:/siat")
from siat import *

#==============================================================================
if __name__=='__main__':
    ticker='600519.SS'
    start='2023-1-1'
    end='2023-4-4'
    info_types=['Close','Volume']
    
    #获取股票价格
    df1=fetch_price_stock(ticker,start,end)
    
    #获取指数价格
    mktidx='000300.SS'
    df1i=fetch_price_stock(mktidx,start,end)
    
    #获取ETF价格
    etf='512690.SS'
    df1e=fetch_price_stock(etf,start,end)
    
    #获取REiTs基金价格
    reits='180801.SZ'
    df1r=fetch_price_stock(reits,start,end)
    
    
if __name__=='__main__':
    Market={'Market':('China','000300.SS','白酒组合1号')}
    Stocks ={'600519.SS':.5,
             '000858.SZ':.3,
             '000596.SZ':.1,
             '000568.SZ':.1}
    portfolio=dict(Market,**Stocks)
    
    start='2023-1-1'
    end='2023-4-4'
    
    #获取投资组合价格
    df2=fetch_price_stock_portfolio(portfolio,start,end)

if __name__=='__main__':
    ticker='850831'
    
    start='2023-1-1'
    end='2023-4-4'
    info_types=['Close','Volume']
    
    #获取申万指数价格
    df3=fetch_price_swindex(ticker,start,end)

#多种证券价格组合
dflist=[df1,df1i,df1e,df1r,df2,df3]

#比较收益与风险指标
cmc1=compare_msecurity_cross(dflist,
                           measure='Exp Ret%',
                           start=start,end=end)

cmc2=compare_msecurity_cross(dflist,
                           measure='Annual Ret%',
                           start=start,end=end)

#比较夏普指标
rar3=rar_ratio_rolling_df(df3,ratio_name='sharpe',window=240)

cmc3=compare_mrar_cross(dflist,rar_name='sharpe',start=start,end=end,window=240)

cmc4=compare_mrar_cross(dflist,rar_name='sortino',start=start,end=end,window=240)

cmc4=compare_mrar_cross(dflist,rar_name='alpha',start=start,end=end,window=240)
#==============================================================================

# 定义投资组合：成份股与初始持股比例
# 初始持股比例跟着感觉走，后面将进行优化
Market={'Market':('China','000300.SS','地产组合1号初版')}
Stocks ={'000002.SZ':.40,#万科A
         '600048.SS':.08,#保利发展
         '001979.SZ':.08,#招商蛇口
         '600325.SS':.08,#华发股份
         '000069.SZ':.08,#华侨城A
         '600383.SS':.08,#金地集团
         '600895.SS':.05,#张江高科
         '601155.SS':.05,#新城控股
         '600606.SS':.05,#绿地控股
         '600208.SS':.05,#新湖中宝
        }
portfolio_v0=dict(Market,**Stocks)


tjend='2022-12-31'
pastyears=3


# 收集投资组合成份股的基础数据
pf_info0=portfolio_hpr(portfolio_v0, #投资组合初版
                      thedate=tjend, #截止日期
                      pastyears=pastyears,   #近三年
                      printout=False,#不打印结果
                      graph=False,   #不绘图
                     )

simulation=100000


# 第一次优化地产组合1号：优化持股比例，基于夏普比率
portfolio_optimize_strategy(
            pf_info0,             #成分股的基础数据
            ratio='sharpe',       #夏普比率
            simulation=simulation,#模拟次数
            )




#==============================================================================
