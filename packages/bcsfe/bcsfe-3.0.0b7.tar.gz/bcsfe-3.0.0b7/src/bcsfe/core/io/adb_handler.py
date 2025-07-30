from __future__ import annotations
from bcsfe import core
from bcsfe.core import io
from bcsfe.cli import dialog_creator, color


class DeviceIDNotSet(Exception):
    pass


class AdbNotInstalled(Exception):
    pass


class AdbHandler(io.root_handler.RootHandler):
    def __init__(self):
        adb_path = core.Path(
            core.core_data.config.get_str(core.ConfigKey.ADB_PATH)
        )
        if not self.is_adb_installed(adb_path):
            raise AdbNotInstalled("Adb is not in PATH environment variable.")
        self.adb_path = adb_path
        self.start_server()
        self.device_id = None
        self.package_name = None

    @staticmethod
    def display_no_adb_error():
        color.ColoredText.localize(
            "adb_not_installed",
            path=core.core_data.config.get_str(core.ConfigKey.ADB_PATH),
        )

    def is_adb_installed(self, path: core.Path) -> bool:
        return path.run("version").success

    def adb_root_success(self) -> bool:
        return (
            self.root_result.result.strip()
            != "adbd cannot run as root in production builds"
        )

    def start_server(self) -> core.CommandResult:
        return self.adb_path.run("start-server")

    def kill_server(self) -> core.CommandResult:
        return self.adb_path.run("kill-server")

    def root(self) -> core.CommandResult:
        return self.adb_path.run(f"-s {self.get_device()} root")

    def get_connected_devices(self) -> list[str]:
        devices = self.adb_path.run("devices").result.split("\n")
        devices = [device.split("\t")[0] for device in devices[1:-2]]
        return devices

    def set_device(self, device_id: str):
        self.device_id = device_id
        self.root_result = self.root()

    def get_device(self) -> str:
        if self.device_id is None:
            raise DeviceIDNotSet("Device ID is not set")
        return self.device_id

    def get_device_name(self) -> str:
        return self.run_shell("getprop ro.product.model").result.strip()

    def run_shell(self, command: str) -> core.CommandResult:
        return self.adb_path.run(f'-s {self.get_device()} shell "{command}"')

    def run_root_shell(self, command: str) -> core.CommandResult:
        return self.run_shell(f"su -c '{command}'")

    def pull_file(
        self, device_path: core.Path, local_path: core.Path
    ) -> core.CommandResult:
        if not self.adb_root_success():
            result = self.run_root_shell(
                f"cp {device_path.to_str_forwards()} /sdcard/ && chmod o+rw /sdcard/{device_path.basename()}"
            )
            if result.exit_code != 0:
                return result
            device_path = core.Path("/sdcard/").add(device_path.basename())

        result = self.adb_path.run(
            f'-s {self.get_device()} pull "{device_path.to_str_forwards()}" "{local_path}"',
        )
        if not result.success:
            return result
        if not self.adb_root_success():
            result2 = self.run_shell(f"rm /sdcard/{device_path.basename()}")
            if result2.exit_code != 0:
                return result2
        return result

    def push_file(
        self, local_path: core.Path, device_path: core.Path
    ) -> core.CommandResult:
        orignal_device_path = device_path.copy_object()
        if not self.adb_root_success():
            device_path = core.Path("/sdcard/").add(device_path.basename())

        result = self.adb_path.run(
            f'-s {self.get_device()} push "{local_path}" "{device_path.to_str_forwards()}"'
        )
        if not result.success:
            return result
        if not self.adb_root_success():
            result2 = self.run_root_shell(
                f"cp '/sdcard/{device_path.basename()}' '{orignal_device_path.to_str_forwards()}' && chmod o+rw '{orignal_device_path.to_str_forwards()}'"
            )
            result3 = self.run_shell(f"rm '/sdcard/{device_path.basename()}'")
            if result2.exit_code != 0:
                return result2
            if result3.exit_code != 0:
                return result3

        return result

    def stat_file(self, device_path: core.Path) -> core.CommandResult:
        return self.run_shell(f"stat {device_path.to_str_forwards()}")

    def does_file_exist(self, device_path: core.Path) -> bool:
        return self.stat_file(device_path).success

    def get_battlecats_packages(self) -> list[str]:
        cmd = "find /data/data/*/files/SAVE_DATA"
        result = self.run_root_shell(cmd)
        if not result.success:
            return []
        packages: list[str] = []
        for package in result.result.split("\n"):
            parts = package.split("/")
            if len(parts) < 4:
                continue
            packages.append(package.split("/")[3])
        return packages

    def save_battlecats_save(self, local_path: core.Path) -> core.CommandResult:
        result = self.pull_file(self.get_battlecats_save_path(), local_path)
        return result

    def load_battlecats_save(self, local_path: core.Path) -> core.CommandResult:
        return self.push_file(local_path, self.get_battlecats_save_path())

    def close_game(self) -> core.CommandResult:
        return self.run_shell(f"am force-stop {self.get_package_name()}")

    def run_game(self) -> core.CommandResult:
        return self.run_shell(
            f"monkey -p {self.get_package_name()} -c android.intent.category.LAUNCHER 1"
        )

    def select_device(self) -> bool:
        devices = self.get_connected_devices()
        device = dialog_creator.ChoiceInput.from_reduced(
            devices, dialog="select_device", single_choice=True
        ).single_choice()
        if not device:
            color.ColoredText.localize("no_device_error")
            return False

        self.set_device(devices[device - 1])
        return True
