function get_token()
{
    $token = invoke-webrequest -Uri "https://172.31.181.46/dna/system/api/v1/auth/token" -headers @{"Authorization"="Basic YWRtaW46Q2lzY28xMjM0NTY="} -ContentType "application/json"
    return $token
}

function get_date()
{
    $start = (([DateTime]::Now.ToUniversalTime().Ticks - 621355968000000000)/10000 - 604800).tostring().Substring(0, 13)
    $end = (([DateTime]::Now.ToUniversalTime().Ticks - 621355968000000000)/10000).tostring().Substring(0, 13)
    $dnadata = invoke-webrequest -Uri "https://172.30.181.46/api/assurance/v1/issue/global" -Method Post -Body '{"filters":{}, "issueStatus":"active"}' -headers @{ "startTime" = "$( $start )"; "endTime" = "$( $end )"; "x-auth-token" = "$( $token )" } -ContentType "application/json" | ConvertFrom-Json
    return $dnadata
}

function pushDataToMsp($exdata)
{
    $createdate = [DateTime]::FromFileTime($exdata.lastOccurrence*10000 + 116444736000000000)
    $pushdata = '{"operation": {"details": {"subject": "EVT BWM DNA Attention-' + $( $displayName ) + '","status": "open","description": "Message:' + $( $displayeName ) + ' \nTime:' + $( $createdate ) + '","requester": "BMW_DNA","site": "BMW Common Site","account": "BMW","priority":"$($data.priority)"}}}'
    Invoke-WebRequest -Uri "https://msp.deliverycenter.cn:8088/sdpapi/request?format=json&data=$( $pushdata )" -Method Post -Headers @{ "contenttype" = "application/json"; "TECHNICIAN_KEY" = "CC9AB615-9EB8-42ED-927C-84CD980D1D23" }
    return
}

