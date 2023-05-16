import os
import json
import pyperclip
from flox import Flox
from plugin.audio_controller import list_devices, find_device, set_default_device

parent_folder_path = os.path.abspath(os.path.dirname(__file__))
settings_dir = os.path.join(parent_folder_path, '../Settings.json')


def list_environments():
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

    if len(envs) > 0:
        return (envs, None)

    error = {
        "title": "No environments have been found in the config file",
        "subtitle": "Open the config file",
        "method": "open_settings"
    }
    return (None, error)


def get_data():
    (envs, env_error) = list_environments()
    devices = list_devices()

    deviceNames = []
    for device in devices:
        deviceNames.append(device.FriendlyName)

    errors = []
    options = [
        {
            "title": "List devices",
            "subtitle": "Copy list of devices",
            "method": "copy",
            "parameters": ["\n".join(deviceNames)]
        },
        {
            "title": "Settings",
            "subtitle": "Open the config file",
            "method": "open_settings",
        }
    ]

    if not envs and env_error:
        errors.append({**env_error, "score": 100})

    if envs:
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

    return (options, devices, errors)


class AudioEnvironments(Flox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        (self.options, self.devices, self.errors) = get_data()

    def query(self, query):
        query = query.strip().lower()

        for error in self.errors:
            self.add_item(**error)

        # Filter options
        for option in self.options:
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

    def copy(self, text):
        pyperclip.copy(text)


if __name__ == "__main__":
    AudioEnvironments()
