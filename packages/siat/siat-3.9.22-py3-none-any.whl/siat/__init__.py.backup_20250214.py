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
try:
    from siat.allin import *
    success=True
except:
    print("  #Warning: failed to enable siat!")
    import sys; version=sys.version
    version_list=version.split('|')
    python_version=version_list[0].strip()
    python_version_list=python_version.split('.')
    python_version2="{0}.{1}".format(python_version_list[0],python_version_list[1])
    
    if python_version2 < '3.11':
        print("  Solution: your Python version is {0}, suggest upgrade to {1} or above".format(python_version2,'3.11'))
    elif python_version2 < '3.12':
        print("  Solution: your Python version is {0}, suggest upgrade to {1} or above".format(python_version2,'3.12'))
    else:
        print("  Solution: your Python version is {}, suggest upgrade to the newest one".format(python_version2))
    
    success=False

if success:
    #==============================================================================
    #同一命令行多个输出，主要用于Jupyter Notebook
    from IPython.core.interactiveshell import InteractiveShell
    InteractiveShell.ast_node_interactivity='all'
    #==============================================================================
    # 检查是否存在新版本
    check_newer_version=False
    
    try:
        import pkg_resources
        current_version=pkg_resources.get_distribution("siat").version
        current_list=current_version.split('.')
        print("Successfully enabled siat version",current_version)
    
        if check_newer_version:
            import luddite
            latest_version=luddite.get_version_pypi("siat")
            latest_list=latest_version.split('.')
            
            newest=True
            for i in range(3):
                #print(i)
                if int(current_list[i]) < int(latest_list[i]):
                    newest=False
            
            if not newest:
                #print("The latest version of siat is",latest_version,'\n')
                print("There is a newer version of siat",latest_version,'\n')
                print("*** How to upgrade siat?")
                print("Upgrade from official website? Command: upgrade_siat()")
                print("Upgrade from Tsinghua? Command: upgrade_siat(alternative='tsinghua')")
                print("Upgrade from Alibaba? Command: upgrade_siat(alternative='alibaba')")
        
    except:
        print("  #Warning: plugin went unexpected with either {0} or {1}".format("pkg_resources","luddite"))
        print("  Solution: please re-run. If problem remains, contact the author of siat for help")
        #pass
    

#==============================================================================
