class html:
    def txt(a,url,b,d,h='div',c='div',e='https:/',g=None):
        import requests, bs4, lxml, re
        if a == 'br':
            dic = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
            }
            res=requests.get(url,headers=dic)
            print(res.text)
            soup=bs4.BeautifulSoup(res.text,'lxml')
            data1=soup.find(c,class_=b)
            w=1
            try:
                while True:
                    with open(str(w)+'.txt',mode='a',encoding='utf-8') as f:
                        f.write(data1.text)
                    data2=soup.find(h,class_=d)
                    if g != None:
                        g=int(g)
                        data2=data2.find_all('a')
                        data2=data2[g]
                    else:
                        data2=data2.find('a')
                    url2=data2['href']
                    a=requests.get(e+url2.strip(),headers=dic)
                    soup = bs4.BeautifulSoup(res.text, 'lxml')
                    data1 = soup.find(c, class_=b)
                    w+=1
            except:
                print('无')
        elif a == 'p':
            import requests, bs4, lxml, re
            dic = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
            }
            a = requests.get(url, headers=dic)
            try:
                while True:
                    soup=bs4.BeautifulSoup(a.text,'lxml')
                    data=soup.find(f,class_=b)
                    data=data.find_all('p')
                    w=1
                    with open(str(w)+'.txt',mode='w',encoding='utf-8') as f:
                        for i in data:
                            f.write(i.text)
                    data2=soup.find(c,class_=d)
                    data2=data2.find('a')
                    url2=data2['href']
                    if 'http' in url2:
                        None
                    else:
                        url2='https:'+url2
                    a=requests.get(url2, headers=dic)
            except:
                print('无')
    def img(url,b=None,c=None):
        import requests, bs4, lxml, re
        dic={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
        }
        a=requests.get(url,headers=dic)
        a.encoding='utf-8'
        soup=bs4.BeautifulSoup(a.text,'lxml')
        if b == None:
            data=soup.find_all('img')
        else:
            data=soup.find('div',class_=b)
            data=data.find_all('img')
        w=1
        for i in data:
            if c == None:
                s=requests.get(i['src'],headers=dic)
                with open(str(w)+'.jpg',mode='ab') as f:
                    f.write(s.content)
            else:
                s=requests.get(c+i['src'],headers=dic)
                with open(i['src']+'.jpg',mode='ab') as f:
                    f.write(s.content)
            w+=1
    def audio(url,b=None):
        import requests, bs4, lxml, re
        dic={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
        }
        w=1
        a=requests.get(url,headers=dic)
        soup=bs4.BeautifulSoup(a.text,lxml)
        if b == None:
            data=soup.find_all('audio')
        else:
            data=soup.find('div',class_=b)
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
class run:
    def music(url,mp3='1'):
        import requests, bs4, lxml, re
        dic={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
        }
        a=requests.get(url,headers=dic)
        with open(mp3+'.mp3',mode='ab') as f:
            f.write(a.content)
    def video(url,mp4='1',q=None):
        import requests, bs4, lxml, re
        dic={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
        }
        a=requests.get(url,headers=dic)
        b=re.sub('#E*',a.text)
        for i in b:
            if q != None:
                a=requests.get(q+i,headers=dic)
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
class show:
    def txt(a,txt,n=1,m=1):
        if a == '连续':
            for i in range(n,m+1):
                with open(str(i)+'.txt',mode='r') as f:
                    p=f.read()
                print(p)
        if a == '单个':
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
        from moviepy.editor import VideoFileClip
        a=VideoFileClip(mp4+'.mp4')
        a.preview()