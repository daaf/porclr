# :pig: porclr

That's right, it's **`porclr`**, the `por`tainer `c`ompose `l`inke`r`! 

Use `porclr` to link or copy Docker Compose files from Portainer to a directory of your choosing. You can then track the latter directory with version control and push it to a remote repo. Never lose the Compose files for your Portainer stacks again!

`porclr` is mainly useful if you defined your stacks _in_ Portainer and don't already have the Compose files under version control.

## Installation
```shell
$ git clone https://github.com/daaf/porclr.git
$ cd porclr
$ python -m pip install -r requirements.txt
```

## Setup
Create a file called `.env` in the root of your local `porclr` repo. Add the following environment variables in the format `KEY=VALUE`:

|Environment variable|Required?|Description|
|:-------------------|:-------:|:----------|
|`PORTAINER_URL`|:ballot_box_with_check:|The URL and port number of the Portainer instance.|
|`LOCAL_REPO`||The absolute path to the directory where the Compose files should be linked or copied. Not required if you plan to pass in the path via the command line.
|`PORTAINER_COMPOSE_DIR`||The location of the Docker volume from which to link/copy the Compose files. Only required if you plan to use the `porclr link` command.|

### Example .env file
```
PORTAINER_URL=127.0.0.1:9443
LOCAL_REPO=/home/myuser/portainer_compose_files
PORTAINER_COMPOSE_DIR=/var/lib/docker/volumes/portainer_data/_data/compose
```

## Usage
`porclr` has two modes: `link` and `copy`.
* `link` creates hard links to the Compose files in a local Portainer volume.
* `copy` copies the Compose files from Portainer via the Portainer API.

```shell
# If you've defined `LOCAL_REPO` in your .env file
$ python -m porclr link
$ python -m porclr copy

# If you haven't defined LOCAL_REPO or want to override it
$ python -m porclr link ~/path/to/dir
$ python -m porclr copy ~/path/to/dir
```

### Authentication
Upon running either `porclr link` or `porclr copy`, you'll be prompted to authenticate with your Portainer credentials.

### Location & directory structure
Both modes create a series of subdirectories&mdash;one for each Compose file&mdash;in a directory that you specify. If you've defined a `LOCAL_REPO` environment variable, the path defined there will be used by default. You can override the `LOCAL_REPO` path by passing in a path as an argument to either `porclr link` or `porclr copy`.

If you haven't defined a `LOCAL_REPO` environment variable, you must pass in a path as an argument.
