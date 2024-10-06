#include <algorithm>
#include <random>
#include "myUtils.cpp"
#include "config.hpp"
#include <thread>

namespace CPU_V2{
    
    const int numeroHilos = 12;
    const int numSimulaciones = BLOCK_COUNT * SIMULACIONES_POR_BLOQUE;
    const int simulacionesPorHilo = numSimulaciones / numeroHilos;

    void SimulacionHilo(double * resultados, int index){
        auto muestra = new double[INDIVIDUOS_POR_SIMULACION + 1];
        
        std::mt19937 gen(20220401);
        std::lognormal_distribution<double> X(0.0, 1.0);

        for(int i = index * simulacionesPorHilo;i<(index + 1) * simulacionesPorHilo;i++){
            for(int j = 0;j<INDIVIDUOS_POR_SIMULACION;j++){
                muestra[j+1] = X(gen);
            }

            std::sort(muestra + 1, muestra + INDIVIDUOS_POR_SIMULACION + 1);
            for(int j = 1;j<=INDIVIDUOS_POR_SIMULACION;j++){
                muestra[j] = muestra[j] + muestra[j-1];
            }

            for(int d = 0; d < NUM_DIVISORES; d++){
                double suma = 0;
                for(int j = 0;j<INDIVIDUOS_POR_SIMULACION;j+=DIVISORES[d]){
                    suma += log((muestra[j+DIVISORES[d]] - muestra[j])/DIVISORES[d]);
                }
                resultados[i * NUM_DIVISORES + d] = suma/(INDIVIDUOS_POR_SIMULACION/DIVISORES[d]);
            }
        }
    }
    
    void SimulacionCPU(){
        auto resultados = (double *)malloc(sizeof(double) * numSimulaciones * NUM_DIVISORES);

        std::thread hilos[numeroHilos];

        for(int i = 0; i < numeroHilos; i++){
            hilos[i] = std::thread(SimulacionHilo, resultados, i);
        }

        for(int i = 0; i < numeroHilos; i++){
            hilos[i].join();
        }

        exportCSV((double *)resultados, DIVISORES, NUM_DIVISORES, NUM_DIVISORES * numSimulaciones, "datos_cpu_v2.csv");
    }
}