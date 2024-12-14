# Peach101

## Peach简介

[模糊测试](https://zh.wikipedia.org/wiki/%E6%A8%A1%E7%B3%8A%E6%B5%8B%E8%AF%95)旨在通过给程序提供大量预期之外的输入来试图触发程序的异常行为。根据用于测试软件的程序输入是通过修改已有数据，还是根据一些约束和规范凭空生成得来，模糊测试可以分为基于变异和基于生成两大类别。在针对协议实现软件的模糊测试中，由于协议实现需要遵守协议**报文规范**和协议**语义规范**（也成为协议状态机），所以有很多工作采用了基于生成的测试用例生成策略。

>模糊测试中的模糊一词来源于英语单词Fuzz，最早出自模糊测试领域的开山之作[《An empirical study of the reliability of UNIX utilities》](https://dl.acm.org/doi/10.1145/96267.96279)，文中设计了一个可以用于生成随机输入的程序Fuzz。Fuzz原意指的是兔毛，模糊测试领域另一著名工具AFL的英文全称也正是美洲长毛兔。细碎的兔毛和大量随机的测试用例确实是有异曲同工之妙。但为了避免直译成兔毛测试，Fuzz就有了一个并不那么形象的中文名——**模糊测试**。

[Peach](https://peachtech.gitlab.io/peach-fuzzer-community/)是一个可以用于测试协议软件的模糊测试器。Peach通过C#编写，借助Mono项目可以直接运行在Windows、Linux等多种平台上。和基于变异的模糊测试器不同，Peach加入了基于生成的样例生成策略，它可以根据给定的模板生成符合要求的测试样例（即用于协议通信的报文）。

Peach所用的规范描述模板被称为**Pit**，它是一套利用XML实现的，用于规定Peach在执行模糊测试时需要遵守的各种协议报文规范和协议语义规范的描述语言。Pit 文件还定义了测试过程中的I/O方式（Publisher）、程序运行监视器（Monitor和Agent）以及用例变异方式（Mutator）。

我们以利用Peach执行协议模糊测试过程为例子，来对描述协议的语法规范和语义规范进行初步的了解。  

!!! info
    Peach项目开始于2004年，2013年之后就不再维护开源版本了。由于年久失修，它所依赖的许多软件包都有很大的变动，如果想要从源码编译Peach会碰到很多障碍，所幸作者提供了编译好的二进制版本（即使是这样，如果在Linux上运行还是会有很多问题）。

## Peach的程序架构

Peach主要由六个部分构成：

- **Model**：用于描述模糊测试操作的数据模型和状态模型。
- **Publisher**：I/O接口，Peach提供了多种I/O方式，可以通过标准输入输出进行，也可以通过文件、TCP、UDP等方式进行数据传输。
- **Mutators**：用于生成测试数据，可以根据默认值生成，也可以根据给定范围生成。
- **Monitors**：调用目标程序，监视目标程序执行情况，并进行一些操作。可以是流量抓包、检测崩溃的debugger，甚至可以在程序崩溃时重新拉起目标程序。
- **Agents**：在本地或者远程运行的特殊Peach进程，主导了一些Monitor和远程Publisher的运行。
- **Logger**：记录目标程序的运行时信息。

Peach的工作流程就围绕这些组件进行，当我们想要测试一个目标时，需要遵循如下步骤：

1. 根据测试创建合适的数据模型和状态模型
2. 挑选和配置Publisher（就是设置合适的I/O接口）
3. 配置Agents/Monitors（设置被测试的目标程序和进程监视器）
4. 配置Logger

**实际上，这些步骤都是通过编写Pit文件实现的。**

在编写好Pit文件后，我们就可以直接让Peach解析Pit文件并进行相应的模糊测试操作。除此之外Peach还提供了一些额外功能，可以通过参数指定。

``` bash
-1：执行第1次测试。
-a：启动Peach代理。不指定”channel”默认为本地代理（默认支持，无需显式启动）；
    “channel”可以指定为”tcp”远程代理。
-c：统计测试用例数。
-t：验证Peach Pit xml文件正确性。
-p：并行Fuzz。运行Peach的机器总数为M，这是第N个。
–debug：调试信息开关。
–skipto：指定Fuzz跳过的测试用例数。
–range：指定Fuzz的测试用例范围
-h：输出帮助菜单
```

## Pit文件

Pit文件本质上是一个[XML](https://www.runoob.com/xml/xml-intro.html)文件。它利用了XML可以自定义标签的特性，在此基础之上拓展出了用于描述Peach所需信息的Pit文件。接下来我们对Pit文件进行粗略的介绍，详细的内容可以查阅[官方文档](https://peachtech.gitlab.io/peach-fuzzer-community/v3/PeachPit.html)。Pit文件中包含了如下信息：

1. 通用设置
2. DataModel
3. StateModel
4. Agents和Monitors（可选）
5. 测试设置

!!! warning
    在阅读以下内容之前请确保对XML文件的组成有基本的了解。

!!! info
    **XML速成**：XML是一种可拓展标记语言，它的基本功能就在于标记。XML文件由元素组成，每个元素都是由标签标记（类似于HTML），每个元素都可以有很多属性，元素之间可以相互嵌套。XML本质上是对数据的标记，如何处理这些数据需要由程序自己决定。Pit文件规范就是Peach自定义的针对XML文件的解析处理方法。

Pit文件的基本框架结构如下，其中包含了根节点\<Peach>\</Peach>和它的三个子元素DataModel，StateModel>，Agent和Test。Peach节点指明了该文件为Pit脚本，是每个Pit脚本中必须包含的元素。

 ```xml
 <?xml version="1.0" encoding="utf-8"?>
 <Peach xmlns="http://peachfuzzer.com/2012/Peach" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
     xsi:schemaLocation="http://peachfuzzer.com/2012/Peach ../peach.xsd">

     <DataModel name="TheDataModel"></DataModel>

     <StateModel name="State" initialState="State1" ></StateModel>

     <Agent name="Local"></Agent>

     <Test name="Default"></Test>

 </Peach>
 ```

### DataModel

Pit文件中至少应该包含一个DataModel元素，它描述了数据的类型信息、关系信息和模糊测试器应采用的变异操作，DataModel之间可以相互引用。

DataModel可以设置属性，用来指明对该元素的属性信息，这样的属性包括指明元素名称的**name**（必须有），用于引用的**ref**（可选），表示数据是否可以变异的**mutable**（可选），检测合法性的**constraint**（可选）。

在DataModel中还可以设置多种子元素，用来表示不同的数据，我们以最简单的String为例，它表示该元素是一个字符串类型的数据，其属性Value表示的就是字符串的实际值，下面的DataModel元素表示的就是一个"Hello World!"字符串。

```xml
    <DataModel name="TheDataModel">
        <String value="Hello World!" />
    </DataModel>
```

### StateModel

StateModel表示的是测试过程中的状态模型，它规定了Peach和测试目标之间是如何交换数据的。每个StateModel都有一个或多个State组成，每个State由一个或多个Action组成。StateModel中的子元素State对Action起封装作用，而Action表示Peach应该执行的操作，这些操作按照Action分布的顺序从上到下执行。在Action元素中可以引用先前定义好的DataModel。

下图展示了一个通过网络进行模糊测试的例子。

```xml
    <StateModel name="TheStateModel" initialState="InitialState">
        <State name="InitialState">

                <!-- Send data -->
                <Action type="output">
                        <DataModel ref="PacketModel1" />
                </Action>

                <!-- Receive response -->
                <Action type="input">
                        <DataModel ref="PacketModel2" />
                </Action>

                <!-- Send data -->
                <Action type="output">
                        <DataModel ref="PacketModel3" />
                </Action>

                <!-- Receive response -->
                <Action type="input">
                        <DataModel ref="PacketModel4" />
                </Action>
        </State>
    </StateModel>
```

### Agent

Agent是一个可选的元素，被用来在本地或者远程配置Monitor。Peach提供了多种可选Monitor用于收集信息和执行特殊操作。比如下面就设计了一个本地运行的Agent，它用来执行一命令。命令的内容是调用一个Python脚本，在每次测试循环后监听目标程序的执行情况，当程序异常退出时告知Peach。

```xml
<Agent name="Local">
        <Monitor class="RunCommand">
            <Param name="Command" value="python"/>
            <Param name="Arguments" value=".\monitor.py" />
            <Param name="FaultOnNonZeroExit" value="true" />
            <Param name="When" value="OnIterationEnd" />
        </Monitor>
</Agent>
```

### Test

Test元素被用于配置模糊测试，它相当于定义了一次模糊测试的过程。Test中的子元素包含了先前定义的StateModel（必需），Publisher（必需），Agents（可选），Logger和模糊测试策略。

```xml

<Test name="Default">

  <!-- 可选的Agent设置 -->
  <Agent ref="Local" platform="windows" />

  <!-- 指定StateModel(必需) -->
  <StateModel ref="TheState" />

  <!-- 指定将要使用的Publisher(必需) -->
  <Publisher class="Tcp">
     <Param name="Host" value="127.0.0.1" />
     <Param name="Port" value="9001" />
  </Publisher>

  <!-- 指定变异策略 -->
  <Strategy class="Random" />

  <!-- 指明存储日志的文件夹 -->
  <Logger class="File">
    <Param name="Path" value="logs" />
  </Logger>
</Test>

```

#### Publisher

Publisher定义了Peach用来发送和接收数据的I/O接口。所有模糊测试过程都需要一个Publisher，不同的Publiser可以用于执行不同的操作动作。例如和文件相关的Publisher可以执行读取和输出文件的操作。和网络通信有关的Publisher可以用来指定IP和端口。

#### Logger

Logger是Peach中可拓展的日志模块，一般用来指定一个文件夹存储模糊测试过程中的日志信息。

## 结语

上述内容主要是对Peach中Pit文件的基本架构进行一个简单的介绍，已经可以用于构建我们的状态机描述实验了。Pit文件还有很多可供拓展的设置，可以根据自己的需要描述相当复杂的文档结构。感兴趣的同学可以通过[官方文档](https://peachtech.gitlab.io/peach-fuzzer-community/WhatIsPeach.html)自行探索。
