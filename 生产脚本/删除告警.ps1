#! /bin/pwsh
while ($true)
{

    Write-Host "请输入需要删除的告警ID,输入0退出"
    $entity = Read-Host
    if ($entity -ne 0)
    {
        $result = Invoke-WebRequest -Method Post  -Uri "https://:8088/api/json/alarm/deleteAlarm?apiKey=&type=Multi&entity=$( $entity ) " | ConvertFrom-Json
        if($result.AlarmOperation.Details.result -eq "success")
        {
            Write-Host "`n删除成功 `n`n"
        }
    }
    else
    {
        break
    }
}