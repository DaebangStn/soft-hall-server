## How to run

1. Install pybluez
```
cd pybluez
python setup.py install
```

2. bluetooth system service to be compatible
```
# edit /etc/systemd/system/dbus-org.bluez.service
ExecStart=/usr/lib/bluetooth/bluetoothd --compat

sudo systemctl daemon-reload
sudo systemctl restart bluetooth
```

3. Pairing
```
bluetoothctl
discoverable on
pairable on

# pairing with sensor
scan on
pair <sensor mac address>
trust <sensor mac address>
```

4. Add SPP service
```
sudo sdptool add sp
```