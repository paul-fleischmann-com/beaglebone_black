package e2edemo

import (
	"encoding/binary"
	"fmt"
	"net"
	"time"

	"golang.org/x/sys/unix"
)

// canFrameSize is sizeof(struct can_frame) from linux/can.h: 4 Byte can_id +
// 1 Byte can_dlc + 3 Byte Padding + 8 Byte Daten.
const canFrameSize = 16

// Conn is a raw SocketCAN (AF_CAN/SOCK_RAW/CAN_RAW) connection bound to a
// single CAN interface (real, vcan or vxcan — SocketCAN treats them
// identically). This talks to the Linux CAN networking stack, not to any
// hardware register directly — actual sensor hardware access stays entirely
// inside the existing HAL (pkg/hal), never here (see Hardware-Regel).
type Conn struct {
	fd int
}

// Open binds a CAN_RAW socket to the named interface (e.g. "vxcan0").
func Open(ifaceName string) (*Conn, error) {
	iface, err := net.InterfaceByName(ifaceName)
	if err != nil {
		return nil, fmt.Errorf("CAN-Interface %q nicht gefunden: %w", ifaceName, err)
	}

	fd, err := unix.Socket(unix.AF_CAN, unix.SOCK_RAW, unix.CAN_RAW)
	if err != nil {
		return nil, fmt.Errorf("CAN-Socket konnte nicht angelegt werden: %w", err)
	}

	if err := unix.Bind(fd, &unix.SockaddrCAN{Ifindex: iface.Index}); err != nil {
		unix.Close(fd)
		return nil, fmt.Errorf("CAN-Socket konnte nicht an %q gebunden werden: %w", ifaceName, err)
	}

	return &Conn{fd: fd}, nil
}

// Send transmits a single classic CAN frame (max. 8 Byte Payload, Standard-ID).
func (c *Conn) Send(id uint32, data []byte) error {
	if len(data) > 8 {
		return fmt.Errorf("CAN-Payload zu groß (%d Byte, max. 8)", len(data))
	}
	frame := make([]byte, canFrameSize)
	binary.LittleEndian.PutUint32(frame[0:4], id)
	frame[4] = byte(len(data))
	copy(frame[8:8+len(data)], data)

	if _, err := unix.Write(c.fd, frame); err != nil {
		return fmt.Errorf("CAN-Frame (ID 0x%X) konnte nicht gesendet werden: %w", id, err)
	}
	return nil
}

// Receive waits up to timeout for the next CAN frame and returns its
// Standard-ID and payload.
func (c *Conn) Receive(timeout time.Duration) (id uint32, data []byte, err error) {
	tv := unix.NsecToTimeval(timeout.Nanoseconds())
	if err := unix.SetsockoptTimeval(c.fd, unix.SOL_SOCKET, unix.SO_RCVTIMEO, &tv); err != nil {
		return 0, nil, fmt.Errorf("Read-Timeout konnte nicht gesetzt werden: %w", err)
	}

	frame := make([]byte, canFrameSize)
	n, err := unix.Read(c.fd, frame)
	if err != nil {
		return 0, nil, fmt.Errorf("kein CAN-Frame innerhalb von %s empfangen: %w", timeout, err)
	}
	if n < 8 {
		return 0, nil, fmt.Errorf("CAN-Frame zu kurz (%d von mind. 8 Byte)", n)
	}

	rawID := binary.LittleEndian.Uint32(frame[0:4])
	dlc := int(frame[4])
	if dlc > 8 {
		dlc = 8
	}
	if 8+dlc > n {
		dlc = n - 8
	}
	payload := make([]byte, dlc)
	copy(payload, frame[8:8+dlc])

	return rawID & unix.CAN_SFF_MASK, payload, nil
}

// Close releases the underlying socket file descriptor.
func (c *Conn) Close() error {
	return unix.Close(c.fd)
}
