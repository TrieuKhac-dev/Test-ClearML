


# Nhận tham số kiểu REMOTE_NAME=... giống dvc_config_env.ps1
$REMOTE_NAME = $null
foreach ($arg in $args) {
    if ($arg -like 'REMOTE_NAME=*') {
        $REMOTE_NAME = $arg -replace 'REMOTE_NAME=', ''
    }
}
if (-not $REMOTE_NAME) {
    Write-Host "ERROR: You must provide REMOTE_NAME=<name> as an argument."
    exit 1
}

$configPath = ".dvc/config.local"
if (-not (Test-Path $configPath)) {
    Write-Host "ERROR: Not found $configPath"
    exit 1
}

$lines = Get-Content $configPath

$inBlock = $false
$accessKey = $null
$secretKey = $null
$endpoint = $null
$bucket = $null

foreach ($line in $lines) {
    $trimmed = $line.Trim()

    # Bắt đầu block remote
    if ($trimmed -eq "['remote ""$REMOTE_NAME""']") {
        $inBlock = $true
        continue
    }

    if ($inBlock) {
        if ($trimmed.StartsWith("[")) { break } # sang block khác
        if ($trimmed -match '^access_key_id\s*=\s*(.+)$') { $accessKey = $matches[1].Trim() }
        if ($trimmed -match '^secret_access_key\s*=\s*(.+)$') { $secretKey = $matches[1].Trim() }
        if ($trimmed -match '^endpointurl\s*=\s*(.+)$') { $endpoint = $matches[1].Trim() }
        if ($trimmed -match '^url\s*=\s*(.+)$') { $bucket = $matches[1].Trim() }
    }
}

if (-not $accessKey) {
    Write-Host "ERROR: access_key_id not found for remote '$REMOTE_NAME' in $configPath"
    exit 1
}
if (-not $secretKey) {
    Write-Host "ERROR: secret_access_key not found for remote '$REMOTE_NAME' in $configPath"
    exit 1
}
if (-not $endpoint) {
    Write-Host "ERROR: endpointurl not found for remote '$REMOTE_NAME' in $configPath"
    exit 1
}

if ($bucket) {
    $bucketName = $bucket -replace "^s3://", ""
} else {
    $bucketName = $REMOTE_NAME
}

$env:AWS_ACCESS_KEY_ID = $accessKey
$env:AWS_SECRET_ACCESS_KEY = $secretKey

aws s3 ls "s3://$bucketName/" --recursive --endpoint-url $endpoint
