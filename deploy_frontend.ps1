# 瀹夊叏閮ㄧ讲鑴氭湰锛坴2锛?
function Get-SecureInput {
    param([string]$prompt)
    $secure = Read-Host $prompt -AsSecureString
    return [Runtime.InteropServices.Marshal]::PtrToStringAuto(
        [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
    )
}

$ak = Get-SecureInput "杈撳叆AccessKeyID"
$sk = Get-SecureInput "杈撳叆AccessKeySecret"

# 涓婁紶鏂囦欢鍒楄〃
$files = @('index.html', 'styles.css', 'main.js')  # 鏍规嵁瀹為檯鏂囦欢璋冩暣

foreach ($file in $files) {
    if (Test-Path "D:/dev_workspace/$file") {
        aliyun oss cp "D:/dev_workspace/$file" "oss://petspec-static/$file" `
            --headers "Cache-Control: no-cache"
        Write-Output "Uploaded: $file"
    }
}

# 楠岃瘉涓婁紶缁撴灉
aliyun oss ls oss://petspec-static/# CDN刷锟斤拷锟斤拷锟筋（锟斤拷锟斤拷锟斤拷远锟街达拷校锟?
ossutil64 sync D:/dev_workspace/ oss://petspec-static/ --update
cdncli refresh https://static.petspec.com/demo_index.html

# 鑵捐浜慏NS閰嶇疆楠岃瘉
Write-Output "`n[姝ｅ湪楠岃瘉DNS閰嶇疆]"
try {
    $dns = Resolve-DnsName petspec.live -Server 119.29.29.29 -ErrorAction Stop
    if ($dns.NameHost -match 'edgeone') {
        Write-Output "[鎴愬姛] DNS宸叉纭厤缃?(鎸囧悜: $($dns.NameHost))"
    } else {
        Write-Warning "[閿欒] DNS鏈寚鍚慐dgeOne"
        Write-Output "璇峰埌鑵捐浜慏NSPod杩涜浠ヤ笅璁剧疆锛?
        Write-Output "1. 璁板綍绫诲瀷: CNAME"
        Write-Output "2. 涓绘満璁板綍: @ 鎴?www"
        Write-Output "3. 璁板綍鍊? 鎮ㄧ殑EdgeOne鍔犻€熷煙鍚?
        Write-Output "4. TTL: 600"
    }
} catch {
    Write-Warning "[閿欒] DNS瑙ｆ瀽澶辫触: $_"
    Write-Output "璇锋鏌ュ煙鍚嶈В鏋愭湇鍔℃槸鍚︽甯?
}

# EdgeOne鍩熷悕褰掑睘楠岃瘉
Write-Output "`n[姝ｅ湪楠岃瘉EdgeOne褰掑睘鏉僝"
try {
    $txtRecords = Resolve-DnsName -Name "edgeonereclaim.petspec.live" -Type TXT -Server 119.29.29.29 -ErrorAction Stop
    $validRecord = $txtRecords.Strings -match "reclaim-"
    
    if ($validRecord) {
        Write-Output "[鎴愬姛] 褰掑睘鏉冮獙璇侀€氳繃 (TXT璁板綍: $($validRecord[0]))"
    } else {
        Write-Warning "[閿欒] 鏈壘鍒版湁鏁圱XT楠岃瘉璁板綍"
        Write-Output "璇峰埌鑵捐浜慏NSPod娣诲姞浠ヤ笅TXT璁板綍锛?
        Write-Output "涓绘満璁板綍: edgeonereclaim"
        Write-Output "璁板綍绫诲瀷: TXT"
        Write-Output "璁板綍鍊? reclaim-dke39dv1ktpnzwg6ha65w1drs1em73u6"
        Write-Output "TTL: 600"
    }
} catch {
    Write-Warning "[閿欒] 褰掑睘鏉冮獙璇佸け璐? $_"
    Write-Output "寤鸿鎿嶄綔锛?
    Write-Output "1. 纭鍩熷悕宸叉坊鍔犲埌鑵捐浜慏NSPod"
    Write-Output "2. 妫€鏌NS鏈嶅姟鍣ㄦ槸鍚﹀凡鏀逛负DNSPod"
    Write-Output "3. 濡傞渶鏆備笉楠岃瘉锛岃鍒癊dgeOne鎺у埗鍙伴€夋嫨'鏆備笉楠岃瘉'"
}

# EdgeOne鏂囦欢楠岃瘉鍔熻兘
function Start-FileVerification {
    $verificationDir = "$PSScriptRoot/.well-known/teo-verification"
    $verificationFile = "$verificationDir/m06934gs5x.txt"
    
    # 鍒涘缓楠岃瘉鏂囦欢
    New-Item -Path $verificationDir -ItemType Directory -Force | Out-Null
    Set-Content -Path $verificationFile -Value "m06934gs5x"
    
    # 涓婁紶鍒癘SS
    aliyun oss cp $verificationFile "oss://petspec-static/.well-known/teo-verification/m06934gs5x.txt" `
        --headers "Cache-Control:no-cache"
    
    # 楠岃瘉鍙闂€?
    $testUrl = "http://petspec.live/.well-known/teo-verification/m06934gs5x.txt"
    $response = try { (Invoke-WebRequest $testUrl -UseBasicParsing).Content } catch { $null }
    
    if ($response -eq "m06934gs5x") {
        Write-Output "[鎴愬姛] 鏂囦欢楠岃瘉鍑嗗瀹屾垚"
    } else {
        Write-Warning "[璀﹀憡] 鏂囦欢楠岃瘉鏈敓鏁堬紝璇锋墜鍔ㄦ鏌ワ細$testUrl"
    }
}
