from typing import Literal
import pty
import os
import subprocess
from threading import Thread
import time
from queue import Queue, Empty
import re
import atexit

Shells = Literal["sh", "bash", "zsh"]

class ShellIO:
    """
    ShellIO provides an interface to run and interact with a Unix-like shell
    (sh, bash, zsh) through a pseudoterminal (PTY), allowing real-time command
    execution and output parsing.
    """

    shells: list['ShellIO'] = []

    def __init__(self, shell_type: Shells, args: list[str] = None) -> None:
        """
        Initialize a ShellIO instance with specified shell type and arguments.

        Args:
            shell_type (Shells): The type of shell ('sh', 'bash', or 'zsh').
            args (list[str]): Additional arguments to pass to the shell.
        """
        self.shell_type: Shells = shell_type
        self.args: list[str] = (args if args is not None else [])
        self.program = [self.shell_type, *self.args]
        self.line_queue = Queue()
        self.cwd = None
        self.shells.append(self)

    def set_cwd(self, path: str) -> None:
        """
        Set the current working directory for the shell process.
        This method must be called before `run()` is invoked.

        Args:
            path (str): Path to the working directory.
        """
        if hasattr(self, 'process') and self.process is not None:
            raise RuntimeError("Cannot set working directory after shell is running.")

        if not os.path.isdir(path):
            raise ValueError(f"Invalid directory: {path}")

        self.cwd = path

    def enqueue_output(self, queue: Queue) -> None:
        while True:
            out = os.read(self.master, 128)
            if not out: time.sleep(0.6)
            else: queue.put(out)

    def clear(self):
        try:
            while True:
                self.line_queue.get(False)
        except Empty:
            pass

    def wait(self, seconds: float):
        time.sleep(seconds)

    def run(self) -> None:
        """
        Start the shell process with a pseudoterminal and begin reading output
        in a background thread.
        """
        args = []

        env = os.environ.copy()

        if self.shell_type == 'bash':
            args = ['--rcfile', '~/.bashrc']
        elif self.shell_type == 'sh':
            args = ['--rcfile', '/etc/profile']
            env["PS1"] = "\\s-\\v\\$ "
        elif self.shell_type == 'zsh':
            args = ['--interactive']
        else:
            raise Exception('Shell should be sh, bash or zsh')

        self.program = [self.shell_type, *args, *self.args]
        self.master, self.slave = pty.openpty()
        self.process = subprocess.Popen(
            self.program,
            stdin=self.slave,
            stdout=self.slave,
            stderr=self.slave,
            text=False,
            shell=False,
            bufsize=0,
            cwd=self.cwd,
            env=env,
            preexec_fn=os.setsid
        )
        self.thread = Thread(target=self.enqueue_output, args=(self.line_queue,))
        self.thread.daemon = True
        self.thread.start()

    def put(self, stdin: str) -> None:
        """
        Send input to the shell.

        Args:
            stdin (str): Input string to write to shell (append '\n' if needed).
        """
        os.write(self.master, stdin.encode())

    def get(self, timeout: float = 0.1) -> list[bytes]:
        """
        Read raw output and return as a list of bytes chunks,
        with ANSI sequences split out.

        Args:
            timeout (float): Max time to wait for each chunk.

        Returns:
            list[bytes]: List of output parts (text and ANSI sequences).
        """
        output = b""
        while True:
            try:
                output += self.line_queue.get(timeout=timeout)
            except Empty:
                break

        return ShellIO.split_bytes_ansi(output)

    @staticmethod
    def split_bytes_ansi(data: bytes) -> list[bytes]:
        """
        Split raw byte output into normal bytes and ANSI escape sequences.

        Args:
            data (bytes): Raw output from shell.

        Returns:
            list[bytes]: Separated normal bytes and ANSI codes.
        """

        ansi_pattern = re.compile(rb'\x1b\[[0-9;?]*[a-zA-Z]')

        result = []
        i = 0
        while i < len(data):
            match = ansi_pattern.match(data, i)
            if match:
                result.append(match.group())
                i = match.end()
            else:
                result.append(data[i:i+1])
                i += 1

        return result


@atexit.register
def kill_all_shells():
    for shell in ShellIO.shells:
        if shell.process.poll() is None:
            shell.process.terminate()


