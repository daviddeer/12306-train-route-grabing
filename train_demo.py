import requests
import json
import save_in_csv as sc
import random

class Train():
    def __init__(self):
        self.left_ticket_baseurl1="https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date="
        self.left_ticket_baseurl2="&leftTicketDTO.from_station="
        self.left_ticket_baseurl3="&leftTicketDTO.to_station="
        self.left_ticket_baseurl4="&purpose_codes=ADULT"
        self.query_bytrain_baseurl1="https://kyfw.12306.cn/otn/czxx/queryByTrainNo?train_no="
        self.query_bytrain_baseurl2="&from_station_telecode="
        self.query_bytrain_baseurl3="&to_station_telecode="
        self.query_bytrain_baseurl4="&depart_date="
        self.user_agent_list=["Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
                    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
                    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
                    ]
        self.headers={"User-Agent":"",
                      "Cookie": "JSESSIONID=6FABBEE8823D677C1DE624679A5912FF; tk=hyMd5Y6fnPtb1hB4FJGXRS7nQarxpRbUqQ8DZIA2Lb4361110; RAIL_EXPIRATION=1563794422813; RAIL_DEVICEID=auuAiez2vuPNnrvPdPs64ATuYzog5qJu46em_HIWlaIz3u6f-D69xp3HVB6xbgO9CuwUc0bxKCrLOU2fw8Sm13M3pnbS1p0X_RhhevOByg2haAq0uxJobFbEIzv_WLdnCHPRkW9Eg6i7W2jhY3c7O2sZideNa9hU; _jc_save_wfdc_flag=dc; _jc_save_fromStation=%u5929%u6D25%2CTJP; _jc_save_toStation=%u676D%u5DDE%2CHZH; _jc_save_toDate=2019-07-20; BIGipServerpool_passport=334299658.50215.0000; route=9036359bb8a8a461c164a04f8f50b252; BIGipServerotn=1324352010.38945.0000; _jc_save_fromDate=2019-07-22"}
        self.already_get_query=[] # 存放已经访问过的车次
        self.query={} # 存放最终数据{"车次号":"[...]",...}

    def get_left_ticket(self,date,start_station,end_station):
        """
        获取剩余车次的信息的函数
        :param date: 日期
        :param start_station: 起始点
        :param end_station: 终点
        :return: 车次号（列表）
        """
        url=self.left_ticket_baseurl1+date+self.left_ticket_baseurl2+start_station+self.left_ticket_baseurl3+end_station+self.left_ticket_baseurl4
        self.headers['User-Agent'] = random.choice(self.user_agent_list)
        res=requests.get(url=url,headers=self.headers) # 获取请求响应
        res.encoding="utf-8"
        res=res.text
        train_nos = [] # 存放车次信息的列表
        try:
            res=json.loads(res,strict=False)
            for li in res["data"]["result"]:
                    train_nos.append(li.split("|")[2])
        except Exception as e: # 如果没有路线，跳过
            print("Located_1")
            print(e)
            train_nos=None
        return train_nos

    def get_query_info(self,train_no,start_station,end_station,date):
        """
        获取每趟车次经过站点的函数
        :param train_no: 车次号
        :param start_station: 起始点
        :param end_station: 终点
        :param date: 日期
        :return: 经过站（列表）
        """
        url=self.query_bytrain_baseurl1+train_no+self.query_bytrain_baseurl2+start_station+self.query_bytrain_baseurl3+end_station+self.query_bytrain_baseurl4+date
        self.headers['User-Agent'] = random.choice(self.user_agent_list)
        res=requests.get(url=url,headers=self.headers) # 获取请求响应
        res.encoding="utf-8"
        res=json.loads(res.text)
        station_list=[]
        for li in res["data"]["data"]:
            station_list.append(li["station_name"])
        return station_list

    def get_cities(self):
        # url="https://www.12306.cn/index/script/core/common/station_name_v10035.js"
        # res=requests.get(url=url,headers=self.headers)
        # res.encoding="utf-8"
        # self.cities={}
        # result=res.text
        # result=result.split("@")
        # i=1
        # while i<len(result):
        #     key=result[i].split("|")[2] # 车站代码
        #     value=result[i].split("|")[1] # 车站名称
        #     self.cities[key]=value
        #     i+=1
        # self.city_nos=[]
        # for city in self.cities.keys():
        #     self.city_nos.append(city)
        self.cities={'北京': 'BJP',
    '上海': 'SHH',
    '成都': 'CDW',
    '杭州': 'HZH',
    '重庆': 'CQW',
    '武汉': 'WHN',
    '西安': 'XAY',
    '苏州': 'SZH',
    '天津': 'TJP',
    '南京': 'NJH',
    '长沙': 'CSQ',
    '郑州': 'ZZF',
    '东莞': 'RTQ',
    '青岛': 'QDK',
    '沈阳': 'SYT',
    '宁波': 'NGH',
    '昆明': 'KMM',
    '广州':'GZQ',
    '香港西九龙':'XJA',
    '石家庄':'SJP',
    '哈尔滨': 'HBB',
    '福州': 'FZS',
    '济南': 'JNK',
    '兰州': 'LZJ',
    '南宁': 'NNZ',
    '太原': 'TYV',
    '长春': 'CCT',
    '合肥': 'HFH',
    '南昌': 'NCG',
    '海口': 'VUQ',
    '贵阳': 'GIW',
    '西宁':'XNO',
    '呼和浩特': 'HHC',
    '拉萨': 'LSO',
    '乌鲁木齐': 'WAR'}
        self.city_nos = []
        for city in self.cities.values():
            self.city_nos.append(city)

    def work_on(self):
        """
        主函数
        :return:
        """
        visited_city=[]
        try:
            self.get_cities() # 获取所有站点的名称和代码
            i=0
            while i<len(self.city_nos):
                visited_city.append(self.city_nos[i])
                j=i+1
                while j<len(self.city_nos):
                    print("----------ct1:"+self.city_nos[i]+" ct2:"+self.city_nos[j]+"----------")
                    train_nos=self.get_left_ticket("2019-07-22",self.city_nos[i],self.city_nos[j]) # 获取两个城市之间的所有车次号
                    if train_nos!=None:
                        for train_no in train_nos: # 对每一个车次号的停靠信息做处理
                            if train_no not in self.already_get_query: # 如果某个车次号存过，则跳过
                                station_list=self.get_query_info(train_no,self.city_nos[i],self.city_nos[j],"2019-07-22") # 获取停靠信息
                                print(station_list)
                                self.query[train_no]=station_list
                                self.already_get_query.append(train_no)
                    j+=1
                i+=1
            print(len(self.already_get_query))
        except Exception as e:
            print("Located_2")
            print(e)
        with open("visited_city.txt","w",encoding="utf-8") as f:
            for ct in visited_city:
                f.write(ct)
        sc.save_in_csv(self.query) # 保存为csv文件

    def test(self):
        self.get_cities()
        num=0
        for ct in self.cities.values():
            if "北京" in ct:
                num+=1
        print(num)

train=Train()
train.work_on()
# train.test()


