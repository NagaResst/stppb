class TestForClass
{
    $title = 'title'
    $messages = ''
    $p = ''
    $isFirst = ''
    $sender = ''
    [Void]
    testwh($title)
    {
        write-host  $title
    }
}

$url = [TestForClass]::new()
$url.testwh($url.title)
$url.sender = 'yes'
Write-Host $url.sendere