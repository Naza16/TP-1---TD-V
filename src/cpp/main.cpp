#include <string>
#include <algorithm> 
#include <iostream>
#include <fstream>
#include "include/json.hpp"
#include <limits>
#include <vector>
#include <cmath>


using namespace nlohmann;
using namespace std;


int BIG_NUMBER = numeric_limits<int>::max();

vector<double> linespace(double minVal, double maxVal, int num) {
    vector<double> res;
    double step = (maxVal - minVal) / (num - 1);
    for(int i = 0; i < num; i++) {
        res.push_back(minVal + i * step);
    }
    return res;
}

vector<pair<double, double>> lista_breakpoints(int m, int n, vector<double> &x, vector<double> &y) {
    vector<double> grillaX = linespace(*min_element(x.begin(), x.end()), *max_element(x.begin(), x.end()), m);
    vector<double> grillaY = linespace(*min_element(y.begin(), y.end()), *max_element(y.begin(), y.end()), n);
    vector<pair<double, double>> breakpoints;
    for(double xi : grillaX) {
        for(double yj : grillaY) {
            breakpoints.push_back(make_pair(xi, yj));
        }
    }
    return breakpoints;
}

int optimalidad(vector<pair<double, double>> &secuencia, vector<double> &x, vector<double> &y) {
    int error = 0;
    for(size_t i = 0; i < secuencia.size() - 1; i++) {
        for(size_t j = 0; j < x.size(); j++) {
            if(x[j] > secuencia[i].first && x[j] < secuencia[i+1].first) {
                double y_pendiente = secuencia[i+1].second - secuencia[i].second;
                double x_pendiente = secuencia[i+1].first - secuencia[i].first;
                if (x_pendiente == 0) {
                    continue;
                }
                double m = y_pendiente / x_pendiente;
                double b = secuencia[i].second - (m * secuencia[i].first);
                error += abs(y[j] - (m * x[j] + b));
            }
        }
    }
    return error;
}

bool factibilidad(vector<pair<double, double>> &secuencia) {
    for(size_t i = 0; i < secuencia.size() - 1; i++) {
        if(secuencia[i].first >= secuencia[i+1].first) {
            return false;
        }
    }
    return true;
}

struct MejorSolucion {
    double obj = numeric_limits<double>::max();
    vector<pair<double, double>> sol;
};

void fuerza_bruta(int m, int n, int k, vector<double> x, vector<double> y, MejorSolucion& best, vector<pair<double, double>> sol_parcial = {}) {
    vector<pair<double, double>> breakpoints = lista_breakpoints(m, n, x, y);
    if(sol_parcial.size() == k) {
        if(factibilidad(sol_parcial)) {
            int current_error = optimalidad(sol_parcial, x, y);
            if(current_error < best.obj) {
                best.obj = current_error;
                best.sol = sol_parcial;
            }
        }
    } else {
        for(const auto& punto : breakpoints) {
            sol_parcial.push_back(punto);
            if (sol_parcial.size() <= k) {
                fuerza_bruta(m, n, k, x, y, best, sol_parcial);
            }
            sol_parcial.pop_back();
        }
    }
}

void backtracking(int m, int n, int k, vector<double> x, vector<double> y, MejorSolucion& best, vector<pair<double, double>> sol_parcial = {}) {
    vector<pair<double, double>> breakpoints = lista_breakpoints(m, n, x, y);
    if(sol_parcial.size() == k) {
        if(factibilidad(sol_parcial)) {
            int current_error = optimalidad(sol_parcial, x, y);
            if(current_error < best.obj) {
                best.obj = current_error;
                best.sol = sol_parcial;
            }
        }
    } else {
        for(const auto& punto : breakpoints) {
            sol_parcial.push_back(punto);
            if (factibilidad(sol_parcial) && optimalidad(sol_parcial, x, y) < best.obj) {
                backtracking(m, n, k, x, y, best, sol_parcial);
            }
            sol_parcial.pop_back();
        }
    }
}

double programacion_dinamica(int m, int n, int k, vector<double> x, vector<double> y, MejorSolucion& best) {
    vector<pair<double, double>> breakpoints = lista_breakpoints(m, n, x, y);
    vector<vector<int>> dp(k + 1, vector<int>(breakpoints.size(), BIG_NUMBER));
    
    // Initialize the first row of DP table
    for (size_t j = 0; j < breakpoints.size(); j++) {
        vector<pair<double, double>> segment = {breakpoints[0], breakpoints[j]};
        dp[1][j] = optimalidad(segment, x, y);
    }

    // Fill the rest of the DP table
    for (int i = 2; i <= k; i++) {
        for (size_t c = 1; c < breakpoints.size(); c++) {
            for (size_t l = 0; l < c; l++) {
                vector<pair<double, double>> segment = {breakpoints[l], breakpoints[c]};
                if (factibilidad(segment)) {
                    int error_segmento = optimalidad(segment, x, y);
                    dp[i][c] = min(dp[i][c], dp[i - 1][l] + error_segmento);
                }
            }
        }
    }

    return *min_element(dp[k].begin(), dp[k].end());
}

int main(int argc, char** argv) {
    char filenumber;
    cout << "Que tipo de instancia desea? Aspen (1), Ethanol Water(2), Optimistic(3), Titanium(4) o Toy(5)? Por favor coloque los numeros que indican la instancia" << endl;
    cin >> filenumber;
    string instance_name = "../../data/";
    switch (filenumber) {
        case '1': instance_name += "aspen_simulation.json"; break;
        case '2': instance_name += "ethanol_water_vle.json"; break;
        case '3': instance_name += "optimistic_instance.json"; break;
        case '4': instance_name += "titanium.json"; break;
        case '5': instance_name += "toy_instance.json"; break;
        default: cerr << "Input invalido. Por favor, reingrese un numero valido entre el (1-5)." << endl; return 1;
    }
    ifstream input(instance_name);
    if (!input.is_open()) {
        cerr << "Error opening file. Please check the file path and permissions." << endl;
        return 1;
    }
    json instance;
    input >> instance;
    input.close();
    int K = instance["n"];
    ofstream output("guardado_output.out");
    output << instance;
    output.close();

    int m = 6, n = 6, N = 5;
    vector<double> x, y; // These should be initialized with actual
