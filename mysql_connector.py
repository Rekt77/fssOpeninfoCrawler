import pymysql

class Connector:
    def __init__(self):
        self.fss_db = pymysql.connect(
            user='root', 
            passwd='test',
            host='127.0.0.1', 
            db='fssRPA', 
            charset='utf8'
        )
        self.cursor = self.fss_db.cursor(pymysql.cursors.DictCursor)

    def insertValues(self,params):
        #id, date, company, reldept, filename, hash
        query = "INSERT INTO PDFS (date,company,reldept,filename,sha1) VALUE ('%s','%s','%s','%s','%s')"%(
            params["date"],
            params["company"],
            params["reldept"],
            params["filename"],
            params["sha1"])

        self.cursor.execute(query)
        self.fss_db.commit()
    
    def findHash(self,hash):
        query = "SELECT sha1 FROM PDFS WHERE sha1='%s'"%(hash)
        print(query)
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result