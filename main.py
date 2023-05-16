import sys
import os
parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, 'lib'))
sys.path.append(os.path.join(parent_folder_path, 'plugin'))

# autopep8: off
from plugin.audio_environments import AudioEnvironments
# autopep8: on

if __name__ == "__main__":
    AudioEnvironments()
