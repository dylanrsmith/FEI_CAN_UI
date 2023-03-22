sudo ifconfig can0 down

sudo ifconfig can1 down

echo down

sudo ip link set can1 up type can bitrate 250000

sudo ip link set can0 up type can bitrate 250000

sudo ifconfig can1 txqueuelen 1000

sudo ifconfig can0 txqueuelen 1000

echo up