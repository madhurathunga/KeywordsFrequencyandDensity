def storeKeywordAndItsCountInDatabase(dict,list):
    j=0
    for kh,freq in dict.items():
        gar=list[j]
        conn.execute('insert into rec(keyword,count,dens) values(?,?,?)',(kh,freq,gar))
        j=j+1
    conn.commit()
def matchKeys(k,dict,keywords):
    found=0
    for sen in keywords.split(','):
        for wor in sen.split(' '):
            if k==wor and found==0:
                dict[k]=1
                found=1
            elif k==wor:
                dict[k]+=1
    if found==0:
        dict[k]=0
from urllib.request import urlopen
from bs4 import BeautifulSoup
from pyexcel_xls import read_data
import sqlite3
conn=sqlite3.connect('mydb2.db')
print('Database created/connected')
conn.execute('drop table if exists rec')
conn.execute('create table rec(keyword text not null,count int not null,dens float not null)')
data={}
data=read_data('Keywords.xlsx')
print('--------Reading URL from Input Excel File--------')
print('-------------------------------------------------')
for values in data.values():
    try:
        urls = values[0]
        key = values[1:]
        z=0
        for url in urls:
            print("URL                        : ",url)
            response = urlopen(url)
            html = response.read().decode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.find("meta", attrs={'name': "Keywords"})
            keywords = title["content"] if title else "No meta title given"
            if keywords=="No meta title given":
                title = soup.find("meta", attrs={'name': "keywords"})
                keywords = title["content"] if title else "No meta title given"
            #print("Keywords                   : ",keywords)
            dict={}
            list=[]
            for ke in key:
                if ke[z]!='':
                    matchKeys(ke[z],dict,keywords)
            sum=0
            print("Keyword and it's frequency : ",dict)
            for num in dict.values():
                sum=sum+num
            for val in dict.values():
                if sum!=0:
                    junk=val/sum
                else:
                    junk=0.0
                list.append(junk)
            print("Density                    : ",list)
            storeKeywordAndItsCountInDatabase(dict, list)
            print('-------------------------------------------------')
            z=z+1
    except IndexError as e:
        pass
conn.close()