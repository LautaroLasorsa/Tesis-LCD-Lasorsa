#ifndef MYUTILS_CPP
#define MYUTILS_CPP

#include <fstream>
#include <string>
#include <iostream>

void exportCSV(const double* datos,const int* titulos, size_t numColumnas, size_t sizeDatos, const std::string& nombreArchivo) {
    std::ofstream archivo(nombreArchivo);

    // Escribir los títulos de las columnas
    for (size_t i = 0; i < numColumnas; ++i) {
        archivo << titulos[i];
        if (i != numColumnas - 1) {
            archivo << "\t";
        }
    }
    archivo << "\n";

    // Escribir los datos de la matriz
    for (size_t i = 0; i < sizeDatos; ++i){
        archivo << datos[i];
        if ((i + 1) % numColumnas != 0) {
            archivo << "\t";
        } else {
            archivo << "\n";
        }
    }

    archivo.close();
}
#endif