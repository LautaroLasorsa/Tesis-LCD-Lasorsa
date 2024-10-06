#include <stdio.h>
#include "gpu_v1.cu"
#include "gpu_v2.cu"
#include "gpu_v3.cu"
#include "gpu_varianzas.cu"
#include "cpu_v1.cpp"
#include "cpu_v2.cpp"



// Given a host function measures the execution time and prints it
void MeasureTime(void (*f)(), const std::string& name) {
    clock_t start = clock();
    f();
    clock_t end = clock();
    printf("%s: %f\n", name.c_str(), (double)(end - start) / CLOCKS_PER_SEC);
}


int main(int argc, char **argv) {

//    MeasureTime(CPU_V2::SimulacionCPU, "CPU V2");
//    MeasureTime(GPU_V3::SimulacionCuda, "GPU V3");
//    MeasureTime(GPU_V2::SimulacionCuda, "GPU V2");
//    MeasureTime(GPU_V1::SimulacionCuda, "GPU V1");
//    MeasureTime(CPU_V1::SimulacionCPU, "CPU V1");
//    MeasureTime(GPU_VARIANZAS::SimulacionCuda,"GPU VARIANZAS");
    MeasureTime(GPU_VARIANZAS::SimulacionCuda,std::string(argv[1]));
    return 0;
}
