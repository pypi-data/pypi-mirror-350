# hold-your-shell

`hold-your-shell` is a command line program (TUI) that previews shell
scripts (or any shebang script) in a pager, and asks the user to
confirm execution.

This single file program is written for Python 3.x and only uses the
stdlib.

![image](https://github.com/user-attachments/assets/2f0c2411-1de6-48ef-a1e2-b4984367e558)

## Install

Pip install:

```
pip install hold-your-shell
```

Manual install:

```
HY_BIN=~/.local/bin/hold-your-shell
mkdir -p $(dirname ${HY_BIN})

wget -O ${HY_BIN} https://raw.githubusercontent.com/EnigmaCurry/hold-your-shell/refs/heads/master/hold_your_shell/hold_your_shell.py

chmod +x ${HY_BIN}
```

## Usage

 * Pipe any script to the stdin of `hold-your-shell`.
 * The script will be previewed on the first tab shown: `Script Preview`.
 * Press TAB to cycle through the other tabs, including `Env Vars`.
 * Use the up and down arrow keys (or `j` and `k`) to scroll the text.
 * After reviewing the script and env vars, choose whether or not you
   you want to run the script. Using the left or right arrows, select
   `Yes` or `No`. Press Enter to confirm your selection.

## Examples

```
echo "whoami" | hold-your-shell
```

```
cat <<'EOF' | hold-your-shell
echo "What is your name?"
read NAME
echo "Hello $NAME"
EOF
```

```
curl https://get.docker.com/ | hold-your-shell
```
