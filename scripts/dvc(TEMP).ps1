# scripts/dvc.ps1
param (
  [string]$Command = "push"
)

Get-Content .env | ForEach-Object {
    if ($_ -match "=") {
        $k, $v = $_ -split "=", 2
        [System.Environment]::SetEnvironmentVariable($k, $v)
    }
}

dvc $Command
