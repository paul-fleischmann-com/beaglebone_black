#!/usr/bin/env bash
# Kopiert das laufende SD-Karten-System auf die eMMC.
# Voraussetzung: von SD-Karte gebootet (mmcblk0=SD, mmcblk1=eMMC)
set -euo pipefail

SD=/dev/mmcblk0
EMMC=/dev/mmcblk1

echo "=== BBB eMMC Flasher ==="
echo "SD:   $SD  ($(lsblk -dno SIZE $SD))"
echo "eMMC: $EMMC  ($(lsblk -dno SIZE $EMMC))"
echo ""
read -p "eMMC wird überschrieben. Fortfahren? [j/N] " CONFIRM
[[ "$CONFIRM" == "j" || "$CONFIRM" == "J" ]] || { echo "Abgebrochen."; exit 1; }

# 1. Boot-Partition kopieren (36 MB)
echo ""
echo "▶ Boot-Partition kopieren (${SD}p1 → ${EMMC}p1)..."
sudo dd if=${SD}p1 of=${EMMC}p1 bs=4M status=progress conv=fsync

# 2. Root-Partition formatieren
echo ""
echo "▶ Root-Partition formatieren (${EMMC}p3)..."
sudo mkfs.ext4 -F ${EMMC}p3

# 3. Root per rsync kopieren
echo ""
echo "▶ Root-Dateisystem kopieren (rsync)..."
sudo mkdir -p /mnt/emmc
sudo mount ${EMMC}p3 /mnt/emmc
sudo rsync -aAX \
  --exclude={"/dev/*","/proc/*","/sys/*","/tmp/*","/run/*","/mnt/*","/media/*","/lost+found"} \
  / /mnt/emmc/

# 4. fstab anpassen (mmcblk0 → mmcblk1)
echo ""
echo "▶ fstab anpassen..."
sudo sed -i 's|/dev/mmcblk0|/dev/mmcblk1|g' /mnt/emmc/etc/fstab
echo "   fstab:"
cat /mnt/emmc/etc/fstab

# 5. Aufräumen
sudo umount /mnt/emmc
sudo sync

echo ""
echo "✓ Fertig! SD-Karte entfernen und USB neu anstecken → bootet von eMMC."
sudo shutdown -h now
