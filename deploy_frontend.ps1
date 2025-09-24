# 安全部署脚本（v2）
function Get-SecureInput {
    param([string]$prompt)
    $secure = Read-Host $prompt -AsSecureString
    return [Runtime.InteropServices.Marshal]::PtrToStringAuto(
        [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
    )
}

$ak = Get-SecureInput "输入AccessKeyID"
$sk = Get-SecureInput "输入AccessKeySecret"

# 上传文件列表
$files = @('index.html', 'styles.css', 'main.js')  # 根据实际文件调整

foreach ($file in $files) {
    if (Test-Path "D:/dev_workspace/$file") {
        aliyun oss cp "D:/dev_workspace/$file" "oss://petspec-static/$file" `
            --headers "Cache-Control: no-cache"
        Write-Output "Uploaded: $file"
    }
}

# 验证上传结果
aliyun oss ls oss://petspec-static/# CDNˢ�����������Զ�ִ�У�
ossutil64 sync D:/dev_workspace/ oss://petspec-static/ --update
cdncli refresh https://static.petspec.com/demo_index.html
