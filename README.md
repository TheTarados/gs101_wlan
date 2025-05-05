This repo contains everything needed to use the WiFi on a Google Pixel 6 running
linux. It also contains a basic framework to access the cellular modem.

## Prerequesites

First, clone the
[repo from Linaro](https://git.codelinaro.org/linaro/googlelt/pixelscripts)
containing everything you need to boot the mainline kernel on the phone. Follow
the setup to have yocto rootfs on the device. (other distros should work. I just
give the method I used)

Go inside the `src/linux` and checkout to  linux 6.14 (commit e48e99b6edf41c69c5528aa7ffb2daf3c59ee105)
Then use `git apply` to apply kernel_rc.patch. It should apply cleanly. There's
no guarantee for next versions but I will try to maintain it if there is a
demand for it.

To `src/pixelscripts/gs101_config.fragment`, add 
```
CONFIG_PCI_EXYNOS=m
CONFIG_PCI_EXYNOS_CAL_GS101=m
CONFIG_PCIE_EXYNOS_RC=m
```
## Basic cellular modem access
To `src/pixelscripts/gs101_config.fragment`, add 
```
CONFIG_EXYNOS_MODEM_IF=m
CONFIG_SEC_MODEM_S5100=m
CONFIG_SHM_IPC=m
CONFIG_BOOT_DEVICE_SPI=m
CONFIG_CP_PKTPROC=m
CONFIG_CP_PKTPROC_UL=m
CONFIG_LINK_DEVICE_PCIE=m
CONFIG_MODEM_IF_QOS=m
CONFIG_LINK_DEVICE_PCIE_IOCC=y
CONFIG_LINK_DEVICE_PCIE_GPIO_WA=y
CONFIG_CP_WRESET_WA=y
CONFIG_EXYNOS_DIT=m
CONFIG_EXYNOS_DIT_VERSION=0x02010000
CONFIG_CH_EXTENSION=m
CONFIG_CPIF_PAGE_RECYCLING=m
```
Add `python` to `conf/local.conf` in the yocto environment. Build the yocto
rootfs, flash it. Build the linux kernel, flash it. You can then boot the phone.

From this repo,
```
adb push ./firmware /lib/
adb push ./open_SIT /
```
Now connect two times to the device via `adb shell`

In the first, run
```
cd open_SIT
python3 server.py
```
In the second, run
```
cd open_SIT
python3 cbd.py
python3 client_sim.py
```

If everything works correctly, you should see answers from the eSIM.

Note: if you have dhcpcd running, it will hang the phone as soon as cbd.py
finishes. This is probably because it tries to access the non-working net
interfaces. If you added 

## Making WiFi work

Add `iw` to `conf/local.conf` in the yocto environment (not obligatory but will
be useful to test wifi). Build the yocto rootfs, flash it. Build the linux
kernel, flash it. You can then boot the phone. Next, do the following commands,
replacing the paths between parenthesis.
```
git clone https://android.googlesource.com/kernel/google-modules/wlan/bcmdhd/bcm4389 -b android-gs-raviole-mainline
cd bcm4389
git apply (path_to_this_repo)/module_wlan.patch
make -C (path_to_linaro)/out/linux M=$PWD ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- -I ./include
adb push ./bcmdhd4389.ko /
```

From this repo,
```
adb shell mkdir lib/firmware
adb push ./firmware/* /lib/firmware/
```

Everything should now be ready. Do
```
adb shell
modprobe /bcmdhd4389.ko
```

To see if it works, you can do
```
ip link set wlan0 up
iw wlan0 scan
```
A list of available WiFi AP should appear. 

The network interfaces can then be used like any other in linux. I have tested
it in client mode and access point mode, both worked without any issue.

## Context
This is not really clean but works out. The driver for the PCIe root controller
can be really simplified and made to go faster. The ideal would be to create
a version which could be mainlined.

The ideal would be to use brcmfmac to manage the modem. However, the bcm4389 is
not supported at the moment and has some modifications when compared with older
modems. I have tried to make it work, got the firmware to flash and got to read
the console but got stuck on the initialization. I can share my work if somebody
is interested in trying to continuing it.
