# Optimización por Enjambre de Partículas (PSO) con Lista Tabú

Este proyecto implementa el algoritmo **PSO** (Optimización por Enjambre de Partículas) adaptado para resolver un problema **combinatorio**, específicamente la asignación de horarios para profesores, materias, aulas y horarios, con restricciones adicionales gestionadas mediante una lista tabú.

## Funcionalidad
El objetivo del algoritmo es generar asignaciones válidas que minimicen los conflictos establecidos como:
- **Conflicto por profesores:** Profesores asignados a múltiples materias en el mismo horario.
- **Conflicto de logística (aulas):** Aulas utilizadas simultáneamente para diferentes clases.
- **Solapamiento:** Solapamientos de horarios entre asignaciones.
cada una de estas restricciones al ser violadas afectan directamente al cálculo del fitness de una solución

### Características principales
- **PSO Adaptado**: Ajuste de "posiciones" y "velocidades" para un problema combinatorio.
- **Lista Tabú**: Evita que las partículas revisiten soluciones ya exploradas.
- **Mutación**: Introduce cambios aleatorios para explorar soluciones más diversas.
- **Reducción del peso inercial**: Comienza con exploración amplia y termina con un enfoque más preciso.

## Partes del Código: Acontinuacion se ofrece una guía sobre lo implmentado en el código
### 1. **Carga de datos**
La función `cargar_csv` importa recursos y disponibilidad desde archivos CSV. Los datos se dividen en:
- **Profesores**
- **Materias**
- **Aulas**
- **Disponibilidad de horarios**

### 2. **Partículas**
Cada partícula representa una posible solución, estructurada como una lista de asignaciones (profesor, materia, aula, horario).

### 3. **Funciones principales**
#### a) **Generar soluciones iniciales**
La función `generar_solucion_aleatoria` crea soluciones asignando horarios aleatorios a los profesores disponibles.

#### b) **Calcular fitness**
La función `calcular_fitness` evalúa la calidad de una solución penalizando los conflictos de:
- Horarios solapados.
- Profesores con múltiples asignaciones simultáneas.
- Aulas compartidas en el mismo horario.

#### c) **Mutar posición**
La función `mutar_posicion` introduce cambios aleatorios en una solución para evitar quedar atrapado en óptimos locales.

#### d) **Ajustar posición**
La función `ajustar_posicion` actualiza la posición de una partícula basándose en su velocidad y en restricciones válidas del problema, como la disponibilidad de horarios.

#### e) **Lista tabú**
Implementada dentro de `actualizar_particulas_con_tabu`, asegura que las partículas no repitan soluciones exploradas anteriormente.

#### f) **Ejecución del algoritmo**
La función `ejecutar_pso` realiza las iteraciones del PSO:
- Calcula nuevas posiciones y velocidades.
- Evalúa el fitness de las partículas.
- Actualiza la mejor solución global y personal.
- Aplica reducción del peso inercial para transicionar de exploración a explotación.

### 4. **Generación de resultados**
#### a) **Tabla de horarios**
Se genera una imagen `horario.png` mostrando la mejor asignación encontrada.

#### b) **Gráfica de convergencia**
Muestra cómo evoluciona el mejor fitness a lo largo de las iteraciones, destacando la iteración donde se alcanzó la mejor solución.

## Parámetros del Algoritmo
| Parámetro         | Descripción                                | Valor Predeterminado |
|-------------------|--------------------------------------------|----------------------|
| `num_particulas`  | Número de partículas en el enjambre        | 50                   |
| `num_iteraciones` | Máximo de iteraciones                      | 100                  |
| `c1`              | Coeficiente cognitivo (exploración)        | 1.0                  |
| `c2`              | Coeficiente social (explotación)           | 2.0                  |
| `w`               | Peso inercial                              | 0.9                  |
| `factor_reduccion`| Reducción del peso inercial por iteración  | 0.99                 |
| `max_tabu_size`   | Tamaño máximo de la lista tabú             | 10                   |

## Cómo Ejecutar
1. Asegúrate de tener Python 3 instalado.
2. Instala las dependencias necesarias:
   ```bash
   pip install matplotlib pandas
   ```
3. Coloca los archivos `recursos.csv` y `disponibilidad.csv` en el mismo directorio que el script.
4. Ejecuta el script principal:
   ```bash
   python version2.py
   ```

## Archivos Generados
- **`horario.png`**: Imagen con la mejor asignación de horarios encontrada.
- **Gráfica de convergencia**: Se muestra en pantalla al finalizar el algoritmo.

## Adaptaciones al PSO Clásico
- Uso de una lista tabú para manejar soluciones repetidas.
- Representación combinatoria de posiciones y velocidades.
- Mutación discreta para diversificar las soluciones.

## Conclusión
Este proyecto adapta PSO para resolver problemas combinatorios, implementando estrategias avanzadas como lista tabú y mutación discreta para mejorar su rendimiento en este contexto.

