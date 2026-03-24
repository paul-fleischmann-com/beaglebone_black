use std::ffi::CStr;
use libc::c_char;
use bme280::BME280;
use linux_embedded_hal::{Delay, I2cdev};

const SEA_LEVEL_PA: f64 = 101325.0;

#[repr(C)]
pub struct RsBme280Data {
    pub temperature: f64,
    pub humidity:    f64,
    pub pressure:    f64,
    pub altitude:    f64,
    pub timestamp:   u64,
    pub error:       i32,
}

fn calc_altitude(p: f64) -> f64 {
    44330.0 * (1.0 - (p * 100.0 / SEA_LEVEL_PA).powf(1.0 / 5.255))
}
fn err(code: i32) -> RsBme280Data {
    RsBme280Data { temperature:0.0,humidity:0.0,pressure:0.0,
                   altitude:0.0,timestamp:0,error:code }
}
/// # Safety
#[no_mangle]
pub unsafe extern "C" fn rs_bme280_read(i2c_path: *const c_char, addr: u8) -> RsBme280Data {
    let path = match CStr::from_ptr(i2c_path).to_str() { Ok(p)=>p, Err(_)=>return err(-1) };
    let i2c  = match I2cdev::new(path)                  { Ok(d)=>d, Err(_)=>return err(-2) };
    let mut d = Delay;
    let mut s = match BME280::new(i2c,addr,&mut d)      { Ok(s)=>s, Err(_)=>return err(-3) };
    if s.init(&mut d).is_err() { return err(-4); }
    match s.measure(&mut d) {
        Ok(m) => {
            let ph = m.pressure as f64 / 100.0;
            RsBme280Data {
                temperature: (m.temperature as f64*100.0).round()/100.0,
                humidity:    (m.humidity    as f64*100.0).round()/100.0,
                pressure:    (ph*100.0).round()/100.0,
                altitude:    (calc_altitude(ph)*10.0).round()/10.0,
                timestamp:   std::time::SystemTime::now()
                    .duration_since(std::time::UNIX_EPOCH)
                    .unwrap_or_default().as_secs(),
                error: 0,
            }
        }
        Err(_) => err(-5),
    }
}
