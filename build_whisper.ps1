[CmdletBinding()]
param (
    [Parameter()]
    [String]
    $WhisperPath,
    [Parameter()]
    [String]
    $Name,
    [Parameter()]
    [String]
    $InstallUri = "https://community.chocolatey.org/install.ps1"
)
begin {
    function IsChocolatelyInstalled {
        [CmdletBinding()]
        param()
    
        $checkPath = if ($env:ChocolateyInstall) { $env:ChocolateyInstall } else { "$env:PROGRAMDATAchocolatey" }
        $Command = Get-Command choco.exe -ErrorAction Ignore
        if ($Command.Path -and (Test-Path -Path $Command.Path)) {
            # choco is in the %PATH% environment variable, assume it's installed
            Write-Warning "'choco' was found at '$($Command.Path)'."
            $true
        }
        elseif (-not (Test-Path $checkPath)) {
            # Install folder doesn't exist
            $false
        }
        elseif (-not (Get-ChildItem -Path $checkPath)) {
            # Install folder exists but is empty
            $false
        }
        else {
            # Install folder exists and is not empty
            Write-Warning "Files from a previous installation of Chocolatey were found at '$($CheckPath)'."
            $true
        }
    }
    function Install-Package {
        [CmdletBinding()]
        param (
            [Parameter(Mandatory)]
            [string]$CommandName
        )


        Invoke-Admin -program choco.exe -argumentString "install $CommandName --yes --nocolor --limitoutput --no-progress"
        $ResultCode = $LASTEXITCODE
        
        if ($ResultCode -eq 0) {
            Write-Host "Correctly Installed Package $CommandName"
            exit 0
        }
        else {
            Write-Error "Failed to install $CommandName."
            Write-Host "Returned exit code: $($ResultCode)"
            exit $ResultCode
        }
    }
    
    function Invoke-Admin() {
        param ( [string]$program = $(throw "Please specify a program" ),
                [string]$argumentString = "",
                [switch]$waitForExit )
    
        Write-Host "Invoking commmad for $program $argumentString"
        $psi = new-object "Diagnostics.ProcessStartInfo"
        $psi.FileName = $program 
        $psi.Arguments = $argumentString
        $psi.Verb = "runas"
        $proc = [Diagnostics.Process]::Start($psi)
        $proc.WaitForExit();
    }
}
process {
    if (-not $(IsChocolatelyInstalled)) {
        # Install Chocolatey
        Write-Host "Chocolatey not installed!"
        Write-Host "Installing Chocolatey..."
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
        $ChocolateyScript = [scriptblock]::Create($(Invoke-RestMethod -Uri $InstallUri))
        try {
            $ChocolateyScript.Invoke()
            Write-Host "Installed Chocolatey."
        }
        catch {
            Write-Error $_
            Write-Host "Failed to install Chocolatey."
            exit 1
        }
    }

    $Command = Get-Command make -ErrorAction Ignore
    if ($Command.Path) {
        Write-Warning "'make' was found at '$($Command.Path)'."
    } else {
        Write-Host "Invoking Function to install package $Name"
        Install-Package -CommandName $Name
    }

    $mingwInstall = "C:\\ProgramData\\mingw64\\install\\mingw64\\bin"
    if (-not $(Test-Path -Path $mingwInstall)) {
        Write-Host "Invoking Function to install package mingw"
        Install-Package -CommandName mingw
    }
    $Command = Get-Command gcc -ErrorAction Ignore
    if ($Command.Path) {
        Write-Warning "'gcc' was found at '$($Command.Path)'."
    } else {
        Write-Host "Updating path to include compilers"
        $env:Path += ";C:\\ProgramData\\mingw64\\install\\mingw64\\bin"
    }

    # Resolve the script directory
    Write-Host "Whisper path set as $WhisperPath"
    $SCRIPT_DIR = $PSScriptRoot
    if (-not $PSScriptRoot) {
        $SCRIPT_DIR = split-path -parent $MyInvocation.MyCommand.Definition
    }
    Write-Host "Script dir set as $SCRIPT_DIR"

    # Change to the whisper.cpp directory
    Set-Location -Path $WhisperPath

    # Build the project
    Invoke-Expression -Command "make"

    # Move the downloaded models to the models directory
    Move-Item -Path "ggml*.bin" -Destination "models/"

    # Go back to the script directory
    Set-Location -Path $SCRIPT_DIR

    # Create the config.json file with the correct paths
    $CONFIG_FILE = Join-Path -Path $SCRIPT_DIR -ChildPath "config.json"
    $MODELS_PATH = Join-Path -Path $WhisperPath -ChildPath "models"

    $configContent = @"
    {
        "main_command": "$($WhisperPath -replace '\\', '\\')",
        "models_path": "$($MODELS_PATH -replace '\\', '\\')"
    }
"@

    Set-Content -Path $CONFIG_FILE -Value $configContent
    Write-Host "Config file created at $CONFIG_FILE"
}
end {}
