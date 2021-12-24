#!/usr/bin/env bash

set -e

VERSION="2.4.7-1ubuntu2.20.04.3"
SERVER_PATH="/etc/openvpn/server"
VPN_VARS='
export KEY_COUNTRY="US"
export KEY_PROVINCE="WA"
export KEY_CITY="Seattle"
export KEY_ORG="cssnr"
export KEY_EMAIL="no-reply@cssnr.com"
export KEY_OU="Hosting"
export KEY_CN="cssnr.com"
export KEY_NAME="server"
'
SERVER_CONF='
port 1194
proto udp
dev tun
server 10.8.0.0 255.255.255.0
ifconfig-pool-persist ipp.txt
keepalive 10 120
comp-lzo
persist-key
persist-tun
status openvpn-status.log
verb 3
ca ca.crt
cert server.crt
key server.key
dh dh.pem
push "redirect-gateway def1 bypass-dhcp"
push "route 192.168.10.0 255.255.255.0"
push "route 192.168.20.0 255.255.255.0"
push "dhcp-option DNS 8.8.8.8"
push "dhcp-option DNS 1.1.1.1"
push "dhcp-option DNS 208.67.222.222"
#user nobody
#group nobody
verify-client-cert none
duplicate-cn
plugin /usr/lib/x86_64-linux-gnu/openvpn/plugins/openvpn-plugin-auth-pam.so login
'

sleep 10

while true; do
    ps -C apt-get,apt,dpkg >/dev/null || break
    sleep 5
done

apt-get -y install "openvpn=${VERSION}" easy-rsa firewalld

/usr/sbin/modprobe tun
echo 'net.ipv4.ip_forward=1' >>/etc/sysctl.conf
sysctl -p /etc/sysctl.conf

make-cadir /etc/openvpn/easy-rsa
echo "${VPN_VARS}" >>/etc/openvpn/easy-rsa/vars
cd /etc/openvpn/easy-rsa

./easyrsa --batch init-pki
./easyrsa --batch build-ca nopass
./easyrsa --batch gen-dh
./easyrsa --batch gen-req server nopass
./easyrsa --batch sign-req server server

cp pki/dh.pem pki/ca.crt pki/issued/server.crt pki/private/server.key "${SERVER_PATH}"
echo "${SERVER_CONF}" >"${SERVER_PATH}/server.conf"

systemctl is-active iptables && systemctl stop iptables
systemctl is-enabled iptables && systemctl disable iptables
systemctl -f enable firewalld
systemctl start firewalld

firewall-cmd --zone=trusted --add-interface=tun0
firewall-cmd --permanent --zone=trusted --add-interface=tun0
firewall-cmd --permanent --add-service openvpn
firewall-cmd --permanent --zone=trusted --add-service openvpn
firewall-cmd --reload

firewall-cmd --add-masquerade
firewall-cmd --add-masquerade --permanent
firewall-cmd --query-masquerade
DEVICE=$(ip route | awk '/^default via/ {print $5}')
firewall-cmd --permanent --direct --passthrough ipv4 -t nat -A POSTROUTING -s 10.8.0.0/24 -o "${DEVICE}" -j MASQUERADE
firewall-cmd --reload

systemctl -f enable openvpn-server@server.service
systemctl start openvpn-server@server.service


CA_CERT=$(awk '{printf "%s\\n", $0}' < "${SERVER_PATH}/ca.crt")
IP_ADDR=$(ip -f inet addr show "${DEVICE}" | grep inet | awk '{print $2}' | awk -F'/' '{print $1}')
PASSWORD=$(tr -dc 'A-Za-z0-9' < /dev/urandom | head -c 12)
useradd -p "$(openssl passwd -1 ${PASSWORD})" -s /usr/sbin/nologin openvpn
echo "${PASSWORD}" > /root/openvpn

curl -X POST "https://intranet-proxy.cssnr.com/callback/" \
    -F "ip_address=${IP_ADDR}" \
    -F "password=${PASSWORD}" \
    -F "ca_cert=${CA_CERT}"
