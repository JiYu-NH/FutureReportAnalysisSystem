from spiders import SinaFuture,Mysteel,Yunken,ChinaGrain,EastMoney,Hexun,TouTiao,CnGold,QHRB,Jinrongjie,AskCi,SMM
import pymongo,os
from time import sleep

#表对象
articleCol= pymongo.MongoClient(host="localhost",port=27017).FutureArticleDB.articleCollection
articleCol.update_many({},{'$set':{"mailed":True}})
#已经爬取的链接列表
BeCrawledUrlList=[]
for item in articleCol.find({},{'url':1}):
    BeCrawledUrlList.append(item.get('url',''))

FuncList=[
    SinaFuture.getSinaArticleList,
    Mysteel.getMysteelArticleList,
    Yunken.getYunkenArticleList,
    ChinaGrain.getChinaGrainArticleList,
    EastMoney.getEastMoneyArticleList,
    Hexun.getHexunArticleList,
    # TouTiao.getTouTiaoArticleLs,
    CnGold.getJinTouArticleLs,
    QHRB.getQHRBArticleList,
    Jinrongjie.getJinrongjieArticleList,
    AskCi.getAskCiArticleList,
    SMM.getSMMArticleList,
]

for f in FuncList:
    f(articleCol,BeCrawledUrlList)

    # try:
    #     pass
    # except Exception as e:
    #     print('有错误')
    #     print(e)
    #     os.system('pause')

##各自的文件存储完成后，汇总

print('总共 %d  条'%articleCol.count_documents({}))
#发送邮件
updateArticleList=[item  for item in articleCol.find({'mailed':False})]
print('本次更新 %d 条'%len(updateArticleList))
print(updateArticleList)
from common import makeEmailHTML,sendEmail
html=makeEmailHTML(updateArticleList)
   
# if sendEmail(html):
#     print('邮件发送成功')
# else:
#     print('邮件发送失败+++++++++++++')
#     os.system('pause')
# sleep(10)