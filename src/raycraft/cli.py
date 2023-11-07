"""Raycraft cli."""
import os
import pathlib
import sys
import time
import traceback
import click
import ray
from ray import serve
import watchfiles
import yaml
from typing import Dict, Tuple
from ray.serve._private.constants import (
    DEFAULT_HTTP_HOST,
    DEFAULT_HTTP_PORT,
    SERVE_NAMESPACE,
)
from ray.autoscaler._private.cli_logger import cli_logger
from ray.dashboard.modules.dashboard_sdk import parse_runtime_env_args
from ray.serve.schema import (
    ServeDeploySchema,
)
from ray._private.pydantic_compat import ValidationError
from ray.serve.config import gRPCOptions
from ray.serve._private import api as _private_api
from ray._private.utils import import_attr

APP_DIR_HELP_STR = (
    "Local directory to look for the IMPORT_PATH (will be inserted into "
    "PYTHONPATH). Defaults to '.', meaning that an object in ./main.py "
    "can be imported as 'main.object'. Not relevant if you're importing "
    "from an installed module."
)
RAY_INIT_ADDRESS_HELP_STR = (
    "Address to use for ray.init(). Can also be specified "
    "using the RAY_ADDRESS environment variable."
)
RAY_DASHBOARD_ADDRESS_HELP_STR = (
    "Address to use to query the Ray dashboard head (defaults to "
    "http://localhost:8265). Can also be specified using the "
    "RAY_DASHBOARD_ADDRESS environment variable."
)


def convert_args_to_dict(args: Tuple[str]) -> Dict[str, str]:
    args_dict = dict()
    for arg in args:
        split = arg.split("=")
        if len(split) != 2:
            raise click.ClickException(
                f"Invalid application argument '{arg}', "
                "must be of the form '<key>=<val>'."
            )

        args_dict[split[0]] = split[1]

    return args_dict

@click.group()
def cli():
    pass

@cli.command(
    short_help="Run RayCraft application(s).",
    help=(
        "Runs an application from the specified import path (e.g., my_script:"
        "app) or application(s) from a YAML config.\n\n"
        "If passing an import path, it must point to a RayCraftAPI instance or "
        "a function that returns one. If a function is used, arguments can be "
        "passed to it in 'key=val' format after the import path, for example:\n\n"
        "serve run my_script:app model_path='/path/to/model.pkl' num_replicas=5\n\n"
        "If passing a YAML config, existing applications with no code changes will not "
        "be updated.\n\n"
        "By default, this will block and stream logs to the console. If you "
        "Ctrl-C the command, it will shut down Serve on the cluster."
    ),
)
@click.argument("config_or_import_path")
@click.argument("arguments", nargs=-1, required=False)
@click.option(
    "--runtime-env",
    type=str,
    default=None,
    required=False,
    help="Path to a local YAML file containing a runtime_env definition. "
    "This will be passed to ray.init() as the default for deployments.",
)
@click.option(
    "--runtime-env-json",
    type=str,
    default=None,
    required=False,
    help="JSON-serialized runtime_env dictionary. This will be passed to "
    "ray.init() as the default for deployments.",
)
@click.option(
    "--working-dir",
    type=str,
    default=None,
    required=False,
    help=(
        "Directory containing files that your application(s) will run in. Can be a "
        "local directory or a remote URI to a .zip file (S3, GS, HTTP). "
        "This overrides the working_dir in --runtime-env if both are "
        "specified. This will be passed to ray.init() as the default for "
        "deployments."
    ),
)
@click.option(
    "--app-dir",
    "-d",
    default=".",
    type=str,
    help=APP_DIR_HELP_STR,
)
@click.option(
    "--address",
    "-a",
    default=os.environ.get("RAY_ADDRESS", None),
    required=False,
    type=str,
    help=RAY_INIT_ADDRESS_HELP_STR,
)
@click.option(
    "--blocking/--non-blocking",
    default=True,
    help=(
        "Whether or not this command should be blocking. If blocking, it "
        "will loop and log status until Ctrl-C'd, then clean up the app."
    ),
)
@click.option(
    "--reload",
    "-r",
    is_flag=True,
    help=(
        "Listens for changes to files in the working directory, --working-dir "
        "or the working_dir in the --runtime-env, and automatically redeploys "
        "the application. This will block until Ctrl-C'd, then clean up the "
        "app."
    ),
)
def run(
    config_or_import_path: str,
    arguments: Tuple[str],
    runtime_env: str,
    runtime_env_json: str,
    working_dir: str,
    app_dir: str,
    address: str,
    blocking: bool,
    reload: bool,
) -> None:
    sys.path.insert(0, app_dir)
    args_dict = convert_args_to_dict(arguments)
    final_runtime_env = parse_runtime_env_args(
        runtime_env=runtime_env,
        runtime_env_json=runtime_env_json,
        working_dir=working_dir,
    )

    if pathlib.Path(config_or_import_path).is_file():
        if len(args_dict) > 0:
            cli_logger.warning(  # type: ignore
                "Application arguments are ignored when running a config file."
            )

        is_config = True
        config_path = config_or_import_path
        cli_logger.print(f"Running config file: '{config_path}'.")

        with open(config_path, "r") as config_file:
            config_dict = yaml.safe_load(config_file)

            try:
                config = ServeDeploySchema.parse_obj(config_dict)

                if "http_options" in config_dict:
                    host = config_dict["http_options"].get("host", DEFAULT_HTTP_HOST)
                else:
                    host = DEFAULT_HTTP_HOST

                if "http_options" in config_dict:
                    port = config_dict["http_options"].get("port", DEFAULT_HTTP_PORT)
                else:
                    port = DEFAULT_HTTP_PORT

            except ValidationError as v2_err:  # type: ignore
                raise v2_err
    else:
        is_config = False
        host = DEFAULT_HTTP_HOST
        port = DEFAULT_HTTP_PORT
        import_path = config_or_import_path
        cli_logger.print(f"Running import path: '{import_path}'.")
        # app = _private_api.call_app_builder_with_args_if_necessary(
        #     import_attr(import_path), args_dict
        # )
        # TODO - better handling of app creation
        raycraft_api = import_attr(import_path, reload_module=True)
        app = raycraft_api()

    # Only initialize ray if it has not happened yet.
    if not ray.is_initialized():
        # Setting the runtime_env here will set defaults for the deployments.
        ray.init(
            address=address, namespace=SERVE_NAMESPACE, runtime_env=final_runtime_env
        )
    elif (
        address is not None
        and address != "auto"
        and address != ray.get_runtime_context().gcs_address
    ):
        # Warning users the address they passed is different from the existing ray
        # instance.
        ray_address = ray.get_runtime_context().gcs_address
        cli_logger.warning(  # type: ignore
            "An address was passed to `serve run` but the imported module also "
            f"connected to Ray at a different address: '{ray_address}'. You do not "
            "need to call `ray.init` in your code when using `serve run`."
        )

    http_options = {"host": host, "port": port, "location": "EveryNode"}
    grpc_options = gRPCOptions()
    # Merge http_options and grpc_options with the ones on ServeDeploySchema. If host
    # and/or port is passed by cli, those continue to take the priority
    if is_config and isinstance(config, ServeDeploySchema):
        config_http_options = config.http_options.dict()
        http_options = {**config_http_options, **http_options}
        grpc_options = gRPCOptions(**config.grpc_options.dict())

    client = _private_api.serve_start(
        http_options=http_options,
        grpc_options=grpc_options,
    )

    try:
        if is_config:
            client.deploy_apps(config)
            cli_logger.success("Submitted deploy config successfully.")
        else:
            serve.run(app, host=host, port=port)
            cli_logger.success("Deployed Serve app successfully.")

        if reload:
            if not blocking:
                raise click.ClickException(
                    "The --non-blocking option conflicts with the --reload option."
                )
            if working_dir:
                watch_dir = working_dir
            else:
                watch_dir = app_dir

            for changes in watchfiles.watch(
                watch_dir,
                rust_timeout=10000,
                yield_on_timeout=True,
            ):
                if changes:
                    cli_logger.info(
                        f"Detected file change in path {watch_dir}. Redeploying app."
                    )
                    # The module needs to be reloaded with `importlib` in order to pick
                    # up any changes.
                    raycraft_api = import_attr(import_path, reload_module=True)
                    app = raycraft_api()

                    # TODO - better handling of app creation
                    # app = _private_api.call_app_builder_with_args_if_necessary(
                    #     , args_dict
                    # )

                    serve.run(app, host=host, port=port)

        if blocking:
            while True:
                # Block, letting Ray print logs to the terminal.
                time.sleep(10)

    except KeyboardInterrupt:
        cli_logger.info("Got KeyboardInterrupt, shutting down...")
        serve.shutdown()
        sys.exit()

    except Exception:
        traceback.print_exc()
        cli_logger.error(  # type: ignore
            "Received unexpected error, see console logs for more details. Shutting "
            "down..."
        )
        serve.shutdown()
        sys.exit()
