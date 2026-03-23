#include "gpio.h"
#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>
static void gpath(char *b,size_t l,uint32_t p,const char *f){
    snprintf(b,l,"/sys/class/gpio/gpio%u/%s",p,f);}
int gpio_export(uint32_t pin){
    char b[8]; int fd=open("/sys/class/gpio/export",O_WRONLY);
    if(fd<0)return -1; snprintf(b,sizeof(b),"%u",pin);
    write(fd,b,strlen(b)); close(fd); usleep(100000); return 0;}
int gpio_unexport(uint32_t pin){
    char b[8]; int fd=open("/sys/class/gpio/unexport",O_WRONLY);
    if(fd<0)return -1; snprintf(b,sizeof(b),"%u",pin);
    write(fd,b,strlen(b)); close(fd); return 0;}
int gpio_set_direction(uint32_t pin,gpio_direction_t dir){
    char p[128]; gpath(p,sizeof(p),pin,"direction");
    int fd=open(p,O_WRONLY); if(fd<0)return -1;
    const char *d=(dir==GPIO_OUTPUT)?"out":"in";
    write(fd,d,strlen(d)); close(fd); return 0;}
int gpio_write(uint32_t pin,int value){
    char p[128]; gpath(p,sizeof(p),pin,"value");
    int fd=open(p,O_WRONLY); if(fd<0)return -1;
    write(fd,value?"1":"0",1); close(fd); return 0;}
int gpio_read(uint32_t pin,int *value){
    char p[128],b[2]; gpath(p,sizeof(p),pin,"value");
    int fd=open(p,O_RDONLY); if(fd<0)return -1;
    read(fd,b,sizeof(b)); *value=(b[0]=='1')?1:0; close(fd); return 0;}
