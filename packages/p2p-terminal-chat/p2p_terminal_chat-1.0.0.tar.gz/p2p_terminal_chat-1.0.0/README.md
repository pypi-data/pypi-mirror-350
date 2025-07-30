# P2P Terminal Chat

A decentralized peer-to-peer chat application that runs in the terminal. This application allows users to send messages and files directly to other users without the need for a central server.

## Features

- P2P (Peer-to-Peer) communication
- Encrypted messages and file transfers
- Unique user IDs based on name and birth date
- Friend system with friend requests
- File sharing capabilities
- Colorful terminal interface
- Real-time messaging
- Automatic port assignment

## Installation

### Using pip (Recommended)

```bash
pip install p2p-terminal-chat
```

Or if you want to install it directly from GitHub:

```bash
pip install git+https://github.com/yourusername/p2p-terminal-chat.git
```

### Manual Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/p2p-terminal-chat.git
cd p2p-terminal-chat
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

After installation, you can start the chat application by simply typing:

```bash
p2pchat
```

### First Time Setup

1. Enter your full name when prompted
2. Enter your birth date in MMDD format (e.g., 0101 for January 1st)
3. The program will automatically assign a port and generate your unique ID

### Available Commands

- `connect <user_id>` - Connect to a peer using their ID
- `send <user_id> <message>` - Send a message to a peer
- `file <user_id> <file_path>` - Send a file to a peer
- `friend <user_id>` - Send a friend request
- `friends` - Show online friends
- `peers` - List connected peers
- `quit` - Exit the application

### Example Usage

1. Start the first user:
```bash
p2pchat
# Enter full name: Alice Smith
# Enter birth date: 0101
```

2. Start the second user in a different terminal:
```bash
p2pchat
# Enter full name: Bob Johnson
# Enter birth date: 0202
```

3. Connect the users:
```bash
connect <user_id>
```

4. Send messages:
```bash
send <user_id> <Hello, how are you?>
```

5. Send files:
```bash
file <user_id> </path/to/file.txt>
```

## Security

- All messages and files are encrypted using Fernet symmetric encryption
- User IDs are generated using a combination of name and birth date
- No central server means no data is stored anywhere except on the users' machines

## Notes

- Both users must be online to communicate
- Files are saved in a `downloads` directory
- The application uses your local IP address for identification
- Your friend list is saved between sessions
- The port is automatically assigned when you start the program

## License

This project is licensed under the MIT License - see the LICENSE file for details. 