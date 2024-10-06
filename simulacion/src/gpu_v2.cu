#include <stdio.h>
#include <curand_kernel.h>
#include <assert.h>
#include "myUtils.cpp"
#include "config.hpp"

namespace GPU_V2{
    
    
    const int SIZE = (INDIVIDUOS_POR_SIMULACION)/32;
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

    // Merge the ranges vec[0:tam] and vec[tam:2*tam] into vec[0:2*tam]
    __device__ void merge(double * vec, double * aux, size_t tam){
        size_t i = 0, j = tam, k = 0;
        while(i < tam && j < 2*tam){
            if(vec[i] < vec[j]){
                aux[k] = vec[i];
                i++;
            }else{
                aux[k] = vec[j];
                j++;
            }
            k++;
        }
        while(i < tam){
            aux[k] = vec[i];
            i++;
            k++;
        }
        while(j < 2*tam){
            aux[k] = vec[j];
            j++;
            k++;
        }
        for(size_t i = 0; i < 2*tam; i++){
            vec[i] = aux[i];
        }
    }

    __global__ void simularLognormales(double * resultados, int * divisores, double ** muestras, double ** auxiliares) {
        int tid = blockIdx.x;
        int index = tid * (2 * SIMULACIONES_POR_BLOQUE);


    //  double * muestra = new double[INDIVIDUOS_POR_SIMULACION];
    //  double * auxiliar = new double[INDIVIDUOS_POR_SIMULACION];

        double * muestra = muestras[blockIdx.x];
        double * auxiliar = auxiliares[blockIdx.x];

        // printf("Simulacion %d => %p %p\n", tid, muestra, auxiliar);

        for (int s = 0; s < (2 * SIMULACIONES_POR_BLOQUE); ++s) {
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
                
                //HeapSort(muestra, INDIVIDUOS_POR_SIMULACION + 1);
                
                //for (int i = 1; i<=INDIVIDUOS_POR_SIMULACION; i++){
                //    muestra[i] = muestra[i] + muestra[i-1];
                // }
            }
            __syncthreads();
            
            if(threadIdx.x<32){
                HeapSort(muestra + 1 + SIZE*threadIdx.x, SIZE);
            }
            
            __syncthreads();

            for(int po2 = 2; po2<=32; po2*=2){
                if(threadIdx.x<32 && threadIdx.x%(po2) == 0){
                    merge(muestra + 1 + SIZE*(threadIdx.x), auxiliar + 1 + SIZE*(threadIdx.x), SIZE*(po2/2));
                }
                __syncthreads();
            }

            if(threadIdx.x == 0){
                for(int i = 0;i<INDIVIDUOS_POR_SIMULACION;i++){
                    assert(muestra[i]<muestra[i+1]+1e-6);
                //    assert(muestra[i]>muestra[i+1]-1e-6);
                }
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
        int numSimulaciones = (BLOCK_COUNT / 2) * (2 * SIMULACIONES_POR_BLOQUE);
        size_t resultSize = numSimulaciones * NUM_DIVISORES * sizeof(double);

        // Allocate memory on host
        double *h_resultados = (double *)malloc(resultSize);

        // Allocate memory on device
        double *d_resultados;
        cudaMalloc(&d_resultados, resultSize);

        // Allocate memory on device for each thread
        double ** h_muestras, ** d_muestras, ** h_auxiliar, ** d_auxiliar;
        h_muestras = (double **)malloc((BLOCK_COUNT / 2) * sizeof(double *));
        h_auxiliar = (double **)malloc((BLOCK_COUNT / 2) * sizeof(double *));

        for (int i = 0; i < (BLOCK_COUNT / 2); ++i) {
            cudaMalloc((void **)&h_muestras[i], (INDIVIDUOS_POR_SIMULACION + 1) * sizeof(double));
            cudaMalloc((void **)&h_auxiliar[i], (INDIVIDUOS_POR_SIMULACION + 1) * sizeof(double));
        }

        cudaMalloc((void **)&d_muestras, (BLOCK_COUNT / 2) * sizeof(double *));
        cudaMalloc((void **)&d_auxiliar, (BLOCK_COUNT / 2) * sizeof(double *));
        
        cudaMemcpy(d_muestras, h_muestras, (BLOCK_COUNT / 2) * sizeof(double *), cudaMemcpyHostToDevice);
        cudaMemcpy(d_auxiliar, h_auxiliar, (BLOCK_COUNT / 2) * sizeof(double *), cudaMemcpyHostToDevice);
        
        // Copy divisors

        int * d_divisores;
        cudaMalloc(&d_divisores, NUM_DIVISORES * sizeof(int));
        cudaMemcpy(d_divisores, DIVISORES, NUM_DIVISORES * sizeof(int), cudaMemcpyHostToDevice);

        // Launch kernel
        simularLognormales<<<(BLOCK_COUNT / 2), NUM_DIVISORES>>>(d_resultados, d_divisores, d_muestras, d_auxiliar);

        // Copy results from device to host
        cudaMemcpy(h_resultados, d_resultados, resultSize, cudaMemcpyDeviceToHost);

        exportCSV(h_resultados, DIVISORES, NUM_DIVISORES, NUM_DIVISORES * numSimulaciones, "datos_gpu_v2.csv");

        // Free memory
        free(h_resultados);
        cudaFree(d_resultados);
        for (int i = 0; i < (BLOCK_COUNT / 2); ++i) {
            cudaFree(h_muestras[i]);
            cudaFree(h_auxiliar[i]);
        }
        free(h_muestras);
        free(h_auxiliar);
        cudaFree(d_muestras);
        cudaFree(d_auxiliar);
        cudaFree(d_divisores);
        
    }
}