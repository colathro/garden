import yaml
import os

global config_file
config_file = 'config.yaml'

def main():
    with open(config_file) as file:
        config_bag = yaml.load(file, Loader=yaml.FullLoader)
    return 0

def is_installed(config_bag):
    try:
        home = config_bag['pi']['home']
        folder = config_bag['pi']['folder']
        install_path = os.path.join(home, folder)
        exists = os.path.exists(install_path)

        if (exists):
            with open('version.txt', 'r') as file:
                version = file.read()
                return True
        else:
            return False
    except e:
        return


if __name__ == "__main__":
    main()