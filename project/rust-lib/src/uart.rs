use std::ffi::CStr;
use libc::{c_char, c_int, c_void};
use serialport::SerialPort;
use std::time::Duration;

// FFI-safe opaque handle — the trait object is heap-allocated and passed as void*
#[repr(C)]
pub struct RsUartHandle { pub r: *mut c_void }
#[repr(C)]
pub struct RsUartData { pub buf: [u8;256], pub len: u32, pub error: i32 }

/// # Safety
#[no_mangle]
pub unsafe extern "C" fn rs_uart_open(port: *const c_char, baud: u32) -> RsUartHandle {
    let path = CStr::from_ptr(port).to_str().unwrap_or("/dev/ttyO1");
    match serialport::new(path, baud).timeout(Duration::from_millis(100)).open() {
        Ok(p)  => RsUartHandle { r: Box::into_raw(Box::new(p)) as *mut c_void },
        Err(_) => RsUartHandle { r: std::ptr::null_mut() },
    }
}
/// # Safety
#[no_mangle]
pub unsafe extern "C" fn rs_uart_write(h: *mut RsUartHandle, buf: *const u8, len: u32) -> c_int {
    if h.is_null() || (*h).r.is_null() { return -1; }
    let port = &mut *((*h).r as *mut Box<dyn SerialPort>);
    let data = std::slice::from_raw_parts(buf, len as usize);
    port.write(data).map(|n| n as c_int).unwrap_or(-1)
}
/// # Safety
#[no_mangle]
pub unsafe extern "C" fn rs_uart_read(h: *mut RsUartHandle) -> RsUartData {
    if h.is_null() || (*h).r.is_null() { return RsUartData { buf: [0;256], len: 0, error: -1 }; }
    let port = &mut *((*h).r as *mut Box<dyn SerialPort>);
    let mut buf = [0u8;256];
    match port.read(&mut buf) {
        Ok(n)  => RsUartData { buf, len: n as u32, error: 0 },
        Err(_) => RsUartData { buf, len: 0, error: -1 },
    }
}
/// # Safety
#[no_mangle]
pub unsafe extern "C" fn rs_uart_close(h: *mut RsUartHandle) {
    if !h.is_null() && !(*h).r.is_null() {
        drop(Box::from_raw((*h).r as *mut Box<dyn SerialPort>));
        (*h).r = std::ptr::null_mut();
    }
}
