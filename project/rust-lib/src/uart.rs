use std::ffi::CStr;
use libc::{c_char, c_int};
use serialport::SerialPort;
use std::time::Duration;

#[repr(C)]
pub struct RsUartHandle { pub port: *mut Box<dyn SerialPort> }
#[repr(C)]
pub struct RsUartData { pub buf: [u8;256], pub len: u32, pub error: i32 }

/// # Safety
#[no_mangle]
pub unsafe extern "C" fn rs_uart_open(port: *const c_char, baud: u32) -> RsUartHandle {
    let path = CStr::from_ptr(port).to_str().unwrap_or("/dev/ttyO1");
    match serialport::new(path,baud).timeout(Duration::from_millis(100)).open() {
        Ok(p)  => RsUartHandle { port: Box::into_raw(Box::new(p)) },
        Err(_) => RsUartHandle { port: std::ptr::null_mut() },
    }
}
/// # Safety
#[no_mangle]
pub unsafe extern "C" fn rs_uart_write(h: *mut RsUartHandle, buf: *const u8, len: u32) -> c_int {
    if h.is_null()||(*h).port.is_null() { return -1; }
    let port = &mut *(*h).port;
    let data = std::slice::from_raw_parts(buf, len as usize);
    port.write(data).map(|n|n as c_int).unwrap_or(-1)
}
/// # Safety
#[no_mangle]
pub unsafe extern "C" fn rs_uart_read(h: *mut RsUartHandle) -> RsUartData {
    if h.is_null()||(*h).port.is_null() { return RsUartData{buf:[0;256],len:0,error:-1}; }
    let port = &mut *(*h).port;
    let mut buf = [0u8;256];
    match port.read(&mut buf) {
        Ok(n)  => RsUartData{buf,len:n as u32,error:0},
        Err(_) => RsUartData{buf,len:0,error:-1},
    }
}
/// # Safety
#[no_mangle]
pub unsafe extern "C" fn rs_uart_close(h: *mut RsUartHandle) {
    if !h.is_null()&&!(*h).port.is_null() {
        drop(Box::from_raw((*h).port)); (*h).port=std::ptr::null_mut();
    }
}
