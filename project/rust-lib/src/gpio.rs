use libc::{c_int, c_char};
use std::ffi::CStr;

#[repr(C)]
pub struct RsGpioData { pub pin: u32, pub value: i32, pub error: i32 }

#[no_mangle]
pub extern "C" fn rs_gpio_read(pin: u32) -> RsGpioData {
    let path = format!("/sys/class/gpio/gpio{}/value", pin);
    match std::fs::read_to_string(&path) {
        Ok(v)  => RsGpioData { pin, value: v.trim().parse().unwrap_or(0), error: 0 },
        Err(_) => RsGpioData { pin, value: 0, error: -1 },
    }
}
#[no_mangle]
pub extern "C" fn rs_gpio_write(pin: u32, value: c_int) -> c_int {
    let path = format!("/sys/class/gpio/gpio{}/value", pin);
    match std::fs::write(&path, if value!=0{"1"}else{"0"}) { Ok(_)=>0, Err(_)=>-1 }
}
#[no_mangle]
pub extern "C" fn rs_gpio_export(pin: u32) -> c_int {
    match std::fs::write("/sys/class/gpio/export", pin.to_string()) {
        Ok(_)  => { std::thread::sleep(std::time::Duration::from_millis(100)); 0 }
        Err(_) => -1,
    }
}
#[no_mangle]
pub extern "C" fn rs_gpio_set_direction(pin: u32, output: c_int) -> c_int {
    let path = format!("/sys/class/gpio/gpio{}/direction", pin);
    match std::fs::write(&path, if output!=0{"out"}else{"in"}) { Ok(_)=>0, Err(_)=>-1 }
}
