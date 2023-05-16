# Flow Launcher Audio Environments plugin

A [Flow Launcher](https://www.flowlauncher.com/) plugin using [Python](https://www.python.org/). It allows the creation and management of multiple audio environments for different use cases.

## How to use

Start by typing `ad` to get the list of commands. You will need to edit the config file (found by typing `ad Settings`) to add your desired audio environments. Your computer's device names can be found by typing `ad List devices`.

## How to install

To install this plugin, download the latest release zip file and extract the contents into a folder inside Flow Launcher's plugin directory. This can be done by searching `Flow Launcher UserData Folder` in the launcher and pressing enter. The plugins are found in the `Plugins` folder.

An example of the plugin path would look like this:

```
C:\Users\Marcel\AppData\Roaming\FlowLauncher\Plugins\Flow.Launcher.Plugin.AudioEnvironments
```

Enabling Audio Environments in Flow Launcher's settings may be required to start using this plugin.

## Development

To use this plugin during development, you need to create a symlink between this directory and Flow Launcher's plugin directory. This can be done by searching `Flow Launcher UserData Folder` in the launcher and pressing enter. The plugins are found in the `Plugins` folder.

You can create a symlink by opening CMD in Windows and typing:

```CMD
mklink /J [flow-launcher-plugin-folder]/[folder-name] [project-root]
```

An example would look like this:

```CMD
mklink /J C:\Users\Marcel\AppData\Roaming\FlowLauncher\Plugins\AudioEnvironments C:\Users\Marcel\code\Flow.Launcher.Plugin.AudioEnvironments
```

After this is set up. You can run:

```CMD
pip install -r ./requirements.txt -t ./lib
```
