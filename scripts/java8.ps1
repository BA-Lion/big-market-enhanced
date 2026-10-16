# Run with &, not dot-sourcing. No persistent environment changes are made.
[CmdletBinding()]
param(
    [ValidateSet('Check', 'Maven', 'Run')]
    [string]$Action = 'Check',
    [string]$JdkHome = $env:BIG_MARKET_JAVA_HOME,
    [string]$MavenHome = $env:BIG_MARKET_MAVEN_HOME,
    [string[]]$ToolArguments = @(),
    [string[]]$JvmArguments = @(),
    [string]$JarPath = 'big-market-app/target/big-market-app.jar',
    [string]$SpringProfile = 'dev',
    [switch]$DryRun
)

if ($MyInvocation.InvocationName -eq '.') {
    throw 'Invoke this script with &, not dot-sourcing.'
}

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$previousJavaHome = $env:JAVA_HOME
$previousPath = $env:Path
$locationPushed = $false
$commandExitCode = 0

try {
    if ([string]::IsNullOrWhiteSpace($JdkHome)) {
        $JdkHome = 'D:\Develop\Java\JDK8\jdk8u504-b01'
    }
    if ([string]::IsNullOrWhiteSpace($MavenHome)) {
        $MavenHome = 'D:\Develop\apache-maven-3.9.16'
    }

    $repositoryRoot = Split-Path -Parent $PSScriptRoot
    $resolvedJdkHome = (Resolve-Path -LiteralPath $JdkHome).ProviderPath
    $javaExecutable = Join-Path $resolvedJdkHome 'bin/java.exe'
    $javacExecutable = Join-Path $resolvedJdkHome 'bin/javac.exe'
    $releaseFile = Join-Path $resolvedJdkHome 'release'
    foreach ($requiredFile in @($javaExecutable, $javacExecutable, $releaseFile)) {
        if (-not (Test-Path -LiteralPath $requiredFile -PathType Leaf)) {
            throw "Required JDK file is missing: $requiredFile"
        }
    }
    $releaseContents = Get-Content -LiteralPath $releaseFile -Raw
    if ($releaseContents -notmatch '(?m)^JAVA_VERSION="1\.8\.[^"]+"\s*$') {
        throw 'This project requires JDK 8. The selected JDK release is not Java 8.'
    }

    $env:JAVA_HOME = $resolvedJdkHome
    $env:Path = "$(Join-Path $resolvedJdkHome 'bin');$previousPath"
    Push-Location -LiteralPath $repositoryRoot
    $locationPushed = $true

    $executable = $javaExecutable
    $invokeArguments = @()
    if ($Action -in @('Check', 'Maven')) {
        $resolvedMavenHome = (Resolve-Path -LiteralPath $MavenHome).ProviderPath
        $executable = Join-Path $resolvedMavenHome 'bin/mvn.cmd'
        if (-not (Test-Path -LiteralPath $executable -PathType Leaf)) {
            throw "Maven executable is missing: $executable"
        }
        if ($JvmArguments.Count -gt 0) {
            throw '-JvmArguments is supported only with -Action Run.'
        }
        if ($Action -eq 'Check') {
            if ($ToolArguments.Count -gt 0) {
                throw '-Action Check does not accept -ToolArguments.'
            }
            $invokeArguments = @('-v')
        } else {
            if ($ToolArguments.Count -eq 0) {
                throw 'Supply Maven goals/options through -ToolArguments, or use -Action Check.'
            }
            $invokeArguments = $ToolArguments
        }
    } else {
        if ([string]::IsNullOrWhiteSpace($SpringProfile)) {
            throw '-SpringProfile cannot be empty.'
        }
        if (-not [System.IO.Path]::IsPathRooted($JarPath)) {
            $JarPath = Join-Path $repositoryRoot $JarPath
        }
        $JarPath = [System.IO.Path]::GetFullPath($JarPath)
        if (-not $DryRun -and -not (Test-Path -LiteralPath $JarPath -PathType Leaf)) {
            throw 'Application JAR is missing. Build it first with -Action Maven.'
        }
        $invokeArguments = @($JvmArguments) + @('-jar', $JarPath, "--spring.profiles.active=$SpringProfile") + @($ToolArguments)
    }

    if ($DryRun) {
        # JSON makes argument boundaries visible without invoking the executable.
        [pscustomobject]@{
            Action = $Action
            WorkingDirectory = $repositoryRoot
            JavaHome = $resolvedJdkHome
            Executable = $executable
            Arguments = @($invokeArguments)
        } | ConvertTo-Json -Depth 4
    } else {
        if ($Action -eq 'Check') {
            & $javaExecutable -version
            if ($LASTEXITCODE -ne 0) { throw "java -version failed: $LASTEXITCODE" }
            & $javacExecutable -version
            if ($LASTEXITCODE -ne 0) { throw "javac -version failed: $LASTEXITCODE" }
        }
        & $executable @invokeArguments
        $commandExitCode = $LASTEXITCODE
    }
} catch {
    Write-Error -Message $_.Exception.Message -ErrorAction Continue
    $commandExitCode = 1
} finally {
    if ($locationPushed) { Pop-Location }
    $env:JAVA_HOME = $previousJavaHome
    $env:Path = $previousPath
}

exit $commandExitCode
