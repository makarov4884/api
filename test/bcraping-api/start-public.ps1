# Bcraping API 공개 서버 시작 스크립트

Write-Host "🚀 Bcraping API 공개 서버 시작..." -ForegroundColor Cyan
Write-Host ""

# ngrok이 설치되어 있는지 확인
$ngrokPath = Get-Command ngrok -ErrorAction SilentlyContinue

if (-not $ngrokPath) {
    Write-Host "❌ ngrok이 설치되지 않았습니다." -ForegroundColor Red
    Write-Host "PowerShell을 다시 시작하거나 다음 명령어로 설치하세요:" -ForegroundColor Yellow
    Write-Host "  winget install Ngrok.Ngrok" -ForegroundColor White
    Write-Host ""
    Write-Host "또는 수동으로 다운로드: https://ngrok.com/download" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ ngrok 발견!" -ForegroundColor Green
Write-Host ""

# 현재 IP 주소 표시
Write-Host "📍 현재 로컬 네트워크 IP 주소:" -ForegroundColor Cyan
$ipAddress = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.InterfaceAlias -notlike "*Loopback*" } | Select-Object -First 1).IPAddress
Write-Host "   http://$ipAddress:8000" -ForegroundColor White
Write-Host "   (같은 WiFi에 연결된 사람들이 사용 가능)" -ForegroundColor Gray
Write-Host ""

# ngrok 실행
Write-Host "🌐 ngrok으로 공개 URL 생성 중..." -ForegroundColor Cyan
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
Write-Host ""

# ngrok 실행 (새 프로세스로)
Start-Process -FilePath "ngrok" -ArgumentList "http", "8000" -NoNewWindow -Wait
