Write-Host "Pull cal as csv from phone using adb-export"
$currentwsldir = wsl wslpath -a $($(Convert-Path .) -replace '\\', '\\')
$scriptwsldir = $currentwsldir+"/lib/adb-export/adb-export.sh"
if (($storagewsldir = Read-Host "Input WINDOWSPath were to store ics calendar Press enter to accept default value $currentwsldir") -eq '') {$storagewsldir=$currentwsldir} else {$storagewsldir = wsl wslpath -a $storagewsldir}

Write-Host "storagewsldir is: $storagewsldir"
Write-Host "scriptwsldir is: $scriptwsldir
"
Write-Host "Executing Export" -BackgroundColor Blue

#bash -c "cd $storagewsldir && echo 'storagewsldir is:' && pwd && $scriptwsldir -e content://com.android.calendar/events "



$storagedir = wsl wslpath -w $storagewsldir
$mostRecentCal = gci $storagedir\com.android.calendar | ? { $_.PSIsContainer } | sort CreationTime -desc | select -f 1
Write-Host "Parse pulled CSV Calendar to ICS Calendar"
py .\csv2ics.py $storagedir\com.android.calendar\$mostRecentCal\data.csv $storagedir\exportedICalendar