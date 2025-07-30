#
#deprecated, we recommend to use install_functions_debian.sh instead. We will going to remove install_functions.sh in a future release.
#
function upgradeSystem() {
  {
    apt-get update
    apt-get -qqy upgrade
  } > /dev/null
}

function cleanupDocker() {
  rm -f /root/.ssh/authorized_keys
  rm -f /root/.ssh/authorized_keys2

  apt-get clean
  apt-get -qqy autoremove --purge
  apt-get -qqy autoclean
  rm -rf /var/lib/apt/lists/

  rm -rf /tmp/*

  find /var/cache -type f -exec rm -rf {} \;
  find /var/log/ -name '*.log' -exec rm -f {} \;
}

function cleanupAmi() {
  rm -f /home/ubuntu/.ssh/authorized_keys
  rm -f /home/ubuntu/.ssh/authorized_keys2
  cleanupDocker
}
