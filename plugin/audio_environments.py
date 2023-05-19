import os
import json
import pyperclip
from flox import Flox
from functools import cached_property
from plugin.audio_controller import list_devices, find_device, set_default_device

parent_folder_path = os.path.abspath(os.path.dirname(__file__))
settings_dir = os.path.join(parent_folder_path, '../Settings.json')


class AudioEnvironments(Flox):
    @cached_property
    def devices(self):
        return list_devices()

    @cached_property
    def options(self):
        envs = []

        try:
            with open(settings_dir, "r") as file:
                data = json.load(file)

                # Validate data
                data_envs = data.get("environments")
                if type(data_envs) is list:
                    for env in data_envs:
                        if type(env) is dict:
                            envs.append(env)
        except FileNotFoundError:
            # Create file if not found
            with open(settings_dir, "w") as file:
                json.dump({"environments": []}, file)

        errors = []
        options = [
            {
                "title": "List devices",
                "subtitle": "Copy list of devices",
                "method": "copy_devices"
            },
            {
                "title": "Settings",
                "subtitle": "Open the config file",
                "method": "open_settings",
            }
        ]

        if len(envs) == 0:
            errors.append({
                "title": "No environments have been found in the config file",
                "subtitle": "Open the config file",
                "method": "open_settings"
            })

        for env in envs:
            options.append(
                {
                    "title": env.get("title"),
                    "subtitle": "Execute this audio environment",
                    "method": "switch_env",
                    "parameters": [env.get("output"), env.get(
                        "input"), env.get("communication")]
                }
            )

        return (errors, options)

    def query(self, query):
        query = query.strip().lower()
        (errors, options) = self.options

        for error in errors:
            self.add_item(**error, score=100)

        # Filter options
        for option in options:
            if not query or query in option.get("title").lower():
                self.add_item(**option)

    def switch_env(self, output, input, communication):
        if output:
            self.switch_device(output, 0)
        if input:
            self.switch_device(input, 0)
            self.switch_device(input, 2)
        if communication:
            self.switch_device(communication, 2)
        else:  # Use output device as communication device if not specified
            self.switch_device(output, 2)

    def switch_device(self, name, role):
        try:
            device = find_device(self.devices, name)
            if device:
                set_default_device(device.id, role)
        except:
            pass

    def open_settings(self):
        os.startfile(settings_dir)

    def copy_devices(self):
        deviceNames = []
        for device in self.devices:
            deviceNames.append(device.FriendlyName)
        pyperclip.copy("\n".join(deviceNames))


if __name__ == "__main__":
    AudioEnvironments()
