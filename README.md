# :pig: porclr

That's right, it's **`porclr`**, the `por`tainer `c`ompose `l`inke`r`! 

Use `porclr` to link Docker Compose files from a Portainer volume to a directory of your choosing. You can then track the latter directory with version control and push it to a remote repo for access whenever and wherever you need it. Never lose your Portainer stacks' Compose files again!
## Installation
---
```shell
$ git clone https://github.com/daaf/porclr.git
$ cd porclr
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## Usage
---
```shell
$ python porclr -l
```