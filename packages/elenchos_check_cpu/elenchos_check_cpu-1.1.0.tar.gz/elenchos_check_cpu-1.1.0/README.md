# Élenchos: Check cpu

A Élenchos command for checking CPU usage.

## Installation and Configuration

Install Élenchos if not already installed:

```shell
cd /opt

mkdir elenchos
cd elenchos

python -m venv .venv
. .venv/bin/activate
pip install elenchos

mkdir bin
ln -s ../.venv/bin/elenchos bin/elenchos
```

Install the `check:cpu` plugin:

```shell
cd /opt/elenchos
. .venv/bin/activate

pip install elenchos_check_cpu
./bin/elenchos gather-commands
```

Create a configuration file `/etc/nrpe.d/check_cpu.cfg` for `nrpe`:

```
command[check_cpu]=/opt/elenchos/bin/elenchos check:cpu <arguments>
```

Possible arguments are:

* `-i`, `--interval=INTERVAL` The interval between the two CPU statistics gatherings in seconds. [default: 2.0]
* `-w`, `--warning[=WARNING]` The warning level for CPU user in %.
* `-c`, `--critical[=CRITICAL]` The critical level for CPU user in %.

The warning and critical CPU levels are optional. Hence, one can use this Élenchos command solely for gather statistics.

Finally, restart the `nrpe` daemon:

```shell
systemctl reload nrpe
```

## License

This project is licensed under the terms of the MIT license.
