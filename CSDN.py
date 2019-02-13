import urllib.request
import re
from selenium import webdriver
from bs4 import BeautifulSoup

url2 = 'https://blog.csdn.net/qq_32465127?viewmode=contents'
url = 'https://blog.csdn.net/qq_32465127/article/list/'

# ============通过selenium获取js动态加载的页数====================
ChromeOptions = webdriver.ChromeOptions()
ChromeOptions.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=ChromeOptions)

try:
    driver.get(url)
except Exception as e:
    print("get website error")

try:
    ui_pagers = driver.find_elements_by_class_name("ui-pager")
except Exception as e:
    print("get class name error")
max = 1
for i in range(len(ui_pagers)):
    try:
        if int(ui_pagers[i].text, base=10) > max:
            max = int(ui_pagers[i].text, base=10)
    except Exception as e:
        print(e)
driver.quit()

# ====================通过urllib获取html文件=================
res = []
repeat = []
for i in range(max):
    headers = ("user-agent",
               "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 BIDUBrowser/8.7 Safari/537.36")
    opener = urllib.request.build_opener()
    opener.addheaders = [headers]  # 添加报头
    urllib.request.install_opener(opener)  # 设置opner全局化
    # 获取网页信息
    data = urllib.request.urlopen(str(url + str(i) + '?')).read().decode('utf-8')
    # 设置正则
    pat = '<a href="(.*?)" target="_blank">'
    # 匹配正则
    res.append(re.compile(pat).findall(data))
# 保存数据

for i in range(len(res)):
    for j in range(len(res[i])):
        if res[i][j] == res[i][j+1]:
            continue
        try:
            # ==========通过urllib获取标题=================
            data_article = urllib.request.urlopen(res[i][j]).read().decode('utf-8')
            compile_rule = '<title>(.*?)</title>'
            try:
                title = re.compile(compile_rule).findall(data_article)
            except Exception as e:
                title = "异常"
                print(e)
                continue
            file = "F:/csdn/" + re.sub("[A-Za-z0-9\!\%\[\]\,\。\+\、\--\//\-\_]", "",str(title[0])) + '.txt'
            html = urllib.request.urlopen(res[i][j])
            bs = BeautifulSoup(html)
            content_list = bs.findAll('div',{'id':'content_views'})
            for content in content_list:
                with open(file, 'a', encoding='utf-8') as f:
                    f.writelines(content.get_text())
                    f.close()
                    print('文章' + str(title[0]) + '爬取成功！')
        except urllib.error.URLError as e:
            if hasattr(e, "code"):
                print(e.code)
            if hasattr(e, "reason"):
                print(e.reason)
