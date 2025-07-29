# cancli

A command line interface to send and receive CAN bus messages.

This program is based on:

- [prompt_toolkit](https://python-prompt-toolkit.readthedocs.io/en/stable/) for the user interface
- [confattr](https://erzo.gitlab.io/confattr/latest/) for parsing user input, providing auto completion and config files
- [cantools](https://github.com/cantools/cantools) for decoding and encoding CAN bus messages
- [python-can](https://python-can.readthedocs.io/en/stable/index.html) for receiving and transmitting CAN bus messages


## Usage

Connect to a CAN bus with `bus can0 500k`.
Incoming messages are printed.
If there are too many messages you can hide some or all of them with `hide`.
You can undo `hide` with `show` or display a hidden message once with `next` or `prev`.

When you load a database file with `db path/to/db.dbc` messages are decoded
and the signals are displayed in human readable form.
If the data base file does not repeat the messages for every possible node
you can specify that part of the arbitration id is a node id with `node-id FF << 8`.

You can send messages with `send msg_name sig1=option1 sig2=3.14`.

You can give different incoming messages different colors with `set color.message=%color.message%,importantmessage:ansired`.
The syntax to add values to a dict setting is explained [here](https://erzo.gitlab.io/confattr/latest/intro.html#using-the-values-of-settings-or-environment-variables).
The available colors are displayed in the auto completion.

Available commands:

- `bitrate`:    Set the default bitrate and change the bitrate of all active buses.
- `bus`:        Activate a bus.
- `read`:       Read CAN bus messages from a log file.
- `db`:         Load a database file (dbc/sym/...).
- `node-id`:    Specify that part of an arbitration id is a node id.
- `mask`:       Specify a mask to modify an arbitration ID in case it is not found in the dbc file.
- `send`/`s`:   Send a message on the last activated CAN bus.
- `hide`/`-`:   Do not print received messages of the specified type.
- `show`/`+`:   Undo the effect of a previous hide command.
- `next`/`/`:   Print the next received message of the specified type regardless of
                whether it has been disabled with the hide command.
- `prev`/`?`:   Print the last received message of the specified type.
- `grep`:       Search for signal.
- `set`:        Change the value of a setting.
- `include`:    Load another config file.
- `save`:       Save the settings.
- `echo`:       Display a message.
- `help`:       Display help.
- `quit`/`q`:   Quit the program.


## Installation

```
pipx install cancli
```


### sudo

In order to set bit rates and create virtual CAN buses root privileges are required.
You can configure sudo to not ask for a password in these circumstances.

Create a group called `can`:

```bash
# groupadd can
```

Add the desired user to the group (this requires a reboot to take effect):

```bash
# gpasswd -a <username> can
```

```
# EDITOR=vim visudo
```

```
%can    ALL=(root) NOPASSWD: /bin/ip link set can? up type can bitrate *
%can    ALL=(root) NOPASSWD: /bin/ip link set can? down
%can    ALL=(root) NOPASSWD: /bin/ip link set can? up

%can    ALL=(root) NOPASSWD: /usr/bin/modprobe vcan
%can    ALL=(root) NOPASSWD: /bin/ip link add dev vcan? type vcan
%can    ALL=(root) NOPASSWD: /bin/ip link set up vcan?
```

Note that the last matching rule wins, not the most specific one.
So in order to make sure that these rules are not overridden by other rules add them at the end of the file.


## Links

- [Documentation](https://gitlab.com/erzo/cancli/-/blob/master/README.md)
- [Source code](https://gitlab.com/erzo/cancli)
- [Bug tracker](https://gitlab.com/erzo/cancli/-/issues)
- [Change log](https://gitlab.com/erzo/cancli/-/tags)


## Running the tests

I am using [mypy](https://www.mypy-lang.org/) for static type checking.
[tox](https://tox.wiki/en/latest/) creates a virtual environment and installs all dependencies for you.
You can install tox with [pipx](https://pypa.github.io/pipx/) (`pipx install tox`).

```bash
$ tox
```

In order to make tox work without an internet connection install [devpi](https://devpi.net/docs/devpi/devpi/stable/%2Bd/index.html):

```bash
$ pipx install devpi-server
$ devpi-init
$ devpi-gen-config
$ su
# cp gen-config/devpi.service /etc/systemd/system/
# systemctl start devpi.service
# systemctl enable devpi.service
```

and add the following line to your bashrc:

```bash
export PIP_INDEX_URL=http://localhost:3141/root/pypi/+simple/
```


## License

This work is free. You can use, copy, modify, and/or distribute it
under the terms of the [BSD Zero Clause License](https://gitlab.com/erzo/cancli/-/blob/master/LICENSE).
