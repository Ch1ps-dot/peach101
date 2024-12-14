# Peach小实验

## 安装需知

Peach支持直接运行二进制程序或从源码进行编译，但是由于依赖库更新的问题，从源码重新编译需要调整很多的设置。为了方便起见，我们在Windows平台采取直接运行二进制程序的方式进行本次实验。请遵循如下步骤，安装并测试Peach的可用性。

1. 在windows平台上克隆本次实验的实验仓库 ```git clone https://github.com/Ch1ps-dot/peach101.git```
2. 进入experiments文件夹，在该目录下打开终端，输入```.\peach.exe```观察是否输出流Peach的帮助信息内容。
3. 如果
   
!!! warning
    如果出现类似如下报错：
    >Peach.Core.PeachException: Error, could not load platform assembly 'Peach.Core.OS. Windows.dll'. The assembly is part of the Internet Security Zone and loading has been blocked.
    
    请在当前目录下找到报错对应的.dll文件，右键打开**属性**设置，在**常规**界面右下角勾选**解除锁定**。