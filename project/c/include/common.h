#ifndef COMMON_H
#define COMMON_H

#define pack2bytesInUint16(var0,var1)  ((uint16_t)((var0) | ((var1) << 8)))
#define pack2bytesInInt16(var0,var1)   ((int16_t)((var0) | ((var1) << 8)))

#endif