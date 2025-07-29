# -*- coding: utf-8 -*-
import os; os.chdir('S:/siat')
from siat import *
#==============================================================================

from sklearn import tree # 导入树
from sklearn.datasets import load_wine #红酒数据集
from sklearn.model_selection import train_test_split #数据集的分割操作

wine = load_wine() #加载数据集

import pandas as pd #利用pandas将data与target拼接成数据表
pd.concat([pd.DataFrame(wine.data),pd.DataFrame(wine.target)],axis=1)

Xtrain,Xtest,Ytrain,Ytest = train_test_split(wine.data,wine.target,test_size=0.3) #将数据集划分为训练集和测试集

clf = tree.DecisionTreeClassifier(criterion='entropy') #实例化一个决策分类树模型
clf = clf.fit(Xtrain,Ytrain) #模型拟合
score = clf.score(Xtest,Ytest) #返回预测的准确度accuracy
feature_name = ['酒精','苹果酸','灰','灰的碱性','镁','总酚','类黄酮','非黄烷类酚类',
                '花青素','颜色强度','色调','od280/od315稀释葡萄酒','脯氨酸']
import graphviz
dot_data = tree.export_graphviz(clf
                               ,out_file = None
                               ,feature_names= feature_name
                               ,class_names=["琴酒","雪莉","贝尔摩德"]
                               ,filled=True
                               ,rounded=True
                               
                               ) # 第一个参数为实例化的模型参数
graph = graphviz.Source(dot_data) #绘制决策树

graph.view()

graph



#==============================================================================

import pandas as pd
data1=pd.DataFrame([
    
    ['NaN','水果',0.339,'ROOT->水果',1],   
    ['NaN','零食',0.225,'ROOT->零食',1],   

    ['水果','柑果',3.241,'水果->柑果',2],   
    ['水果','梨果',0.054,'水果->梨果',2],   

    ['柑果','橙子',1.457,'柑果->橙子',3],   
    ['柑果','橘子',0.237,'柑果->橘子',3],   
    ['柑果','柚子',1.800,'柑果->柚子',3],   

    ['柚子','葡萄柚',9.544,'柚子->沙田柚',4],   
    ['橙子','甜橙',1.078,'橙子->甜橙',4],   
    ['橙子','脐橙',1.656,'橙子->脐橙',4],   
    
    ], columns=['pnode','node','gap','edge','lv'])

from graphviz import Digraph
# 实例化一个Digraph对象(有向图)，name:生成的图片的图片名，format:生成的图片格式
dot= Digraph(name="DuPont_Identity",format="svg")

# 将所有列的数据都转成list格式
node_list = data1['node'].tolist()
gap_list=data1['gap'].tolist()
edge_list=data1['edge'].tolist()
lv_list=data1['lv'].tolist()

# dot.node定义节点名称，name：这个节点对象的名称，label:节点名,color：画节点的线的颜色
# fontname：防止字体乱码情况
for i in range(len(node_list)):
    dot.node(name=edge_list[i].split('->')[1]+"_"+edge_list[i].split('->')[0],
             label=node_list[i]+'\n'+"Gap:{:.2f}K".format(gap_list[i]),
             shape='box',
             color="peachpuff",
             style = "filled",
             fontname="Microsoft YaHei")

# add edges 1-4层
for i in range(len(node_list)):
    target_list=edge_list[i].split('->')[1]+"|"+edge_list[i].split('->')[0]
    # add edge 第一层
    if lv_list[i]==1 and "ROOT" in target_list:
        dot.edge('Company',target_list)
    # add edge 第二层
    for j in range(len(node_list)):
        temp_list=edge_list[j].split('->')[1]+"|"+edge_list[j].split('->')[0]
        if lv_list[i]==2 and lv_list[j]==1 and (target_list.split("|")[1] == temp_list.split("|")[0]) :
            dot.edge(temp_list,target_list)
    # add edge 第三层
        if lv_list[i]==3 and lv_list[j]==2 and (target_list.split("|")[1] == temp_list.split("|")[0]):
            dot.edge(temp_list,target_list)
   # add edge 第四层         
        if lv_list[i]==4 and lv_list[j]==3 and (target_list.split("|")[1] == temp_list.split("|")[0]):
            dot.edge(temp_list,target_list)


# filename:图片的名称，若无filename，则使用Digraph对象的name，默认会有gv后缀
# directory:图片保存的路径，默认是在当前路径下保存
# dot.view(filename="水果零食业绩归因", directory="D:\MyTest")
import graphviz
g = graphviz.Source(dot) #绘制决策树
g.view()

g


#==============================================================================

import pandas as pd
data1=pd.DataFrame([
    
    ['NaN','水果',-4.373,0.339,'ROOT->水果',1],   
    ['NaN','零食',-3.492,0.225,'ROOT->零食',1],   

    ['水果','柑果',-1.575,3.241,'水果->柑果',2],   
    ['水果','梨果',-4.380,0.054,'水果->梨果',2],   

    ['柑果','橙子',-3.025,1.457,'柑果->橙子',3],   
    ['柑果','橘子',-5.707,0.237,'柑果->橘子',3],   
    ['柑果','柚子',-6.765,1.800,'柑果->柚子',3],   

    ['柚子','葡萄柚',-1.158,9.544,'柚子->沙田柚',4],   
    ['橙子','甜橙',-1.170,1.078,'橙子->甜橙',4],   
    ['橙子','脐橙',-1.640,1.656,'橙子->脐橙',4],   

    
    ], columns=['pnode','node','gap','gap_rate','edge','lv'])


# 实例化一个Digraph对象(有向图)，name:生成的图片的图片名，format:生成的图片格式
dot= Digraph(name="G",format="png")
 
# 将所有列的数据都转成list格式
node_list = data1['node'].tolist()
gap_list=data1['gap'].tolist()
gap_rate_list=data1['gap_rate'].tolist()
edge_list=data1['edge'].tolist()
lv_list=data1['lv'].tolist()
 
# dot.node定义节点名称，name：这个节点对象的名称，label:节点名,color：画节点的线的颜色
# fontname：防止字体乱码情况
for i in range(len(node_list)):
    if gap_rate_list[i]>0.5: 
        dot.node(name=edge_list[i].split('->')[1]+"|"+edge_list[i].split('->')[0],
                 label=node_list[i]+'\n'+"Gap:{:.2f}K".format(gap_list[i]/1000),
                 color="lightsalmon",
                 style = "filled",
                 fontname="Microsoft YaHei")
    else:
        dot.node(name=edge_list[i].split('->')[1]+"|"+edge_list[i].split('->')[0],
                 label=node_list[i]+'\n'+"Gap:{:.2f}K".format(gap_list[i]/1000),
                 color="peachpuff",
                 style = "filled",
                 fontname="Microsoft YaHei")


# add edges 1-4层
for i in range(len(node_list)):
    target_list=edge_list[i].split('->')[1]+"|"+edge_list[i].split('->')[0]
    # add edge 第一层
    if lv_list[i]==1 and "ROOT" in target_list:
        dot.edge('total_gap',target_list)
    # add edge 第二层
    for j in range(len(node_list)):
        temp_list=edge_list[j].split('->')[1]+"|"+edge_list[j].split('->')[0]
        if lv_list[i]==2 and lv_list[j]==1 and (target_list.split("|")[1] == temp_list.split("|")[0]) :
            dot.edge(temp_list,target_list)
    # add edge 第三层
        if lv_list[i]==3 and lv_list[j]==2 and gap_rate_list[j]>0.1 and (target_list.split("|")[1] == temp_list.split("|")[0]):
            dot.edge(temp_list,target_list)
   # add edge 第四层         
        if lv_list[i]==4 and lv_list[j]==3 and gap_rate_list[j]>0.1 and (target_list.split("|")[1] == temp_list.split("|")[0]):
            dot.edge(temp_list,target_list)


# filename:图片的名称，若无filename，则使用Digraph对象的name，默认会有gv后缀
# directory:图片保存的路径，默认是在当前路径下保存
# dot.view(filename="水果零食业绩归因", directory="D:\MyTest")
dot.view()


#==============================================================================
from graphviz import Digraph

dot = Digraph(comment='The Test Table')
# 添加圆点A,A的标签是Dot A
dot.node('A', 'Dot A')
# 添加圆点 B, B的标签是Dot B
dot.node('B', 'Dot B')
# dot.view()
# 添加圆点 C, C的标签是Dot C
dot.node(name='C', label= 'Dot C',color='red')
# dot.view()

# 创建一堆边，即连接AB的两条边，连接AC的一条边。
dot.edges(['AB', 'AC', 'AB'])
# dot.view()
# 在创建两圆点之间创建一条边
dot.edge('B', 'C', 'test')
# dot.view()

# 获取DOT source源码的字符串形式
print(dot.source)
dot.view()
dot.render('test-table.gv', view=True)







#==============================================================================

import graphviz

# 创建Digraph对象
dot = graphviz.Digraph(comment='Simple Process')

# 添加节点
dot.node('A', 'Start')
dot.node('B', 'Process 1')
dot.node('C', 'Process 2')
dot.node('D', 'End')

# 添加边
dot.edges(['AB', 'BC', 'CD'])

# 保存为PNG图片
dot.format = 'png'
# 渲染和保存流程图
dot.render(filename='simple-process', directory='D:/QTEMP', cleanup=True)
#==============================================================================

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
plt.subplots_adjust(left=0.00, bottom=0.0, right=1.00, top=0.95, wspace=0.0, hspace=0.00)


def hexagon_with_text(ax,x,y,text,size,**kwargs):
    xy=np.array([x,y])
    hexagon = mpatches.RegularPolygon(xy, 6, radius=size,facecolor='#5472bb',edgecolor='#3f597c', orientation=np.pi / 2)
    ax.add_patch(hexagon)
    ax.text(xy[0],xy[1],text,fontsize=size*14,color='white',va='center',ha='center')

def circle_with_text(ax,x,y,text,size,**kwargs):
    xy=np.array([x,y])
    circle = mpatches.Circle(xy, radius=size,facecolor='#83aa51',edgecolor='#546538')
    ax.add_patch(circle)
    ax.text(xy[0],xy[1],text,fontsize=size*14,color='white',va='center',ha='center')

def arrow(ax,x,y,size,**kwargs):
    ax.plot(x,y,**kwargs)
    theta=np.arctan2(x[1]-x[0],y[1]-y[0])
    xy=np.array([x[1]-size*np.sin(theta),y[1]-size*np.cos(theta)])
    triangle = mpatches.RegularPolygon(xy, 3, radius=size,color=kwargs['color'], orientation=-theta)
    ax.add_patch(triangle)

def arrow_with_rad(ax,x,y,radius,size,**kwargs):
    d=np.sqrt((x[1]-x[0])**2+(y[1]-y[0])**2)

    theta=np.arctan2(x[1]-x[0],y[0]-y[1])

    x0=(x[0]+x[1])/2+np.cos(theta)*np.sqrt(radius**2-(d/2)**2)
    y0=(y[0]+y[1])/2+np.sin(theta)*np.sqrt(radius**2-(d/2)**2)

    theta1=np.arctan2(y[0]-y0,x[0]-x0)
    theta2=np.arctan2(y[1]-y0,x[1]-x0)

    arc_x = []
    arc_y = []

    for theta in np.arange(theta1,theta2+(np.pi*2),np.pi/180):
        temp_x=x0 + radius * np.cos(theta)
        temp_y=y0 + radius * np.sin(theta)
        if((temp_x-x[0])**2+(temp_y-y[0])**2>1 and (temp_x-x[1])**2+(temp_y-y[1])**2>1):
            arc_x.append(temp_x)
            arc_y.append(temp_y)
    ax.plot(arc_x,arc_y,**kwargs)

    theta=np.arctan2(arc_y[-2]-arc_y[-1],arc_x[-2]-arc_x[-1])
    xy=np.array([arc_x[-1]+size*np.cos(theta),arc_y[-1]+size*np.sin(theta)])
    triangle = mpatches.RegularPolygon(xy, 3, radius=size,color=kwargs['color'], orientation=np.pi/2+theta)
    ax.add_patch(triangle)

ax=plt.subplot(1,1,1,aspect='equal')
ax.axis('off')

circle_with_text(ax,2,23,'$\mathrm{U_{1}}$',1)
circle_with_text(ax,2,20,'$\mathrm{U_{2}}$',1)
circle_with_text(ax,2,17,'$\mathrm{U_{3}}$',1)
circle_with_text(ax,2,14,'$\mathrm{U_{4}}$',1)

hexagon_with_text(ax,8,22.5,'$\mathrm{I_{1}}$',1)
hexagon_with_text(ax,8,18.5,'$\mathrm{I_{2}}$',1)
hexagon_with_text(ax,8,14.5,'$\mathrm{I_{3}}$',1)

arrow(ax,[3,8+np.cos(np.pi*3/3)],[23,22.5+np.sin(np.pi*3/3)],0.3,color='#b65576',linestyle='--')
arrow(ax,[3,8+np.cos(np.pi*2/3)],[23,14.5+np.sin(np.pi*2/3)],0.3,color='#b65576',linestyle='--')
arrow(ax,[3,8+np.cos(np.pi*4/3)],[17,22.5+np.sin(np.pi*4/3)],0.3,color='#b65576',linestyle='--')
arrow(ax,[3,8+np.cos(np.pi*4/3)],[14,18.5+np.sin(np.pi*4/3)],0.3,color='#b65576',linestyle='--')

arrow(ax,[3,8+np.cos(np.pi*3/3)],[20,18.5+np.sin(np.pi*3/3)],0.3,color='#b9b8bd',linestyle='--')
arrow(ax,[3,8+np.cos(np.pi*3/3)],[17,14.5+np.sin(np.pi*3/3)],0.3,color='#b9b8bd',linestyle='--')
arrow(ax,[3,8+np.cos(np.pi*3/3)],[14,14.5+np.sin(np.pi*3/3)],0.3,color='#b9b8bd',linestyle='--')

ax.text(10.5,15,'${G_{r}}$',fontsize=20)

circle_with_text(ax,4.2,10.5,'$\mathrm{U_{1}}$',1)
circle_with_text(ax,9.0,10.0,'$\mathrm{U_{2}}$',1)
circle_with_text(ax,8.5,5.8,'$\mathrm{U_{3}}$',1)
circle_with_text(ax,3.8,6.8,'$\mathrm{U_{4}}$',1)

theta=-np.pi/2-np.arctan2(9.0-4.2,10.0-10.5)
arrow(ax,[9.0+np.cos(theta),4.2-np.cos(theta)],[10.0+np.sin(theta),10.5-np.sin(theta)],0.3,color='#8199bb')

theta=-np.pi/2-np.arctan2(8.5-9.0,5.8-10.0)
arrow(ax,[8.5+np.cos(theta),9.0-np.cos(theta)],[5.8+np.sin(theta),10.0-np.sin(theta)],0.3,color='#8199bb')

theta=-np.pi/2-np.arctan2(3.8-4.2,6.8-10.5)
arrow(ax,[3.8+np.cos(theta),4.2-np.cos(theta)],[6.8+np.sin(theta),10.5-np.sin(theta)],0.3,color='#8199bb')

theta=-np.pi/2-np.arctan2(3.8-8.5,6.8-5.8)
arrow(ax,[3.8+np.cos(theta),8.5-np.cos(theta)],[6.8+np.sin(theta),5.8-np.sin(theta)],0.3,color='#8199bb')

theta=-np.pi/2-np.arctan2(4.2-8.5,10.5-5.8)
arrow(ax,[4.2+np.cos(theta),8.5-np.cos(theta)],[10.5+np.sin(theta),5.8-np.sin(theta)],0.3,color='#8199bb')

arrow_with_rad(ax,[4.2,3.8],[10.5,6.8],1.9,0.3,color='#8199bb')

ax.text(10.5,8,r'${G_s}$',fontsize=20)

circle_with_text(ax,25.0,19.0,'$\mathrm{U_{1}}$',1)
circle_with_text(ax,35.0,17.0,'$\mathrm{U_{2}}$',1)
circle_with_text(ax,32.0,8.0,'$\mathrm{U_{3}}$',1)
circle_with_text(ax,24.0,10.0,'$\mathrm{U_{4}}$',1)

hexagon_with_text(ax,32.5,14.0,'$\mathrm{I_{1}}$',1)
hexagon_with_text(ax,23.0,16.0,'$\mathrm{I_{2}}$',1)
hexagon_with_text(ax,27.0,13.0,'$\mathrm{I_{3}}$',1)

theta=-np.pi/2-np.arctan2(35.0-25.0,17.0-19.0)
arrow(ax,[35.0+np.cos(theta),25.0-np.cos(theta)],[17.0+np.sin(theta),19.0-np.sin(theta)],0.3,color='#8199bb')

theta=-np.pi/2-np.arctan2(24.0-25.0,10.0-19.0)
arrow(ax,[24.0+np.cos(theta),25.0-np.cos(theta)],[10.0+np.sin(theta),19.0-np.sin(theta)],0.3,color='#8199bb')

theta=-np.pi/2-np.arctan2(24.0-32.0,10.0-8.0)
arrow(ax,[24.0+np.cos(theta),32.0-np.cos(theta)],[10.0+np.sin(theta),8.0-np.sin(theta)],0.3,color='#8199bb')

theta=-np.pi/2-np.arctan2(32.0-35.0,8.0-17.0)
arrow(ax,[32.0+np.cos(theta),35.0-np.cos(theta)],[8.0+np.sin(theta),17.0-np.sin(theta)],0.3,color='#8199bb')

theta=-np.pi/2-np.arctan2(25.0-32.0,19.0-8.0)
arrow(ax,[25.0+np.cos(theta),32.0-np.cos(theta)],[19.0+np.sin(theta),8.0-np.sin(theta)],0.3,color='#8199bb')

theta=-np.pi/2-np.arctan2(24.0-23-np.cos(np.pi*5/3),10.0-16.0-np.sin(np.pi*5/3))
arrow(ax,[24.0+np.cos(theta),23.0+np.cos(np.pi*5/3)],[10.0+np.sin(theta),16.0+np.sin(np.pi*5/3)],0.3,color='#b65576',linestyle='--')

theta=-np.pi/2-np.arctan2(32.0-32.5-np.cos(np.pi*4/3),8.0-14.0-np.sin(np.pi*4/3))
arrow(ax,[32.0+np.cos(theta),32.5+np.cos(np.pi*4/3)],[8.0+np.sin(theta),14.0+np.sin(np.pi*4/3)],0.3,color='#b65576',linestyle='--')

theta=-np.pi/2-np.arctan2(25.0-32.0-np.cos(np.pi*2/3),19.0-8.0-np.sin(np.pi*2/3))
arrow(ax,[25.0+np.cos(theta),27.0+np.cos(np.pi*2/3)],[19.0+np.sin(theta),13.0+np.sin(np.pi*2/3)],0.3,color='#b65576',linestyle='--')
arrow(ax,[25.0+np.cos(theta),32.5+np.cos(np.pi*3/3)],[19.0+np.sin(theta),14.0+np.sin(np.pi*3/3)],0.3,color='#b65576',linestyle='--')

theta=-np.pi/2-np.arctan2(24.0-23-np.cos(np.pi*5/3),10.0-16.0-np.sin(np.pi*5/3))
arrow(ax,[24.0+np.cos(theta),23.0+np.cos(np.pi*5/3)],[10.0+np.sin(theta),16.0+np.sin(np.pi*5/3)],0.3,color='#b65576',linestyle='--')

theta=-np.pi/2-np.arctan2(35.0-23-np.cos(np.pi*0/3),17.0-16.0-np.sin(np.pi*0/3))
arrow(ax,[35.0+np.cos(theta),23.0+np.cos(np.pi*0/3)],[17.0+np.sin(theta),16.0+np.sin(np.pi*0/3)],0.3,color='#b9b8bd',linestyle='--')

theta=-np.pi/2-np.arctan2(24.0-27-np.cos(np.pi*4/3),10.0-13.0-np.sin(np.pi*4/3))
arrow(ax,[24.0+np.cos(theta),27.0+np.cos(np.pi*4/3)],[10.0+np.sin(theta),13.0+np.sin(np.pi*4/3)],0.3,color='#b9b8bd',linestyle='--')

theta=-np.pi/2-np.arctan2(32.0-27-np.cos(np.pi*5/3),8.0-13.0-np.sin(np.pi*5/3))
arrow(ax,[32.0+np.cos(theta),27.0+np.cos(np.pi*5/3)],[8.0+np.sin(theta),13.0+np.sin(np.pi*5/3)],0.3,color='#b9b8bd',linestyle='--')

arrow_with_rad(ax,[25,24],[19,10],4.8,0.3,color='#8199bb')

bbox_props = dict(boxstyle="rarrow,pad=0.3", fc="#629cce", ec="#657084", lw=2)

ax.text(16, 18, " "*15, ha="center", va="center", rotation=345,
            size=15,
            bbox=bbox_props)

ax.text(16, 9, " "*15, ha="center", va="center", rotation=30,
            size=15,
            bbox=bbox_props)

arrow(ax,[10,13],[24.5,24.5],0.3,color='#b65576',linestyle='--')
arrow(ax,[20,23],[24.5,24.5],0.3,color='#b9b8bd',linestyle='--')
arrow(ax,[27,30],[24.5,24.5],0.3,color='#8199bb')

ax.text(9.5,24.5,'Purchase-P',fontsize=15,va='center',ha='right')
ax.text(19.5,24.5,'Purchase-N',fontsize=15,va='center',ha='right')
ax.text(26.5,24.5,'Trust',fontsize=15,va='center',ha='right')

fig=plt.gcf()
fig.set_size_inches(14, 8)

ax.set_xlim(0,40)
ax.set_ylim(0,25)

plt.show()


#==============================================================================
