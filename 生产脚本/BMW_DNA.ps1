function get_token()
{
    $token = invoke-webrequest -Uri "https://{IP}/dna/system/api/v1/auth/token" -headers @{  } -ContentType "application/json"
    return $token
}

function get_date($token)
{
    $start = (([DateTime]::Now.ToUniversalTime().Ticks - 621355968000000000)/10000 - 604800).tostring().Substring(0, 13)
    $end = (([DateTime]::Now.ToUniversalTime().Ticks - 621355968000000000)/10000).tostring().Substring(0, 13)
    $dnadata = invoke-webrequest -Uri "https://{ip}/api/assurance/v1/issue/global" -Method Post -Body '{"filters":{}, "issueStatus":"active"}' -headers @{ "startTime" = "$( $start )"; "endTime" = "$( $end )"; "x-auth-token" = "$( $token )" } -ContentType "application/json" | ConvertFrom-Json
    return $dnadata
}

function pushDataToMsp($exdata)
{
    $createdate = [DateTime]::FromFileTime($exdata.lastOccurrence*10000 + 504911520000000000)
    $pushdata = '{"operation": {"details": {"subject": "EVT BWM DNA Attention-' + $( $exdata.category ) + '","status": "open","description": "Message:' + $( $displayeName ) + ' \nDevice:' + $( $exdata.deviceRole ) + '\nAreaCount:' + $( $exdata.areaCount ) + '\nBuildingCount:' + $( $exdata.buildingCount ) + '\nFloorCount:' + $( $exdata.floorCount ) + '\nDeviceCount:' + $( $exdata.deviceCount ) + '\nTime:' + $( $createdate ) + '","requester": "BMW_DNA","site": "BMW Common Site","account": "BMW","priority":"$($data.priority)"}}}'
    Invoke-WebRequest -Uri "https://{MSPIP}/sdpapi/request?format=json&data=$( $pushdata )" -Method Post -Headers @{ "contenttype" = "application/json"; "TECHNICIAN_KEY" = "" }
}

