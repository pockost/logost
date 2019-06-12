#!/usr/bin/env bash

# A best practices Bash script template with many useful functions. This file
# sources in the bulk of the functions from the source.sh file which it expects
# to be in the same directory. Only those functions which are likely to need
# modification are present in this file. This is a great combination if you're
# writing several scripts! By pulling in the common functions you'll minimise
# code duplication, as well as ease any potential updates to shared functions.

# A better class of script...
set -o errexit          # Exit on most errors (see the manual)
set -o errtrace         # Make sure any error trap is inherited
set -o nounset          # Disallow expansion of unset variables
set -o pipefail         # Use last non-zero exit code in a pipeline
#set -o xtrace          # Trace the execution of the script (debug)

# DESC: Usage help
# ARGS: None
# OUTS: None
function script_usage() {
    cat << EOF
Usage:
     -h|--help                  Displays this help
     -v|--verbose               Displays verbose output
    -nc|--no-colour             Disables colour output
    -y|--yes                    Automatic yes to prompts
EOF
}


# DESC: Parameter parser
# ARGS: $@ (optional): Arguments provided to the script
# OUTS: Variables indicating command-line parameters and options
function parse_params() {
    local param
    APT_YES_OPTION=""
    while [[ $# -gt 0 ]]; do
        param="$1"
        shift
        case $param in
            -h|--help)
                script_usage
                exit 0
                ;;
            -v|--verbose)
                verbose=true
                ;;
            -nc|--no-colour)
                no_colour=true
                ;;
            -y|--yes)
                cron=true
                assume_yes=true
                APT_YES_OPTION="-y"
                ;;
            *)
                script_exit "Invalid parameter was provided: $param" 2
                ;;
        esac
    done

}

function welcome() {
  pretty_print "Welcome to logost installer provided by POCKOST SAS"
  pretty_print ""
  pretty_print "This script will"
  pretty_print ""
  pretty_print " - Install docker engine"
  pretty_print " - Install docker-compose"
  pretty_print " - Install git"
  pretty_print " - Install and configure logost"
  pretty_print ""

  pretty_print "Are you sure ? [N/y]" $fg_blue true
  if [[ -z ${assume_yes-} ]]; then
    read PROCEED
  else
    PROCEED=yes
  fi
  case ${PROCEED:-"n"} in
    [Yy]* ) echo "Starting installation" ;;
    [Nn]* ) script_exit "Exiting..." 1 ;;
  esac

  pretty_print "Check we are root or sudo is installed"
  check_superuser || script_exit "Please install sudo or run as root"

}

function install_docker() {
  verbose_print "Check OS Distro is Debian"

  OS_DISTRO=$( awk '{ print $1 }' /etc/issue )

  echo
  if [ "${OS_DISTRO}" != "Debian" ] ; then
    pretty_print "This script only work on debian" $fg_red
    script_exit "Exiting ..." 2
  fi

  verbose_print "Start installing docker"
  pretty_print "Start docker installation"

  verbose_print "Update APT source"
  run_as_root apt-get update

  verbose_print "Install prerequisite"
  run_as_root apt-get install ${APT_YES_OPTION} apt-transport-https ca-certificates curl gnupg2 software-properties-common

  verbose_print "Add docker apt PGP key"
  run_as_root bash -c 'curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -'

  verbose_print "Add docker apt repository"
  run_as_root add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"

  verbose_print "Update APT source"
  run_as_root apt-get update

  verbose_print "Install docker"
  run_as_root apt-get install ${APT_YES_OPTION} docker-ce docker-ce-cli containerd.io

  verbose_print "Add current user in docker group"
  run_as_root adduser -quiet $USER docker

  pretty_print "Docker installation completed" $fg_magenta

  pretty_print "Start docker-compose installation"

  verbose_print "Download docker-compose script"
  run_as_root curl -L "https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

  verbose_print "Chmod docker compose"
  run_as_root chmod +x /usr/local/bin/docker-compose

  pretty_print "docker-compose installation completed" $fg_magenta
}


function install_git() {
  pretty_print "Start git installation"

  verbose_print "Update APT source"
  run_as_root apt-get update

  verbose_print "Install prerequisite"
  run_as_root apt-get install ${APT_YES_OPTION} git

  pretty_print "git installation completed" $fg_magenta
}

function install_logost() {
  pretty_print "Start git installation"

	verbose_print "Create project directory"
  if [ -e $HOME/docker/logost ]
  then
    pretty_print "Logost project already exist, update ? [N/y]" $fg_blue true
    if [[ -z ${assume_yes-} ]]; then
      read UPDATE
    else
      UPDATE=yes
    fi
    case ${UPDATE:-"n"} in
      [Yy]* ) UPDATE=yes ; echo "Starting installation" ;;
      * ) UPDATE=no ;;
    esac
  else
    git clone https://github.com/pockost/logost.git $HOME/project/logost
  fi

  pushd $HOME/project/logost

  if [ "$UPDATE" == "yes" ] ; then
    pretty_print "Update logost"
    git pull origin master
  fi

  pretty_print "Download docker image"
  docker-compose -f local.yml pull

  if [ "$UPDATE" == "yes" ] ; then
    pretty_print "Rebuild image"
  docker-compose -f local.yml build
  fi
  pretty_print "Start logost..."
  docker-compose -f local.yml up -d

  pretty_print "Wait for logost to start..."
  sleep 20

  pretty_print "logost installation completed" $fg_magenta
}

function display_info() {
  pretty_print "Connection information are :"
  pretty_print ""
  GUESS_IP=$( ip a s |grep inet|grep -v inet6|grep -v 172.1|grep -v 127.0.0.1|grep -v '10.0.2.15'|awk '{ print $2 }'|cut -d'/' -f1)
  pretty_print "External IP(s) : $IP" $fg_blue
  pretty_print "Web access : http://${IP}:3000/" $fg_blue

}

# DESC: Main control flow
# ARGS: $@ (optional): Arguments provided to the script
# OUTS: None
function main() {
    # shellcheck source=source.sh
    source "$(dirname "${BASH_SOURCE[0]}")/source.sh"

    trap script_trap_err ERR
    trap script_trap_exit EXIT

    script_init "$@"
    parse_params "$@"
    cron_init
    colour_init
    lock_init system

    welcome
    install_docker
    install_git
    install_logost
    display_info
}


# Make it rain
main "$@"

# vim: syntax=sh cc=80 tw=79 ts=4 sw=4 sts=4 et sr
