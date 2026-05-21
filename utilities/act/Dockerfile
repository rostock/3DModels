# Warm act image: catthehacker/ubuntu + Blender 4.2 LTS + X11 deps preinstalled.
# Cuts ~1h off each `act` run by avoiding the per-run Blender download.
#
# Prerequisite: download the Blender tarball into this directory first:
#   curl --retry 5 --retry-delay 30 --retry-max-time 7200 -fL \
#     "https://download.blender.org/release/Blender4.2/blender-4.2.9-linux-x64.tar.xz" \
#     -o utilities/act/blender-4.2.9-linux-x64.tar.xz
#
# Build:
#   docker build \
#     --build-arg HTTP_PROXY=$HTTP_PROXY \
#     --build-arg HTTPS_PROXY=$HTTPS_PROXY \
#     --build-arg NO_PROXY=$NO_PROXY \
#     -t act-blender:4.2.9 -f utilities/act/Dockerfile utilities/act
#
# Then run act with `-P ubuntu-latest=act-blender:4.2.9 --pull=false`.
# The workflow's "Install Blender" + "install gitpython for Blender" steps detect
# the preinstalled tools and skip the download.

FROM catthehacker/ubuntu:act-latest

ARG BLENDER_VERSION=4.2.9
ARG BLENDER_MAJOR=4.2

RUN apt-get update -qq \
 && apt-get install -y -qq \
      libxxf86vm1 libxfixes3 libxi6 libxkbcommon0 libxrender1 \
      libgl1 libxrandr2 libxcursor1 libxinerama1 libsm6 \
 && rm -rf /var/lib/apt/lists/*

COPY blender-${BLENDER_VERSION}-linux-x64.tar.xz /tmp/blender.tar.xz

RUN mkdir -p /opt/blender \
 && tar -xf /tmp/blender.tar.xz -C /opt/blender --strip-components=1 \
 && rm /tmp/blender.tar.xz \
 && ln -sf /opt/blender/blender /usr/local/bin/blender \
 && blender --version

RUN BLENDER_PY=$(ls /opt/blender/${BLENDER_MAJOR}/python/bin/python3.*[0-9]) \
 && "$BLENDER_PY" -m ensurepip --upgrade \
 && "$BLENDER_PY" -m pip install gitpython
