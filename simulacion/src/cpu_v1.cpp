#include <algorithm>
#include <random>
#include "myUtils.cpp"
#include "config.hpp"

namespace CPU_V1{
    void SimulacionCPU(){
        int numSimulaciones = BLOCK_COUNT * SIMULACIONES_POR_BLOQUE;
        auto resultados = new double[numSimulaciones][NUM_DIVISORES]; 
        auto muestra = new double[INDIVIDUOS_POR_SIMULACION + 1];
        
        std::mt19937 gen(20220401);
        std::lognormal_distribution<double> X(0.0, 1.0);

        for(int i = 0;i<numSimulaciones;i++){
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
                resultados[i][d] = suma/(INDIVIDUOS_POR_SIMULACION/DIVISORES[d]);
            }
        }

        exportCSV((double *)resultados, DIVISORES, NUM_DIVISORES, NUM_DIVISORES * numSimulaciones, "datos_cpu_v1.csv");
    }
}