function upgradeSystem() {
  apk -U upgrade
}

function cleanupDocker() {
  rm -f /root/.ssh/authorized_keys
  rm -f /root/.ssh/authorized_keys2

  apk cache clean
  
  rm -rf /tmp/*

  find /var/cache -type f -exec rm -rf {} \;
  find /var/log/ -name '*.log' -exec rm -f {} \;
}

function cleanupAmi() {
  rm -f /home/ubuntu/.ssh/authorized_keys
  rm -f /home/ubuntu/.ssh/authorized_keys2
  cleanupDocker
}
