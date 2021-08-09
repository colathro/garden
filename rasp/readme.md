# this is the pi Setup to setup auto-start configs for the pi

this folder is intended to bootstrap your pi and is the only thing needed to be put onto the pi manually.

sftp this folder in and setup the configs targetting your github repo.

run the following to configure the pi with the neccesary dependencies:

sudo apt install git
sudo apt-get install python3-pip

git clone your repo in your install_dir, this should make install_folder.

install dependencies:

pip3 install -r requirements.txt
