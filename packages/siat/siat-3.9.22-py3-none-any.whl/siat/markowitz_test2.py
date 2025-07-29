# -*- coding: utf-8 -*-
import os; os.chdir('S:/siat')
from siat import *

#==============================================================================
# 近三年期间
start='2023-1-1'; end='2023-4-10'

# 一级行业
print_industry_sw(itype='I')

# 二级行业
print_industry_sw(itype='T')

# 三级行业
print_industry_sw(itype='3')

# 搜索行业数据并进行初步计算：基于申万行业分类
# 本步骤可能耗费较多时间，具体取决于网速和电脑计算速度
idf1,idfall1=get_industry_info_sw(start,end,itype='I')

idf2,idfall2=get_industry_info_sw(start,end,itype='T')

idf3,idfall3=get_industry_info_sw(start,end,itype='3')

# 收益排名
idf=idf1
df1=rank_industry_sw(idf1,measure='Exp Ret%',
                     axisamp=0.9)

df2=rank_industry_sw(idf2,measure='Exp Ret%')

industries=['游戏Ⅲ','通信网络设备及器件','国际工程','横向通用软件','激光设备','集成电路封测','安防设备']
df3=rank_industry_sw(idf3,measure='Exp Ret%',industries=industries,axisamp=2.5)


# 选择感兴趣的行业，观察其持有收益率的发展趋势
industries1=industry_sw_codes(['电力设备','食品饮料','国防军工','银行'])
df1i=compare_industry_sw(idfall,industries1,measure='Exp Ret%')

# 收益-风险性价比

# 全行业，夏普比率横向对比
df1sharpe=rank_industry_sw_sharpe(idfall,base_return='Exp Ret%',axisamp=0.8)

# 感兴趣行业，时间序列对比
df1isharpe=compare_industry_sw_sharpe(idfall,industries1,
                               base_return='Exp Ret%')







#==============================================================================

# 一级行业
print_industry_sw(itype='I')

# 搜索行业数据并进行初步计算：基于申万行业分类
# 本步骤可能耗费较多时间，具体取决于网速和电脑计算速度
idf1,idfall1=get_industry_info_sw(start,end,itype='I')
idf=idf1

industries=['801770', '801720', '医药生物']
df1=rank_industry_sw(idf1,measure='Exp Ret%',industries=industries,axisamp=0.9,printout=True)

#==============================================================================
