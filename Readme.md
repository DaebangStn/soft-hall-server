## How to run

1. Install pybluez
```
cd pybluez
python setup.py install
```

2. Configure hci controller discoverable and pair-able
```
bluetoothctl
list # to get the hci controller MAC address
select <MAC>
discoverable on
pairable on
```

3. Add SPP service
```
sudo sdptool add sp
```