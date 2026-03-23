#include "bme280.h"
#include "common.h"
#include <stdio.h>
#include <math.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <linux/i2c-dev.h>
#include <time.h>

static int i2c_write_reg(int fd, uint8_t reg, uint8_t val) {
    uint8_t buf[2]={reg,val}; return write(fd,buf,2)!=2?-1:0;
}
static int i2c_read_reg(int fd, uint8_t reg, uint8_t *buf, int len) {
    if(write(fd,&reg,1)!=1) return -1;
    return read(fd,buf,len)!=len?-1:0;
}

static int read_calibration(bme280_dev_t *dev) {
    int returnValue = -1;
    uint8_t buf[24];
     if (i2c_read_reg(dev->fd,0x88,buf,24) >= 0)  {
        bme280_calib_t *c=&dev->calib;
        c->T1=pack2bytesInUint16(buf[0],buf[1]); 
        c->T2=pack2bytesInInt16(buf[2],buf[3]); 
        c->T3=pack2bytesInInt16(buf[4],buf[5]); 
        c->P1=pack2bytesInUint16(buf[6],buf[7]); 
        c->P2=pack2bytesInInt16(buf[8],buf[9]);  
        c->P3=pack2bytesInInt16(buf[10],buf[11]); 
        c->P4=pack2bytesInInt16(buf[12],buf[13]); 
        c->P5=pack2bytesInInt16(buf[14],buf[15]);  
        c->P6=pack2bytesInInt16(buf[16],buf[17]); 
        c->P7=pack2bytesInInt16(buf[18],buf[19]);  
        c->P8=pack2bytesInInt16(buf[20],buf[21]);  
        c->P9=pack2bytesInInt16(buf[22],buf[23]); 
        uint8_t h1[1] = {0}; i2c_read_reg(dev->fd,0xA1,h1,1);
        c->H1=h1[0];
        uint8_t hb[7] = {0}; i2c_read_reg(dev->fd,0xE1,hb,7);
        c->H2=pack2bytesInInt16(hb[0],hb[1]);
        c->H3=hb[2];
        c->H4=((int16_t)hb[3]<<4)|((int16_t)(hb[4]&0x0F));
        c->H5=((int16_t)hb[5]<<4)|((int16_t)(hb[4]>>4));
        c->H6=(int8_t)hb[6];
        returnValue = 0;
    }
    return returnValue;
}
int bme280_init(bme280_dev_t *dev) {
    dev->fd=open(BME280_I2C_BUS,O_RDWR);
    if(dev->fd<0) return -1;
    if(ioctl(dev->fd,I2C_SLAVE,BME280_ADDR)<0) return -2;
    uint8_t id[1]; i2c_read_reg(dev->fd,0xD0,id,1);
    if(id[0]!=0x60) return -3;
    i2c_write_reg(dev->fd,0xE0,0xB6); usleep(10000);
    if(read_calibration(dev)<0) return -4;
    i2c_write_reg(dev->fd,0xF2,0x01);
    i2c_write_reg(dev->fd,0xF4,0x57);
    i2c_write_reg(dev->fd,0xF5,0xA0);
    usleep(100000); return 0;
}
static double comp_temp(bme280_dev_t *dev, int32_t raw) {
    bme280_calib_t *c=&dev->calib;
    double v1=((double)raw/16384.0-(double)c->T1/1024.0)*(double)c->T2;
    double v2=((double)raw/131072.0-(double)c->T1/8192.0)*
              ((double)raw/131072.0-(double)c->T1/8192.0)*(double)c->T3;
    dev->t_fine=(int32_t)(v1+v2); return (v1+v2)/5120.0;
}
static double comp_press(bme280_dev_t *dev, int32_t raw) {
    bme280_calib_t *c=&dev->calib;
    double v1=(double)dev->t_fine/2.0-64000.0;
    double v2=v1*v1*(double)c->P6/32768.0+v1*(double)c->P5*2.0;
    v2=v2/4.0+(double)c->P4*65536.0;
    v1=((double)c->P3*v1*v1/524288.0+(double)c->P2*v1)/524288.0;
    v1=(1.0+v1/32768.0)*(double)c->P1;
    if(v1==0.0) return 0;
    double p=1048576.0-(double)raw;
    p=((p-v2/4096.0)*6250.0)/v1;
    v1=(double)c->P9*p*p/2147483648.0; v2=p*(double)c->P8/32768.0;
    return (p+(v1+v2+(double)c->P7)/16.0)/100.0;
}
static double comp_hum(bme280_dev_t *dev, int32_t raw) {
    bme280_calib_t *c=&dev->calib;
    double h=(double)dev->t_fine-76800.0;
    h=((double)raw-((double)c->H4*64.0+(double)c->H5/16384.0*h))*
      ((double)c->H2/65536.0*(1.0+(double)c->H6/67108864.0*h*
      (1.0+(double)c->H3/67108864.0*h)));
    h*=1.0-(double)c->H1*h/524288.0;
    if(h>100.0) {
      h=100.0;
    }
    else if(h<0.0) {
        h=0.0;
    }
    return h;
}
int bme280_read(bme280_dev_t *dev, bme280_data_t *out) {
    uint8_t raw[8];
    if(i2c_read_reg(dev->fd,0xF7,raw,8)<0) return -1;
    int32_t rp=((int32_t)raw[0]<<12)|((int32_t)raw[1]<<4)|(raw[2]>>4);
    int32_t rt=((int32_t)raw[3]<<12)|((int32_t)raw[4]<<4)|(raw[5]>>4);
    int32_t rh=((int32_t)raw[6]<<8)|raw[7];
    out->temperature=round(comp_temp(dev,rt)*100)/100;
    out->pressure=round(comp_press(dev,rp)*100)/100;
    out->humidity=round(comp_hum(dev,rh)*100)/100;
    out->altitude=round(44330.0*(1.0-pow(out->pressure*100/SEA_LEVEL_PA,1.0/5.255))*10)/10;
    out->timestamp=(uint64_t)time(NULL); return 0;
}
void bme280_close(bme280_dev_t *dev) { if(dev->fd>=0){close(dev->fd);dev->fd=-1;} }
