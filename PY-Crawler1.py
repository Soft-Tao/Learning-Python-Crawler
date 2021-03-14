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
