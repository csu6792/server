# server
  * raspberry pi 4
  * Ubuntu 20   

gcp e2-micro (2 個 vCPU，1 GB 記憶體),us-west1-b ,30 GB 的標準永久磁碟儲存空間

if 
meson_options.txt:1:0: ERROR: Unknown type feature.

run
```
pip3 install --user meson
```
```
export PATH=~/.local/bin:$PATH
```
# server

```
sudo apt-get update && sudo apt-get upgrade
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
======================================install  cmake & libwebsockets:
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
======================================install  janus-gateway:
```
cd ~
git clone https://github.com/meetecho/janus-gateway.git
cd janus-gateway
git checkout 3cfdf6f
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

====================================install nginx:
```
sudo apt install nginx
cd ~/janus-gateway
sudo cp -a html/* /var/www/html
```
====================================install ssl:
```
sudo apt-get install ssl-cert
sudo make-ssl-cert generate-default-snakeoil
```

====================================set config:
```
sudo nano /etc/nginx/sites-available/default
```

```
server {
        listen 80 default_server;
        listen [::]:80 default_server;
        listen 443 ssl default_server;         # コメントアウト外す
        listen [::]:443 ssl default_server;    # コメントアウト外す
        include snippets/snakeoil.conf;    # コメントアウト外す
        root /var/www/html;
        index index.html index.htm index.nginx-debian.html;
        server_name _;
        location / {
                try_files $uri $uri/ =404;
        }
}
```

reset nginx
```
sudo systemctl restart nginx.service
```

====================================set config:
```
sudo nano /opt/janus/etc/janus/janus.transport.http.jcfg
```

```
general: {
        https = true
        secure_port = 8089
}
certificates: {
        cert_pem = "/etc/ssl/certs/ssl-cert-snakeoil.pem"
        cert_key = "/etc/ssl/private/ssl-cert-snakeoil.key"
}
```

====================================set config:
```
sudo nano /opt/janus/etc/janus/janus.plugin.streaming.jcfg
```

```
h264-sample: {
        type = "rtp"
        id = 10
        description = "H.264 live stream coming from gstreamer"
        audio = false
        video = true
        videoport = 8000
        videopt = 100
        videortpmap = "H264/90000"
        videofmtp = "profile-level-id=42e01f;packetization-mode=1"
        secret = "adminpwd"
}
```

====================================run test:
```
sudo /opt/janus/bin/janus
```

# client

====================================install ffmpeg:
```
sudo apt install ffmpeg
```

```
ffmpeg \
    -f v4l2 -thread_queue_size 8192 -input_format yuyv422 \
    -video_size 1280x720 -framerate 10 -i /dev/video0 \
    -c:v h264_omx -profile:v baseline -b:v 1M -bf 0 \
    -flags:v +global_header -bsf:v "dump_extra=freq=keyframe" \
    -max_delay 0 -an -bufsize 1M -vsync 1 -g 10 \
    -f rtp rtp://127.0.0.1:8000/
```
# set ssl
====================================
```
sudo mkdir /etc/nginx/ssl

sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/ssl/nginx.key -out /etc/nginx/ssl/nginx.crt
```

```
Country Name (2 letter code) [AU]:TW
State or Province Name (full name) [Some-State]:Taiwan
Locality Name (eg, city) []:Taipei
Organization Name (eg, company) [Internet Widgits Pty Ltd]:My Company
Organizational Unit Name (eg, section) []:My Unit
Common Name (e.g. server FQDN or YOUR name) []:myhost.gtwang.org
Email Address []:user@gtwang.org
```

```
server {
  listen 80 default_server;
  listen [::]:80 default_server;

 
  rewrite ^(.*) https://$host$1 permanent;
}
server {
  
  listen 443 ssl default_server;
  listen [::]:443 ssl default_server;

  
  ssl_certificate /etc/nginx/ssl/nginx.crt;
  ssl_certificate_key /etc/nginx/ssl/nginx.key;

  
}
```

```
openssl rsa -in domain.com.key -text > key.pem
openssl x509 -inform PEM -in domain.com.crt > cert.pem
```

# other set
====================================set config:
```
sudo nano /etc/nginx/sites-available/default
```

```
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    listen 443 ssl default_server;
    listen [::]:443 ssl default_server;

    server_name _;

    ssl_certificate     /etc/ssl/certs/ssl-cert-csutest.pem;
    ssl_certificate_key /etc/ssl/private/ssl-cert-csutest.key;

    location /janus {
        proxy_pass http://localhost:8088;
    }

    location / {
        proxy_pass http://localhost:8080;
    }
}
```

reset nginx
```
sudo systemctl restart nginx.service
```

#support audio stream
======
```
ffmpeg \
	-f alsa -ac 1 -i plughw:CARD=StudioTM,DEV=0 \
	-vn \
	-f rtp rtp://127.0.0.1:8001/ \
    -f v4l2 -thread_queue_size 8192 -input_format yuyv422 \
    -video_size 1280x720 -framerate 10 -i /dev/video0 \
    -c:v h264_omx -profile:v baseline -b:v 1M -bf 0 \
    -flags:v +global_header -bsf:v "dump_extra=freq=keyframe" \
    -max_delay 0 -an -bufsize 1M -vsync 1 -g 10 \
    -f rtp rtp://127.0.0.1:8000/
```
```
audio = true
audioport = 8001
audiopt = 111
audiortpmap = "opus/48000/2" 
```

# support webscoket
======
```
location /socket.io {
        include proxy_params;
        proxy_http_version 1.1;
        proxy_buffering off;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_pass http://127.0.0.1:5000/socket.io;
}
```

```
gunicorn --worker-class eventlet -w 2 -b 0.0.0.0:8080 main_server:app --daemon

sudo apt-get install python3-pip
pip3 install eventlet==0.30.2
pip3 install Flask-MQTT
pip3 install flask
pip3 install Flask-SocketIO
```

# mapping

```
sudo nano /opt/janus/etc/janus/janus.jcfg
# nat nat1_1 change #
```
