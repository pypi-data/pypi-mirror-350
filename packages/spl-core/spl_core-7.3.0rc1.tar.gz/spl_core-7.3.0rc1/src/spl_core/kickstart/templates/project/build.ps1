﻿<#
.DESCRIPTION
    Wrapper for installing dependencies, running and testing the project
#>

param(
    [Parameter(Mandatory = $false, HelpMessage = 'Install all dependencies required to build. (Switch, default: false)')]
    [switch]$install = $false,
    [Parameter(Mandatory = $false, HelpMessage = 'Install Visual Studio Code. (Switch, default: false)')]
    [switch]$installVSCode = $false,
    [Parameter(Mandatory = $false, HelpMessage = 'Build the target.')]
    [switch]$build = $false,
    [Parameter(Mandatory = $false, HelpMessage = 'Command to be executed (String)')]
    [string]$command = "",
    [Parameter(Mandatory = $false, HelpMessage = 'Clean build, wipe out all build artifacts. (Switch, default: false)')]
    [switch]$clean = $false,
    [Parameter(Mandatory = $false, HelpMessage = 'Build kit to be used. (String: "prod" or "test", default: "prod")')]
    [string]$buildKit = "prod",
    [Parameter(Mandatory = $false, HelpMessage = 'Target to be built. (String, default: "all")')]
    [string]$target = "all",
    [Parameter(Mandatory = $false, HelpMessage = 'Variants (of the product) to be built. (List of strings, leave empty to be asked or "all" for automatic build of all variants)')]
    [string[]]$variants = $null,
    [Parameter(Mandatory = $false, HelpMessage = 'filter for self tests, e.g. "Disco or test_Disco.py" (see https://docs.pytest.org/en/stable/usage.html).')]
    [string]$filter = "",
    [Parameter(Mandatory = $false, HelpMessage = 'Additional build arguments for Ninja (e.g., "-d explain -d keepdepfile" for debugging purposes)')]
    [string]$ninjaArgs = "",
    [Parameter(Mandatory = $false, HelpMessage = 'Delete CMake cache and reconfigure. (Switch, default: false)')]
    [switch]$reconfigure = $false
)

# Call a command and handle its exit code
Function Invoke-CommandLine {
    [Diagnostics.CodeAnalysis.SuppressMessageAttribute('PSAvoidUsingInvokeExpression', '', Justification = 'Usually this statement must be avoided (https://learn.microsoft.com/en-us/powershell/scripting/learn/deep-dives/avoid-using-invoke-expression?view=powershell-7.3), here it is OK as it does not execute unknown code.')]
    param (
        [Parameter(Mandatory = $true, Position = 0)]
        [string]$CommandLine,
        [Parameter(Mandatory = $false, Position = 1)]
        [bool]$StopAtError = $true,
        [Parameter(Mandatory = $false, Position = 2)]
        [bool]$Silent = $false
    )
    if (-Not $Silent) {
        Write-Output "Executing: $CommandLine"
    }
    $global:LASTEXITCODE = 0
    Invoke-Expression $CommandLine
    if ($global:LASTEXITCODE -ne 0) {
        if ($StopAtError) {
            Write-Error "Command line call '$CommandLine' failed with exit code $global:LASTEXITCODE"
        }
        else {
            if (-Not $Silent) {
                Write-Output "Command line call '$CommandLine' failed with exit code $global:LASTEXITCODE, continuing ..."
            }
        }
    }
}

# Update/Reload current environment variable PATH with settings from registry
Function Initialize-EnvPath {
    # workaround for system-wide installations
    if ($Env:USER_PATH_FIRST) {
        $Env:Path = [System.Environment]::GetEnvironmentVariable("Path", "User") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "Machine")
    }
    else {
        $Env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
    }
}

function Test-RunningInCIorTestEnvironment {
    return [Boolean]($Env:JENKINS_URL -or $Env:PYTEST_CURRENT_TEST -or $Env:GITHUB_ACTIONS)
}

# Consider CI environment variables (e.g. on Jenkins BRANCH_NAME and CHANGE_TARGET) to filter tests in release branch builds
function Get-ReleaseBranchPytestFilter {
    $ChangeId = $env:CHANGE_ID
    $BranchName = $env:BRANCH_NAME
    $ChangeTarget = $env:CHANGE_TARGET

    $targetBranch = ''

    if (-not $ChangeId -and $BranchName -and $BranchName.StartsWith("release/")) {
        $targetBranch = $BranchName
    }

    if ($ChangeId -and $ChangeTarget -and $ChangeTarget.StartsWith("release/") ) {
        $targetBranch = $ChangeTarget
    }

    $filter = ''
    if ($targetBranch -and ($targetBranch -match 'release/([^/]+/[^/]+)(.*)')) {
        $filter = $Matches[1].Replace('/', ' and ')
    }

    return $filter
}

# Build with given parameters
Function Invoke-Build {
    param (
        [Parameter(Mandatory = $false)]
        [bool]$clean = $false,
        [Parameter(Mandatory = $false)]
        [string]$buildKit = "prod",
        [Parameter(Mandatory = $true)]
        [string]$target = "all",
        [Parameter(Mandatory = $false)]
        [string[]]$variants = $null,
        [Parameter(Mandatory = $false)]
        [string]$filter = "",
        [Parameter(Mandatory = $false)]
        [string]$ninjaArgs = "",
        [Parameter(Mandatory = $false)]
        [bool]$reconfigure = $false
    )
    if ("selftests" -eq $target) {
        # Run python tests to test all relevant variants and platforms (build kits)
        # (normally run in CI environment/Jenkins)
        Write-Output "Running all selfstests ..."

        # Build folder for CMake builds
        $buildFolder = "build"

        # fresh and clean CMake builds
        if ($clean) {
            if (Test-Path -Path $buildFolder) {
                Write-Output "Removing build folder '$buildFolder' ..."
                Remove-Item $buildFolder -Force -Recurse
            }
        }

        # Filter pytest test cases
        $filterCmd = ''
        $releaseBranchFilter = Get-ReleaseBranchPytestFilter
        if ($releaseBranchFilter) {
            $filterCmd = "-k '$releaseBranchFilter'"
        }
        # otherwise consider command line option '-filter' if given
        elseif ($filter) {
            $filterCmd = "-k '$filter'"
        }

        # Test result of pytest
        $pytestJunitXml = "test/output/test-report.xml"

        # Delete any old pytest result
        if (Test-Path -Path $pytestJunitXml) {
            Remove-Item $pytestJunitXml -Force
        }

        # Finally run pytest
        Invoke-CommandLine -CommandLine ".venv\Scripts\pipenv run python -m pytest test --junitxml=$pytestJunitXml $filterCmd"
    }
    else {
        if ((-Not $variants) -or ($variants -eq 'all')) {
            $dirs = Get-Childitem -Include config.cmake -Path variants -Recurse | Resolve-Path -Relative
            $variantsList = @()
            Foreach ($dir in $dirs) {
                $variant = (get-item $dir).Directory.BaseName
                $variantsList += $variant
            }
            $variantsSelected = @()
            if (-Not $variants) {
                # variant selection by user if not specified
                Write-Information -Tags "Info:" -MessageData "no '--variant <variant>' was given, please select from list:"
                Foreach ($variant in $variantsList) {
                    Write-Information -Tags "Info:" -MessageData ("(" + [array]::IndexOf($variantsList, $variant) + ") " + $variant)
                }
                $variantsSelected += $variantsList[[int](Read-Host "Please enter selected variant number")]
                Write-Information -Tags "Info:" -MessageData "Selected variant is: $variantsSelected"
            }
            else {
                # otherwise build all variants
                $variantsSelected = $variantsList
            }
        }
        else {
            $variantsSelected = $Variants.Replace('\', '/').Replace('./variant/', '').Replace('./variants/', '').Split(',')
        }

        # Select 'test' build kit based on target
        if ($target.Contains("unittests") -or $target.Contains("reports") -or $target.Contains("docs")) {
            $buildKit = "test"
        }

        Foreach ($variant in $variantsSelected) {
            Write-Output "Building target '$target' with build kit '$buildKit' for variant '$variant' ..."

            $buildFolder = "build/$variant/$buildKit"
            # fresh and clean build
            if ($clean) {
                if (Test-Path -Path $buildFolder) {
                    Write-Output "Removing build folder '$buildFolder' ..."
                    Remove-Item $buildFolder -Force -Recurse
                }
            }

            # delete CMake cache and reconfigure
            if ($reconfigure) {
                if (Test-Path -Path "$buildFolder/CMakeCache.txt") {
                    Remove-Item "$buildFolder/CMakeCache.txt" -Force
                }
                if (Test-Path -Path "$buildFolder/CMakeFiles") {
                    Remove-Item "$buildFolder/CMakeFiles" -Force -Recurse
                }
            }

            # CMake configure
            $additionalConfig = "-DBUILD_KIT='$buildKit'"
            if ($buildKit -eq "test") {
                $additionalConfig += " -DCMAKE_TOOLCHAIN_FILE='tools/toolchains/gcc/toolchain.cmake'"
            }
            Invoke-CommandLine -CommandLine ".venv\Scripts\pipenv run cmake -B '$buildFolder' -G Ninja -DVARIANT='$variant' $additionalConfig"

            # CMake clean all dead artifacts. Required when running incremented builds to delete obsolete artifacts.
            Invoke-CommandLine -CommandLine ".venv\Scripts\pipenv run cmake --build '$buildFolder' --target $target -- -t cleandead"
            # CMake build
            Invoke-CommandLine -CommandLine ".venv\Scripts\pipenv run cmake --build '$buildFolder' --target $target -- $ninjaArgs"
        }
    }
}

function Invoke-Bootstrap {
    # Download bootstrap scripts from external repository
    Invoke-RestMethod -Uri https://raw.githubusercontent.com/avengineers/bootstrap-installer/v1.17.0/install.ps1 | Invoke-Expression
    # Execute bootstrap script
    . .\.bootstrap\bootstrap.ps1
    # For incremental build: clean up virtual environment from old dependencies
    Invoke-CommandLine ".venv\Scripts\pipenv clean"
}

## start of script
# Always set the $InformationPreference variable to "Continue" globally,
# this way it gets printed on execution and continues execution afterwards.
$InformationPreference = "Continue"

# Stop on first error
$ErrorActionPreference = "Stop"

Push-Location $PSScriptRoot
Write-Output "Running in ${pwd}"

try {
    if (Test-RunningInCIorTestEnvironment -or $Env:USER_PATH_FIRST) {
        Initialize-EnvPath
    }

    if ($install) {
        # bootstrap environment
        Invoke-Bootstrap
    }

    if ($build) {
        # Call build system
        Invoke-Build `
            -target $target `
            -buildKit $buildKit `
            -variants $variants `
            -clean $clean `
            -reconfigure $reconfigure `
            -ninjaArgs $ninjaArgs `
            -filter $filter
    }
}
finally {
    Pop-Location
    if (-Not (Test-RunningInCIorTestEnvironment)) {
        Read-Host -Prompt "Press Enter to continue ..."
    }
}
## end of script
