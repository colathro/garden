import yaml
import os
import git
import subprocess

global config_file
config_file = "config.yaml"


def install(name):
    subprocess.call(['pip', 'install', name])


def main():
    with open(config_file) as file:
        config_bag = yaml.load(file, Loader=yaml.FullLoader)

    os.chdir('/')
    if(is_installed(config_bag)):
        update_code(config_bag)
    else:
        install_code(config_bag)
    pip_install(config_bag)
    return 0


def is_installed(config_bag):
    install_path = get_install_directory(config_bag)
    return os.path.exists(install_path)


def get_install_directory(config_bag):
    home = get_home_directory(config_bag)
    folder = config_bag["pi"]["install-folder"]
    return os.path.join(home, folder)


def get_home_directory(config_bag):
    return config_bag["pi"]["install-dir"]


def pip_install(config_bag):
    os.chdir(get_install_directory(config_bag))
    subprocess.call(['pip3', 'install', '-r', 'requirements.txt'])


def update_code(config_bag):
    repo = git.Repo(get_install_directory(config_bag))
    origin = repo.remotes.origin
    origin.pull()


def install_code(config_bag):
    install_directory = get_install_directory(config_bag)
    os.makedirs(install_directory, exist_ok=True)
    repo = git.Git(get_home_directory(config_bag))
    repo.clone(config_bag['github']['repo'])


if __name__ == "__main__":
    main()
