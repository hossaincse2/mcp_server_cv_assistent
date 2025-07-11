# Method 1: Find and kill process using port 6277
# Windows Command Prompt:
netstat -ano | findstr :6277
taskkill /PID <PID_NUMBER> /F

# Windows PowerShell:
Get-NetTCPConnection -LocalPort 6277
Stop-Process -Id <PID_NUMBER> -Force

# Method 2: Kill all Python processes (if you're sure)
# Windows:
taskkill /F /IM python.exe

# Method 3: Kill all MCP processes
# Windows:
taskkill /F /IM "mcp*"

# Method 4: Use a different port for MCP
# Add this to your server.py or use command line option
mcp dev server.py --port 6278

# Method 5: Find process by name and kill
# Windows PowerShell:
Get-Process -Name "*mcp*" | Stop-Process -Force
Get-Process -Name "*python*" | Where-Object {$_.MainWindowTitle -like "*mcp*"} | Stop-Process -Force