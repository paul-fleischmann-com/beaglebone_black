fn main() {
    let crate_dir = std::env::var("CARGO_MANIFEST_DIR").unwrap();
    cbindgen::Builder::new()
        .with_crate(&crate_dir)
        .with_config(cbindgen::Config::from_file("cbindgen.toml").unwrap_or_default())
        .generate()
        .expect("cbindgen failed")
        .write_to_file("hardware_rs.h");
}
