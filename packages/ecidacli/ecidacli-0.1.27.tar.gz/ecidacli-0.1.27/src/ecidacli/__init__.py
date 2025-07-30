import argparse
import importlib.util
import os
import importlib
import subprocess
import sys
import yaml
from . import docker_interface
import pkg_resources
from pathlib import Path
import ast


ast_import_ecida = ast.ImportFrom(
    module="Ecida",
    names=[ast.alias(name="EcidaModule", asname=None, lineno=0, col_offset=0)],
    level=0,
    lineno=0,
    col_offset=0,
    end_lineno=0,
    end_col_offset=0,
)


def is_using_r(py_file_path):
    directory = os.path.dirname(os.path.abspath(py_file_path))
    requirements_path = os.path.join(directory, "requirements.txt")

    if not os.path.isfile(requirements_path):
        raise FileNotFoundError(f"requirements.txt not found in directory: {directory}")

    try:
        with open(requirements_path, "r") as req_file:
            for line in req_file:
                # Remove comments and extra whitespace
                line_clean = line.split("#")[0].strip()
                # Handle lines like "rpy2", "rpy2==3.5", or "rpy2>=3"
                if line_clean.lower().startswith("rpy2"):
                    return True
    except:
        # Propagate any exception that might occur while reading the file
        raise

    return False


def add_resource_command(parent_parser, action, res_short, resource_full, func):
    resource_parser = parent_parser.add_parser(
        res_short, help=f"{action} a {resource_full}"
    )
    resource_parser.add_argument(
        "name", metavar="NAME", help=f"Name of the {resource_full} to {action}"
    )
    resource_parser.set_defaults(func=func)
    return resource_parser


def read_from_templates(filename):
    byte_stream = pkg_resources.resource_string(__name__, f"ecida-templates/{filename}")
    return byte_stream.decode("utf-8")


def write_content_to_file(content, filename):
    output_path = os.path.join(os.getcwd(), filename)
    with open(output_path, "w") as output_file:
        output_file.write(content)


def create_module_py(args):
    module_name = args.name.lower()
    content = read_from_templates("module.py")
    content = content.replace("MODULE_NAME", module_name)
    write_content_to_file(content, f"{module_name}.py")


def create_environment_yaml(args):
    namespace_name = args.name.lower()
    content = read_from_templates("namespace.yaml")
    content = content.replace("NAMESPACE_NAME", namespace_name)
    write_content_to_file(content, f"ecida-env-{namespace_name}.yaml")


def copy_from_templates(filename):
    content = read_from_templates(filename)
    write_content_to_file(content, filename)


def init_codebase(args):
    create_module_py(args)
    copy_from_templates("requirements.txt")
    copy_from_templates(".gitignore")


def create_deploy_docker_image(image_tag: str, main_file: str):
    r_image = is_using_r(main_file)
    base_image = "ecida/python:3.10-slim-bookworm"
    if r_image:
        base_image += "-wr"

    workdir = "/app"

    dockerfile = [
        f"FROM {base_image}",
        f"WORKDIR {workdir}",
        "ENV PYTHONUNBUFFERED=1",
        "COPY requirements.txt .",
        "RUN pip install --no-cache-dir -r requirements.txt",
        "COPY . .",
        f'CMD ["python", "{main_file}"]',
    ]

    with open("Dockerfile", "w") as f:
        f.write("\n".join(dockerfile))

    # fmt: off
    subprocess.check_call([
        "docker", "buildx", "build",
        "--cache-from", f"type=registry,ref={image_tag}",
        "--cache-to", "type=inline",
        "-t", image_tag,
        ".",
        "--push"
    ])
    # fmt: on

    os.remove("Dockerfile")


def apply_yaml(Module, image_tag: str, secret: str, dir_path: str):
    module_name = f"{Module.name}-{Module.version}"
    files = {}

    for key, git in Module.directories.items():
        files[key] = {
            "localPath": key,
        }
        if "source" in git and git["source"] != "":
            git["secret"] = secret
            files[key]["preload"] = {
                "git": {
                    "source": git["source"],
                    "folder": git["folder"],
                    "secret": git["secret"],
                }
            }
    kafka = {}
    if len(Module.topics_envVars) > 0:
        kafka = {
            "server": "KAFKA_BOOTSTRAP_SERVER",
            "securityProtocol": "KAFKA_SECURITY_PROTOCOL",
            "saslMechanism": "KAFKA_SASL_MECHANISM",
            "username": "KAFKA_USERNAME",
            "password": "KAFKA_PASSWORD",
            "topics": Module.topics_envVars,
        }

    data = {
        "apiVersion": "ecida.org/v5alpha1",
        "kind": "Module",
        "metadata": {
            "name": module_name,
            "namespace": "ecida-repository",
            "labels": {"template": "default"},
            "annotations": {
                "description": getattr(Module, "description", "Not Provided")
            },
        },
        "spec": {
            "definitions": {
                "inputs": Module.inputs,
                "outputs": Module.outputs,
                "configs": Module.configs,
            },
            "implementations": {
                "docker": {"image": image_tag},
                "kafka": kafka,
                "file": files,
                "env": {"ECIDA_DEPLOY": "true"},
            },
        },
    }
    yaml_filename = f"auto_generated_{module_name}.yaml"
    path = Path.joinpath(dir_path, yaml_filename)
    with open(path, "w") as f:
        yaml.dump(data, f)
        print(yaml_filename + " is generated")


def create_image_tag(username: str, M) -> str:
    imageName = username + "/" + M.name.lower()
    latest_tag, error = docker_interface.fetch_latest_tag(imageName)
    if error is None:
        imageTag, error = docker_interface.increment_tag(latest_tag)
        if error is not None:
            imageTag = latest_tag + ".1"
    else:
        imageTag = M.version.lower()
    return imageName + ":" + imageTag


def main():
    parser = argparse.ArgumentParser(prog="ecidacli")
    parser.add_argument(
        "-f", "--main-file", help="main file to process (example: main.py)"
    )

    subparsers = parser.add_subparsers(
        required=True, metavar="COMMAND", title=None, dest="command"
    )
    parser_manifests = subparsers.add_parser(
        "manifests", help="generate the kubernetes manifests"
    )
    parser_build = subparsers.add_parser(
        "build", help="build the container and push it to container registry"
    )
    subparsers.add_parser("version", help="print ecidacli version")

    parser_build.add_argument(
        "-u", "--username", help="username for container registry authentication"
    )
    parser_manifests.add_argument(
        "-u", "--username", help="username for container registry authentication"
    )
    parser_manifests.add_argument(
        "-s", "--secret", help="name of secret in the kubernetes-cluster"
    )
    parser_manifests.add_argument(
        "-d",
        "--dir",
        help="directory to put yaml files [default: manifests]",
        default="manifests",
    )

    create_parser = subparsers.add_parser(
        "create", help="create resources e.g. module and environment"
    )
    create_subparsers = create_parser.add_subparsers(
        metavar="RESOURCE", title=None, dest="resource"
    )
    add_resource_command(
        create_subparsers, "create", "module", "module", create_module_py
    )
    add_resource_command(
        create_subparsers, "create", "env", "environment", create_environment_yaml
    )

    parser_init = subparsers.add_parser("init", help="Initialize the codebase")
    parser_init.add_argument("name", metavar="NAME", help="Name of the first module")
    parser_init.set_defaults(func=init_codebase)

    args = parser.parse_args()

    try:
        if args.command == "manifests":
            manifests(args)
        elif args.command == "build":
            build(args)
        elif args.command == "version":
            print("ecidacli version: v0.1.23")
        else:
            args.func(args)

    except subprocess.CalledProcessError as e:
        print(e)
        sys.exit(1)

    except Exception as e:
        print(e)


def load_function(file_path, func_name):
    with open(file_path, "r") as f:
        code = f.read()

    tree = ast.parse(code)

    code1 = """
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
    """
    import_logging = ast.parse(code1)

    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]

    globals_in_module = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    # Check if the value assigned is a plain string (not f-strings or expressions)
                    if isinstance(node.value, ast.Constant):
                        globals_in_module[target.id] = (
                            node.value.s
                        )  # `s` gives the string value

    for func in functions:
        if func.name == func_name:
            # Create a new module with the function definition
            new_code = ast.Module([ast_import_ecida, func], type_ignores=[])
            new_code.body = import_logging.body + new_code.body
            new_module = compile(new_code, file_path, "exec")

            # Create a new module object
            spec = importlib.util.spec_from_loader(func_name, loader=None)
            module = importlib.util.module_from_spec(spec)

            # Execute the new module
            exec(new_module, globals_in_module)
            module.__dict__.update(globals_in_module)
            # Return the function
            return getattr(module, func_name)
    raise ValueError(f"Function '{func_name}' not found in file '{file_path}'")


def manifests(args):
    main_file = args.main_file
    username = args.username
    secret = args.secret
    manifests_dir = args.dir

    func = load_function(main_file, "create_module")
    M = func()
    image_tag = create_image_tag(username, M)

    dir_path = Path(main_file).parent.absolute()
    dir_path = Path.joinpath(dir_path, manifests_dir)
    dir_path.mkdir(exist_ok=True, parents=True)

    apply_yaml(M, image_tag, secret, dir_path)


def build(args):
    main_file = args.main_file
    username = args.username

    func = load_function(main_file, "create_module")
    M = func()
    image_tag = create_image_tag(username, M)

    dirname = os.path.dirname(main_file)
    os.chdir(dirname)
    basefile = os.path.basename(main_file)
    create_deploy_docker_image(image_tag, basefile)
    print(f"{main_file} built successfully")


if __name__ == "__main__":
    main()
