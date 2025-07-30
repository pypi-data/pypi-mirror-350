class html:
    def txts(mode,url,text_class,a_class,text_label='div',a_label='div',prefix='https:/',where_a=None):
        import requests, bs4, lxml, re
        if mode == 'br':
            dic = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
            }
            res=requests.get(url,headers=dic)
            soup=bs4.BeautifulSoup(res.text,'lxml')
            data1=soup.find(text_label,class_=text_class)
            w=1
            try:
                while True:
                    with open(str(w)+'.txt',mode='a',encoding='utf-8') as f:
                        f.write(data1.text)
                    data2=soup.find(a_label,class_=a_class)
                    if where_a != None:
                        g=int(where_a)
                        data2=data2.find_all('a')
                        data2=data2[g]
                    else:
                        data2=data2.find('a')
                    url2=data2['href']
                    a=requests.get(prefix+url2.strip(),headers=dic)
                    soup = bs4.BeautifulSoup(res.text, 'lxml')
                    data1 = soup.find(text_label, class_=text_class)
                    w+=1
            except:
                print('None')
        elif mode == 'p':
            import requests, bs4, lxml, re
            dic = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
            }
            a = requests.get(url, headers=dic)
            try:
                while True:
                    soup=bs4.BeautifulSoup(a.text,'lxml')
                    data=soup.find(text_label,class_=text_class)
                    data=data.find_all('p')
                    w=1
                    with open(str(w)+'.txt',mode='w',encoding='utf-8') as f:
                        for i in data:
                            f.write(i.text)
                    data2=soup.find(a_label,class_=a_class)
                    if where_a  != None:
                        where_a=int(where_a)
                        data2=data2.find_all('a')[where_a]
                    url2=data2['href']
                    url2 += prefix
                    a=requests.get(url2, headers=dic)
            except:
                print('None')
    def txt(url,mode='p',txt_div_class=None,txt='1'):
        import requests,bs4,lxml
        if mode == 'br':
            dic = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
            }
            a=requests.get(url,headers=dic)
            a=bs4.BeautifulSoup(a.text,'lxml')
            with open(txt+'.txt',mode='a') as f:
                f.write(a.text)
        if mode == 'p':
            dic = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
            }
            a=requests.get(url,headers=dic)
            a=bs4.BeautifulSoup(a.text,'lxml')
            a=a.find_all('p')
            with open(txt+'.txt',mode='a') as f:
                for i in a:
                    f.write(i.text)
    def img(url,img_div_class=None,prefix=None):
        import requests, bs4, lxml, re
        dic={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
        }
        a=requests.get(url,headers=dic)
        a.encoding='utf-8'
        soup=bs4.BeautifulSoup(a.text,'lxml')
        if img_div_class == None:
            data=soup.find_all('img')
        else:
            data=soup.find('div',class_=img_div_class)
            data=data.find_all('img')
        w=1
        for i in data:
            if prefix == None:
                s=requests.get(i['src'],headers=dic)
                with open(str(w)+'.jpg',mode='ab') as f:
                    f.write(s.content)
            else:
                s=requests.get(prefix+i['src'],headers=dic)
                with open(i['src']+'.jpg',mode='ab') as f:
                    f.write(s.content)
            w+=1
    def audio(url,audio_div=None):
        import requests, bs4, lxml, re
        dic={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
        }
        w=1
        a=requests.get(url,headers=dic)
        soup=bs4.BeautifulSoup(a.text,lxml)
        if audio_div == None:
            data=soup.find_all('audio')
        else:
            data=soup.find('div',class_=audio_div)
            data.find_all('audio')
        for i in data:
            if 'https://' in i['src']:
                q=i['src'].strip()
            else:
                q='https://'+i['src'].strip()
            a=requests.get(q,headers=dic)
            with open(str(w)+'.mp3','ab') as f:
                f.write(a.content)
            w+=1
    def table(url,turn=None,arrange=''):
        import pandas as pd
        res = pd.read_html(url)
        res = res[0]
        if turn == None:
            None
        elif turn:
            res=res.sort_values(by=arrange,ascending=turn)
        else:
            res=res.sort_values(by=arrange, ascending=turn)
        res.to_excel('1.xlsx')
class run:
    def music(url,mp3_name='1'):
        import requests, bs4, lxml, re
        dic={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
        }
        a=requests.get(url,headers=dic)
        with open(mp3_name+'.mp3',mode='ab') as f:
            f.write(a.content)
    def video(url,mp4='1',prefix=None):
        import requests, bs4, lxml, re
        dic={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
        }
        a=requests.get(url,headers=dic)
        b=re.sub('#E*',a.text)
        for i in b:
            if prefix != None:
                a=requests.get(prefix+i,headers=dic)
            else:
                a=requests.get(i)
            with open(mp4+'.mp4',mode='ab') as f:
                f.write(a.content)
    def txt(url,txt='1'):
        import requests, bs4, lxml, re
        dic={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'}
        res=requests.get(url,headers=dic)
        soup=bs4.BeautifulSoup(res.text,'lxml')
        data=soup.find_all('p')
        for i in data:
            with open(txt+'.txt',mode='a') as f:
                f.write(i.text)
    def table(url,turn=None,arrange=''):
        import pandas as pd
        res = pd.read_html(url)
        res = res[0]
        if turn == None:
            None
        elif turn:
            res=res.sort_values(by=arrange,ascending=turn)
        else:
            res=res.sort_values(by=arrange, ascending=turn)
        res.to_excel('1.xlsx')
class show:
    def txt(mode,txt,start=1,end=1):
        if mode == 'many':
            for i in range(start,end+1):
                with open(str(i)+'.txt',mode='r') as f:
                    p=f.read()
                print(p)
        if mode == 'only':
            with open(txt+'.txt', mode='r') as f:
                p = f.read()
            print(p)
    def image(img):
        from PIL import Image
        a=Image.open('img'+'.jpg')
        a.show()
    def music(mp3):
        from audioplayer import AudioPlayer
        m=AudioPlayer(mp3+'.mp3')
        m.play(block=True)
    def video(mp4):
        from moviepy import VideoFileClip
        a=VideoFileClip(mp4+'.mp4')
        a.preview()
def handle_excel(mode='merge'):
    import pandas as pd
    if mode == 'merge':
        lst = []
        for i in range(int(input())):
            data = pd.read_excel(input())
            lst.append(data)
        data=pd.concat(lst)
        data.to_excel('requests-ss-excel.xlsx')
    if mode == 'statistics':
        d=input()
        a=pd.value_counts(d)
        return a
    if mode == 'duplicate':
        h=pd.read_excel(input()+'.xlsx')
        h=h.drop_duplicates(subset=input())
        h.to_excel('requests-ss-excel.xlsx')