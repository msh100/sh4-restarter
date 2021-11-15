# Superhub 4 Restarter

This utility is designed to reboot the Superhub 4
[when it enters a bad state](https://github.com/msh100/modem-stats/issues/2),
using a TP-Link Smart Plug.


## Supported Smart Plugs

This utility depends on
[python-kasa](https://github.com/python-kasa/python-kasa) and therefore
supports all of the smart plugs that are supported there.

 * HS100
 * HS103
 * HS105
 * HS107
 * HS110
 * [KP105](https://amzn.to/30o6vW8)
 * KP115
 * KP401


## Usage

Firstly, it's important to remember that this utility will hard reboot the
Superhub 4 at the wall.
Because of this, this utility is only designed to work in Modem Mode, where the
network is still functional (without internet) during the whole process.

We address the Smart Plug directly.
Therefore it's important that its IP address is statically defined on your DHCP
server.


### Configuration

Variable     | Description
-------------|-------------
`PLUG_IP`    | The IP address of the Kasa Smart Plug
`START_HOUR` | The start of the timeframe this script is allowed to reboot.
`END_HOUR`   | The end of the timeframe this script is allowed to reboot.


### Docker

```yaml
version: "2.1"
services:
  sh4-restarter:
    image: msh100/sh4-restarter
    restart: unless-stopped
    environment:
        PLUG_IP: 192.168.1.102
        START_HOUR: 2
        END_HOUR: 7
```
