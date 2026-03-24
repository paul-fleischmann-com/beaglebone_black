use std::ffi::CStr;
use libc::c_char;
use bme280::i2c::BME280;
use linux_embedded_hal::I2cdev;
use embedded_hal::i2c::I2c as BlockingI2c;

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
    RsBme280Data { temperature: 0.0, humidity: 0.0, pressure: 0.0,
                   altitude: 0.0, timestamp: 0, error: code }
}

// Wrap blocking I2cdev to implement embedded-hal-async's I2c trait
struct SyncI2c(I2cdev);

impl embedded_hal_async::i2c::ErrorType for SyncI2c {
    type Error = <I2cdev as embedded_hal::i2c::ErrorType>::Error;
}

impl embedded_hal_async::i2c::I2c for SyncI2c {
    async fn read(&mut self, addr: u8, buf: &mut [u8]) -> Result<(), Self::Error> {
        BlockingI2c::read(&mut self.0, addr, buf)
    }
    async fn write(&mut self, addr: u8, buf: &[u8]) -> Result<(), Self::Error> {
        BlockingI2c::write(&mut self.0, addr, buf)
    }
    async fn write_read(&mut self, addr: u8, w: &[u8], r: &mut [u8]) -> Result<(), Self::Error> {
        BlockingI2c::write_read(&mut self.0, addr, w, r)
    }
    async fn transaction(&mut self, addr: u8, ops: &mut [embedded_hal::i2c::Operation<'_>]) -> Result<(), Self::Error> {
        BlockingI2c::transaction(&mut self.0, addr, ops)
    }
}

// Wrap blocking sleep to implement embedded-hal-async's DelayNs trait
struct SyncDelay;

impl embedded_hal_async::delay::DelayNs for SyncDelay {
    async fn delay_ns(&mut self, ns: u32) {
        std::thread::sleep(std::time::Duration::from_nanos(ns as u64));
    }
}

/// # Safety
#[no_mangle]
pub unsafe extern "C" fn rs_bme280_read(i2c_path: *const c_char, addr: u8) -> RsBme280Data {
    let path = match CStr::from_ptr(i2c_path).to_str() { Ok(p) => p.to_owned(), Err(_) => return err(-1) };
    let i2c  = match I2cdev::new(&path)                 { Ok(d) => d,            Err(_) => return err(-2) };
    let mut s = BME280::new(SyncI2c(i2c), addr);
    let mut d = SyncDelay;
    futures::executor::block_on(async move {
        if s.init(&mut d).await.is_err() { return err(-4); }
        match s.measure(&mut d).await {
            Ok(m) => {
                let ph = m.pressure as f64 / 100.0;
                RsBme280Data {
                    temperature: (m.temperature as f64 * 100.0).round() / 100.0,
                    humidity:    (m.humidity    as f64 * 100.0).round() / 100.0,
                    pressure:    (ph * 100.0).round() / 100.0,
                    altitude:    (calc_altitude(ph) * 10.0).round() / 10.0,
                    timestamp:   std::time::SystemTime::now()
                        .duration_since(std::time::UNIX_EPOCH)
                        .unwrap_or_default().as_secs(),
                    error: 0,
                }
            }
            Err(_) => err(-5),
        }
    })
}
