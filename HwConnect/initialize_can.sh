sudo ip link set can0 up type can bitrate 250000
echo "CAN 0 @ 250 kb/s"

sudo ip link set can1 up type can bitrate 250000
echo "CAN 1 @ 250 kb/s"

sudo ifconfig can0 txqueuelen 1000

sudo ifconfig can1 txqueuelen 1000

echo "CAN Interface Ready !"