#TODO add duration component so that some dont end up with no end
from pathlib import Path
from sys import argv

csvPath = Path(argv[1]) 
outputdir = Path(argv[2])
calendar = str(argv[3])

print("Reading form csvPath: "+str(csvPath))

#csvdata: array of dictonaries accessible by rownumber and headerkey=icscomponent. every row is one event
#array which contains the rows from the csvfile  as ordereddicts [row0(header),row1,row2,...] accessible by keys specified in the csvheader thus csvdata[row][headerkey] returns the entry from the specified row which is in the column of the specified headerkey

#csvcalendars: dictonary of arrays of dictonaries accessible by calendarName and headerkey=icscomponent
# = {calendar1Name: [Event1,...],calendar2Name: [Event1,...]}

############################## Open csvfile and store as list of dicts in dict accessible by calendarName
csvdata = []	
import csv
try:
	with open(str(csvPath),"r") as fp:
		reader = csv.DictReader(fp,skipinitialspace=True) #reads the rows as 
		for row in reader:	# Iterate through the remaining rows
			csvdata.append(row)
except FileNotFoundError:
	print("Csv Data File not found. Did the Export Finish?")
	exit()

csvcalendars = {}
for i in range(len(csvdata)): #iterates through all the rows=events of the csv
	key = csvdata[i]['calendar_displayName']  # calendarnames are the dictonarykey
	value = csvdata[i]#value = event
    
	if key not in csvcalendars: #if the key isnt already in the dict
		csvcalendars[csvdata[i]['calendar_displayName']] = [value] #add dictentry with the calendarname as key and the event as value
	elif type(csvcalendars[key])==list: #if the key is already in the dict 
		csvcalendars[key].append(value) #add event to calendar
	else:#dk never happens i think 
		csvcalendars[key] = [csvcalendars[key][0],value] #why would you do this instead of just appending? this works only the second time
		print(type(csvcalendars[key]))
		print("IDDDDDKKKKKKKKKKK WHHHHAAAAAATS HAPPENING")
		input()
		exit()#break everything if this happens
		
#csvcalendars
############################## functions to convert value types
	
import random	
import time, pytz #used for time only berlin for now | improve with localize
import icalendar
from icalendar import Calendar, Event, vText, vDuration
from datetime import datetime

def display(cal):
    return cal.to_ical().decode('utf-8').replace('\r\n', '\n').strip()

allDay = 0 #default
def setAllday(b): #boolean
    global allDay
    allDay = int(b)
    print("set Allday to: "+str(allDay) +str(type(allDay)))
    
setAllday(1)#test
if(allDay!=1):
    raise ValueError

def timestamp_to_timeValue(epochTime):
    #print("AAAAAAAAAAAAAA"+ str(type(allDay))+str(allDay)+str(type(allDay)))
    if(allDay==1):
        return timestamp_to_date(epochTime)
    elif(allDay==0):
        return timestamp_to_time(epochTime)
    else:
        raise ValueError

def timestamp_to_date(epochTime):
    return  datetime.fromtimestamp(float(epochTime)/1000.).date()#.astimezone(pytz.timezone('UTC')).replace(tzinfo=None)#.replace(tzinfo=pytz.timezone('Europe/Berlin'))#'Europe/Berlin'))
#print(timestamp_to_date('1559174400000'))

def timestamp_to_time(epochTime):
    return  datetime.fromtimestamp(float(epochTime)/1000.)#.astimezone(pytz.timezone('UTC')).replace(tzinfo=None)#.replace(tzinfo=pytz.timezone('Europe/Berlin'))#'Europe/Berlin'))
#timestamp_to_time('1559174400000')+

#timestamp_to_timeValue('1559174400000') #test

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

############################## Create a dict of ICalendars filled and add their events

icscalendars = {}#create dict containg iCalendars 
for calendarName in csvcalendars:
    icscalendars[calendarName] = Calendar() #create iCalendar type entry for every calendar in csvcalendars
    icscalendars[calendarName].add('prodid', '-//z3r0r4/Android2Pc-iCalendar-sync//') # This property specifies the identifier for the product that created the iCalendar object.
    icscalendars[calendarName].add('version', '2.0')
    icscalendars[calendarName].add('X-WR-TIMEZONE','Europe/Berlin')

def add_events_to_ics(calendarName):#adds all events to an calendar from the dict
    for csvEvent in csvcalendars[calendarName]:
        print("EventName:",csvEvent['title'])#get event title
        event = Event()
        setAllday(csvEvent['allDay'])#workaround that is used for some reason ELIMINATE
        for headerKey in csvEvent:   
            if headerKey in header2componentMap and csvEvent[headerKey]!='NULL':
                print("   "+headerKey+" exists")
                print("       set to:"+str(mapHeader2Component(headerKey,csvEvent[headerKey])))
                event.add(*mapHeader2Component(headerKey,csvEvent[headerKey]))
        event['uid'] = display(event['dtstart'])+"/"+event['summary']+"@"+calendarName
        icscalendars[calendarName].add_component(event)
 
 
add_events_to_ics(calendar)
print(display(icscalendars[calendar]))

############################## export Icalendar
import tempfile, os

print("Saving CSV to: "+str(outputdir)+'\ '+calendar+'-calendar-export.ics')
f = open(os.path.join(str(outputdir), calendar+'-calendar-export.ics'), 'wb')#+datetime.now().strftime("y%Y%m%d_d%H%M")+'.ics'), 'wb') #(filename,mode) wb indicates that the file is opened in binary mode since its a binary file
f.write(icscalendars[calendar].to_ical())
f.close()
print("converted calendar from CSV to ICS!")
print("saved ics to: "+str(outputdir))