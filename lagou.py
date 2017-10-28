#coding:utf8
from selenium import webdriver
import time
import json
import time
from lxml import etree
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from mysql import Mydb
mydb=Mydb()
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap['phantomjs.page.settings.userAgent'] = ( 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36')
driver = webdriver.PhantomJS(desired_capabilities=dcap)

driver.get('https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=')
#driver.save_screenshot('lagou.png')
#print driver.page_source
with open ('lagou.json','a') as f:
    while True:
        xml = etree.HTML(driver.page_source)
        li_list=xml.xpath('//div[@id="s_position_list"]/ul/li')
        for li in li_list:
            item={}
            item['name']=li.xpath('.//div[@class="p_top"]/a/h3')[0].text.strip()
            item['time']=li.xpath('.//div[@class="p_top"]/span')[0].text.strip()
            item['salary']=li.xpath('.//div[@class="li_b_l"]/span')[0].text.strip()
            item['company_type']=li.xpath('.//div[@class="industry"]')[0].text.strip()
            item['company_name']=li.xpath('.//div[@class="company_name"]/a')[0].text.strip()
            sql = 'insert into lagou(name,time,salary,company_type,company_name) values("%s","%s","%s","%s","%s") on duplicate key update time=values(time),salary=values(salary),company_type=values(company_type)' %(item['name'],item['time'],item['salary'],item['company_type'],item['company_name'])
            # 执行sql
            mydb.execute(sql)
            f.write(json.dumps(item,ensure_ascii=False).encode('utf-8')+'\n')
        if driver.page_source.find('pager_next pager_next_disabled')!=-1:
            break
        driver.find_elements_by_xpath("//span[@action='next']")[0].click()
        time.sleep(2)

mydb.close()





