
# Parse REMOTE_NAME=...
$DVC_REMOTE_NAME = $null
foreach ($arg in $args) {
    if ($arg -like 'REMOTE_NAME=*') {
        $DVC_REMOTE_NAME = $arg -replace 'REMOTE_NAME=', ''
    }
}
if ($DVC_REMOTE_NAME) {
    $env:DVC_REMOTE_NAME = $DVC_REMOTE_NAME
}

# Nạp biến từ file .env
Get-Content .env | ForEach-Object {
    if ($_ -match "^\s*([^#][^=]*)=(.*)$") {
        [System.Environment]::SetEnvironmentVariable($matches[1], $matches[2])
    }
}

# Lấy tên remote từ biến DVC_REMOTE_NAME (bắt buộc phải truyền vào)
if (-not $env:DVC_REMOTE_NAME) {
    Write-Host "Please set DVC_REMOTE_NAME environment variable or pass REMOTE_NAME=<name> as an argument!"
    exit 1
}

# Chuyển tên remote sang dạng biến (in hoa, thay - thành _)
$remote_var = $env:DVC_REMOTE_NAME.ToUpper().Replace('-', '_')

$access_key_var = "DVC_${remote_var}_ACCESS_KEY_ID"
$secret_key_var = "DVC_${remote_var}_SECRET_ACCESS_KEY"
$endpoint_var = "DVC_${remote_var}_ENDPOINT_URL"

$access_key = [Environment]::GetEnvironmentVariable($access_key_var)
$secret_key = [Environment]::GetEnvironmentVariable($secret_key_var)
$endpoint = [Environment]::GetEnvironmentVariable($endpoint_var)

dvc remote modify --local $env:DVC_REMOTE_NAME access_key_id $access_key
dvc remote modify --local $env:DVC_REMOTE_NAME secret_access_key $secret_key
dvc remote modify --local $env:DVC_REMOTE_NAME endpointurl $endpoint