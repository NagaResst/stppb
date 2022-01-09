$username = Read-Host "please enter username"
$passwd = Read-Host "please enter password"
$pwd=ConvertTo-SecureString $passwd -AsPlainText -Force
#将字符串转换为系统登录凭据
$cred=New-Object System.Management.Automation.PSCredential($username,$pwd)
#生成登录信息
$server = Read-Host "please enter server's IP addresss"
#注意你的powershell版本 5.0可能不支持用IP地址登录远程设备， 只能使用计算机名
Enter-PSSession -ComputerName $server -Credential $cred

