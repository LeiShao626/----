<#
  论文仓库一键同步（跨电脑可用版）
  运行方式：双击「同步.cmd」，或在本目录执行
            powershell -ExecutionPolicy Bypass -File sync.ps1
  流程：环境自检 → 身份自检 → 代理自动适配 → 暂存 → 提交 → 拉取(rebase) → 推送
#>

try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch { }
$ErrorActionPreference = 'Continue'
if (Get-Variable -Name PSNativeCommandUseErrorActionPreference -ErrorAction SilentlyContinue) {
    $PSNativeCommandUseErrorActionPreference = $false
}

function Info($m) { Write-Host $m -ForegroundColor Cyan }
function Ok($m)   { Write-Host $m -ForegroundColor Green }
function Warn($m) { Write-Host $m -ForegroundColor Yellow }
function Bad($m)  { Write-Host $m -ForegroundColor Red }

function Test-LocalPort([int]$Port) {
    try {
        $r = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
        return [bool]$r
    } catch {
        try {
            $c = New-Object Net.Sockets.TcpClient
            $c.Connect('127.0.0.1', $Port)
            $c.Close()
            return $true
        } catch { return $false }
    }
}

$RepoUrl = 'https://github.com/LeiShao626/----.git'

Set-Location -LiteralPath $PSScriptRoot
Info "=== 论文仓库一键同步 ==="
Info "目录: $PSScriptRoot"

# ---------- 1) 环境自检 ----------
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Bad "X 没有检测到 git。请先安装 Git for Windows："
    Bad "    https://git-scm.com/download/win"
    exit 1
}

if (-not (Test-Path -LiteralPath (Join-Path $PSScriptRoot '.git'))) {
    Bad "X 这里不是 git 仓库（缺少 .git 目录），无法同步。"
    if (Test-Path -LiteralPath (Join-Path $PSScriptRoot '.gitignore')) {
        Warn "  看起来你是下载了 ZIP 压缩包 —— ZIP 里不包含 .git，所以无法直接同步。"
        Warn "  请改用克隆方式，在上一级目录执行："
        Warn "      git clone $RepoUrl"
    }
    exit 1
}
Ok "V 已检测到 git 仓库"

# 让中文文件名正常显示（否则会显示成 \345\220\214 这种转义）
& git config --local core.quotepath false 2>$null | Out-Null

# ---------- 2) 提交身份自检（新电脑必做） ----------
$gName  = (& git config user.name  2>$null)
$gEmail = (& git config user.email 2>$null)
if ([string]::IsNullOrWhiteSpace($gName) -or [string]::IsNullOrWhiteSpace($gEmail)) {
    Warn "! 这台电脑还没配置 git 提交身份，直接提交会失败，现在补上："
    if ([string]::IsNullOrWhiteSpace($gName)) {
        $v = Read-Host "  你的名字（回车用默认：Shao Lei）"
        if ([string]::IsNullOrWhiteSpace($v)) { $v = 'Shao Lei' }
        & git config --local user.name $v
        Ok "  已设置 user.name = $v"
    }
    if ([string]::IsNullOrWhiteSpace($gEmail)) {
        $v = Read-Host "  你的邮箱（回车用默认：2995451959@qq.com）"
        if ([string]::IsNullOrWhiteSpace($v)) { $v = '2995451959@qq.com' }
        & git config --local user.email $v
        Ok "  已设置 user.email = $v"
    }
} else {
    Ok "V 提交身份: $gName <$gEmail>"
}

# ---------- 3) 远程仓库自检 ----------
$origin = (& git remote get-url origin 2>$null)
if ([string]::IsNullOrWhiteSpace($origin)) {
    & git remote add origin $RepoUrl 2>$null
    Ok "V 已补上远程仓库: $RepoUrl"
} else {
    Ok "V 远程仓库: $origin"
}

# ---------- 4) 代理自动适配（换电脑的关键） ----------
$candidatePorts = @(18081, 18080, 7897, 7890, 10809, 10808, 1080, 8888, 8080)
$proxyUrl = $null

$cur = (& git config --get http.proxy 2>$null)
if (-not [string]::IsNullOrWhiteSpace($cur)) {
    $cur = $cur.Trim()
    $p = 0
    if ($cur -match '(\d+)\s*$') { $p = [int]$Matches[1] }
    if ($p -gt 0 -and (Test-LocalPort $p)) {
        $proxyUrl = $cur
        Ok "V 沿用已配置的代理: $proxyUrl"
    } else {
        Warn "! 已配置的代理 $cur 端口未监听，改为自动探测。"
    }
}

if (-not $proxyUrl) {
    foreach ($p in $candidatePorts) {
        if (Test-LocalPort $p) {
            $proxyUrl = "http://127.0.0.1:$p"
            Ok "V 自动检测到本地代理: $proxyUrl"
            break
        }
    }
}

if ($proxyUrl) {
    $ProxyArgs = @('-c', "http.proxy=$proxyUrl", '-c', "https.proxy=$proxyUrl")
    & git config --local http.proxy  $proxyUrl 2>$null
    & git config --local https.proxy $proxyUrl 2>$null
} else {
    $ProxyArgs = @('-c', 'http.proxy=', '-c', 'https.proxy=')
    Warn "! 未检测到本地代理，将尝试直连 GitHub。"
    Warn "  如果你在中国大陆，直连通常会被阻断 —— 请先打开 VPN 再重试。"
}

# ---------- 5) 暂存改动 ----------
$branch = (& git rev-parse --abbrev-ref HEAD 2>$null)
if ([string]::IsNullOrWhiteSpace($branch) -or $branch -eq 'HEAD') { $branch = 'master' }

Info ""
Info "--- 扫描本地改动（分支 $branch）---"
& git @ProxyArgs add -A
$staged = @(& git @ProxyArgs diff --cached --name-only)
$ahead = 0
try { $ahead = [int](& git @ProxyArgs rev-list --count "origin/$branch..HEAD" 2>$null) } catch { $ahead = 0 }

if ($staged.Count -eq 0 -and $ahead -eq 0) {
    Ok "V 没有任何改动，本地与远程已一致，无需同步。"
    exit 0
}

if ($staged.Count -gt 0) {
    Info "  待提交 $($staged.Count) 个文件："
    $staged | Select-Object -First 15 | ForEach-Object { "    $_" }
    if ($staged.Count -gt 15) { "    ... 其余 $($staged.Count - 15) 个" }
} else {
    Info "  没有新改动，但有 $ahead 个本地提交尚未推送。"
}

# ---------- 6) 提交 ----------
if ($staged.Count -gt 0) {
    $defaultMsg = "同步更新 " + (Get-Date -Format 'yyyy-MM-dd HH:mm')
    Info ""
    Info "--- 提交 ---"
    $msg = Read-Host "  提交说明（直接回车使用默认：$defaultMsg）"
    if ([string]::IsNullOrWhiteSpace($msg)) { $msg = $defaultMsg }
    & git @ProxyArgs commit -m $msg | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Bad "X 提交失败，请把上面的信息发给助手。"
        exit 1
    }
    Ok "V 已提交: $msg"
}

# ---------- 7) 先拉取，避免推送被拒 ----------
Info ""
Info "--- 拉取远程改动 ---"
& git @ProxyArgs pull --rebase origin $branch 2>&1 | ForEach-Object { "    $_" }
if ($LASTEXITCODE -ne 0) {
    Warn "! 拉取或变基出现问题。"
    Warn "  如需放弃本次变基：git rebase --abort"
    Warn "  请把上面的信息发给助手处理。"
    exit 1
}

# ---------- 8) 推送 ----------
Info ""
Info "--- 推送 ---"
& git @ProxyArgs push -u origin $branch 2>&1 | ForEach-Object { "    $_" }
if ($LASTEXITCODE -ne 0) {
    Bad "X 推送失败。常见原因：VPN 没开 / 登录凭据失效。"
    Bad "  请把上面的信息发给助手，我来处理。"
    exit 1
}

Ok ""
Ok "V 同步完成！"
Info "最近的提交："
& git @ProxyArgs log --oneline -3 | ForEach-Object { "    $_" }
exit 0
