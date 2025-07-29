# -*- coding: utf-8 -*-
"""
功能：一次性引入SIAT的所有模块
作者：王德宏，北京外国语大学国际商学院
版权：2021-2024(C) 仅限教学使用，商业使用需要授权
联络：wdehong2000@163.com
"""

#==============================================================================
#屏蔽所有警告性信息
import warnings; warnings.filterwarnings('ignore')
#==============================================================================
from siat.allin import *
#==============================================================================
#同一命令行多个输出，主要用于Jupyter Notebook
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity='all'
#==============================================================================
# 检查是否存在新版本
try:
    import pkg_resources
    current_version=pkg_resources.get_distribution("siat").version
    current_list=current_version.split('.')
    print("Successfully imported siat version",current_version)

    import luddite
    latest_version=luddite.get_version_pypi("siat")
    latest_list=latest_version.split('.')
    
    newest=True
    for i in range(3):
        #print(i)
        if int(current_list[i]) < int(latest_list[i]):
            newest=False
    
    """
    if not newest:
        print("The latest version of siat is",latest_version,'\n')
        print("*** If you expect to upgrade siat in Anaconda Prompt, use the instruction below:")
        print("    pip install siat --upgrade")
        print("*** If you expect to upgrade in Jupyter, add a \'!\' right before the instruction above",'\n')
        
        print("*** If you encounter incompatible plug-in, try to uninstall siat first and reinstall it:")
        print("    pip uninstall siat")
        print("    pip install siat",'\n')
        
        print("*** If you have a slow internet connection, use an option trailing the instruction above:")
        print("    -i https://mirrors.aliyun.com/pypi/simple/",'\n')
    
        print("If you have done any of the above, restart the Python (eg. restarting the kernel)")
        print("Provided you still need additional help, please contact wdehong2000@163.com")
    """
    if not newest:
        #print("The latest version of siat is",latest_version,'\n')
        print("Now there is a newer version of siat",latest_version,'\n')
        print("*** How to upgrade siat?")
        print("Upgrade directly from official source? use command: upgrade_siat()")
        print("Upgrade from Tsinghua? use command: upgrade_siat(alternative='tsinghua')")
        print("Upgrade from Alibaba? use command: upgrade_siat(alternative='alibaba')")
    
except:
    pass
    

#==============================================================================
