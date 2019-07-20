import requests
import json
def save_in_csv(dic):
	with open("file02.csv","w",encoding="utf-8") as f:
		f.write("起点,终点,划分,经纬度\n")
		tem_save={}
		start={}
		end={}
		for i in dic:
			for j in range(0,len(dic[i])-1):
				if dic[i][j] in tem_save:
					start=tem_save[dic[i][j]]
				else:
					start=get_json(dic[i][j]+"站")
					tem_save[dic[i][j]]=start
				if dic[i][j+1] in tem_save:
					end=tem_save[dic[i][j+1]]
				else:
					end=get_json(dic[i][j+1]+"站")
					tem_save[dic[i][j+1]]=end
				print(dic[i][j])
				f.write(dic[i][j]+"站,"+dic[i][j+1]+"站,"+i+","+"\"["+start["longitude"]+","+start["latitude"]+"],["+end["longitude"]+","+end["latitude"]+"]\"")
				f.write("\n")
def get_json(kw):
	try:
		url="https://restapi.amap.com/v3/place/text?key=8325164e247e15eea68b59e89200988b&offset=10&keywords="
		url+=kw
		headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'}
		html=requests.get(url=url,headers=headers).text
		data=json.loads(html)
		str=data['pois'][0]['location'].split(",")
		dic={
		"longitude":str[0],
		"latitude":str[1],
		}
		print(dic)
		return dic
	except:
		dic={
		"longitude":kw+"error",
		"latitude":kw+"error"
		}
		return dic