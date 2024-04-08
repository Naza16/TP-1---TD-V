import json
import numpy as np
import itertools
BIG_NUMBER = 1e10 # Revisar si es necesario.

def lista_breakpoints(m, n,x,y):
    """
    Genera una lista de todos los posibles breakpoints en una grilla m x n.
    """
    grid_x = np.linspace(min(x), max(x), num=m, endpoint=True)
    grid_y = np.linspace(min(y), max(y), num=n, endpoint=True)
    return [(x, y) for x in grid_x for y in grid_y]

def generar_breakpoints(breakpoints, k):
    """
    Devuelve una lista con todas las posibles combinaciones de k breakpoints.
    """
    return list(itertools.combinations(breakpoints, k))

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

def brute_force(m, n, k,best, x, y):
    puntos = lista_breakpoints(m, n,x,y)
    breakpoints = generar_breakpoints(puntos, k)
    
    for bp in breakpoints:
        if factibilidad(bp):
            error = optimalidad(bp, x, y)
            if error < best['obj']:
                best['obj'] = error
                best['sol'] = bp
                
    return best
    
def main():

	# Ejemplo para leer una instancia con json
	instance_name = "titanium.json"
	filename = "./data/" + instance_name
	with open(filename) as f:
		instance = json.load(f)
	
	K = instance["n"]
	m = 6
	n = 6
	N = 5
	
	# Ejemplo para definir una grilla de m x n.
	grid_x = np.linspace(min(instance["x"]), max(instance["x"]), num=m, endpoint=True)
	grid_y = np.linspace(min(instance["y"]), max(instance["y"]), num=n, endpoint=True)
    
	best = {'obj': float('inf'), 'sol': set()}
	sol_parcial = set()
	result = brute_force(m, n, K, best, instance["x"], instance["y"])
	print("Best Objective:", result['obj'])
	print("Best Solution:", result['sol'])

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

if __name__ == "__main__":
	main()