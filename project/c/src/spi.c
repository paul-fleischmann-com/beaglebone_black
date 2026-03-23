#include "spi.h"
#include "common.h"
#include <string.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <linux/spi/spidev.h>
int spi_open(spi_dev_t *dev,const char *device,uint32_t speed,uint8_t mode){
    dev->fd=open(device,O_RDWR); if(dev->fd<0)return -1;
    strncpy(dev->device,device,sizeof(dev->device)-1);
    dev->speed=speed; dev->mode=mode; dev->bits=8;
    ioctl(dev->fd,SPI_IOC_WR_MODE,&mode);
    ioctl(dev->fd,SPI_IOC_WR_BITS_PER_WORD,&dev->bits);
    ioctl(dev->fd,SPI_IOC_WR_MAX_SPEED_HZ,&speed); return 0;}
int spi_transfer(spi_dev_t *dev,const uint8_t *tx,uint8_t *rx,size_t len){
    struct spi_ioc_transfer tr={
        .tx_buf=(unsigned long)tx,
        .rx_buf=(unsigned long)rx,
        .len=(uint32_t)len,
        .speed_hz=dev->speed,
        .bits_per_word=dev->bits};
    return ioctl(dev->fd,SPI_IOC_MESSAGE(1),&tr);}
void spi_close(spi_dev_t *dev){if(dev->fd>=0){close(dev->fd);dev->fd=-1;}}
