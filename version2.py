import csv
import random
import matplotlib.pyplot as plt
import pandas as pd

num_particulas = 50
num_iteraciones = 100
c1 = 1.0
c2 = 2.0
w = 0.9
factor_reduccion = 0.99
lista_tabu = []
max_tabu_size = 10

def cargar_csv(path):
    with open(path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]

recursos = cargar_csv('./recursos.csv')
profesores = [r for r in recursos if r['Tipo'] == 'Profesor']
materias = [r for r in recursos if r['Tipo'] == 'Materia']
aulas = [r for r in recursos if r['Tipo'] == 'Salón']
disponibilidad_horarios = cargar_csv('./disponibilidad.csv')

def generar_solucion_aleatoria():
    solucion = []
    profesores_aleatorios = random.sample(profesores, len(profesores))
    for profesor in profesores_aleatorios:
        materia = random.choice(materias)
        aula = random.choice(aulas)
        disponibilidad_filtrada = [h for h in disponibilidad_horarios if h['RecursoID'] == aula['RecursoID']]
        if not disponibilidad_filtrada:
            continue
        disponibilidad = random.choice(disponibilidad_filtrada)
        solucion.append({
            'profesor': profesor['Nombre'],
            'materia': materia['Nombre'],
            'aula': aula['Nombre'],
            'dia': disponibilidad['Día'],
            'horario_inicio': disponibilidad['HorarioInicio'],
            'horario_fin': disponibilidad['HorarioFin']
        })
        
        
    return solucion

def calcular_fitness(solucion):
    penalizaciones = 0
    for i, asignacion in enumerate(solucion):
        for j in range(i + 1, len(solucion)):
            if (
                asignacion['dia'] == solucion[j]['dia'] and asignacion['horario_inicio'] < solucion[j]['horario_fin'] and
                asignacion['horario_fin'] > solucion[j]['horario_inicio']
            ):
                penalizaciones += 1
            if asignacion['profesor'] == solucion[j]['profesor'] and (asignacion['dia'] == solucion[j]['dia'] and
                asignacion['horario_inicio'] < solucion[j]['horario_fin'] and asignacion['horario_fin'] > solucion[j]['horario_inicio']):
                penalizaciones += 1
            if asignacion['aula'] == solucion[j]['aula'] and (
                asignacion['dia'] == solucion[j]['dia'] and
                asignacion['horario_inicio'] < solucion[j]['horario_fin'] and
                asignacion['horario_fin'] > solucion[j]['horario_inicio']
            ):
                penalizaciones += 1
    return -penalizaciones

def mutar_posicion(posicion):
    if random.random() < 0.4:
        idx = random.randint(0, len(posicion) - 1)
        recurso_id = posicion[idx]['aula']
        disponibilidad_filtrada = [h for h in disponibilidad_horarios if h['RecursoID'] == recurso_id]
        if not disponibilidad_filtrada:
            nueva_aula = random.choice(aulas)
            posicion[idx]['aula'] = nueva_aula['RecursoID']
            disponibilidad_filtrada = [h for h in disponibilidad_horarios if h['RecursoID'] == nueva_aula['RecursoID']]
        if not disponibilidad_filtrada:
            return posicion
        nueva_disponibilidad = random.choice(disponibilidad_filtrada)
        posicion[idx].update({
            'dia': nueva_disponibilidad['Día'],
            'horario_inicio': nueva_disponibilidad['HorarioInicio'],
            'horario_fin': nueva_disponibilidad['HorarioFin']
        })
    return posicion

def ajustar_posicion(posicion, velocidad):
    nueva_posicion = []
    for asignacion in posicion:
        disponibilidad = [h for h in disponibilidad_horarios if h['RecursoID'] == asignacion['aula']]
        if disponibilidad:
            indice_actual = next((i for i, h in enumerate(disponibilidad) if h['HorarioInicio'] == asignacion['horario_inicio']), -1)
            nuevo_indice = (indice_actual + int(round(velocidad))) % len(disponibilidad)
            nueva_posicion.append({
                'profesor': asignacion['profesor'],
                'materia': asignacion['materia'],
                'aula': asignacion['aula'],
                'dia': disponibilidad[nuevo_indice]['Día'],
                'horario_inicio': disponibilidad[nuevo_indice]['HorarioInicio'],
                'horario_fin': disponibilidad[nuevo_indice]['HorarioFin']
            })
        else:
            nueva_posicion.append(asignacion)
    return nueva_posicion

def actualizar_particulas_con_tabu(particulas, g_best):
    global w
    for particula in particulas:
        particula['velocidad'] = (
            w * particula['velocidad'] +
            c1 * random.random() * (calcular_fitness(particula['p_best']) - calcular_fitness(particula['posicion'])) +
            c2 * random.random() * (calcular_fitness(g_best['posicion']) - calcular_fitness(particula['posicion']))
        )
        particula['posicion'] = ajustar_posicion(particula['posicion'], particula['velocidad'])
        particula['posicion'] = mutar_posicion(particula['posicion'])
        if particula['posicion'] in lista_tabu:
            particula['posicion'] = generar_solucion_aleatoria()
        particula['fitness'] = calcular_fitness(particula['posicion'])
        if particula['fitness'] > calcular_fitness(particula['p_best']):
            particula['p_best'] = particula['posicion']
        if len(lista_tabu) >= max_tabu_size:
            lista_tabu.pop(0)
        lista_tabu.append(particula['posicion'])

def inicializar_particulas():
    particulas = []
    contador = 0  # Contador para las partículas impresas
    for _ in range(num_particulas):
        solucion_inicial = generar_solucion_aleatoria()
        particula = {
            'posicion': solucion_inicial,
            'velocidad': random.uniform(0, 1.0),
            'p_best': solucion_inicial,
            'fitness': calcular_fitness(solucion_inicial)
        }
        particulas.append(particula)
        if contador < 3:  # Imprimir solo las primeras tres partículas
            print(f"Partícula {contador + 1}: {particula}")
            contador += 1
    return particulas


def ejecutar_pso():
    global w
    particulas = inicializar_particulas()
    g_best = max(particulas, key=lambda p: p['fitness'])
    evolucion_fitness = []
    for iteracion in range(num_iteraciones):
        print(f"Iteración {iteracion + 1}/{num_iteraciones} - Mejor Fitness hasta ahora: {g_best['fitness']}")
        actualizar_particulas_con_tabu(particulas, g_best)
        mejor_particula = max(particulas, key=lambda p: p['fitness'])
        if mejor_particula['fitness'] > g_best['fitness']:
            g_best = mejor_particula
            print(f"Nueva mejor solución encontrada en la iteración {iteracion + 1} con fitness: {g_best['fitness']}")
        w *= factor_reduccion
        evolucion_fitness.append(g_best['fitness'])
    print(f"Mejor solución encontrada: Fitness = {g_best['fitness']}")
    return g_best, evolucion_fitness

def guardar_tabla_horarios(solucion, filename="horario.png"):
    df = pd.DataFrame(solucion)
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis('off')
    ax.axis('tight')
    table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.auto_set_column_width(col=list(range(len(df.columns))))
    plt.savefig(filename)
    plt.close()

def graficar_convergencia(evolucion):
    mejor_iteracion = evolucion.index(max(evolucion))
    plt.plot(evolucion, label="Fitness por Iteración")
    plt.scatter(mejor_iteracion, max(evolucion), color='red', label="Mejor Solución")
    plt.title("Convergencia del algoritmo PSO")
    plt.xlabel("Iteraciones")
    plt.ylabel("Mejor Fitness")
    plt.legend()
    plt.grid()
    plt.show()

print("Recursos cargados:", len(recursos))
print("Disponibilidad cargada:", len(disponibilidad_horarios))
resultado, evolucion = ejecutar_pso()
guardar_tabla_horarios(resultado['posicion'], filename="horario.png")
graficar_convergencia(evolucion)
