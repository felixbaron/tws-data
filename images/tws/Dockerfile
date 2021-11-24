FROM azul/zulu-openjdk

# Install packages
RUN apt-get update
RUN apt-get install -y wget zip xvfb x11vnc openjfx

## Run TWS Offline Installer
WORKDIR /home
RUN wget https://download2.interactivebrokers.com/installers/tws/latest-standalone/tws-latest-standalone-linux-x64.sh
RUN chmod u+x ./tws-latest*.sh
RUN echo "\n" | /home/tws-latest-*.sh

## Add TWS launch script
ENV DISPLAY :1
ADD run.sh /home
RUN chmod a+x ./run.sh
#
## Optional: automation
## https://github.com/IbcAlpha/IBC
## https://dimon.ca/how-to-setup-ibc-and-tws-on-headless-ubuntu-in-10-minutes/
#
## Run TWS Offline
EXPOSE 5900
EXPOSE 7496
CMD /home/run.sh