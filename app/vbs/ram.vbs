strComputer = "."
set objWMI = GetObject("winmgmts:\\" & strComputer & "\root\cimv2")
set colOS = objWMI.InstancesOf("Win32_OperatingSystem")
for each objOS in colOS
strReturn = "内存总数: " &  round(objOS.TotalVisibleMemorySize / 1024) & " MB" & vbCrLf &"内存可用数: " & round(objOS.FreePhysicalMemory / 1024) & " MB" & vbCrLf &"内存使用率 :" & Round(((objOS.TotalVisibleMemorySize-objOS.FreePhysicalMemory)/objOS.TotalVisibleMemorySize)*100) & "%"
Wscript.Echo strReturn
next