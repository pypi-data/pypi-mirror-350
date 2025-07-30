# ECIDA

```
usage: ecidacli [-h] [-f MAIN_FILE] COMMAND ...

options:
  -h, --help            show this help message and exit
  -f MAIN_FILE, --main-file MAIN_FILE
                        main file to process (example: main.py)

  COMMAND
    manifests           generate the kubernetes manifests
    build               build the container and push it to container registry
    version             print ecidacli version
    create              create resources e.g. module and environment
    init                Initialize the codebase
```

```
usage: ecidacli manifests [-h] [-u USERNAME] [-s SECRET] [-d DIR]

options:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        username for container registry authentication
  -s SECRET, --secret SECRET
                        name of secret in the kubernetes-cluster
  -d DIR, --dir DIR     directory to put yaml files [default: manifests]
```

```
usage: ecidacli build [-h] [-u USERNAME]

options:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        username for container registry authentication
```

```
usage: ecidacli create [-h] RESOURCE [name]

options:
  -h, --help  show this help message and exit
  [name]      Name of resource
  RESOURCE
    module    create a module
    env       create a environment
```

```
usage: ecidacli init [-h] NAME

positional arguments:
  NAME        Name of the first module

options:
  -h, --help  show this help message and exit
```