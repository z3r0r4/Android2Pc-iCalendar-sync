Write-Host "Pull cal as csv from phone using adb-export.sh then parse it using csv2ics.py"
#$currentwsldir = wsl wslpath -a $($(Convert-Path .) -replace '\\', '\\')
$currentwsldir = wsl wslpath -a $($PSScriptRoot -replace '\\', '\\')
$scriptwsldir = $currentwsldir+"/lib/adb-export/adb-export.sh"
if (($storagewsldir = Read-Host "Input WINDOWS-Path were to store ics calendar (Press enter to accept default value $currentwsldir)") -eq '') {$storagewsldir=$currentwsldir} else {$storagewsldir = wsl wslpath -a $storagewsldir}
$calendarName = Read-Host "Name of Calendar that should be exported"

Write-Host "storagewsldir is: $storagewsldir"
Write-Host "scriptwsldir is: $scriptwsldir
"
Write-Host "Pulling Calendars from Phone" -BackgroundColor Blue

#bash -c "cd $storagewsldir && echo 'storagewsldir is:' && pwd && $scriptwsldir -e content://com.android.calendar/events "

$storagedir = wsl wslpath -w $storagewsldir
$currentdir = $PSScriptRoot
If(!(test-path $storagedir\com.android.calendar)){New-Item -ItemType Directory -Force -Path $storagedir\com.android.calendar}
If(!(test-path $storagedir\exportedICalendar)){New-Item -ItemType Directory -Force -Path $storagedir\exportedICalendar}
$mostRecentCal = gci $storagedir\com.android.calendar  | ? { $_.PSIsContainer } | sort CreationTime -desc | select -f 1 
Write-Host "Parse pulled CSV Calendar to ICS Calendar" -BackgroundColor Blue
py $currentdir\csv2ics.py $storagedir\com.android.calendar\$mostRecentCal\data.csv $storagedir\exportedICalendar $calendarName