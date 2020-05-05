import requests
import json
import sys
import time
import csv
import pandas as pd
from importlib import reload
def doubleDigit(num):
    if num < 10 :
        return '0'+str(num)
    else:
        return str(num)


def main(v_id,c_id):
    if sys.version_info[0] == 2:
        reload(sys)
        sys.setdefaultencoding('utf-8')
    
    
    videoId = v_id
    clientId = c_id
    

    chat = []
    time = []
    user = []
    
    nextCursor = ''
    
    params = {}
    params['client_id'] = clientId
    
    
    i = 0
    while True :
        if i == 0 :
            URL = 'https://api.twitch.tv/v5/videos/'+videoId+'/comments?content_offset_seconds=0' 
            i += 1
        else:
            URL = 'https://api.twitch.tv/v5/videos/'+videoId+'/comments?cursor=' 
            URL +=  nextCursor   
            

        response = requests.get(URL, params=params)
        
        j = json.loads(response.text)
        # with open('api.json','a',encoding='utf-8') as file:
        #     json.dump(j,file,indent='\t',ensure_ascii=False)
        for k in range(0,len(j["comments"])):
            timer = j["comments"][k]["content_offset_seconds"]
            
            timeMinute = int(timer/60)

            if timeMinute >= 60 :
                timeHour = int(timeMinute/60)
                timeMinute %= 60
            else :
                timeHour = int(timeMinute/60)
    
            timeSec = int(timer%60)
            
            time.append(doubleDigit(timeHour)+':'+doubleDigit(timeMinute)+':'+doubleDigit(timeSec))
            user.append(j["comments"][k]["commenter"]["display_name"])
            chat.append(j["comments"][k]["message"]["body"])
        if '_next' not in j:
            break
        
        nextCursor = j["_next"]

    f = open(videoId+".csv", mode='w',encoding='utf-8-sig',newline='')
    wr = csv.writer(f)
    for x in range(0, len(time)):
        tmp = [str(time[x]), str(user[x]), str(chat[x])]
        wr.writerow(tmp)
    f.close()

def analysis(v_id):
    df = pd.read_csv(v_id+'.csv', names=['time', 'name', 'chat'])
    timeCountDf = df.groupby('time').count()['chat']  # 정렬 안되어 있는것
    sortedTimeCountDf = df['time'].value_counts()  # 시간별 채팅횟수 내림차순
    ax = timeCountDf.plot(title='chat numbers', figsize=(15, 5))
    fig = ax.get_figure()
    fig.savefig(v_id+'.png')
    output = sortedTimeCountDf[sortedTimeCountDf == sortedTimeCountDf.max()]
    timeList = output.index.values
    timeList.sort()
    with open(v_id+'_time.txt','w') as file:
        for time in timeList:
            file.write(time+'\n')

if __name__ == "__main__":
    startTime = time.time()
    main(sys.argv[1], sys.argv[2])
    print('---{} seconds---'.format(time.time() - startTime))
    analysis(sys.argv[1])