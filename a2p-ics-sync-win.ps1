Write-Host "Pull cal as csv from phone using adb-export"
$currentdir = wsl wslpath -a $($(Convert-Path .) -replace '\\', '\\')
$scriptdir = $currentdir+"/lib/adb-export/adb-export.sh"
if (($storagedir = Read-Host "Input Path were to store ics calendar Press enter to accept default value $currentdir") -eq '') {$storagedir=$currentdir}

Write-Host "storagedir is: $storagedir"
Write-Host "scriptdir is: $scriptdir
"
Write-Host "Executing Export" -BackgroundColor Blue

bash -c "cd $storagedir && echo 'storagedir is:' && pwd && $scriptdir -e content://com.android.calendar/events "