# encoding:utf8

import requests
from lxml import etree
import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


class GenerateCookie(object):
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.browser.set_window_size(1050, 840)
        self.wait = WebDriverWait(self.browser, 20)

    def get_cookie(self):
        self.browser.delete_all_cookies()
        self.browser.get("https://www.itjuzi.com")
        self.wait.until(EC.visibility_of_element_located((By.ID, 'top')))
        cookie = self.browser.get_cookie("acw_sc__")
        self.browser.quit()
        return {cookie["name"]: cookie["value"]}

    def run(self):
        cookie = self.get_cookie()
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Host": "www.itjuzi.com",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Mobile Safari/537.36",
            "Referer": "https://www.itjuzi.com/investevents?page=2",
            "Upgrade-Insecure-Requests": "1",
            "If-Modified-Since": "Tue, 03 Apr 2018 02:03:48 GMT",
            }

        for i in range(1, 20):
            print("=======正在爬取第{}页=======".format(i))
            url = "https://www.itjuzi.com/investevents?page="+str(i)
            res = requests.get(url, headers=headers, cookies=cookie)
            html = etree.HTML(res.text)
            li_list = html.xpath("//ul[@class='list-main-eventset']/li")
            for li in li_list:
                cell_date = li.xpath("./i[@class='cell date']/span/text()")  # 时间
                main_cell = li.xpath(".//p[@class='title']//span/text()")  # 公司
                rounds = li.xpath(".//span[@class='tag gray']/text()")  # 轮次
                money = li.xpath("./i[@class='cell money']/text()")  # 投资金额
                cell_name = li.xpath("./i[@class='cell name']//a/text()|./i[@class='cell name']//span/text()")  # 投资方
                item = {"date":"".join(cell_date).replace(".", "-"),
                        "company": "".join(main_cell),
                        "rounds": "".join(rounds),
                        "money": "".join(money),
                        "cell_name": ",".join(cell_name)
                        }
                print("时间:{date}  公司:{company}  轮次:{rounds}  投资金额:{money}  投资方:{cell_name}".format_map(item))
            time.sleep(1.2)


if __name__ == "__main__":
    gc = GenerateCookie()
    gc.run()


