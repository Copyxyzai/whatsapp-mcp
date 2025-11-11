# Quick Start Guide - WhatsApp MCP Web Interface

## 🎯 Goal
Access your WhatsApp messages through a web browser with an easy-to-use interface.

## ⚡ Quick Setup (5 minutes)

### Step 1: Prerequisites Check
Make sure you have:
- ✅ WhatsApp bridge already running (authenticated with QR code)
- ✅ Python 3.6+ installed
- ✅ Go installed (for the bridge)

### Step 2: Start WhatsApp Bridge
```bash
# Terminal 1 - Start the WhatsApp bridge
cd whatsapp-bridge
go run main.go
```

Wait for the message: "✓ Connected to WhatsApp!"

### Step 3: Start Web Interface
```bash
# Terminal 2 - Start the web interface
cd web-interface
./start.sh          # Linux/macOS
# OR
start.bat           # Windows
```

### Step 4: Access the Interface
Open your browser and go to: **http://localhost:5000**

## 🎨 Using the Interface

### First Time Usage

When you first open the interface, you'll see:

```
┌─────────────────────────────────────────────────────────┐
│  WhatsApp MCP                                           │
│  Web Interface                                          │
└─────────────────────────────────────────────────────────┘
┌─────────────┬─────────────────────────────────────────┐
│  Chats      │  Welcome to WhatsApp MCP Web            │
│  ────────── │                                         │
│  [Search]   │  Select a chat to start messaging      │
│             │                                         │
│  Chat 1     │                                         │
│  Chat 2     │                                         │
│  Chat 3     │                                         │
│             │                                         │
└─────────────┴─────────────────────────────────────────┘
```

### Selecting a Chat

1. **Click on any chat** in the left sidebar
2. The chat will open on the right side
3. You'll see the conversation history

```
┌─────────────┬─────────────────────────────────────────┐
│  Chats      │  John Doe                     [Refresh] │
│             │  1234567890@s.whatsapp.net              │
│  [Search]   ├─────────────────────────────────────────┤
│             │                                         │
│ ✓ John Doe  │  [Them] Hey! How are you?              │
│   Chat 2    │         10:30 AM                        │
│   Chat 3    │                                         │
│             │                      [You] I'm good!    │
│             │                           10:31 AM      │
│             │                                         │
│             ├─────────────────────────────────────────┤
│             │ [Type a message...          ] [Send]    │
└─────────────┴─────────────────────────────────────────┘
```

### Sending a Message

1. **Type your message** in the input field at the bottom
2. **Press Enter** or click the "Send" button
3. Your message appears immediately in green (right-aligned)
4. Messages refresh automatically every 30 seconds

### Searching for Chats

1. **Click in the search box** at the top of the chat list
2. **Type a name, number, or keyword**
3. Chats are filtered in real-time as you type
4. Clear the search box to see all chats again

## 🎓 Tips & Tricks

### Keyboard Shortcuts
- **Enter**: Send message (when in message input)
- **Ctrl+F**: Focus on search box (browser default)
- **Escape**: Clear search (custom implementation)

### Refresh Options
- **Auto-refresh**: Happens every 30 seconds automatically
- **Manual refresh**: Click the ↻ button
  - In chat list: Refreshes all chats
  - In conversation: Refreshes current messages

### Understanding Chat Indicators
- **Green badge**: Indicates a group chat
- **Time stamp**: Shows last message time
  - "10:30 AM" = Today
  - "Yesterday" = Yesterday
  - "Nov 10" = This year
  - "Nov 10, 2024" = Previous years

### Message Indicators
- **📎**: Media file was sent/received
- **Green background**: Messages you sent
- **White background**: Messages you received

## 🔧 Customization

### Change Port
Edit `app.py`, last line:
```python
app.run(host='0.0.0.0', port=5000, debug=True)
```
Change `5000` to your preferred port.

### Adjust Refresh Rate
Edit `static/js/app.js`, last line:
```javascript
}, 30000);  // 30 seconds
```
Change `30000` to your preferred milliseconds (e.g., `60000` = 1 minute).

### Modify Colors
Edit `static/css/style.css`:
- Line ~33: `.header` background color
- Line ~93: `.sidebar-header` WhatsApp green
- Line ~267: `.message.sent` background (your messages)
- Line ~272: `.message.received` background (their messages)

## ⚠️ Troubleshooting

### "Failed to load chats"
**Cause**: WhatsApp bridge is not running or database doesn't exist yet.

**Solution**:
1. Make sure the bridge is running: `cd whatsapp-bridge && go run main.go`
2. Wait for it to sync messages (may take a few minutes first time)
3. Click the refresh button (↻)

### "Failed to connect to WhatsApp bridge"
**Cause**: Bridge API is not accessible.

**Solution**:
1. Check if bridge is running on port 8080
2. Try accessing: http://localhost:8080 in browser
3. Check `WHATSAPP_API_BASE_URL` in `app.py`

### Messages not updating
**Solution**:
1. Click the refresh button (↻)
2. Check browser console for errors (F12)
3. Verify WhatsApp bridge is connected

### Can't send messages
**Cause**: Bridge might be disconnected.

**Solution**:
1. Check bridge terminal for "Connected to WhatsApp"
2. Try restarting the bridge
3. Verify the chat JID is correct

## 🔒 Security Best Practices

### For Local Use
- Default settings are fine
- Access only via `http://localhost:5000`

### For Network Access
If you want to access from other devices on your network:

1. **Keep on private network only** - Don't expose to internet
2. **Use a firewall** - Block external access
3. **Consider authentication** - Add login requirement
4. **Use HTTPS** - Set up SSL certificates

### For Production
**DO NOT** use this setup directly in production without:
- Adding authentication (username/password)
- Implementing HTTPS/SSL
- Setting up proper firewall rules
- Adding rate limiting
- Implementing session management

## 📱 Mobile Access

To access from your phone on the same network:

1. Find your computer's local IP:
   ```bash
   # Linux/macOS
   ifconfig | grep "inet "
   
   # Windows
   ipconfig
   ```

2. On your phone's browser, go to:
   ```
   http://YOUR_COMPUTER_IP:5000
   ```
   
   Example: `http://192.168.1.100:5000`

## 🎉 You're All Set!

You can now:
- ✅ View all your WhatsApp chats
- ✅ Read message history
- ✅ Send messages to anyone
- ✅ Search through your chats
- ✅ Access WhatsApp from your browser

Enjoy your web-based WhatsApp experience! 🚀

## 📚 Need More Help?

- Check the [README.md](README.md) for detailed information
- Review [FEATURES.md](FEATURES.md) for all available features
- Check the troubleshooting section above
- Review the main [WhatsApp MCP README](../README.md)

## 🐛 Found a Bug?

Please report issues on the GitHub repository with:
- What you were trying to do
- What happened instead
- Error messages (if any)
- Browser and OS information
