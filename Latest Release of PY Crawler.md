# Latest Release of PY Crawler

<center>xxt 于 2021.3.14</center>

> ### 更新了！更新了！！针对北科新闻点击量问题的更新

- ### 亮点速览

  - #### **新增了一个库`re`用于后面的在字符串中按格式截取想要的部分**

    ```python
    import re
    ```

    ```python
    num = int (re.findall("document\.write\(\'(\d+)\'\);",requ1.text)[0])
    Click_list.append(num)
    ```

    使用了`re.findall`函数来完成这一功能

  - #### 新增了判断语句来应付某些新闻超链接的网址不同寻常自带前缀的问题

    ```python
    if link[0:4] != "http":
      link = 'http://news.ustb.edu.cn' + link
    ```

    注意`link[0:4]`的含义是从**第1个到第4个**字符

  - #### 新增了判断语句来应付某些新闻超链接打开之后是校园网关连接

    ```python
    if len(sel1.xpath ('//*[@id="bkrw_centent"]/div[1]/p[3]/script/@src')) == 0:
      Click_list.append("error")
      continue
    ```

    打开后是校园网网关连接，自然爬取不到点击量，但是为了防止爬到空列表出现越界错误，先行**判断列表是否为空**（是不是爬取到了点击量），若为空，对应点击量存为“error”，防止出现错位

- ### 完整代码

  ```python
  import requests
  from lxml import etree
  import xlwt
  import re
  
  count = 0
  name_list = []#新闻标题
  time_list = []#新闻时间
  content_list = []#新闻内容
  Click_list = []
  
  url = 'http://news.ustb.edu.cn/xinwendaodu/'
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
  
      link = li.xpath('p[1]/a/@href')[0].strip()
  
      if link[0:4] != "http":
          link = 'http://news.ustb.edu.cn' + link
  
      requ = requests.get(link)
      requ.encoding = 'utf-8'
      sel1 = etree.HTML(requ.text)
      link1 = "http://news.ustb.edu.cn" + sel1.xpath ('//*[@id="bkrw_centent"]/div[1]/p[3]/script/@src')[0]
      requ1 = requests.get(link1)
      requ1.encoding = 'utf-8'
      # print(requ1.text)
      num = int (re.findall("document\.write\(\'(\d+)\'\);",requ1.text)[0])
      Click_list.append(num)
  
      count += 1
  
  for i in range(2,50):#根据需要爬
  
      url = "http://news.ustb.edu.cn/xinwendaodu/index_" + str(i) + ".html"
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
  
          link = li.xpath('p[1]/a/@href')[0].strip()
  
          if link[0:4] != "http":
              link = 'http://news.ustb.edu.cn' + link
  
          requ = requests.get(link)
          requ.encoding = 'utf-8'
          sel1 = etree.HTML(requ.text)
          if len(sel1.xpath ('//*[@id="bkrw_centent"]/div[1]/p[3]/script/@src')) == 0:
              Click_list.append("error")
              continue
          link1 = "http://news.ustb.edu.cn" + sel1.xpath ('//*[@id="bkrw_centent"]/div[1]/p[3]/script/@src')[0]
          requ1 = requests.get(link1)
          requ1.encoding = 'utf-8'
          # print(requ1.text)
          num = int (re.findall("document\.write\(\'(\d+)\'\);",requ1.text)[0])
          Click_list.append(num)
  
          count += 1
  
  
  #data to excel
  
  #font
  font = xlwt.Font()
  font.name = "Times New Roman"
  font.bold = True
  font.height = 20*22
  
  font1 = xlwt.Font()
  font1.name = "Calibri"
  font1.height = 20*14
  
  style = xlwt.XFStyle ()
  style.font = font
  style1 = xlwt.XFStyle ()
  style1.font = font1
  
  workbook = xlwt.Workbook(encoding = "utf-8")
  worksheet = workbook.add_sheet('sheet1')
  worksheet.write(0, 0, "title", style)
  worksheet.write(0, 1, "time", style)
  worksheet.write(0, 2, "click", style)
  worksheet.write(0, 3, "content", style)
  worksheet.write(0, 4, "总计：" + str(count) + "篇", style)
  
  worksheet.col(0).width = 20000
  worksheet.col(1).width = 10000
  worksheet.col(2).width = 3000
  worksheet.col(3).width = 10000
  
  for i in range (1, count):
      worksheet.row(i).height = 1000
      worksheet.write(i, 0, name_list[i], style1)
      worksheet.write(i, 1, time_list[i], style1)
      worksheet.write(i, 3, content_list[i], style1)
      worksheet.write(i, 2, Click_list[i], style1)
  
  workbook.save('Crawler1.xls')
  ```

- ### 缺陷

  #### 如果想要爬取很多页的新闻点击量，例如860页，则需要访问网页的次数大概为860X15X2次，这么多次网页访问中很有可能出现网络不稳定而导致程序中断，我们并没有解决这个问题，因此需要一个具备异常处理能力的程序能使得出现网络问题而中断时，从断点开始继续访问

