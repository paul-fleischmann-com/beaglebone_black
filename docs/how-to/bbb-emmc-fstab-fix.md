# BBB eMMC fstab-Fix (nach fehlgeschlagenem rsync-Flash)

Wenn der BBB nach manuellem `rsync`-Flash in eine Boot-Loop gerät,
weil die eMMC-fstab leer ist oder noch `mmcblk0`-Pfade enthält.

## Schritt 1 — fstab reparieren

```bash
sudo mount /dev/mmcblk1p3 /mnt
sudo tee /mnt/etc/fstab << 'EOF'
/dev/mmcblk1p3  /               ext4  noatime,errors=remount-ro  0  1
/dev/mmcblk1p1  /boot/firmware  vfat  user,uid=1000,gid=1000,defaults  0  2
/dev/mmcblk1p2  none            swap  sw  0  0
debugfs  /sys/kernel/debug  debugfs  mode=755,uid=root,gid=gpio,defaults  0  0
EOF
cat /mnt/etc/fstab
sudo umount /mnt
```

## Schritt 2 — Boot-Partition kopieren (Kernel + Bootloader)

```bash
sudo dd if=/dev/mmcblk0p1 of=/dev/mmcblk1p1 bs=4M status=progress
sudo sync
sudo shutdown -h now
# SD-Karte entfernen, USB neu anstecken → bootet von eMMC
```

> **Hinweis:** Empfohlene Methode zum eMMC-Flashen ist `sudo beagle-flasher`
> (siehe `bbb-neu-aufsetzen.md`). Dieser Fix greift nur wenn beagle-flasher
> nicht verfügbar ist und ein rsync-basiertes Flash schiefgelaufen ist.
