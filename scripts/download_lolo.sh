#!/bin/bash
set -e

LOLO_VERSION="0.7.3"
LOLO_URL="https://github.com/CitrineInformatics/lolo/releases/download/v${LOLO_VERSION}/lolo-${LOLO_VERSION}.jar"
TARGET_DIR="slamd/libs"

echo "🔽 Downloading Lolo JAR..."
mkdir -p "${TARGET_DIR}"
curl -L "${LOLO_URL}" -o "${TARGET_DIR}/lolo-${LOLO_VERSION}.jar"
echo "✅ Lolo JAR downloaded to ${TARGET_DIR}/lolo-${LOLO_VERSION}.jar"
