#! /bin/pwsh
# 允许powershell信任自签名证书
add-type @"
    using System.Net;
    using System.Security.Cryptography.X509Certificates;
    public class TrustAllCertsPolicy : ICertificatePolicy {
        public bool CheckValidationResult(
            ServicePoint srvPoint, X509Certificate certificate,
            WebRequest request, int certificateProblem) {
            return true;
        }
    }
"@

[System.Net.ServicePointManager]::CertificatePolicy = New-Object TrustAllCertsPolicy

# 用于获取DNAC访问的token 账号密码加密方式为 Basic "账号:密码"
function get_token()
{
    $token = invoke-webrequest -Uri "https://host/dna/system/api/v1/auth/token" -Method Post -headers @{ "authorization" = "Basic " } -ContentType "application/json" | ConvertFrom-Json
    return $token.Token
}
# 时间戳转换
function get_date($token)
{
    $start = (([DateTime]::Now.ToUniversalTime().Ticks - 621355968000000000)/10000 - 604800).tostring().Substring(0, 13)
    $end = (([DateTime]::Now.ToUniversalTime().Ticks - 621355968000000000)/10000).tostring().Substring(0, 13)
    $dnaData = invoke-webrequest -Uri "https://host/api/assurance/v1/issue/global" -Method Post -Body '{"filters":{}, "issueStatus":"active"}' -headers @{ "startTime" = "$( $start )"; "endTime" = "$( $end )"; "x-auth-token" = "$( $token )" } -ContentType "application/json" | ConvertFrom-Json
    return $dnaData
}
# 将查询到的数据推送到MSP
function pushDataToMsp($exdata)
{
    #$createdate = [DateTime]::FromFileTime($exdata.lastOccurrence*10000 + 504911520000000000)
    $createDate = Get-Date
    $pushData = '{"operation": {"details": {"subject": "EVT BWM DNA Attention-' + $( $exdata.category ) + '","status": "open","description": "Message:' + $( $displayeName ) + ' \nDevice:' + $( $exdata.deviceRole ) + '\nAreaCount:' + $( $exdata.areaCount ) + '\nBuildingCount:' + $( $exdata.buildingCount ) + '\nFloorCount:' + $( $exdata.floorCount ) + '\nDeviceCount:' + $( $exdata.deviceCount ) + '\nTime:' + $( $createDate ) + '","requester": "BMW_DNA","site": "BMW Common Site","account": "BMW","priority":"$($data.priority)"}}}'
    Invoke-WebRequest -Uri "https:///sdpapi/request?format=json&data=$( $pushData )" -Method Post -Headers @{ "contenttype" = "application/json"; "TECHNICIAN_KEY" = "" }
}


$token = get_token
$dnaData = get_date($token)
#Write-Host $dnadata
$alarmList = @()

foreach ($data in $dnaData.response)
{
    # 将查询到的告警加入到列表
    $alarmList += $data.lastOccurrence
    #Write-Host $($data)
}

Write-Host $alarmList

foreach ($exData in $dnaData.response)
{
    pushDataToMsp($exData)
}


Start-sleep -s 3600

# 创建新的对象与上一次获取到的告警列表进行比对，如果有新增旧推送到MSP
for ($true) {

    $newDnaData = get_date($token)
    foreach ($newdata in $newDnaData.response)
    {
        if ($newdata.lastOccurrence -notin $alarmList)
        {
            Write-Host "Have a new Alarm"
            pushDataToMsp($newdata)
        }
    }
    foreach ($data in $newDnaData)
    {
        $alarmList += $data.lastOccurrence
        #Write-Host $($data)
    }
    Start-sleep -s 3600
} 
 
