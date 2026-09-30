<#
.SYNOPSIS
    Formosis - 建立一份新論文/報告/簡報（獨立 git repo）

.DESCRIPTION
    1. 把 profiles\<profile>\skeleton\ 複製到 Formosis 根目錄下的 <資料夾名稱>\
    2. 在該資料夾 git init，成為你自己的論文 repo（與工具 repo 分開，更新工具不會動到論文）
    3. 在工具 repo 的 .git\info\exclude 忽略該資料夾（只影響本機，不改動任何受版控的檔案）
    4. 寫入 .claude\settings.json，讓在論文資料夾開的 Claude Code 不載入工具開發用的 CLAUDE.md

    論文資料夾必須直接放在 Formosis 根目錄下：skeleton 內的指令以 ..\scripts\ 呼叫編譯腳本。

.EXAMPLE
    .\scripts\new-thesis.ps1 thesis-ncu my-thesis

.EXAMPLE
    .\scripts\new-thesis.ps1 slides-ncu my-defense
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$ProfileName,
    [Parameter(Mandatory = $true, Position = 1)]
    [string]$Name
)

$ErrorActionPreference = "Stop"

function Write-Ok      { param([string]$Message) Write-Host "[OK]    " -ForegroundColor Green -NoNewline; Write-Host $Message }
function Write-WarnMsg { param([string]$Message) Write-Host "[WARN]  " -ForegroundColor Yellow -NoNewline; Write-Host $Message }
function Write-ErrorMsg { param([string]$Message) Write-Host "[ERROR] " -ForegroundColor Red -NoNewline; Write-Host $Message }

# git 的 stderr 在 PowerShell 5.1 會被包成錯誤；比照 build.ps1 的 Invoke-Native，改看 $LASTEXITCODE
function Invoke-Git {
    param([string[]]$ArgList)
    $prevPref = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try {
        $out = & git @ArgList 2>&1
        return @{ Code = $LASTEXITCODE; Output = $out }
    } finally {
        $ErrorActionPreference = $prevPref
    }
}

$ScriptDir = Split-Path -Parent $PSCommandPath
$RepoRoot = Split-Path -Parent $ScriptDir
$Skeleton = Join-Path $RepoRoot "profiles\$ProfileName\skeleton"
$Target = Join-Path $RepoRoot $Name

if (-not (Test-Path $Skeleton)) {
    Write-ErrorMsg "找不到 profile：$ProfileName（可用清單：.\scripts\build.ps1 -ListProfiles）"
    exit 1
}
if ($Name -notmatch '^[A-Za-z0-9._-]+$') {
    Write-ErrorMsg "資料夾名稱只能用英數字、點、底線、連字號（中文或空白路徑會讓部分 LaTeX 工具出錯）：$Name"
    exit 1
}
if (@("profiles", "shared", "scripts", "docs", "examples", "docker", "tests", ".git", ".github") -contains $Name) {
    Write-ErrorMsg "'$Name' 是 Formosis 自己的資料夾，請換個名字"
    exit 1
}
if (Test-Path $Target) {
    Write-ErrorMsg "$Target 已存在"
    exit 1
}

# 1. 複製 skeleton
New-Item -ItemType Directory -Path $Target | Out-Null
Get-ChildItem -Path $Skeleton -Force | Copy-Item -Destination $Target -Recurse -Force
Write-Ok "已從 profiles\$ProfileName\skeleton\ 建立 $Name\"

$utf8NoBom = New-Object System.Text.UTF8Encoding $false

# 2. 論文 repo 的 .gitignore（編譯產物）
$gitignore = @(
    "# 編譯產物（需要保存 PDF 時可 git add -f paper.pdf）",
    "*.pdf", "*.tex", "*.aux", "*.bbl", "*.bcf", "*.blg", "*.log", "*.out", "*.run.xml",
    "*.toc", "*.lof", "*.lot", "*.xdv", "slides.html", ".DS_Store", "Thumbs.db"
) -join "`n"
[System.IO.File]::WriteAllText((Join-Path $Target ".gitignore"), $gitignore + "`n", $utf8NoBom)

# 3. 在論文資料夾開 Claude Code 時，不載入上層工具 repo 的開發用 CLAUDE.md
$claudeDir = Join-Path $Target ".claude"
New-Item -ItemType Directory -Path $claudeDir -Force | Out-Null
$rootName = Split-Path -Leaf $RepoRoot
$settings = "{`n  `"claudeMdExcludes`": [`n    `"**/$rootName/CLAUDE.md`"`n  ]`n}`n"
[System.IO.File]::WriteAllText((Join-Path $claudeDir "settings.json"), $settings, $utf8NoBom)

$hasGit = [bool](Get-Command git -ErrorAction SilentlyContinue)

# 4. 工具 repo 忽略論文資料夾（本機設定，不改動受版控的檔案）
if ($hasGit) {
    $r = Invoke-Git @("-C", $RepoRoot, "rev-parse", "--git-path", "info/exclude")
    if ($r.Code -eq 0) {
        $exclude = ([string]($r.Output | Select-Object -First 1)).Trim()
        if (-not [System.IO.Path]::IsPathRooted($exclude)) { $exclude = Join-Path $RepoRoot $exclude }
        $excludeDir = Split-Path -Parent $exclude
        if (-not (Test-Path $excludeDir)) { New-Item -ItemType Directory -Path $excludeDir -Force | Out-Null }
        $line = "/$Name/"
        $existing = @()
        if (Test-Path $exclude) { $existing = Get-Content -LiteralPath $exclude -Encoding UTF8 }
        if ($existing -notcontains $line) {
            [System.IO.File]::AppendAllText($exclude, "$line`n", $utf8NoBom)
        }
        Write-Ok "Formosis repo 已忽略 $Name\（寫在 .git\info\exclude）"
    }
}

# 5. 論文資料夾成為獨立 git repo
if ($hasGit) {
    Invoke-Git @("-C", $Target, "init", "-q") | Out-Null
    Invoke-Git @("-C", $Target, "symbolic-ref", "HEAD", "refs/heads/main") | Out-Null
    Invoke-Git @("-C", $Target, "add", "-A") | Out-Null
    $c = Invoke-Git @("-C", $Target, "commit", "-q", "-m", "chore: 以 Formosis $ProfileName 建立")
    if ($c.Code -eq 0) {
        Write-Ok "已初始化 $Name\ 為獨立 git repo（分支 main）"
    } else {
        Write-WarnMsg "已 git init，但第一次 commit 失敗（多半是還沒設定 git user.name / user.email）"
        Write-WarnMsg "設定後在 $Name\ 內執行：git commit -m 'chore: 初始化'"
    }
} else {
    Write-WarnMsg "找不到 git，略過版本控制初始化"
}

$mainMd = "paper.md"
if (Test-Path (Join-Path $Target "slides.md")) { $mainMd = "slides.md" }
Write-Host ""
Write-Host "下一步："
Write-Host "  cd $Name"
Write-Host "  # 編輯 $mainMd 開頭的 YAML，替換 <placeholder>"
Write-Host "  ..\scripts\build.ps1 $mainMd"
Write-Host ""
Write-Host "要備份到 GitHub：在 GitHub 建一個 private repo，然後在 $Name\ 內執行"
Write-Host "  git remote add origin <你的 repo 網址>"
Write-Host "  git push -u origin main"
