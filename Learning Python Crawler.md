# Learning Python Crawler

<center>xxt 于 2021.3.13</center>

## 认识HTML

- ### 元素和标签

  HTML语言是一种标记语言，通过标签来在网页上展示你所要呈现的内容

  ```html
  <html>
    <head>
    </head>
    
    <body>
      <div>
      </div>
      <div>
        <p>
          这是一个段落
        </p>
        <div>
          <a href = "http://baidu.cn">超链接，点击进入百度</a>
          <span>这是一句段落内的话</span>
        </div>
      </div>
    </body>
  </html>  
  ```

  我们称<>......</>**为一个元素**，<>**称为标签**

  观察上面的一段HTML语言可以看到，每一个元素的头部和尾部都有一个标签，例如`<p>这是一个段落</p>`，放在尾部的标签内容比放在头部的标签内容多了一个`/` 

  其中，`<body>`表示页面的**可见内容**，在`<body>`之内，有很多的`<div>`结构，可以将其理解为一个文件夹，自然地，`<div>`有同胞关系，也有父子关系，即，`<div>`内部也可以放`<div>`元素

  当我们需要写入文字内容的时候，需要用到`<p>`元素(Paragragh)，`<span>`元素可以灵活地添加语句

  `<a>`元素表示超链接：

  ![image-20210313193741554](https://github.com/Soft-Tao/Learning-Python-Crawler/blob/main/Photos%20in%20Learning%20Python%20Craawler/image-20210313193741554.png?raw=true)

  这里写在`<>`之内的内容，成为元素`<a>`的**属性**，例如href

  这一个元素在页面上展示给我们的样子就是：<u>超链接</u>，<u>点击进入百度</u>，鼠标点击后去往网址为`herf = "http://baidu.cn"`的网站

  属性`id`则可以给一个元素起名字，提高可读性

  阅读下面一段

  ![image-20210313194403578](/Users/xuxutao/Library/Application Support/typora-user-images/image-20210313194403578.png)

  首先看到id = "bkrw_centent"（**难道不应该是"content"吗**。。。），很明显网页设计者就是想告诉我们我们要爬取的新闻内容应该就在这个`<div>`元素里面，继续

  ![image-20210313194957002](/Users/xuxutao/Library/Application Support/typora-user-images/image-20210313194957002.png)

  我们发现，`<div id = "brew_centent">`的子元素`<div id = "bkrw_left">`下有一堆`<div>`，用浏览器的开发者工具可以看到这一堆`<div>`中每一个都对应的是一个新闻**（后面我们将会看到，具有同胞关系的元素可以用.xpath在python中取成一个列表）**，打开其中一个，发现他由两个`<p>`元素组成，第一个`<p>`元素里面只有一个`<a>`元素，在开发者工具中可以看到这个元素对应着新闻标题：

  ![image-20210313195655642](/Users/xuxutao/Library/Application Support/typora-user-images/image-20210313195655642.png)

  它是一个超链接，这也就是为什么它对应的元素是一个`<a>`元素了

- ### Xpath中的节点和路径表达式

  Xpath中的节点一共有7中，我们只需要知道上述的元素也是一种节点，一个HTML文件可以理解为一个树状结构，自上而下的主干，通过`<div>`元素来延伸出枝叶，每一个`<a>` `<p>` `<span>` `<img>`元素就好比枝干末尾的树叶，他们一起构成**节点树**

  

  要想获取某一个元素，就得寻找一条路径，描述这种路径用到的就是**路径表达式**

  看下面的一段HTML语句：

  ```html
  <body>
    <div id = "背景图片"></div>
    <div id = "新闻栏目">
      <div id = "第一条新闻">
        <p id = "one">
          这是标题
        </p>
        <p>
          这是简要内容
        </p>
        <a href = "http://pornhub.com">[详情]</a>
      </div>
      <div id = "第二条新闻"></div>
      <div id = "第三条新闻"></div>
      <div id = "四条新闻"></div>
      <div id = "5新闻"></div>
      <div id = "six"></div>
      <div id = "7"></div>
    </div>
    <div id = "致谢"></div>
  </body>
  ```

  接下来我要取标题元素：

  ![image-20210313201810414](/Users/xuxutao/Library/Application Support/typora-user-images/image-20210313201810414.png)

  它的路径表达式为

  `/body/div[@id = "新闻栏目"]/div[@id = "第一条新闻"]/p[@id = "one"]`

  如果你还记得我之前提到的具有同胞关系的元素可以当成列表处理，那么根据：`<div id = "新闻栏目">`是并列的三个`<div>`元素的第二个，`<div id = "第一条新闻">`是它的同胞中的第一个，`<p id = "one">`是两个`<p>`元素中的第一个，路径表达式也可以写成

  `/body/div[2]/div[1]/p[1]`

  **显然，这种表达式更为简洁**

  另外，补充一个语法：

  ![image-20210313203057623](/Users/xuxutao/Library/Application Support/typora-user-images/image-20210313203057623.png)

  相当于一个查找功能，当你不想一个一个地写路径表达式的时候经常会用到它，例如

  `//*p`——选取当前目录中的所有`<p>`元素

  `//*div[@id = "news"]`——选取当前目录中所有的属性id="news"的`<div>`元素

  `//*[@href = "http://baidu.cn"]`——选取当前目录中属性href = "http://baidu.cn"的元素

  也就是说，`//*` **可以用于选取所有元素、选取所有指定类型的元素、选取所有指定属性的元素、选取所有指定类型和属性的元素**

  

  值得注意的是，在python中，我们往往希望**获得这个元素中的文字内容，而不是整个元素**，这时候只需要在这个元素的路径表达式后边加上`/text()`即可

## 两个重要的库——request和etree

- ### Requests

  顾名思义，requests用于进行网络请求，在python爬虫中最常用到的就是`requests.get()`函数，该函数的参数为**想要获取源码网页的网址**，并返回该网页的源码

  ```python
  import requests
  
  url = "http://baidu.cn"
  re = requests.get(url) #获取百度首页的源码，并返回给变量re
  ```

  对于变量re可以有以下操作，`re.encoding`表示获取当前的编码方式，`re.text`以当前的编码方式解码，并以字符串形式获取

  对于一个访问到的**中文网站**源码，我们可以先看看它的编码方式，并打印其内容

  ```
  print (re.encoding)
  print (re.text)
  ```

  运行结果部分如下：

  ![image-20210313205633917](/Users/xuxutao/Library/Application Support/typora-user-images/image-20210313205633917.png)

  编码方式为ISO-8859-1

  ![image-20210313205744865](/Users/xuxutao/Library/Application Support/typora-user-images/image-20210313205744865.png)

  **（出现外星语！）**

  问题在于，中文网站应该使用**utf-8**编码方式才不会出现乱码，对此，可以修改`re.encoding`

  ```python
  re.encoding = "utf-8"
  ```

- ### Etree

  etree在爬虫的用处就在于，当我拿到一个网页的源代码后**（是字符串）**，我们需要将其**转换为HTML语言**，这样才能用Xpath去取得我们想要的元素

  

  所使用的就是etree库中的`etree.HTML()`函数，其参数可以为字符串，返回一个HTML文档

  ```python
  from lxml import etree
  
  selector = etree.HTML(re.text) #将前面爬到的网页源码（字符串形式）转变为HTML文档，并返回给变量selector
  ```

  此后我们要获取某一个元素，就可以通过`selector.xpath(路径表达式)`啦～

## xlwt

- ### 简介

  python中的一个库，可以通过它来**操作excel**

- ### 语法

  只是一个文件操作的库，相对来说比较容易理解，这里罗列有关语法

  ```python
  import xlwt
  
  #新建一个excel文件
  my_workbook = xlwt.Workbook (encoding = "utf-8")
  #新建一个工作簿
  my_worksheet = my_workbook.add_sheeet ("My WorkSheet 1")
  
  #写入
  #参数对应的值为行指标，列指标，写入的内容 （⚠️：行（列）指标为0，对应第一行）
  my_worksheet.write(0, 0, "hello")
  
  #保存，参数是文件名
  my_workbook.save("hello.xls")
  ```

  新建、写入、保存是最基本的操作，能够满足python爬虫的最基本需求

  利用xlwt可以完成excel中所有的操作，包括调整行高和列宽，设置字体，设置背景色，合并行和列，插入公式等等

  具体可以参见https://www.jianshu.com/p/4e39444d5ebc

## Crawler搭建——以北科新闻网为例

> 本段所有的代码块顺次拼接即为完整的程序

- ### 总体思路和观察

  需要爬取所有的新闻标题，内容简介，发布时间，可以分别使用列表来储存；爬取的不只是一个网页的内容，因此需要循环；总的顺序就是：循环爬取，整体导入excel

  

  既然提到了循环，循环爬取多个网页，**规律**何在呢？也就是说，我们的循环变量`i`在哪里？

  ![image-20210313213609398](/Users/xuxutao/Library/Application Support/typora-user-images/image-20210313213609398.png)

  ![image-20210313213620400](/Users/xuxutao/Library/Application Support/typora-user-images/image-20210313213620400.png)

  这是**第一页的网址**

  在跳转到第二页，**第二页的网址为**

  ![image-20210313213729296](/Users/xuxutao/Library/Application Support/typora-user-images/image-20210313213729296.png)

  **第578页的网址为**

  ![image-20210313213820487](/Users/xuxutao/Library/Application Support/typora-user-images/image-20210313213820487.png)

  所以，除了第一页比较特殊，其余的页面网址都有共同的部分和递变规律：

  `http://news.ustb.edu.cn/xinwendaodu/index_`+`i`+`.html`

- ### 准备工作

  ```python
  #导入所需的库
  import requests
  from lxml import etree
  import xlwt
  
  count = 0 #计数器，可以方便我们检查是否爬到了所有的新闻
  name_list = []#新闻标题
  time_list = []#新闻时间
  content_list = []#新闻内容
  
  url = 'http://news.ustb.edu.cn/xinwendaodu/' #第一页的网址
  resp = requests.get(url) #拿到网页源码，储存至变量resp
  resp.encoding = 'utf-8' #修改编码方式
  sel=etree.HTML(resp.text) #以utf-8解码，并转换成HTML文档，储存至变量sel
  ```

- ### 第一页的爬取

  之前提到过，为同胞关系的元素可以当作类似列表来处理，在一个页面内，有十五个新闻，它们一定是同胞关系<u>（希望如此）</u>，打开开发者工具查看一下，发现确实如此

  ![image-20210313214848387](/Users/xuxutao/Library/Application Support/typora-user-images/image-20210313214848387.png)

  它们同是元素`<div class = "bkrw_left">`的子元素，而`<div class = "bkrw_left">`又在元素`<div id = "bkrw_centent">`之下，这时候可以运用`//*`的查找功能，而不用去管元素`<div id = "bkrw_centent">`众多先辈

  ```python
  li_list=sel.xpath('//*[@id="bkrw_centent"]/div[1]/div')
  #找到所有的  属性id = "bkrw_centent"元素（事实上只有一个）/它的第一个子<div>元素/div元素
  ```

  满足这条路径的元素有多个，因此得到了一个列表`li_list`，事实上，如果只有一个元素，也是得到一个列表，只不过列表长度为1而已；事实上，这个页面有15条新闻，该列表的长度为15

  

  接下来，需要知道标题，内容简介，时间的具体位置，利用开发者工具：

  ![image-20210313220304041](/Users/xuxutao/Library/Application Support/typora-user-images/image-20210313220304041.png)

  可以看到，第i个标题是上述`li_list`里面的第i个元素的第一个`<p>`中的`<a>`中的文字部分，

  它的路径表达式为（只考虑之后的，因为下面的`li.xpath`是从li这个元素之后开始查找）：`p[1]/a`

  

  ```python
  for li in li_list[:-1]:#遍历这个列表
  
      news_titles=li.xpath('p[1]/a/text()')[0].strip() #定义一个临时变量news_titles用于储存第i个新闻的标题
      news_times = li.xpath('p[2]/span/text()')[0].strip()
      news_contents = li.xpath('p[2]/text()')[0].strip()
  ```

  **关于上面为什么会有`[0]`**，如果你理解了`.xpath`所得到的**是一个列表**就不会有这样的疑问了

  `.strip()`是一个字符串处理的函数，其功能是**除去该字符串首尾多余的空格**

  **别忘了要用`/text()`来取HTML元素中的字符串！**

  ```python
      time_list.append(news_times) #将得到的临时变量加入到结果列表中
      name_list.append(news_titles)
      content_list.append(news_contents)
  
      count += 1 #爬完了一个新闻的相关内容，计数
  ```

  `.append()`函数将元素添加到列表的末位

- ### 第2页到第860页的循环爬取

  ```python
  for i in range(2,861):#根据需要爬
  
      url = "http://news.ustb.edu.cn/xinwendaodu/index_" + str(i) + ".html" #这是之前找到的网址规律
      #其余部分和爬取第一页一模一样
      resp = requests.get(url)
      resp.encoding = 'utf-8'
      sel=etree.HTML(resp.text)
      li_list=sel.xpath('//*[@id="bkrw_centent"]/div[1]/div')
  
      for li in li_list[:-1]:
  
          news_titles=li.xpath('p[1]/a/text()')[0].strip()
          news_times = li.xpath('p[2]/span/text()')[0].strip()
          news_contents = li.xpath('p[2]/text()')[0].strip()
  
          time_list.append(news_times)
          name_list.append(news_titles)
          content_list.append(news_contents)
  
          count += 1
  ```

- ### 导入到excel中

  ```python
  #字体格式的设置
  font = xlwt.Font()  
  font.name = "Times New Roman"
  font.bold = True
  font.height = 20*22
  
  #字体格式的设置
  font1 = xlwt.Font()
  font1.name = "Calibri"
  font1.height = 20*14
  
  #字体格式的设置
  style = xlwt.XFStyle ()
  style.font = font
  style1 = xlwt.XFStyle ()
  style1.font = font1
  
  workbook = xlwt.Workbook(encoding = "utf-8") #创建excel文件
  worksheet = workbook.add_sheet('sheet1') #创建工作簿
  
  #写入第一行表头
  worksheet.write(0, 0, "title", style)
  worksheet.write(0, 1, "time", style)
  worksheet.write(0, 2, "content", style)
  worksheet.write(0, 3, "总计：" + str(count) + "篇", style)
  
  #行高列宽的设置
  worksheet.col(0).width = 20000
  worksheet.col(1).width = 10000
  worksheet.col(2).width = 10000
  
  #写入爬到的数据，运用循环结构
  for i in range (1, count):
      worksheet.row(i).height = 1000
      worksheet.write(i, 0, name_list[i], style1)
      worksheet.write(i, 1, time_list[i], style1)
      worksheet.write(i, 2, content_list[i], style1)
  
  #保存
  workbook.save('Crawler.xls')
  ```

  有关字体格式、行高列宽的设置由于并不是爬虫到excel的必要操作，本文也没有提及，具体可以参考之前提到的那个网址～

---

<center>THE END</center>
