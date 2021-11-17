# syntax = docker/dockerfile:1.3-labs
FROM azul/zulu-openjdk
# Run TWS Offline Installer
RUN apt-get update
RUN apt-get install -y wget zip
RUN wget https://download2.interactivebrokers.com/installers/tws/latest-standalone/tws-latest-standalone-linux-x64.sh
RUN chmod u+x tws-latest-*.sh
RUN printf '%s\n' | (./tws-latest-standalone-linux-x64.sh; exit 0)


# Install IBC for automation
RUN wget https://github.com/IbcAlpha/IBC/releases/download/3.11.0/IBCLinux-3.11.0.zip

# https://github.com/roblav96/headless-ib-gateway-installation-ubuntu-server
# https://github.com/IbcAlpha/IBC
# https://github.com/ib-controller/ib-controller
# https://dimon.ca/how-to-setup-ibc-and-tws-on-headless-ubuntu-in-10-minutes/