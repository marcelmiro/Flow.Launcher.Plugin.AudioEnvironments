import warnings
from comtypes import CLSCTX_ALL, CoCreateInstance
from pycaw.pycaw import AudioUtilities
import plugin.policyconfig as pc

warnings.filterwarnings("ignore")


def list_devices():
    devices = []

    for device in AudioUtilities.GetAllDevices():
        if str(device.state) == "AudioDeviceState.Active":
            devices.append(device)

    return devices


def find_device(devices, name):
    for device in devices:
        if device.FriendlyName == name:
            return device


def set_default_device(device_id, role):
    """
    Switches the audio device to the specified device ID and role.

    Args:
        deviceId (str): The ID of the device to switch the audio to.
        role (ROLE): The role of the audio stream, i.e. 0 for default device and 2 for default communication device.

    Returns:
        None
    """
    policy_config = CoCreateInstance(
        pc.CLSID_PolicyConfigClient,
        pc.IPolicyConfig,
        CLSCTX_ALL
    )
    policy_config.SetDefaultEndpoint(device_id, role)
    # policy_config.Release()
