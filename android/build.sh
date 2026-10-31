#!/bin/bash
# Compila y firma matebit.apk sin Android Studio ni Gradle (probado en Ubuntu 24.04).
#
# Requisitos:
#   sudo apt install default-jdk-headless aapt apksigner zipalign dalvik-exchange libandroid-23-java
#
# Variables opcionales: ANDROID_JAR, DX, KEYSTORE, KEYSTORE_PASS
set -euo pipefail
cd "$(dirname "$0")"

JAR="${ANDROID_JAR:-/usr/lib/android-sdk/platforms/android-23/android.jar}"
DX="${DX:-/usr/lib/android-sdk/build-tools/debian/dx}"
KS="${KEYSTORE:-matebit.keystore}"
KS_PASS="${KEYSTORE_PASS:-matebit123}"

python3 ../tools/build.py >/dev/null   # deja assets/index.html al día

VC=$(sed -n 's/.*android:versionCode="\([0-9]*\)".*/\1/p' AndroidManifest.xml)
VN=$(sed -n 's/.*android:versionName="\([^"]*\)".*/\1/p' AndroidManifest.xml)

rm -rf out && mkdir -p out/classes out/dex
javac --release 8 -Xlint:-options -cp "$JAR" -d out/classes src/com/matebit/app/MainActivity.java
"$DX" --dex --output=out/dex/classes.dex out/classes
aapt package -f -M AndroidManifest.xml -S res -A assets -I "$JAR" \
  --min-sdk-version 21 --target-sdk-version 34 --version-code "$VC" --version-name "$VN" \
  -F out/app-unsigned.apk out/dex

if [ ! -f "$KS" ]; then
  echo "Creando clave de firma nueva en $KS"
  echo "GUARDA UNA COPIA: sin ella no podrás actualizar encima de una instalación anterior."
  keytool -genkeypair -keystore "$KS" -alias matebit -keyalg RSA -keysize 2048 -validity 10000 \
    -storepass "$KS_PASS" -keypass "$KS_PASS" -dname "CN=MateBit, O=Personal"
fi

zipalign -f -p 4 out/app-unsigned.apk out/app-aligned.apk
apksigner sign --ks "$KS" --ks-key-alias matebit --ks-pass "pass:$KS_PASS" --key-pass "pass:$KS_PASS" \
  --out out/matebit.apk out/app-aligned.apk
zipalign -c -p 4 out/matebit.apk
apksigner verify out/matebit.apk

mkdir -p ../dist && cp out/matebit.apk ../dist/matebit.apk
echo "Listo: dist/matebit.apk (versión $VN, código $VC)"
