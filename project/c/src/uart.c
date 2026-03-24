#include "uart.h"
#include <string.h>
#include <fcntl.h>
#include <unistd.h>
#include <termios.h>
#include <sys/select.h>
static speed_t baud_to_speed(uint32_t b){
    switch(b){case 9600:return B9600;case 19200:return B19200;
    case 38400:return B38400;case 57600:return B57600;default:return B115200;}}
int uart_open(uart_dev_t *dev,const char *port,uint32_t baud){
    dev->fd=open(port,O_RDWR|O_NOCTTY|O_NONBLOCK);
    if(dev->fd<0)return -1;
    strncpy(dev->port,port,sizeof(dev->port)-1); dev->baud=baud;
    struct termios tty; tcgetattr(dev->fd,&tty);
    speed_t sp=baud_to_speed(baud); cfsetispeed(&tty,sp); cfsetospeed(&tty,sp);
    tty.c_cflag=(tty.c_cflag&~CSIZE)|CS8|CLOCAL|CREAD;
    tty.c_cflag&=~(PARENB|PARODD|CSTOPB|CRTSCTS);
    tty.c_iflag=IGNPAR; tty.c_oflag=0; tty.c_lflag=0;
    tcsetattr(dev->fd,TCSANOW,&tty); return 0;}
int uart_write(uart_dev_t *dev,const uint8_t *buf,size_t len){return(int)write(dev->fd,buf,len);}
int uart_read(uart_dev_t *dev,uint8_t *buf,size_t len,int timeout_ms){
    fd_set fds; struct timeval tv={.tv_sec=timeout_ms/1000,.tv_usec=(timeout_ms%1000)*1000};
    FD_ZERO(&fds); FD_SET(dev->fd,&fds);
    if(select(dev->fd+1,&fds,NULL,NULL,&tv)<=0)return -1;
    return(int)read(dev->fd,buf,len);}
int uart_flush(uart_dev_t *dev){return tcflush(dev->fd,TCIOFLUSH);}
void uart_close(uart_dev_t *dev){if(dev->fd>=0){close(dev->fd);dev->fd=-1;}}
