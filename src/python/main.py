import json
import numpy as np
import itertools
import matplotlib.pyplot as plt
BIG_NUMBER = 1e10 # Revisar si es necesario.

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
    breakpoints = lista_breakpoints(m, n,x,y)
    
    if len(sol_parcial) == k:
        if factibilidad(sol_parcial):
            current_error = optimalidad(sol_parcial, x, y)
            if current_error < best['obj']:
                best['obj'] = current_error
                best['sol'] = sol_parcial.copy()
    else:
        for punto in breakpoints:
                sol_parcial.append(punto)
                backtracking(m, n, k, best, x, y, sol_parcial)
                sol_parcial.remove(punto) 
def backtracking(m, n, k, best, x, y, sol_parcial=None):
    if sol_parcial is None:
        sol_parcial = []
    breakpoints = lista_breakpoints(m, n,x,y)
    
    if len(sol_parcial) == k:
        current_error = optimalidad(sol_parcial, x, y)
        if current_error < best['obj']:
            best['obj'] = current_error
            best['sol'] = sol_parcial.copy()
    else:
        for punto in breakpoints:
                sol_parcial.append(punto)
                if factibilidad(sol_parcial) and optimalidad(sol_parcial,x,y)<best['obj']:
                    backtracking(m, n, k, best, x, y, sol_parcial)

                sol_parcial.remove(punto) 

#Solucion Dinamica utilizando el metodo top-down
def dinamica(m, n, x, y, k, j=None, memo=None):
    if memo is None:
        memo = {}
    if j is None:
        breakpoints = lista_breakpoints(m, n, x, y)
        j = len(breakpoints) - 1
    else:
        breakpoints = lista_breakpoints(m, n, x, y)[:j+1]
    if k == 0 or j < 0:
        return BIG_NUMBER
    if k == 1:
        if factibilidad([breakpoints[0],breakpoints[j]]):
            return optimalidad([breakpoints[0], breakpoints[j]], x, y)
    if (k, j) in memo:
        return memo[(k, j)]

    min_error = BIG_NUMBER
    for i in range(j):
        current_error = optimalidad([breakpoints[i], breakpoints[j]], x, y)
        previous_error = dinamica(m, n, x, y, k-1, i, memo)
        min_error = min(min_error, previous_error + current_error)

    memo[(k, j)] = min_error
    return min_error

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
    instance_name = "optimistic_instance.json"
    filename = "./data/" + instance_name
    with open(filename) as f:
        instance = json.load(f)
    
    K = instance["n"]
    m = 8
    n = 8
    N = 4
    
    # Ejemplo para definir una grilla de m x n.
    #grid_x = np.linspace(min(instance["x"]), max(instance["x"]), num=m, endpoint=True)
    #grid_y = np.linspace(min(instance["y"]), max(instance["y"]), num=n, endpoint=True)
    
    best = {'obj': BIG_NUMBER, 'sol': set()}

    fuerza_bruta(m, n, 8, best, instance["x"], instance["y"])
    print("Error:", best['obj'])
    print("Mejor Solucion:", best['sol'])
    
    plottear_solucion(instance['x'], instance['y'], best['sol'])

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
