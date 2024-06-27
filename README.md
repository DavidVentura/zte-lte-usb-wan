
# ZTE Control

I bought an [ZTE MF79U](https://support.ztedevices.com/en-gl/select-product/mf79u/) as a backup link for my homelab, but it decides to turn its WAN link off periodically.

With this script, you can check whether the WAN connection is up or down, and set it up. Requires `requests` to be available.


Usage:

```python
import os
m = Modem('192.168.0.1')
m.login(os.environ['ZTE_PASSWORD'])
if not m.is_wan_up():
    print("ugh, wan down")
    m.set_wan_up()
```
