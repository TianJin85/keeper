Set objFSO = CreateObject("Scripting.FileSystemObject")
Set colDrives = objFSO.Drives  
For Each objDrive in colDrives  
If objDrive.IsReady = True Then 
Wscript.Echo "盘符: " & objDrive.DriveLetter  
wscript.echo "磁盘序列号:" & objDrive.SerialNumber  
wscript.echo "磁盘类型:" & objDrive.DriveType  
wscript.echo "文件系统的类型:" & objDrive.filesystem  
wscript.echo "磁盘名称: " & objDrive.VolumeName  
wscript.echo "总容量:" &objDrive.TotalSize  
Wscript.Echo "剩余容量: " & objDrive.FreeSpace  
wscript.echo "可选容量:" & objDrive.AvailableSpace  
Else 
Wscript.Echo "盘符: " & objDrive.DriveLetter  
End If 
Next