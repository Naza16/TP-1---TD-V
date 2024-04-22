import json
import time
import numpy as np
import matplotlib.pyplot as plt
start = time.time()
BIG_NUMBER = 1e10

def lista_breakpoints(m, n,x,y):
    """
    Genera una lista de todos los posibles breakpoints en una grilla m x n.
    """
    grid_x = np.linspace(min(x), max(x), num=m, endpoint=True)
    grid_y = np.linspace(min(y), max(y), num=n, endpoint=True)
    return [(x, y) for x in grid_x for y in grid_y]

def optimalidad(secuencia, x, y):
    """
    La funcion calcula el error de un conjunto de breakpoints.
    """
    error = 0
    for i in range(len(secuencia)-1):
        for j in range(len(x)):
            if x[j] > secuencia[i][0] and x[j] <= secuencia[i+1][0]:
                y_pendiente = secuencia[i+1][1] - secuencia[i][1]
                x_pendiente = secuencia[i+1][0] - secuencia[i][0]
                if x_pendiente == 0: continue
                m = y_pendiente / x_pendiente
                b = secuencia[i][1] - (m * secuencia[i][0])
                error += np.abs(y[j] - (m * x[j] + b))
    return error

def factibilidad(secuencia):
    """
    La funcion chequea si la combinacion de breakpoints cumple con los criterios de factibilidad.
    """
    for i in range(len(secuencia)-1):
       #Chequea si el siguiente breakpoint esta atras del actual o no
        if secuencia[i][0] >= secuencia[i+1][0]:
            return False
    return True

def fuerza_bruta(m, n, k, best, x, y, sol_parcial=None):
    if sol_parcial is None:
        sol_parcial = []
    breakpoints = lista_breakpoints(m, n, x, y)
    
    if len(sol_parcial) == k:
        if factibilidad(sol_parcial):
            current_error = optimalidad(sol_parcial, x, y)
            if current_error < best['obj']:
                best['obj'] = current_error
                best['sol'] = sol_parcial.copy()
        return

    for punto in breakpoints:
        if punto not in sol_parcial: 
            sol_parcial.append(punto)
            fuerza_bruta(m, n, k, best, x, y, sol_parcial)
            sol_parcial.remove(punto)

def backtracking(m, n, k, best, x, y, sol_parcial=None):
    if sol_parcial is None:
        sol_parcial = []
    breakpoints = lista_breakpoints(m, n,x,y)
    
    if len(sol_parcial) == k:
        current_error = optimalidad(sol_parcial, x, y)
        if current_error < best['obj'] and sol_parcial[k-1][0]>=x[len(x)-1]:
            best['obj'] = current_error
            best['sol'] = sol_parcial.copy()
    else:
        for punto in breakpoints:
                sol_parcial.append(punto)
                if factibilidad(sol_parcial) and optimalidad(sol_parcial,x,y)<best['obj'] and sol_parcial[0][0]<=x[0]:
                    backtracking(m, n, k, best, x, y, sol_parcial)

                sol_parcial.remove(punto) 


def dinamica(m, n, x, y, k):

    breakpoints = lista_breakpoints(m, n, x, y)
    dp = [[BIG_NUMBER for _ in range(len(breakpoints))] for _ in range(k + 1)]
    for j in range(len(breakpoints)):
        dp[1][j] = optimalidad([breakpoints[0], breakpoints[j]], x, y)
    for i in range(2, k + 1):
        for j in range(1, len(breakpoints)): 
            for l in range(j):
                if factibilidad([breakpoints[l], breakpoints[j]]):
                    error_segmento = optimalidad([breakpoints[l], breakpoints[j]], x, y)
                    dp[i][j] = min(dp[i][j], dp[i - 1][l] + error_segmento)
    return min(dp[k])



def plottear_solucion(x_data, y_data, breakpoints):
    plt.scatter(x_data, y_data, color='blue', label='Data Points')
    breakpoints = sorted(breakpoints, key=lambda point: point[0])
    x_breaks, y_breaks = zip(*breakpoints)
    plt.plot(x_breaks, y_breaks, color='red', marker='o', linestyle='-', linewidth=2, markersize=5, label='Piecewise Linear Fit')
    if x_breaks[0] > min(x_data):
        plt.plot([min(x_data), x_breaks[0]], [y_breaks[0], y_breaks[0]], 'r--', linewidth=1)
    if x_breaks[-1] < max(x_data):
        plt.plot([x_breaks[-1], max(x_data)], [y_breaks[-1], y_breaks[-1]], 'r--', linewidth=1)

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('PWL Plotteado Sobre los Datapoints')
    plt.legend()
    plt.show()

def main():
    # Ejemplo para leer una instancia con json
    instance_name = "titanium.json"
    filename = "../../data/" + instance_name
    with open(filename) as f:
        instance = json.load(f)
    
    K = instance["n"]
    m = 6
    n = 6
    N = 4
    
    best = {'obj': BIG_NUMBER, 'sol': set()}
    backtracking(m,n,6,best,instance['x'],instance['y'])
    print("Error:", best['obj'])
    print("Mejor Solucion:", best['sol'])
    plottear_solucion(instance['x'], instance['y'], best['sol'])

    #print(dinamica(m,n,instance['x'],instance['y'],50))
    end=time.time()
    print(end-start)
'''
	best = {}
	best['sol'] = [None]*(N+1)
	best['obj'] = BIG_NUMBER
	
	# Posible ejemplo (para la instancia titanium) de formato de solucion, y como exportarlo a JSON.
	# La solucion es una lista de tuplas (i,j), donde:
	# - i indica el indice del punto de la discretizacion de la abscisa
	# - j indica el indice del punto de la discretizacion de la ordenada.
	best['sol'] = [(0, 0), (1, 0), (2, 0), (3, 2), (4, 0), (5, 0)]
	best['obj'] = 5.927733333333335

	# Represetnamos la solucion con un diccionario que indica:
	# - n: cantidad de breakpoints
	# - x: lista con las coordenadas de la abscisa para cada breakpoint
	# - y: lista con las coordenadas de la ordenada para cada breakpoint
	solution = {}
	solution['n'] = len(best['sol'])
	solution['x'] = [grid_x[x[0]] for x in best['sol']]
	solution['y'] = [grid_y[x[1]] for x in best['sol']]
	solution['obj'] = best['obj']

	# Se guarda el archivo en formato JSON
	with open('solution_' + instance_name, 'w') as f:
		json.dump(solution, f)

'''
if __name__ == "__main__":
	main()
