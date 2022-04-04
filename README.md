# :pig: porclr

That's right, it's **`porclr`**, the `por`tainer `c`ompose `l`inke`r`! 

Use `porclr` to link or copy Docker Compose files from a Portainer volume to a directory of your choosing. You can then track the latter directory with version control and push it to a remote repo. Never lose the Compose files for your Portainer stacks again!

`porclr` is mainly useful if you defined your stacks _in_ Portainer and don't already have the Compose files under version control.

## Installation
```shell
$ git clone https://github.com/daaf/porclr.git
$ cd porclr
$ python -m pip install -r requirements.txt
```

## Usage
```shell
$ python -m porclr link 127.0.0.1:9000 .
$ python -m porclr copy 127.0.0.1:9000 .
```
