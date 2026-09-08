<#
  论文仓库一键同步
  运行方式：双击「同步.cmd」，或在本目录执行  pwsh -File sync.ps1
  流程：检查 VPN 代理 → 暂存改动 → 提交 → 拉取远程(rebase) → 推送到 GitHub
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

Set-Location -LiteralPath $PSScriptRoot
Info "=== 论文仓库一键同步 ==="
Info "目录: $PSScriptRoot"

# 1) 仓库检查
if (-not (Test-Path -LiteralPath (Join-Path $PSScriptRoot '.git'))) {
    Bad "X 这里不是 git 仓库（缺少 .git 目录），无法同步。"
    exit 1
}

# 2) VPN 代理检查（GitHub 直连会被阻断，必须走代理）
$proxyPort = 18081
$proxyUrl  = "http://127.0.0.1:$proxyPort"
$proxyUp = $false
try { $proxyUp = [bool](Get-NetTCPConnection -LocalPort $proxyPort -State Listen -ErrorAction SilentlyContinue) } catch { }
if ($proxyUp) {
    Ok "V 代理可用: $proxyUrl"
} else {
    Warn "! 代理端口 $proxyPort 未监听 —— GoGoJumpVPN 似乎没有启动。"
    Warn "  直连 GitHub 通常会被阻断，推送很可能失败。"
    $ans = Read-Host "  仍要继续吗？(y/N)"
    if ($ans -notmatch '^[yY]') {
        Warn "  已取消。请先打开 GoGoJumpVPN，再重新双击本脚本。"
        exit 0
    }
}

# 3) 扫描并暂存改动
Info ""
Info "--- 扫描本地改动 ---"
git add -A
$staged = @(git diff --cached --name-only)
$ahead = 0
try { $ahead = [int](git rev-list --count origin/master..HEAD 2>$null) } catch { $ahead = 0 }

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

# 4) 提交
if ($staged.Count -gt 0) {
    $defaultMsg = "同步更新 " + (Get-Date -Format 'yyyy-MM-dd HH:mm')
    Info ""
    Info "--- 提交 ---"
    $msg = Read-Host "  提交说明（直接回车使用默认：$defaultMsg）"
    if ([string]::IsNullOrWhiteSpace($msg)) { $msg = $defaultMsg }
    git commit -m $msg | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Bad "X 提交失败，请把上面的信息发给助手。"
        exit 1
    }
    Ok "V 已提交: $msg"
}

# 5) 先拉取远程改动，避免推送被拒
Info ""
Info "--- 拉取远程改动 ---"
git pull --rebase origin master 2>&1 | ForEach-Object { "    $_" }
if ($LASTEXITCODE -ne 0) {
    Warn "! 拉取或变基出现问题。"
    Warn "  如需放弃本次变基：git rebase --abort"
    Warn "  请把上面的信息发给助手处理。"
    exit 1
}

# 6) 推送
Info ""
Info "--- 推送 ---"
git push -u origin master 2>&1 | ForEach-Object { "    $_" }
if ($LASTEXITCODE -ne 0) {
    Bad "X 推送失败。常见原因：VPN 没开 / 登录凭据失效。"
    Bad "  请把上面的信息发给助手，我来处理。"
    exit 1
}

Ok ""
Ok "V 同步完成！"
Info "最近的提交："
git log --oneline -3 | ForEach-Object { "    $_" }
exit 0
