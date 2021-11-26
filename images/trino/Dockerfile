FROM azul/zulu-openjdk:17

# Presto version will be passed in at build time
ARG TRINO_VERSION

# Set the URL to download
ARG TRINO_BIN=https://repo1.maven.org/maven2/io/trino/trino-server/${TRINO_VERSION}/trino-server-${TRINO_VERSION}.tar.gz

# Update the base image OS and install wget and python
RUN apt-get update
RUN apt-get install -y wget python

# Download Presto and unpack it to /opt/trino
RUN wget --quiet ${TRINO_BIN}
RUN mkdir -p /opt
RUN tar -xf trino-server-${TRINO_VERSION}.tar.gz -C /opt
RUN rm trino-server-${TRINO_VERSION}.tar.gz
RUN ln -s /opt/trino-server-${TRINO_VERSION} /opt/trino

# Copy configuration files on the host into the image
ADD etc /opt/trino-server-${TRINO_VERSION}/etc

## Download the Presto CLI and put it in the image
RUN wget --quiet https://repo1.maven.org/maven2/io/trino/trino-cli/${TRINO_VERSION}/trino-cli-${TRINO_VERSION}-executable.jar
RUN mv trino-cli-*.jar /usr/local/bin/trino
RUN chmod +x /usr/local/bin/trino

## Specify the entrypoint to start
ENTRYPOINT /opt/trino/bin/launcher run