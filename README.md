# server


if 
meson_options.txt:1:0: ERROR: Unknown type feature.

run
```
pip3 install --user meson
```
```
export PATH=~/.local/bin:$PATH
```
======================================install lib:
```
sudo apt install libmicrohttpd-dev libjansson-dev \
        libssl-dev  libsofia-sip-ua-dev libglib2.0-dev \
        libopus-dev libogg-dev libcurl4-openssl-dev liblua5.3-dev \
        libconfig-dev pkg-config gengetopt libtool automake make  
        
```   
======================================install meson ninja-build:
```
sudo apt install meson ninja-build
```
======================================install  libnice:
```
cd ~
git clone https://gitlab.freedesktop.org/libnice/libnice
cd libnice
meson --prefix=/usr --libdir=lib build
ninja -C build
sudo ninja -C build install
```
======================================install  libsrtp:
```
 cd ~
wget https://github.com/cisco/libsrtp/archive/v2.3.0.tar.gz
tar xfv v2.3.0.tar.gz
cd libsrtp-2.3.0
./configure --prefix=/usr --enable-openssl
make shared_library && sudo make install
```
##======================================install  cmake & libwebsockets:
```
sudo apt install cmake
```

```
cd ~
git clone https://libwebsockets.org/repo/libwebsockets
cd libwebsockets
git checkout v3.2-stable
mkdir build
cd build
cmake -DLWS_MAX_SMP=1 -DCMAKE_INSTALL_PREFIX:PATH=/usr -DCMAKE_C_FLAGS="-fpic" ..
make && sudo make install
```
##======================================install  janus-gateway:
```
cd ~
git clone https://github.com/meetecho/janus-gateway.git
cd janus-gateway
./autogen.sh
./configure --prefix=/opt/janus
make
sudo make install
sudo make configs
```
====================================run test:
```
sudo /opt/janus/bin/janus
```
