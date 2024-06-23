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
        CmdletBinding()
        param()

        choco.exe install $Name --yes --nocolor --limitoutput --no-progress
        $ResultCode = $LASTEXITCODE
        
        if ($ResultCode -eq 0) {
            Write-Host "Correctly Installed $Name"
            exit 0
        }
        else {
            Write-Error "Failed to install $Name."
            Write-Host "Returned exit code: $($ResultCode)"
            exit $ResultCode
        }
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

    $(Install-Package)

    # Resolve the script directory
    $SCRIPT_DIR = Split-Path (Split-Path $WhisperPath)
    $WHISPER_DIR = $WhisperPath
    if ($args.Count -eq 0) {
        Write-Host "No whisper.cpp dir provided! Searching in same directory ..."
        $WHISPER_DIR = Join-Path -Path (Split-Path -Path $MyInvocation.MyCommand.Definition -Parent) -ChildPath "whisper.cpp"
    }



    # Change to the whisper.cpp directory
    Set-Location -Path $WHISPER_DIR

    # Build the project
    Invoke-Expression -Command "make"

    # Move the downloaded models to the models directory
    Move-Item -Path "ggml*.bin" -Destination "models/"

    # Go back to the script directory
    Set-Location -Path $SCRIPT_DIR

    # Create the config.json file with the correct paths
    $CONFIG_FILE = Join-Path -Path $SCRIPT_DIR -ChildPath "config.json"
    $MODELS_PATH = Join-Path -Path $WHISPER_DIR -ChildPath "models"

    $configContent = @'
    {
        "main_command": "$WHISPER_DIR",
        "models_path": "$MODELS_PATH"
    }
'@

    Set-Content -Path $CONFIG_FILE -Value $configContent
    Write-Host "Config file created at $CONFIG_FILE"
}
end {}
