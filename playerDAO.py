# Football Player DAO
# Author: Rachel King

import mysql.connector
import dbconfig as cfg
class PlayerDAO:
    connection=""
    cursor =''
    host=       ''
    user=       ''
    password=   ''
    database=   ''
    
    def __init__(self):
        self.host=       cfg.mysql['host']
        self.user=       cfg.mysql['user']
        self.password=   cfg.mysql['password']
        self.database=   cfg.mysql['database']

    def getcursor(self): 
        self.connection = mysql.connector.connect(
            host=       self.host,
            user=       self.user,
            password=   self.password,
            database=   self.database,
        )
        self.cursor = self.connection.cursor()
        return self.cursor

    def closeAll(self):
        self.connection.close()
        self.cursor.close()
         
    def getAll(self):
        cursor = self.getcursor()
        sql="select * from player"
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
        #print(results)
        for result in results:
            #print(result)
            returnArray.append(self.convertToDictionary(result))
        
        self.closeAll()
        return returnArray

    def findByID(self, id):
        cursor = self.getcursor()
        sql="select * from player where id = %s"
        values = (id,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        returnvalue = self.convertToDictionary(result)
        self.closeAll()
        return returnvalue

    def create(self, player):
        cursor = self.getcursor()
        sql="insert into player (name, age, nationality) values (%s,%s,%s)"
        values = (player.get("name"), player.get("age"), player.get("nationality"))
        cursor.execute(sql, values)

        self.connection.commit()
        newid = cursor.lastrowid
        player["id"] = newid
        self.closeAll()
        return player


    def update(self, id, player):
        cursor = self.getcursor()
        sql="update player set name= %s,age=%s, nationality=%s  where id = %s"
        
        values = (player.get("name"), player.get("age"), player.get("nationality"),id)
        cursor.execute(sql, values)
        self.connection.commit()
        self.closeAll()
        
    def delete(self, id):
        cursor = self.getcursor()
        sql="delete from player where id = %s"
        values = (id,)

        cursor.execute(sql, values)

        self.connection.commit()
        self.closeAll()
        
        print("delete done")

    def convertToDictionary(self, resultLine):
        attkeys=['id','name','age', "nationality"]
        player = {}
        currentkey = 0
        for attrib in resultLine:
            player[attkeys[currentkey]] = attrib
            currentkey = currentkey + 1 
        return player

        
playerDAO = PlayerDAO()