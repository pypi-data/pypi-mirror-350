param(
  [Parameter(Mandatory=$true)]
  [string]$PackageName,
  [Parameter(Mandatory=$true)]
  [string]$Path
)
Set-Location $Path
$venvDir   = Join-Path $Path 'winvenv'
$pythonExe = Join-Path $venvDir 'Scripts\python.exe'

if (-not (Test-Path $pythonExe)) {
  Write-Error "python.exe not found under '$venvDir'."
  exit 1
}

& $pythonExe -m pip install $PackageName
if ($LASTEXITCODE -ne 0) {
  Write-Error "Failed to install '$PackageName'."
  exit $LASTEXITCODE
}