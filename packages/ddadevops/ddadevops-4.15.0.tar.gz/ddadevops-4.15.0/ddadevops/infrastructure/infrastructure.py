from subprocess import Popen, PIPE, run, CalledProcessError
from pathlib import Path
from sys import stdout
from os import chmod, environ
from json import load, dumps
import yaml
from pkg_resources import resource_string


class ResourceApi:
    def read_resource(self, path: str) -> bytes:
        return resource_string("ddadevops", path)


class FileApi:
    def __init__(self):
        self.execution_api = ExecutionApi()

    def clean_dir(self, directory: str):
        self.execution_api.execute("rm -rf " + directory)
        self.execution_api.execute("mkdir -p " + directory)

    def cp(self, src: str, target_dir: str, check=True):
        self.execution_api.execute(f"cp {src} {target_dir}", check=check)

    def cp_force(self, src: str, target_dir: str, check=True):
        self.execution_api.execute(f"cp -f {src}* {target_dir}", check=check)

    def cp_recursive(self, src: str, target_dir: str, check=True):
        self.execution_api.execute(f"cp -r {src} {target_dir}", check=check)

    def write_data_to_file(self, path: Path, data: bytes):
        with open(path, "w", encoding="utf-8") as output_file:
            output_file.write(data.decode(stdout.encoding))

    def write_yaml_to_file(self, path: Path, data: map):
        with open(path, "w", encoding="utf-8") as output_file:
            yaml.dump(data, output_file)
        chmod(path, 0o600)

    def write_json_to_file(self, path: Path, data: map):
        with open(path, "w", encoding="utf-8") as output_file:
            output_file.write(dumps(data))
        chmod(path, 0o600)

    def read_json_fro_file(self, path: Path) -> map:
        with open(path, "r", encoding="utf-8") as input_file:
            return load(input_file)


class ImageApi:
    def __init__(self):
        self.execution_api = ExecutionApi()

    def image(self, name: str, path: Path):
        self.execution_api.execute_live(
            f"docker build -t {name} --file {path}/image/Dockerfile {path}/image"
        )

    def drun(self, name: str):
        self.execution_api.execute_live(
            f'docker run -it {name} /bin/bash'
        )

    def dockerhub_login(self, username: str, password: str):
        self.execution_api.execute_secure(
            f"docker login --username {username} --password {password}",
            "docker login --username ***** --password *****",
        )

    def dockerhub_publish(self, name: str, username: str, tag: str):
        self.execution_api.execute_live(f"docker tag {name} {username}/{name}:{tag}")
        self.execution_api.execute_live(f"docker push {username}/{name}:{tag}")

    def test(self, name: str, path: Path):
        self.execution_api.execute_live(
            f"docker build -t {name} -test --file {path}/test/Dockerfile {path}/test"
        )


class ExecutionApi:
    def execute(self, command: str, dry_run=False, shell=True, check=True):
        output = ""
        if dry_run:
            print(command)
        else:
            try:
                output = run(
                    command,
                    shell=shell,
                    check=check,
                    stdout=PIPE,
                    stderr=PIPE,
                    text=True,
                ).stdout
                output = output.rstrip()
            except CalledProcessError as exc:
                print(
                    f"Command failed with code: {exc.returncode} and message: {exc.stderr}"
                )
                raise exc
        return output

    def execute_secure(
        self,
        command: str,
        sanitized_command: str,
        dry_run=False,
        shell=True,
        check=True,
    ):
        try:
            output = self.execute(command, dry_run, shell, check)
            return output
        except CalledProcessError as exc:
            sanitized_exc = exc
            sanitized_exc.cmd = sanitized_command
            raise sanitized_exc

    def execute_live(self, command: str, dry_run=False, shell=True):
        if dry_run:
            print(command)
        else:
            process = Popen(command, shell=shell)
            outs, errs = process.communicate()
            while outs is not None:
                stdout.buffer.write(outs)
            if process.returncode != 0:
                raise RuntimeError(f"Execute live '{command}' failed with code {process.returncode}\nerrs: {errs}")


class EnvironmentApi:
    def get(self, key):
        return environ.get(key)

    def is_defined(self, key):
        return key in environ


class CredentialsApi:
    def __init__(self):
        self.execution_api = ExecutionApi()

    def gopass_field_from_path(self, path, field):
        credential = None
        if path and field:
            print("get field for: " + path + ", " + field)
            credential = self.execution_api.execute(
                ["gopass", "show", path, field], shell=False
            )
        return credential

    def gopass_password_from_path(self, path):
        credential = None
        if path:
            print("get password for: " + path)
            credential = self.execution_api.execute(
                ["gopass", "show", "--password", path], shell=False
            )
        return credential


class GitApi:
    def __init__(self):
        self.execution_api = ExecutionApi()

    # pylint: disable=invalid-name
    def get_latest_n_commits(self, n: int):
        return self.execution_api.execute(f'git log --oneline --format="%s %b" -n {n}')

    def get_latest_commit(self):
        return self.get_latest_n_commits(1)

    def tag_annotated(self, annotation: str, message: str, count: int):
        return self.execution_api.execute(
            f"git tag -a {annotation} -m '{message}' HEAD~{count}"
        )

    def tag_annotated_second_last(self, annotation: str, message: str):
        return self.tag_annotated(annotation, message, 1)

    def get_latest_tag(self):
        return self.execution_api.execute("git describe --tags --abbrev=0")

    def get_current_branch(self):
        return "".join(self.execution_api.execute("git branch --show-current")).rstrip()

    def init(self, default_branch: str = "main"):
        self.execution_api.execute("git init")
        self.execution_api.execute(f"git checkout -b {default_branch}")

    def set_user_config(self, email: str, name: str):
        self.execution_api.execute(f"git config user.email {email}")
        self.execution_api.execute(f"git config user.name {name}")

    def add_file(self, file_path: Path):
        return self.execution_api.execute(f"git add {file_path}")

    def add_remote(self, origin: str, url: str):
        return self.execution_api.execute(f"git remote add {origin} {url}")

    def commit(self, commit_message: str):
        return self.execution_api.execute(f'git commit -m "{commit_message}"')

    def push(self):
        return self.execution_api.execute("git push")

    def push_follow_tags(self):
        return self.execution_api.execute("git push --follow-tags")

    def checkout(self, branch: str):
        return self.execution_api.execute(f"git checkout {branch}")


class TerraformApi:
    pass


class ArtifactDeploymentApi:
    def __init__(self):
        self.execution_api = ExecutionApi()

    def create_forgejo_release(self, api_endpoint_url: str, tag: str, token: str):
        command = (
            f'curl -X "POST" "{api_endpoint_url}" '
            + ' -H "accept: application/json" -H "Content-Type: application/json"'
            + f' -d \'{{ "body": "Provides files for release {tag}", "tag_name": "{tag}"}}\''
        )  # noqa: E501
        print(command + ' -H "Authorization: token xxxx"')
        return self.execution_api.execute_secure(
            command=command + f' -H "Authorization: token {token}"',
            sanitized_command=command + ' -H "Authorization: token xxxx"',
        )

    def add_asset_to_release(
        self,
        api_endpoint_url: str,
        attachment: Path,
        attachment_type: str,
        token: str,
    ):
        command = (
            f'curl -X "POST" "{api_endpoint_url}"'
            + ' -H "accept: application/json"'
            + ' -H "Content-Type: multipart/form-data"'
            + f' -F "attachment=@{attachment};type={attachment_type}"'
        )  # noqa: E501
        print(command + ' -H "Authorization: token xxxx"')
        return self.execution_api.execute_secure(
            command=command + f' -H "Authorization: token {token}"',
            sanitized_command=command + ' -H "Authorization: token xxxx"',
        )

    def calculate_sha256(self, path: Path):
        shasum = f"{path}.sha256"
        self.execution_api.execute(
            f"sha256sum {path} > {shasum}",
        )
        return shasum

    def calculate_sha512(self, path: Path):
        shasum = f"{path}.sha512"
        self.execution_api.execute(
            f"sha512sum {path} > {shasum}",
        )
        return shasum
