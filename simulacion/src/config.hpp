#ifndef CONFIG_HPP
#define CONFIG_HPP
const int SIMULACIONES_POR_BLOQUE = 25;
const int INDIVIDUOS_POR_SIMULACION = 1000000;
const int BLOCK_COUNT = 400;

const int DIVISORES[] = {1, 2, 4, 5, 8, 10, 16, 20, 25, 32, 40, 50, 64, 80, 100, 125, 160, 200, 250, 320, 400, 500, 625, 800, 1000, 1250, 1600, 2000, 2500, 3125, 4000, 5000, 6250, 8000, 10000, 12500, 15625, 20000, 25000, 31250, 40000, 50000, 62500, 100000, 125000, 200000, 250000, 500000, 1000000};
const double VARIANZAS[] = {1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0};
//const int DIVISORES[] = {1, 2, 4, 5, 10, 20, 25, 50, 100};
const int NUM_DIVISORES = sizeof(DIVISORES) / sizeof(int);
const int NUM_VARIANZAS = sizeof(VARIANZAS) / sizeof(double);
const int SIMULACIONES_POR_VARIANZA = (BLOCK_COUNT * SIMULACIONES_POR_BLOQUE + NUM_VARIANZAS-1)/NUM_VARIANZAS;
#endif
