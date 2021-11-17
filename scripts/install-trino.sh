#!/bin/bash

wget https://repo1.maven.org/maven2/io/trino/trino-server/364/trino-server-364.tar.gz
tar xvzf trino-server-*.tar.gz -C /opt
rm trino-server-*.tar.gz
mv /opt/trino-server-* /opt/trino
mkdir /opt/trino/etc
mkdir /opt/trino/catalog

cat << EOF > /opt/trino/etc/jvm.config
-server
-Xmx4G
-XX:-UseBiasedLocking
-XX:+UseG1GC
-XX:G1HeapRegionSize=32M
-XX:+ExplicitGCInvokesConcurrent
-XX:+HeapDumpOnOutOfMemoryError
-XX:+ExitOnOutOfMemoryError
-XX:ReservedCodeCacheSize=512M
-XX:PerMethodRecompilationCutoff=10000
-XX:PerBytecodeRecompilationCutoff=10000
-Djdk.nio.maxCachedBufferSize=2000000
-Djdk.attach.allowAttachSelf=true
EOF

cat << EOF > /opt/trino/etc/node.properties
node.environment=stock_analyser
EOF

cat << EOF > /opt/trino/etc/config.properties
coordinator=true
node-scheduler.include-coordinator=true
http-server.http.port=8080
query.max-memory=5GB
query.max-memory-per-node=1GB
query.max-total-memory-per-node=2GB
discovery-server.enabled=true
discovery.uri=http://localhost:8080
EOF

cat << EOF > /opt/trino/catalog/stock_data.properties
connector.name=stock_data
connection-url=jdbc:postgresql://0.0.0.0:5432/stock_data
connection-user=postgres
connection-password=postgres
EOF

chmod +x /opt/trino/bin/launcher
echo "Launch trino with: /opt/trino/bin/launcher run"
