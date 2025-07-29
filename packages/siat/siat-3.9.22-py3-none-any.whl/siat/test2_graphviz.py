# -*- coding: utf-8 -*-

import os; os.chdir("S:/siat")
from siat import *

#==============================================================================

def define_dupont_orgchart(company_name,dpdf):
    """
    功能：定义杜邦分解图示的结构框架
    dpdf：数据框，项目名称，数值
    """
    
    # 定义杜邦分解项目变量
    roe=company_name+'\n\n'+'净资产收益率'
    
    roa='总资产净利率'
    em='权益乘数'
    
    pm='销售净利率'
    tat='总资产周转率'
    debtRatio='资产负债率'
    
    netProfit='净利润'
    sales1='销售收入'
    sales2='销售收入'
    totalAssets='资产总额'
    
    totalCosts='成本费用'
    currentAssets='流动资产'
    LTAssets='长期资产'
    
    salesCosts='销售成本'
    salesExpenses='销售费用'
    mgmtExpenses='管理费用'
    financialExpenses='财务费用'
    incomeTax='所得税费用'
    otherExpenses='其他支出'
    
    monetaryFunds='货币资金'
    securityAssets='有价证券'
    accountReceivables='应收款项'   #含应收张狂和应收票据
    prepaid='预付款项'
    inventory='存货'
    otherCurrentAssets='其他流动资产'
    
    fixedAssets='固定资产'
    LTInvestment='长期投资'
    intangibleAssets='无形资产'
    deferredAssets='递延资产'
    goodwill='商誉'
    
    #合成具体的分解项目
    
    
    
    # 定义杜邦分解框架
    import pandas as pd
    df=pd.DataFrame([
        
        [1,1,roe,roa,''],   
        [1,2,roe,em,''],   
        
        [2,3,em,debtRatio,''],   
        
        [2,1,roa,pm,''],   
        [2,2,roa,tat,''],   
        
        [3,1,pm,netProfit,''],   
        [3,2,pm,sales1,''],   
        
        [3,3,tat,sales1,''],   
        [3,4,tat,totalAssets,''],   
        
        [4,1,netProfit,sales2,''],
        [4,2,netProfit,totalCosts,''],
        
        [5,1,totalCosts,salesCosts,''],
        [5,2,totalCosts,salesExpenses,''],
        [5,3,totalCosts,mgmtExpenses,''],
        [5,4,totalCosts,financialExpenses,''],
        [5,5,totalCosts,incomeTax,''],
        [5,6,totalCosts,otherExpenses,''],
        
        [4,3,totalAssets,currentAssets,''],
        [4,4,totalAssets,LTAssets,''],
        
        [5,7,currentAssets,monetaryFunds,''],
        [5,8,currentAssets,securityAssets,''],
        [5,9,currentAssets,accountReceivables,''],
        [5,10,currentAssets,prepaid,''],
        [5,11,currentAssets,inventory,''],
        [5,12,currentAssets,otherCurrentAssets,''],
        
        [5,13,LTAssets,fixedAssets,''],
        [5,14,LTAssets,LTInvestment,''],
        [5,15,LTAssets,intangibleAssets,''],
        [5,16,LTAssets,deferredAssets,''],
        [5,17,LTAssets,goodwill,''],
        
        [9,1,salesCosts,'',''],
        [9,2,salesExpenses,'',''],
        [9,3,mgmtExpenses,'',''],
        [9,4,financialExpenses,'',''],
        [9,5,incomeTax,'',''],
        [9,6,otherExpenses,'',''],
        
        [9,7,monetaryFunds,'',''],
        [9,8,securityAssets,'',''],
        [9,9,accountReceivables,'',''],
        [9,10,prepaid,'',''],
        [9,11,inventory,'',''],
        [9,12,otherCurrentAssets,'',''],
        
        [9,13,fixedAssets,'',''],
        [9,14,LTInvestment,'',''],
        [9,15,intangibleAssets,'',''],
        [9,16,deferredAssets,'',''],
        [9,17,goodwill,'',''],
        
        ], columns=['level','seq','mother','child','edge text'])
    
    df.sort_values(by=['level','seq'],ascending=[True,True],inplace=True)
    
    return df


def draw_orgchart(df,shape='polygon', \
                  shape_color='black',fontcolor='blue',edge_color='red'):
    """
    功能：基于df的结构绘制杜邦分解图示
    df的结构字段：
    mother：上级节点，任意字符串，中间可用'\n'换行
    child：下级节点
    edge_text：连线上的文字
    """
    from graphviz import Digraph
    photo=Digraph('picture',format='svg')
    nodes={}
    
    for index,row in df.iterrows():
        mother_name=row['mother']
        child_name=row['child']
        edge_text=row['edge text']
        
        orientation='0.0'
        if child_name == '':
            orientation='90'
        
        if mother_name not in nodes.keys():
            photo.node(name=mother_name,shape=shape,color=shape_color, \
                       fontname="Microsoft Yahei",fontcolor=fontcolor,orientation=orientation)
        if child_name not in nodes.keys():
            if child_name != '':
                photo.node(name=child_name,shape=shape,color=shape_color, \
                           fontname="Microsoft Yahei",fontcolor=fontcolor)
            
        nodes[mother_name]=1
        nodes[child_name]=1
        
        if child_name != '':
            photo.edge(mother_name,child_name,color=edge_color,label=edge_text)
    
    photo.view()
    
    return
    

if __name__ == "__main__":
    df=define_dupont_orgchart(company_name='',dpdf='')
    draw_orgchart(df)

















#==============================================================================
if __name__=='__main__':
    ticker="600519.SS" 
    fsdate='2022-12-31'
    
    g=dupont_decompose_china(ticker,fsdate)

def dupont_decompose_china(ticker,fsdate):
    """
    功能：杜邦分析分解图
    ticker: 股票代码
    fsdate： 财报日期
    """
    #检查日期
    result,fspd,_=check_period(fsdate,fsdate)
    if not result:
        print("  #Error(dupont_decompose_china): invalid date",fsdate)
        return None
    
    #获取财报
    fs=get_fin_stmt_ak(ticker)
    if fs is None:
        print("  #Error(dupont_decompose_china): stock not found for",ticker)
        return None
    
    fs1=fs[fs.index==fspd]
    if len(fs1)==0:
        print("  #Error(dupont_decompose_china): financial statements not found for",ticker,'@',fsdate)
        return None

    #亿元
    yi=100000000

    company_name=codetranslate(ticker)
    # 定义杜邦分解项目变量
    
    roe=company_name+'\n\n'+'净资产收益率'
    totalOEValue=round(fs1['所有者权益(或股东权益)合计'].values[0] / yi,1)
    
    roa='总资产净利率'
    
    em='权益乘数'
    
    pm='销售净利率'
    
    tat='总资产周转率'
    
    debtRatio='资产负债率'
    totalLiabValue=round(fs1['负债合计'].values[0] / yi,1)
    
    netProfit='净利润'
    netProfitValue=round(fs1['五、净利润'].values[0] / yi,1)
    roePct=round(netProfitValue / totalOEValue *100,2)
    
    sales='销售收入'
    salesValue=round(fs1['一、营业总收入'].values[0] / yi,1)
    pmPct=round(netProfitValue / salesValue *100,2)
    
    totalAssets='资产总额'
    totalAssetsValue=round(fs1['资产总计'].values[0] / yi,1)
    tatValue=round(salesValue / totalAssetsValue *100,2)
    emValue=round(totalAssetsValue / totalOEValue,2)
    debtRatioPct=round(totalLiabValue / totalAssetsValue *100,2)
    roaPct=round(netProfitValue / totalAssetsValue *100,2)
    
    totalCosts='成本费用'
    totalCostsValue=round(fs1['二、营业总成本'].values[0] / yi,1)
    
    currentAssets='流动资产'
    currentAssetsValue=round(fs1['流动资产合计'].values[0] / yi,1)
    
    LTAssets='非流动资产'
    LTAssetsValue=round(fs1['非流动资产合计'].values[0] / yi,1)
    
    salesCosts='营业\\n成本'
    salesCostsValue=round(fs1['营业成本'].values[0] / yi,1)
    
    periodExpenses='期间\\n费用'
    salesExpenses='销售\\n费用'
    salesExpensesValue=round(fs1['销售费用'].values[0] / yi,1)
    
    mgmtExpenses='管理\\n费用'
    mgmtExpensesValue=round(fs1['管理费用'].values[0] / yi,1)
    
    rndExpenses='研发\\n费用'
    rndExpensesValue=round(fs1['研发费用'].values[0] / yi,1)
    """
    #是否中国股票
    result,prefix,suffix=split_prefix_suffix(ticker)
    if not (suffix in STOCK_SUFFIX_CHINA):
        print("  #Error(dupont_decompose_china): not a stock in China",ticker)
        return None        
    
    #财务报告摘要
    try:
        fsabs = ak.stock_financial_abstract(prefix)
    except:
        print("  #Warning(dupont_decompose_china): financial summary not found for",ticker)
        return None
    """
    financialExpenses='利息\\n费用'
    financialExpensesValue=round(fs1['应付利息'].values[0] / yi,1)
    
    taxExpenses='税金'
    taxExpensesValue=round((fs1['营业税金及附加'].values[0] + fs1['减：所得税费用'].values[0]) / yi,1)
    
    otherExpenses='其他支出'
    otherExpensesVaue=round((fs1['开发支出'].values[0] + fs1['减：营业外支出'].values[0]) / yi,1)
    
    monetaryFunds='货币\\n资金'
    monetaryFundsValue=round(fs1['货币资金'].values[0] / yi,1)
    
    securityAssets='金融\\n资产'
    securityAssetsValue=round((fs1['交易性金融资产'].values[0] + \
                               fs1['衍生金融资产'].values[0] + \
                               fs1['买入返售金融资产'].values[0]) / yi,1)
    
    ar_prepaid='应收\\n与\\n预付'
    accountReceivables='应收\\n款项'
    accountReceivablesValue=round((fs1['应收票据及应收账款'].values[0] + fs1['其他应收款(合计)'].values[0]) / yi,1)  
    
    prepaid='预付\\n款项'
    prepaidValue=round(fs1['预付款项'].values[0] / yi,1)
    
    inventory='存货'
    inventoryValue=round(fs1['存货'].values[0] / yi,1)
    
    otherCurrentAssets='其他\\n流动\\n资产'
    otherCurrentAssetsValue=round(fs1['其他流动资产'].values[0] / yi,1)
    
    fixedAssets='固定\\n资产'
    fixedAssetsValue=round(fs1['固定资产及清理(合计)'].values[0] / yi,1)
    
    LTInvestment='长期\\n投资'
    LTInvestmentValue=round((fs1['发放贷款及垫款'].values[0] + \
                        fs1['可供出售金融资产'].values[0] + \
                        fs1['持有至到期投资'].values[0] + \
                       #fs1['长期应收款'].values[0] + \
                        fs1['长期股权投资'].values[0] + \
                        fs1['投资性房地产'].values[0] + \
                        fs1['在建工程(合计)'].values[0]) / yi,1)
    
    intangibleAssets='无形\\n资产'
    intangibleAssetsValue=round(fs1['无形资产'].values[0] / yi,1)
    
    deferredAssets='递延\\n资产'
    deferredAssetsValue=round(fs1['递延所得税资产'].values[0] / yi,1)
    
    goodwill='商誉'
    goodwillValue=round(fs1['商誉'].values[0] / yi,1)

    #合成具体的分解项目
    roe=roe+'\n'+str(roePct)+'%'
    roa=roa+'\n'+str(roaPct)+'%'
    em=em+'\n'+str(emValue)
    pm=pm+'\n'+str(pmPct)+'%'
    tat=tat+'\n'+str(tatValue)

    netProfit=netProfit+'\n'+str(netProfitValue)
    totalAssets=totalAssets+'\n'+str(totalAssetsValue)
    totalCosts=totalCosts+'\n'+str(totalCostsValue)
    sales=sales+'\n'+str(salesValue)
    currentAssets=currentAssets+'\n'+str(currentAssetsValue)
    LTAssets=LTAssets+'\n'+str(LTAssetsValue)
    
    salesCosts=salesCosts+'\n'+str(salesCostsValue)
    taxExpenses=taxExpenses+'\n'+str(taxExpensesValue)
    
    salesExpenses=salesExpenses+'\n'+str(salesExpensesValue)
    mgmtExpenses=mgmtExpenses+'\n'+str(mgmtExpensesValue)
    financialExpenses=financialExpenses+'\n'+str(financialExpensesValue)
    rndExpenses=rndExpenses+'\n'+str(rndExpensesValue)

    monetaryFunds=monetaryFunds+'\n'+str(monetaryFundsValue)
    securityAssets=securityAssets+'\n'+str(securityAssetsValue)
    accountReceivables=accountReceivables+'\n'+str(accountReceivablesValue)
    prepaid=prepaid+'\n'+str(prepaidValue)
    inventory=inventory+'\n'+str(inventoryValue)

    fixedAssets=fixedAssets+'\n'+str(fixedAssetsValue)
    LTInvestment=LTInvestment+'\n'+str(LTInvestmentValue)
    intangibleAssets=intangibleAssets+'\n'+str(intangibleAssetsValue)

    #下面字段：“序号”、“父单位”、“父单位层级”、“子单位”、“子单位层级”、“父单位持股比例”
    #注意：最后面的空格字段为必须，否则显示顺序不受控
    L=[
        [1, roe, 1, roa, 2, ' '],
        [2, roe, 1, em, 2, ' '],
        [3, roa, 2, pm, 3, ' '],
        [4, roa, 2, tat, 3, ' '],
        [5, pm, 3, netProfit, 4, ' '],
        [6, pm, 3, sales, 4, ' '],
        [7, netProfit, 4, sales, 5, ' '],
        [8, netProfit, 4, totalCosts, 5, ' '],
        [9, totalCosts, 5, salesCosts, 6, ' '],
        
        [10, totalCosts, 5, periodExpenses, 6, ' '],
        [11, periodExpenses, 6, salesExpenses, 7, ' '],
        [12, periodExpenses, 6, mgmtExpenses, 7, ' '],
        [13, periodExpenses, 6, financialExpenses, 7, ' '],
        [14, periodExpenses, 6, rndExpenses, 7, ' '],
        
        [15, totalCosts, 5, taxExpenses, 6, ' '],
        
        [16, tat, 3, sales, 4, ' '],
        [17, tat, 3, totalAssets, 4, ' '],
        [18, totalAssets, 4, currentAssets, 5, ' '],
        [19, totalAssets, 4, LTAssets, 5, ' '],
        
        [20, currentAssets, 5, monetaryFunds, 6, ' '],
        [21, currentAssets, 5, securityAssets, 6, ' '],
        
        [22, currentAssets, 5, ar_prepaid, 6, ' '],
        [23, ar_prepaid, 6, accountReceivables, 7, ' '],        
        [24, ar_prepaid, 6, prepaid, 7, ' '],
        
        [25, currentAssets, 5, inventory, 10, ' '],
       #[26, currentAssets, 5, otherCurrentAssets, 11, ' '],
        
        [27, LTAssets, 5, fixedAssets, 6, ' '],
        [28, LTAssets, 5, LTInvestment, 6, ' '],
        [29, LTAssets, 5, intangibleAssets, 6, ' '],
       #[30, LTAssets, 5, deferredAssets, 6, ' '],
       #[31, LTAssets, 5, goodwill, 6, ' '],
        
    ]    
    
    dic={}
    father_name_list=[]
    child_name_list=[]
    equity_portion_list=[]
    for i1 in range(len(L)):
        
        M=L[i1]
        father_name=M[1]
        father_name_list.append(M[1])
        father_layer=M[2]
        child_name=M[3]
        child_name_list.append(M[3])
        child_layer=M[4]
        equity_portion=M[5]
        equity_portion_list.append(M[5])
        
        #debug使用
        #print(i1,M,father_name,father_layer,child_name,child_layer,equity_portion)
        
        for x in father_name:
            dic[father_name]=father_layer   #生成父单位名称和对应的层级（用字典考虑去重）
        
        for y in child_name:
            dic[child_name]=child_layer     #将子单位名称和对应的层级也添加到字典中
            
    name_layer_list = sorted(dic.items(), key=lambda x: x[1]) #对字典按值（value）进行排序（默认由小到大）
    
    u=[]
    for z in name_layer_list:
        company_name=z[0]
        layer=z[1]
        u.append(z[1])
    number_of_layers=max(u) #计算出层数
    
    from graphviz import Digraph
    #按各公司的层数生产分层的节点：
    g=Digraph(name='DuPont Decompose')
    
    for key in dic:
        for n in range(number_of_layers+1):
            if dic[key]==n:
                with g.subgraph() as layer_n:
                    layer_n.attr(rank='same')
                    layer_n.node(name=key,color='blue',shape='box',fontname='Microsoft YaHei')
    
    #生产各节点间的连线：
    for i2 in range(len(L)):
        g.edge(father_name_list[i2],child_name_list[i2],label=equity_portion_list[i2],color='red',fontname='Microsoft Yahei')
    
    g.view()  
    
    #打印信息
    print("注:",company_name,"\b，金额单位：亿元，财报日期:",fsdate)
    print("1、应收款项包括应收账款和应收票据")
    print("2、递延资产为递延所得税资产")
    print("3、税金包括营业税金及附加以及所得税费用")
    print("4、此处的金融资产包括交易性金融资产、衍生金融资产和买入返售金融资产")
    print("5、此处的长期投资包括发放贷款及垫款、可供出售金融资产、持有至到期投资、长期股权投资、投资性房地产以及在建工程")

    return g

if __name__=='__main__':
    ticker="600519.SS" 
    fsdate='2022-12-31'
    
    g=dupont_decompose_china(ticker,fsdate)


#==============================================================================
