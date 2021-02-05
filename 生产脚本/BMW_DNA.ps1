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

function get_token()
{
    $token = invoke-webrequest -Uri "https:///dna/system/api/v1/auth/token" -Method Post -headers @{ "authorization" = "Basic " } -ContentType "application/json" | ConvertFrom-Json
    return $token.Token
}

function get_date($token)
{
    $start = (([DateTime]::Now.ToUniversalTime().Ticks - 621355968000000000)/10000 - 604800).tostring().Substring(0, 13)
    $end = (([DateTime]::Now.ToUniversalTime().Ticks - 621355968000000000)/10000).tostring().Substring(0, 13)
    $dnadata = invoke-webrequest -Uri "https:///api/assurance/v1/issue/global" -Method Post -Body '{"filters":{}, "issueStatus":"active"}' -headers @{ "startTime" = "$( $start )"; "endTime" = "$( $end )"; "x-auth-token" = "$( $token )" } -ContentType "application/json" | ConvertFrom-Json
    return $dnadata
}

function pushDataToMsp($exdata)
{
    #$createdate = [DateTime]::FromFileTime($exdata.lastOccurrence*10000 + 504911520000000000)
    $createdate = Get-Date
    $pushdata = '{"operation": {"details": {"subject": "EVT BWM DNA Attention-' + $( $exdata.category ) + '","status": "open","description": "Message:' + $( $displayeName ) + ' \nDevice:' + $( $exdata.deviceRole ) + '\nAreaCount:' + $( $exdata.areaCount ) + '\nBuildingCount:' + $( $exdata.buildingCount ) + '\nFloorCount:' + $( $exdata.floorCount ) + '\nDeviceCount:' + $( $exdata.deviceCount ) + '\nTime:' + $( $createdate ) + '","requester": "BMW_DNA","site": "BMW Common Site","account": "BMW","priority":"$($data.priority)"}}}'
    Invoke-WebRequest -Uri "https:///sdpapi/request?format=json&data=$( $pushdata )" -Method Post -Headers @{ "contenttype" = "application/json"; "TECHNICIAN_KEY" = "" }
}



$token = get_token
$dnadata = get_date($token)
#Write-Host $dnadata
$alarmlist = @()

foreach ($data in $dnadata.response)
{
    $alarmlist += $data.lastOccurrence
    #Write-Host $($data)
}

Write-Host $alarmlist

foreach ($exdata in $dnadata.response)
{
    pushDataToMsp($exdata)
}


Start-sleep -s 3600

for ($true) {
    $newdnadata = get_date($token)
    foreach ($newdata in $newdnadata.response)
    {
        if ($newdata.lastOccurrence -notin $alarmlist)
        {
            Write-Host "Have a new Alarm"
            pushDataToMsp($newdata)
        }
    }
    foreach ($data in $newdnadata)
    {
        $alarmlist += $data.lastOccurrence
        #Write-Host $($data)
    }
    Start-sleep -s 3600
} 
 
