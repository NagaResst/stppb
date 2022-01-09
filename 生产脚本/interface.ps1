#! /bin/pwsh

$interfacedata = (Get-Content "interfaceList.json" | ConvertFrom-Json)
#读取要抓取的接口列表dd 读取json格式的数据作为对象储存在一个变量里
#powershell的变量可以作为对象  对数据的使用有良好的支持性
#输出表头  会覆盖上次抓取的文件
Write-Output `t deviceName | Out-File  -NoNewline  "interface.xls"
Write-Output `t interfaceName | Out-File -Append -NoNewline  "interface.xls"
Write-Output `t  Rx-Min | Out-File -Append -NoNewline  "interface.xls"
Write-Output `t Rx-Max | Out-File -Append -NoNewline  "interface.xls"
Write-Output `t Rx-Avg | Out-File -Append -NoNewline  "interface.xls"
Write-Output `t Rx-95th | Out-File -Append -NoNewline  "interface.xls"
Write-Output `t Tx-Min | Out-File -Append -NoNewline  "interface.xls"
Write-Output `t Tx-Max | Out-File -Append -NoNewline  "interface.xls"
Write-Output `t Tx-Avg | Out-File -Append -NoNewline  "interface.xls"
Write-Output `t Tx-95th | Out-File -Append -NoNewline  "interface.xls"
Write-Host Starting work!
#XLS文件是一个简单的excel表格 本质上也可以用记事本打开 但是不支持xlsx

#遍历接口列表  向表格输出数据  同时显示接口抓取进度
foreach ($interf IN $interfacedata.data)
{
    $data = Invoke-WebRequest -Uri "$( $interfacedata.httpadd )/api/json/device/getInterfaceGraphs?interfaceName=$( $interf.interfaceID )&graphName=utilization&isFluidic=true&period=Last_Month&apiKey=$( $interfacedata.apikey )"  | ConvertFrom-Json
    $summary = Invoke-WebRequest -Uri "$( $interfacedata.httpadd )/api/json/device/getInterfaceSummary?interfaceName=$( $interf.interfaceID )&apiKey=$( $interfacedata.apikey )"  | ConvertFrom-Json
    <#
    foreach是powershell提供的遍历函数  可以自动遍历括号内的列表
    ($interf IN $interfacedata.data) 此条将接口列表中的 data 部分单独提取出来作为 interf 对象使用 会遍历interf (即$interfacedata.data)中的所有内容  此函数中使用的时候使用 interf
    #>
    #echo  "http://localhost:8088/api/json/device/getInterfaceGraphs?interfaceName=$($interf.interfaceID)&graphName=utilization&isFluidic=true&period=Last_Month&apiKey=fb03c0f3839789c0e16b1bdd9c4348ac"
    Write-Output `n $interf.sequence | Out-File -Append -NoNewLine "interface.xls"
    Write-Output `t $interf.device | Out-File -Append -NoNewLine "interface.xls"
    Write-Output `t $summary.intfDisplayName | Out-File -Append  -NoNewline "interface.xls"
    Write-Output `t $data.consolidatedValues.'Rx Utilization'.'minVal' | Out-File -Append -NoNewline  "interface.xls"
    Write-Output `t $data.consolidatedValues.'Rx Utilization'.'maxVal' | Out-File -Append -NoNewline  "interface.xls"
    Write-Output `t $data.consolidatedValues.'Rx Utilization'.'avgVal' | Out-File -Append -NoNewline  "interface.xls"
    Write-Output `t $data.consolidatedValues.'Rx Utilization'.'95thpercentileValue' | Out-File -Append -NoNewline "interface.xls"
    Write-Output `t $data.consolidatedValues.'Tx Utilization'.'minVal' | Out-File -Append -NoNewline "interface.xls"
    Write-Output `t $data.consolidatedValues.'Tx Utilization'.'maxVal' | Out-File -Append -NoNewline "interface.xls"
    Write-Output `t $data.consolidatedValues.'Tx Utilization'.'avgVal' | Out-File -Append -NoNewline "interface.xls"
    Write-Output `t $data.consolidatedValues.'Tx Utilization'.'95thpercentileValue' | Out-File -Append -NoNewline "interface.xls"
    Write-Host `n NO. $interf.sequence
    Write-Host `t $interf.device  -NoNewline
    Write-Host `t $summary.intfDisplayName  -NoNewline
    Write-Host `t Rx-min $data.consolidatedValues.'Rx Utilization'.'minVal'  -NoNewline
    Write-Host `t Rx-max $data.consolidatedValues.'Rx Utilization'.'maxVal'  -NoNewline
    Write-Host `t Rx-avg $data.consolidatedValues.'Rx Utilization'.'avgVal'  -NoNewline
    Write-Host `t Rx-95th $data.consolidatedValues.'Rx Utilization'.'95thpercentileValue'  -NoNewline
    Write-Host `t Tx-min $data.consolidatedValues.'Tx Utilization'.'minVal'  -NoNewline
    Write-Host `t Tx-max $data.consolidatedValues.'Tx Utilization'.'maxVal' -NoNewline
    Write-Host `t Tx-avg $data.consolidatedValues.'Tx Utilization'.'avgVal'  -NoNewline
    Write-Host `t Tx-95th $data.consolidatedValues.'Tx Utilization'.'95thpercentileValue'
    #Write-Progress 提供一个可视化的进度条用于查看现在任务执行的进度
    Write-Progress -Activity "Starting..." -PercentComplete $( $interf.sequence / $interfacedata.data.Length * 100 )  -CurrentOperation "$( $interf.sequence ) / $( $interfacedata.data.Length )  Finished" -Status "Loading..."
}

Write-Host `n "Report is complete!"