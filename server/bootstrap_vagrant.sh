#!/usr/bin/env bash

VAGRANT_DIR=/vagrant
PROJECT_NAME=obshtestvobg
DB_NAME=$PROJECT_NAME

sudo apt-get update -y

# usability (can be omitted)
sudo apt-get update -y
touch $HOME/.hushlogin
sudo apt-get install expect curl zsh fortune cowsay htop git build-essential -y
wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh
sudo mkdir -p $HOME/.oh-my-zsh/custom/plugins
git clone git://github.com/zsh-users/zsh-syntax-highlighting.git  $HOME/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting
sudo chsh -s `which zsh` vagrant
sed -i 's/^plugins=(.*/plugins=(git django python pip virtualenvwrapper emoji-clock zsh-syntax-highlighting bower)/' $HOME/.zshrc
echo "export LC_ALL=en_US.UTF-8" >> $HOME/.zshrc
echo "export LANG=en_US.UTF-8" >> $HOME/.zshrc


# settings
if [ -f "$VAGRANT_DIR/server/settings_app.py" ]; then
    rm $VAGRANT_DIR/server/.env.vagrant
fi
cp $VAGRANT_DIR/server/.env.sample $VAGRANT_DIR/server/.env.vagrant

# nodejs
wget -qO- https://raw.github.com/creationix/nvm/v0.4.0/install.sh | sh
source $HOME/.nvm/nvm.sh
nvm install 0.10
nvm alias default 0.10

# bower as frontned package manager
npm install bower -g

# ruby
git clone https://github.com/sstephenson/rbenv.git ~/.rbenv
echo 'export PATH="$HOME/.rbenv/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(rbenv init -)"' >> ~/.zshrc
source $HOME/.zshrc
git clone https://github.com/sstephenson/ruby-build.git ~/.rbenv/plugins/ruby-build
rbenv install 2.1.1
rbenv global 2.1.1

# sass as CSS precompiler
gem install compass --pre
source $HOME/.zshrc

# asset compiler packages
sudo apt-get install libxml2-dev libxslt-dev -y

# database
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password password'
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password password'
sudo apt-get install mysql-server -y
mysql -uroot -ppassword -e "SET PASSWORD = PASSWORD('');"
sed -i 's/^DATABASE_USER=.*/DATABASE_USER=root/' $VAGRANT_DIR/server/.env.vagrant
sed -i 's/^DATABASE_PASS=.*/DATABASE_PASS=/' $VAGRANT_DIR/server/.env.vagrant
mysql -uroot -e "CREATE DATABASE \`$DB_NAME\` CHARACTER SET utf8 COLLATE utf8_general_ci;"
sudo apt-get install python-dev libmysqlclient-dev -y

# django project specific
sudo apt-get install python-pip -y
sudo pip install virtualenvwrapper
source virtualenvwrapper.sh
(cd $VAGRANT_DIR && mkvirtualenv $PROJECT_NAME --no-site-packages)
workon $PROJECT_NAME
pip install -r $VAGRANT_DIR/requirements.dev.txt

# django database init
export PROJECT_ENV_FILE="server/.env.vagrant"
python $VAGRANT_DIR/manage.py syncdb --noinput
python $VAGRANT_DIR/manage.py migrate
expect -c "spawn python $VAGRANT_DIR/manage.py createsuperuser --username=admin --email=" -c "expect \"Password:\"" -c "send \"admin\n\"" -c "expect \"Password (again):\"" -c "send \"admin\n\"" -c "expect eof"


# servers
sudo apt-get install nginx-full uwsgi uwsgi-plugin-python -y
sudo usermod -a -G vagrant www-data
sudo ln -s $VAGRANT_DIR/server/settings_nginx.vagrant.conf /etc/nginx/sites-enabled/vagrant.conf
sudo ln -s $VAGRANT_DIR/server/settings_uwsgi.vagrant.ini /etc/uwsgi/apps-enabled/vagrant.ini
sudo rm /etc/nginx/sites-available/default
sudo service nginx restart
sudo service uwsgi restart
echo "start on vagrant-mounted

script
  service nginx restart
  service uwsgi restart
  (cd $VAGRANT_DIR && source virtualenvwrapper.sh && workon $PROJECT_NAME && pip install -r requirements.dev.txt)
end script" | sudo tee /etc/init/vagrant-fix.conf

# bower
(cd $VAGRANT_DIR/web && bower install)