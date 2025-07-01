# Server Management Guide

## Current Status
Your Phase 1 server is running in the background with process ID 70527.

## Useful Commands

### Check if server is running
```bash
curl http://localhost:8000/health
```

### View server logs
```bash
tail -f server.log
```

### Check server process
```bash
ps aux | grep "python main.py"
```

### Stop the server
```bash
kill 70527
# or find and kill by process name
pkill -f "python main.py"
```

### Restart the server
```bash
# Stop current server
pkill -f "python main.py"

# Start new server
cd api_gateway
source venv/bin/activate
nohup python main.py > server.log 2>&1 &
```

### Switch to Phase 2 server
```bash
# Stop Phase 1
pkill -f "python main.py"

# Start Phase 2
cd api_gateway
source venv/bin/activate
nohup python main_phase2.py > server_phase2.log 2>&1 &
```

## Alternative: Use tmux (Recommended for Development)

### Start a tmux session
```bash
tmux new-session -d -s unillm-server
tmux send-keys -t unillm-server "cd api_gateway && source venv/bin/activate && python main.py" Enter
```

### Attach to session
```bash
tmux attach-session -t unillm-server
```

### Detach from session (keep running)
Press `Ctrl+B` then `D`

### List sessions
```bash
tmux list-sessions
```

### Kill session
```bash
tmux kill-session -t unillm-server
```

## Alternative: Use screen

### Start a screen session
```bash
screen -S unillm-server
cd api_gateway
source venv/bin/activate
python main.py
```

### Detach from screen (keep running)
Press `Ctrl+A` then `D`

### Reattach to screen
```bash
screen -r unillm-server
```

### List screen sessions
```bash
screen -ls
```

### Kill screen session
```bash
screen -S unillm-server -X quit
```

## Testing the Server

### Quick health check
```bash
curl http://localhost:8000/health
```

### Test with authentication
```bash
cd api_gateway
source venv/bin/activate
python test_phase1_auth.py
```

### Test with curl
```bash
curl -X POST http://localhost:8000/chat/completions \
  -H "Authorization: Bearer YOUR_OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
``` 