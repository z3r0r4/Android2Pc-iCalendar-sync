# Android2Pc-iCalendar-sync
## A2P-ics-sync

A Python script to sync Android calendars to a pc using the iCalendar format.

My goal was to sync my Android calendar with my Thunderbird-Lightning calendar.<br>
While it's easily possible to sync to, and view a Thunderbird-Lightning calendar from an Android Phone (i.e. with [ICSx⁵](https://icsx5.bitfire.at/)), the reverse seemed nearly impossible to do efficiently.
Although there are a lot of Android apps that enable the user to manually export their calendar as a iCalendar (i.e. with [Calendar Import-Export](https://github.com/PrivacyApps/calendar-import-export) or [iCal Import/Export CalDAV](https://play.google.com/store/apps/details?id=tk.drlue.icalimportexport)<sup>1</sup>), I wasn't able to find any good solution to automate this process.
<br><sub><sup>1</sup>(got the feature I am searching for, but sadly only as a proprietary paid extension)</sub>

After spending half a week of searching for a script that could be used to export the android calendar, I decided to create my own.

The Python script retrieves the content provider's data as a CSV file using [adb-export](https://github.com/sromku/adb-export), and then converts it into a iCalendar (.ics) file using [icalendar](https://github.com/collective/icalendar).<br>
As development continues it should support all necessary used property values of a typical calendar.
