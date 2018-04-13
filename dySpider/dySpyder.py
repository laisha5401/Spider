# coding:utf8

import time
import csv
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class DouYu():

    def __init__(self):
        self.driver = webdriver.Chrome()    # 初始化浏览器对象
        self.num = 0    # 总直播人数
        self.count = 0  # 总观众人数
        self.dySpider_csv_file = open('dySpider.csv', 'wb')
        self.dySpider_csv_write = csv.writer(self.dySpider_csv_file, delimiter=',')

    def douyuSpider(self):
        self.driver.get("https://www.douyu.com/directory/all")
        while True:
            # BeautifulSoup可将lxml做解析器，是内置解析器
            soup = bs(self.driver.page_source, 'lxml')
            # 房间名，返回列表
            names = soup.find_all("span", {"class": "dy-name ellipsis fl"})
            # 观看人数，返回列表
            numbers = soup.find_all("span", {"class": "dy-num fr"})

            for name, number in zip(names, numbers):
                dy_name = name.get_text(strip=True)
                dy_number = number.get_text(strip=True)
                # ，get_text()用来获取标签内里面的文本内容，"strip=True"能去除文本内容前后多余的空格
                print u"观众人数：" + dy_number + u"\t房间名：" + dy_name
                self.num += 1
                count = number .get_text(strip=True)
                if count[-1] == "万":
                    countNum = float(count[:-1])*10000
                else:
                    countNum = float(count)
                self.count += countNum

                self.dySpider_csv_write.writerow([dy_number, dy_name])

            # 一直点击下一页
            self.driver.find_element_by_class_name("shark-pager-next").click()
            time.sleep(2)
            # 如果在页面源码中找到下一页为隐藏的标签，就退出循环
            if self.driver.page_source.find("shark-pager-next shark-pager-disable shark-pager-disable-next") != -1:
                break

        self.dySpider_csv_file.close()

        print "当前网站直播人数：%s" % self.num
        print "当前网站观众人数：%s" % self.count


if __name__ == "__main__":
    d = DouYu()
    d.douyuSpider()

    sys.exit()



# # 浏览器页面最大化
# driver.maximize_window()
#
# # 隐形等待，是设置了一个最长等待时间，如果在规定时间内网页加载完成，则执行下一步，否则一直等到时间截止，然后执行下一步。
# # 隐性等待对整个driver的周期都起作用，所以只要设置一次即可；
# driver.implicitly_wait(10)
#
# # 模拟点击下一页按钮
# driver.find_element_by_class_name("shark-pager-next").click()
#
# # selenium的page_source方法可以获取到页面源码；
# # 打印页面源码查看
# print driver.page_source
#
# # 退出浏览器及驱动进程
# driver.quit()

# # 打开csv文件
# csv_file = open('dySpyder.csv', 'wb')
# # 创建write对象，指定文件与分隔符
# csv_write = csv.writer(csv_file, delimiter=',')

