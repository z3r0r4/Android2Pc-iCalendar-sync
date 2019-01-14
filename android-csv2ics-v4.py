#!/usr/bin/env python
# coding: utf-8

# In[102]:


from pathlib import Path
path = Path(r"D:\Programme\UBUNTU\Ubuntu.1604.2017.711.0_v1\rootfs\root\com.android.calendar\events-22-55-08\data.csv")


# In[103]:


csvdata = []
import csv
with open(path,"r") as fp:
    reader = csv.DictReader(fp,skipinitialspace=True)
    #data = next(reader)
    for row in reader: # Iterate the remaining rows
        csvdata.append(row)
#csvdata


# In[104]:


#creates dictonary that contains the events seperated by calendar 
csvcalendars = {} 
# = {calendar1Name: [Event1,...],calendar2Name: [Event1,...]}

for i in range(len(csvdata)):
    key = csvdata[i]['calendar_displayName']  # key = calendarname
    value = csvdata[i]#value = event
    
    if key not in csvcalendars:
        csvcalendars[csvdata[i]['calendar_displayName']] = [value]
    elif type(csvcalendars[key])==list:
         csvcalendars[key].append(value)
    else:
        csvcalendars[key] = [csvcalendars[key][0],value]
csvcalendars


# In[ ]:





# In[105]:


import icalendar
from icalendar import Calendar, Event, vText,  vDuration
from datetime import datetime
import random

def display(cal):
    return cal.to_ical().decode('utf-8').replace('\r\n', '\n').strip()


# In[106]:


allDay = 0 
def setAllday(b):
    global allDay
    allDay = b
def getAllday(): return bool(allDay)


# In[107]:


import time, pytz #used for time only berlin for now | improve with localize



def timestamp_to_timeValue(epochTime):
    if(allDay):
        return timestamp_to_date(epochTime)
    elif(allDay==False):
        return timestamp_to_time(epochTime)
    else:
        raise ValueError

def timestamp_to_date(epochTime):
    return  datetime.fromtimestamp(float(epochTime)/1000.).date()#.astimezone(pytz.timezone('UTC')).replace(tzinfo=None)#.replace(tzinfo=pytz.timezone('Europe/Berlin'))#'Europe/Berlin'))
#print(timestamp_to_date('1559174400000'))

def timestamp_to_time(epochTime):
    return  datetime.fromtimestamp(float(epochTime)/1000.).astimezone(pytz.timezone('UTC')).replace(tzinfo=None)#.replace(tzinfo=pytz.timezone('Europe/Berlin'))#'Europe/Berlin'))
#timestamp_to_time('1559174400000')+


# In[108]:


timestamp_to_timeValue('1559174400000')


# In[109]:


header2componentMap = {
        "title"        :lambda v:("summary",v),
        "description"  :lambda v:("description",v),
        "eventLocation":lambda v:("location",v),
        "dtstart"      :lambda t:("dtstart",timestamp_to_timeValue(t)),
        "dtend"        :lambda t:("dtend",timestamp_to_timeValue(t)),
        #"duration"     :lambda d:("duration",vDuration.from_ical(d)), #doesnt work because it requires a pt infront of time values but there is only a p
        #allday is set when no end or duration is given doesnt work yet sets day from 2am to 2am
        #"rrule"        :lambda rule:("rrule",rule),
    }

def mapHeader2Component(headerKey,value):
    return header2componentMap[headerKey](value)
#print(*mapHeader2Component("title","1"))


# In[116]:


icscalendars = {}
for calendarName in csvcalendars:
    icscalendars[calendarName] = Calendar()
    icscalendars[calendarName].add('prodid', '-//My calendar//')
    icscalendars[calendarName].add('version', '2.0')
    icscalendars[calendarName].add('X-WR-TIMEZONE','Europe/Berlin')

    
def add_events_to_ics(calendarName):
    for csvEvent in csvcalendars[calendarName]:
        print("EventName:",csvEvent['title'])
        event = Event()
        event['uid'] = str(random.random())+"@R4"       
        setAllday(csvEvent['allDay'])
        
        for headerKey in csvEvent:   
            
            if headerKey in header2componentMap and csvEvent[headerKey]!='NULL':
                print("   "+headerKey+" exists")
                print("       set to:"+str(mapHeader2Component(headerKey,csvEvent[headerKey])))
                event.add(*mapHeader2Component(headerKey,csvEvent[headerKey]))
                
        icscalendars[calendarName].add_component(event)
        
add_events_to_ics("S4-R4")


# In[111]:


print(display(icscalendars["S4-R4"]))


# In[112]:


import tempfile, os
directory = Path(r"")
f = open(os.path.join(directory, 'MYFILEYEEEEEEEEEE.ics'), 'wb') #(filename,mode) wb indicates that the file is opened in binary mode since its a binary file
f.write(icscalendars["S4-R4"].to_ical())
f.close()


# In[ ]:





# In[ ]:




