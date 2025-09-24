# 生成符合RFC 1123格式的Date头信息
$date = (Get-Date).ToUniversalTime().ToString('ddd, dd MMM yyyy HH:mm:ss') + ' GMT'
Write-Host "使用Date头信息: $date"

# 设置API URL
$apiUrl = "https://productdesc-api-fgysjgufnw.cn-hangzhou.fcapp.run/health"

# 使用Invoke-WebRequest测试
Write-Host "\n使用Invoke-WebRequest测试API..."
Try {
    $response = Invoke-WebRequest -Uri $apiUrl -Headers @{"Date" = $date} -TimeoutSec 10 -UseBasicParsing
    Write-Host "响应状态码: $($response.StatusCode)"
    Write-Host "响应内容: $($response.Content)"
} Catch {
    Write-Host "错误: $_"
}

# 使用curl测试（如果系统中有curl）
Write-Host "\n使用curl测试API..."
Try {
    $env:date_header = $date
    cmd /c "curl -v -H \"Date: %date_header%\" $apiUrl"
} Catch {
    Write-Host "curl错误: $_"
}