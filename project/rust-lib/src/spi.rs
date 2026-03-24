use std::ffi::CStr;
use libc::c_char;
use spidev::{Spidev,SpidevOptions,SpidevTransfer,SpiModeFlags};

#[repr(C)]
pub struct RsSpiData { pub buf: [u8;256], pub len: u32, pub error: i32 }

/// # Safety
#[no_mangle]
pub unsafe extern "C" fn rs_spi_transfer(
    device: *const c_char, speed: u32, tx_buf: *const u8, tx_len: u32) -> RsSpiData {
    let path = CStr::from_ptr(device).to_str().unwrap_or("/dev/spidev0.0");
    let mut spi = match Spidev::open(path) { Ok(s)=>s, Err(_)=>return RsSpiData{buf:[0;256],len:0,error:-1} };
    let opts = SpidevOptions::new().bits_per_word(8).max_speed_hz(speed)
        .mode(SpiModeFlags::SPI_MODE_0).build();
    if spi.configure(&opts).is_err() { return RsSpiData{buf:[0;256],len:0,error:-2}; }
    let tx = std::slice::from_raw_parts(tx_buf, tx_len as usize);
    let mut rx = vec![0u8;tx_len as usize];
    let mut tr = SpidevTransfer::read_write(tx,&mut rx);
    match spi.transfer(&mut tr) {
        Ok(_)  => { let mut buf=[0u8;256]; buf[..rx.len()].copy_from_slice(&rx);
                    RsSpiData{buf,len:tx_len,error:0} }
        Err(_) => RsSpiData{buf:[0;256],len:0,error:-3},
    }
}
