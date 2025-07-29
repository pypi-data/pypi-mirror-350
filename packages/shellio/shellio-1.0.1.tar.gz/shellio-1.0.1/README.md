# shellio

ShellIO is a Python interface for interacting with Unix-like shells (sh, bash, zsh) using pseudoterminals (PTY). It enables real-time communication with interactive shell processes, capturing and parsing output including ANSI escape sequences.

### Features
- ✅ Spawn interactive shell sessions (sh, bash, zsh)
- 📤 Send input directly to the shell (stdin)
- 📥 Read output instantly using PTY — no line buffering delay
- 🧩 Detect and split ANSI escape sequences from raw output
- 🧼 Automatically terminates all shell processes on exit
- 🧵 Background threading for non-blocking output reading
- 🔀 Supports multiple concurrent shell instances

### Use Cases
- Terminal emulators
- Shell automation tools
- Output parsers
- Teaching/debugging shell interactions

### Instalation

```bash
$ pip install shellio
```

### Example of usage:

```py

from shellio import ShellIO

# Initialize a new shell object
shell = ShellIO('bash', []) # zsh, sh or bash

# You can specify a path where to start the shell
shell.set_cwd('.')

# Start the process
shell.run()

# Clear last output file
open('output.txt', 'w').close()

# Put the first command with a return
shell.put('ls -la\n')

# Wait a second for output
shell.wait(2)

# Put the second command
shell.put('touch works.txt\n')

# Read all bytes from shell and save it to a file
for b in shell.get(timeout=0.01):
    print(b.decode(), end='')
    with open('output.txt', 'a') as file:
        file.write(b.decode())

```

