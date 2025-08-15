#!/bin/bash

URL="https://github.com/openssl/openssl/releases/download/openssl-3.5.2/openssl-3.5.2.tar.gz"
ARCHIVE="openssl-3.5.2.tar.gz"
DIR="openssl-3.5.2"

echo "Extracting"
wget "$URL"
tar -xzf "$ARCHIVE"
cd "$DIR"

echo "Modifying VERSION.dat..."
sed -i '3s/.$/3/' VERSION.dat
TODAY=$(date +%d-%m-%Y)
sed -i "/^RELEASE_DATE=/c\\RELEASE_DATE=\"$TODAY\"" VERSION.dat

echo "Patching"
FILE="include/openssl/ssl.h.in"
sed -i '202,204c\
#  define TLS_DEFAULT_CIPHERSUITES "TLS_AES_128_CCM_SHA256"' "$FILE"
echo "Successfully updated $FILE"

FILE="ssl/ssl_ciph.c"
# Match the line defining TLS_DEFAULT_CIPHERSUITES and replace it and the next two continuation lines
sed -i '2249,2251c\
    return "TLS_AES_128_CCM_SHA256";' "$FILE"
echo "Successfully updated $FILE"

./Configure
make
rm -r openssl-3.5.3/
mv "openssl-3.5.2/" "openssl-3.5.3/"
rm "$ARCHIVE"