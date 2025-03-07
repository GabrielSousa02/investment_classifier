# Company Classifier

## How to run this project

This project only uses:
- python -> 3.11
- pandas -> 2.0.1
- python-dateutil -> 2.8.2
- numpy -> 1.26.4
- pyyaml -> 6.0.2
- pytest -> 8.3.5

Therefore, it's possible to use a local `python environment` and, run:

```shell
    python main.py
```

To create the `python environment` you can run:

```shell
    python -m venv ./.venv
```

And then the following, to activate it:

```shell
    source ./.venv/bin/activate
```

Also, feel free to use any other environment manager, e.g.: `pyenv` or any other
that you like.

You can also use `docker compose`, the option for `compose` is to facilitate
the `volume` emulation inside the container, and any dynamic changes, not
having to rebuild the container and copying the files all over again.

To run on Docker:

```shell
    docker compose up
```

The above command will run the script once and save the file on your local
directory, since the entire directory is being emulated inside the `container`.

## How to configure this project

There are three important files:
- config.yaml
- rules.yaml
- .env

The first two are included with functional data in it, since they do not have
any sensitive data.
The `.env` file needs to be created locally, even it the parameters are 
empty.

Please take a brief look at their specific documentation:
- [How to set up the config.yaml file](./docs/how-to-setup-config.md)
- [How to set up the rules.yaml file](./docs/how-to-setup-rules.md)
