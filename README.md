# Smart Home

## Networking setup
#### General Info
- Raspberry Pi will serve as wireless access point for esp32 devices
- Devices will communicate over tcp sockets

#### Access Point
- Install linux-wifi-hotspot on raspberry pi device
- If only one wifi card/adaptor is used then the wifi must be turned off before creating access point
- Command to run hotspot on single adapter no internet: `sudo create_ap --no-virt wlan0 lo <SSID> <Password>`
- Hotspot with 2 wifi devices and set gateway IP: `sudo create_ap --no-virt -g 192.168.12.1 wlan1 wlan0 <SSID> <Password>`
- Gateway IP is important that we know for the client programs to know the server IP when run (Arduino has a method for obtaining gateway after)
- There is a method to create a hidden network but for demo it might not be a great idea

#### Firewall
The firewall must be set on the raspberry pi server to accept connections on the agreed upon port.
- For iptables run: `iptables -A INPUT -p tcp --dport <data-port> -j ACCEPT` where `<data-port>` is the port being used
