#include <stdio.h>
#include <curand_kernel.h>
#include "myUtils.cpp"
#include "config.hpp"

namespace GPU_V1{
    #define LEFT_CHILD(x) ((x) * 2 + 1)
    #define RIGHT_CHILD(x) ((x) * 2 + 2)
    __device__ void heapify(double *array, int n, int i) {
        int largest = i;
        int left = LEFT_CHILD(i);
        int right = RIGHT_CHILD(i);

        if (left < n && array[left] > array[largest]) {
            largest = left;
            
        }

        if (right < n && array[right] > array[largest]) {
            largest = right;
        }

        if (largest != i) {
            double temp = array[i];
            array[i] = array[largest];
            array[largest] = temp;
            heapify(array, n, largest);
        }
    }

    __device__ void HeapSort(double *f, size_t s) {
        // Build heap (rearrange array)
        for (int i = s / 2 - 1; i >= 0; --i) {
            heapify(f, s, i);
        }

        // One by one extract an element from heap
        for (int i = s - 1; i > 0; --i) {
            // Move current root to end
            double temp = f[0];
            f[0] = f[i];
            f[i] = temp;

            // call max heapify on the reduced heap
            heapify(f, i, 0);
        }
    }

    #undef LEFT_CHILD
    #undef RIGHT_CHILD

    __global__ void simularLognormales(double * resultados, int * divisores, double ** muestras) {
        int tid = blockIdx.x;
        int index = tid * SIMULACIONES_POR_BLOQUE;


    //  double * muestra = new double[INDIVIDUOS_POR_SIMULACION];
    //  double * auxiliar = new double[INDIVIDUOS_POR_SIMULACION];

        double * muestra = muestras[blockIdx.x];
        
        // printf("Simulacion %d => %p %p\n", tid, muestra, auxiliar);

        for (int s = 0; s < SIMULACIONES_POR_BLOQUE; ++s) {
            __syncthreads();
            double * resultado = resultados + (index+s) * NUM_DIVISORES;
            curandState state;
            curand_init(index + s, 0, 0, &state);

            if(threadIdx.x == 0){
                for (int i = 0; i < INDIVIDUOS_POR_SIMULACION; ++i) {
                    muestra[i+1] = curand_log_normal(&state, 0.0f, 1.0f);
                //    printf("%f ", muestra[i+1]);
                }
                //printf("\n");
                
                HeapSort(muestra, INDIVIDUOS_POR_SIMULACION + 1);
                
                for (int i = 1; i<=INDIVIDUOS_POR_SIMULACION; i++){
                    muestra[i] = muestra[i] + muestra[i-1];
                }
            }
            __syncthreads();
            // printf("threadIdx.x = %d\n", threadIdx.x);
            double suma = 0;
            for(int i = 0; i < INDIVIDUOS_POR_SIMULACION; i+=divisores[threadIdx.x]){
                suma += log((muestra[i+divisores[threadIdx.x]] - muestra[i])/divisores[threadIdx.x]);
            }
            resultado[threadIdx.x] = suma/(INDIVIDUOS_POR_SIMULACION/divisores[threadIdx.x]);
            __syncthreads();
        }
    }

    __host__ void SimulacionCuda(){
        const int numSimulaciones = BLOCK_COUNT * SIMULACIONES_POR_BLOQUE;
        size_t resultSize = numSimulaciones * NUM_DIVISORES * sizeof(double);

        // Allocate memory on host
        double *h_resultados = (double *)malloc(resultSize);

        // Allocate memory on device
        double *d_resultados;
        cudaMalloc(&d_resultados, resultSize);

        // Allocate memory on device for each thread
        double ** h_muestras, ** d_muestras;
        h_muestras = (double **)malloc(BLOCK_COUNT * sizeof(double *));

        for (int i = 0; i < BLOCK_COUNT; ++i) {
            cudaMalloc((void **)&h_muestras[i], (INDIVIDUOS_POR_SIMULACION + 1) * sizeof(double));
        }

        cudaMalloc((void **)&d_muestras, BLOCK_COUNT * sizeof(double *));
        cudaMemcpy(d_muestras, h_muestras, BLOCK_COUNT * sizeof(double *), cudaMemcpyHostToDevice);

        // Copy divisors

        int * d_divisores;
        cudaMalloc(&d_divisores, NUM_DIVISORES * sizeof(int));
        cudaMemcpy(d_divisores, DIVISORES, NUM_DIVISORES * sizeof(int), cudaMemcpyHostToDevice);

        // Launch kernel
        simularLognormales<<<BLOCK_COUNT, NUM_DIVISORES>>>(d_resultados, d_divisores, d_muestras);

        // Copy results from device to host
        cudaMemcpy(h_resultados, d_resultados, resultSize, cudaMemcpyDeviceToHost);

        exportCSV(h_resultados, DIVISORES, NUM_DIVISORES, NUM_DIVISORES * numSimulaciones, "datos_gpu_v1.csv");

        // Free memory
        free(h_resultados);
        cudaFree(d_resultados);
        for (int i = 0; i < BLOCK_COUNT; ++i) {
            cudaFree(h_muestras[i]);
        }
        free(h_muestras);
        cudaFree(d_muestras);
        cudaFree(d_divisores);
        
    }
}