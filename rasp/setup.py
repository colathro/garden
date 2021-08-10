import yaml
import os
import git
import subprocess

global config_file
config_file = "config.yaml"


def main():
    with open(config_file) as file:
        config_bag = yaml.load(file, Loader=yaml.FullLoader)

    os.chdir('/')
    if(is_installed(config_bag)):
        update_code(config_bag)
    else:
        install_code(config_bag)
    pip_install(config_bag)
    update_rc_local(config_bag)
    return 0


def is_installed(config_bag):
    install_path = get_install_directory(config_bag)
    return os.path.exists(install_path)


def get_install_directory(config_bag):
    home = get_home_directory(config_bag)
    folder = config_bag["pi"]["install_folder"]
    return os.path.join(home, folder)


def get_home_directory(config_bag):
    return config_bag["pi"]["install_dir"]


def get_target_folder(config_bag):
    return config_bag["target"]["target_folder"]


def get_target_entry(config_bag):
    return config_bag["target"]["target_entry"]


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


def get_new_rc_local(config_bag):
    install_directory = get_install_directory(config_bag)
    return os.path.join(install_directory, 'rasp/rc.local')


def update_rc_local(config_bag):
    os.chdir('/')
    with open('/etc/rc.local', 'w') as rc_local:
        with open(get_new_rc_local(config_bag), 'r') as new_rc_local:
            content = new_rc_local.read()
            content = content.replace('{install_dir}',
                                      get_install_directory(config_bag))
            content = content.replace('{target_folder}',
                                      get_target_folder(config_bag))
            content = content.replace('{target_entry}',
                                      get_target_entry(config_bag))
        rc_local.write(content)


if __name__ == "__main__":
    main()
