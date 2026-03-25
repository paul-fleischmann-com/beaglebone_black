Deploy the built binaries and shared libraries to the BeagleBone Black and restart the service.

First verify the binaries exist:
```bash
ls -lh bin/embedded project/go-api/libs/libhardware.so project/go-api/libs/libhardware_rs.so
```

If they are missing, run `make all` first before deploying.

Then deploy:
```bash
make deploy
```

This copies `bin/embedded`, `libhardware.so`, and `libhardware_rs.so` to `debian@192.168.7.2:/app/` and restarts the `embedded-sw` systemd service.

After deploying, verify the service is running:
```bash
ssh debian@192.168.7.2 "systemctl status embedded-sw"
```
