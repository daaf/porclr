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

## Setup
Create a file called `.env` in the root of your local `porclr` repo. Add the following environment variables in the format `KEY=VALUE`:

|Environment variable|Required?|Example value|Description|
|:-------------------|:-------:|:------------|:----------|
|`PORTAINER_URL`|:ballot_box_with_check:|`127.0.0.1:9443`|The URL and port number of the Portainer instance.|
|`LOCAL_REPO`|:ballot_box_with_check:|`/home/myuser/portainer_compose_files`|The absolute path to the directory where the Compose files should be linked or copied.
|`PORTAINER_COMPOSE_DIR`||`/var/lib/docker/volumes/portainer_data/_data/compose`|The location of the Docker volume from which to link/copy the Compose files. Only required if you plan to use the `porclr link` command.|

## Usage
```shell
$ python -m porclr link
$ python -m porclr copy
```
