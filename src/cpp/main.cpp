#include <string>
#include <iostream>
#include <fstream>
#include "include/json.hpp"


// Para libreria de JSON.
using namespace nlohmann;

//Lista NO TESTEADA
std::vector<std::pair<double,double>> lista_breakpoints(int m, int n, std::vector<double> grid_x, std::vector<double> grid_y){
    int i = 0;
    std::vector<std::pair<double,double>> resultado;
    while(i < m){
        resultado[i].first = grid_x[i];
        resultado[i].second = grid_y[i];
        }
    return resultado;
}
//Lista NO TESTEADA
double optimalidad(std::vector<std::pair<double,double>> secuencia, std::vector<double> x, std::vector<double> y) {
    double error = 0;
    
    for(int i = 0; i < secuencia.size(); i++){
        for(int j = 0; j < x.size(); j++){
            if(x[j] > secuencia[i].first && x[j] <= secuencia[i+1].first){
                double y_pendiente = secuencia[i+1].second - secuencia[i].second;
                double x_pendiente = secuencia[i+1].first - secuencia[i].first;
                if(x_pendiente == 0){
                    return;
                }
                double m = y_pendiente / x_pendiente;
                double b = secuencia[i].second - (m * secuencia[i].first);
                error += abs(y[j] - (m * x[j] + b));
            }
        }
    }
    return error;
}
//Lista NO TESTEADA
bool factibilidad(std::vector<std::pair<double,double>> secuencia){
    for(int i = 0; i < secuencia.size(); i++){
        if(secuencia[i].first >= secuencia[i+1].first){
            return false;
        }
    }
    return true;
}

int main(int argc, char** argv) {
    std::string instance_name = "../../data/titanium.json";
    std::cout << "Reading file " << instance_name << std::endl;
    std::ifstream input(instance_name);

    json instance;
    input >> instance;
    input.close();

    int K = instance["n"];
    int m = 6;
    int n = 6;
    int N = 5;

    std::vector<double> grid_y = instance["y"];
    std::vector<double> grid_x = instance["x"];
    std::cout << K << std::endl;

    // Aca empieza la magia.

    // Ejemplo para guardar json.
    // Probamos guardando el mismo JSON de instance, pero en otro archivo.
    std::ofstream output("test_output.out");

    output << instance;
    output.close();

    return 0;
}