import _mysql
import universal
import datetime
import logwriter
#init() function creates connection as soon as it starts and ends the same at the end.
#for using loop() function first create a connection using createconnection and after putting all the data close the connection by executing closeconeection
def createconnection():
    try:
        universal.con = _mysql.connect(universal.host,universal.user,universal.password)
        universal.con.query("use "+ universal.dbname)
    except _mysql.Error, e:
        logwriter.logwrite(str(e))
        universal.logflag = 1

def closeconnection():
    try:
        universal.con.close()
    except _mysql.Error, e:
        logwriter.logwrite(str(e))
        universal.logflag = 1
def transform(tag):
  f = "%d/%m/%Y"
  s=universal.data[tag]
  s=s.lower()
  if(bool(s.find('a')!=-1)|bool(s.find('n')!=-1)):
    s="01/01/0001"
  s=s.replace('.','/').replace('-','/')
  ss=datetime.datetime.strptime(s, f)
  universal.data[tag]=str(ss.year)+"/"+str(ss.month)+"/"+str(ss.day)
 # print(universal.data[tag])
def init():
    try:
        universal.con = _mysql.connect(universal.host,universal.user,universal.password)
        universal.con.query("create database if not exists "+universal.dbname)
        universal.con.query("use "+universal.dbname)
        universal.con.query("create table if not exists "+universal.tablename+"("+
                  "Application_No varchar(50),"+ 
                  "Date_of_filing_of_Application DATE,"+
                  "Publication_Date DATE,"+
                  "Name_of_Applicant varchar(1000),"+
                  "Title_of_Invention varchar(1000),"+
                  "Name_of_Inventor varchar(1500),"+
                  "Abstract varchar(3500),"+
                  "No_of_Pages varchar(30),"+
                  "No_of_Claims varchar(30),"+
                  "International_Classification varchar(50),"+
                  "Priority_Document_No varchar(50),"+
                  "Priority_date DATE,"+
                  "Name_of_Priority_country varchar(30),"+
                  "International_Publication_No varchar(30),"+
                  "International_Application_No varchar(30),"+
                  "International_Application_No_filing_date DATE,"+
                  "Patent_of_addition_to_Application_No varchar(30),"+
                  "Patent_of_addition_to_Application_No_filing_date DATE,"+
                  "Divisional_Application_No varchar(30),"+
                  "Divisional_Application_No_filing_date DATE"+
                  ")")
    except Exception as e:
        logwriter.logwrite(str(e))
        universal.logflag = 1
    finally:
        closeconnection()

def loop():
    try:
        transform("Date of filing of Application")
        transform("Publication Date")
        transform("Priority Date")
        transform("IAFiling Date")
        transform("IBFiling Date")
        transform("ICFiling Date")
        q = ('insert into '+universal.tablename+' values("'+
            universal.data["Application No."]+'","'+
            universal.data["Date of filing of Application"]+'","'+
            universal.data["Publication Date"]+'","'+
            universal.data["Name of Applicant"]+'","'+
            universal.data["Title of the invention"]+'","'+
            universal.data["Name of Inventor"]+'","'+
            universal.data["Abstract"]+'","'+
            universal.data["No. of Pages"]+'","'+
            universal.data["No. of Claims"]+'","'+
            universal.data["International classification"]+'","'+
            universal.data["Priority Document No"]+'","'+
            universal.data["Priority Date"]+'","'+
            universal.data["Name of priority country"]+'","'+
            universal.data["International Publication No"]+'","'+
            universal.data["International Application No"]+'","'+
            universal.data["IAFiling Date"]+'","'+
            universal.data["Patent of Addition to Application Number"]+'","'+
            universal.data["IBFiling Date"]+'","'+
            universal.data["Divisional to Application Number"]+'","'+
            universal.data["ICFiling Date"]+'")')
        universal.con.query(q)
        #print(q)
    except Exception as e:
        logwriter.logwrite(str(e))
        universal.logflag = 1
