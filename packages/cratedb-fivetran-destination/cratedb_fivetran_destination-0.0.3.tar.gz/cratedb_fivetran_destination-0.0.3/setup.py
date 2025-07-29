# Python package with custom build steps.
# https://github.com/pypa/setuptools/discussions/3762
import subprocess
import urllib.request
from pathlib import Path

from setuptools import Command, setup
from setuptools.command.build import build


class FivetranSdk(Command):
    """
    ## About

    Fivetran SDK uses gRPC to talk to partner code. The partner side of the interface is
    always the server side. Fivetran implements the client side and initiates the requests.

    Python SDK API code needs to be produced from protobuf schema files.

    ## Proto files

    Partners should not add the proto files to their repos. Proto files should be pulled
    in from this repo at build time and added to .gitignore so they are excluded.

    Always use proto files from latest release and update your code if necessary. Older
    releases proto files can be considered deprecated and will be expired at later date.

    -- https://github.com/fivetran/fivetran_sdk/blob/main/development-guide.md#proto-files
    """

    def initialize_options(self) -> None:
        # Version pinning by Git reference.
        self.fivetran_sdk_tag = "b9492119b"

        # Where the Python SDK API files will be generated.
        self.output_path = Path("src/fivetran_sdk")

        # Where the protobuf schema files are stored.
        self.protos_path = Path("protos")
        self.protos_path.mkdir(parents=True, exist_ok=True)

        # Which protobuf schema files to acquire.
        self.proto_urls = [
            f"https://raw.githubusercontent.com/fivetran/fivetran_sdk/{self.fivetran_sdk_tag}/common.proto",
            f"https://raw.githubusercontent.com/fivetran/fivetran_sdk/{self.fivetran_sdk_tag}/connector_sdk.proto",
            f"https://raw.githubusercontent.com/fivetran/fivetran_sdk/{self.fivetran_sdk_tag}/destination_sdk.proto",
        ]

    def finalize_options(self) -> None:
        # Currently not used.
        self.pkg_name = self.distribution.get_name().replace("-", "_")

    def get_source_files(self) -> "list[str]":
        if self.protos_path.is_dir():
            return [str(path) for path in self.protos_path.glob("*.proto")]
        return []

    def download(self):
        for url in self.proto_urls:
            urllib.request.urlretrieve(url, self.protos_path / Path(url).name)  # noqa: S310

    def run(self) -> None:
        """
        Invoke gRPC generator.
        """
        if not (
            "editable_wheel" in self.distribution.commands
            or "bdist_wheel" in self.distribution.commands
        ):
            return
        self.download()
        protoc_call = [
            "python3",
            "-m",
            "grpc_tools.protoc",
            f"--proto_path={self.protos_path}",
            f"--python_out={self.output_path}",
            f"--pyi_out={self.output_path}",
            f"--grpc_python_out={self.output_path}",
            *self.get_source_files(),
        ]
        subprocess.check_call(protoc_call)  # noqa: S603

        # Generated files need special treatment.
        self.patch_files()

    def patch_files(self):
        """
        Generated files need special treatment, because the import statements are not right.

        TODO: Why does `grpc_tools.protoc` generate code like this?
        """
        for patch_file in [
            f"{self.output_path}/destination_sdk_pb2.py",
            f"{self.output_path}/destination_sdk_pb2_grpc.py",
        ]:
            payload = Path(patch_file).read_text()
            payload = payload.replace(
                "import common_pb2 as common__pb2", "from . import common_pb2 as common__pb2"
            )
            payload = payload.replace(
                "import destination_sdk_pb2 as destination__sdk__pb2",
                "from . import destination_sdk_pb2 as destination__sdk__pb2",
            )
            Path(patch_file).write_text(payload)


class CustomBuild(build):
    sub_commands = [("build_custom", None)] + build.sub_commands


setup(cmdclass={"build": CustomBuild, "build_custom": FivetranSdk})
