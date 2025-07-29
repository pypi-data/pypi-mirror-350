# Nombre Normalizer ES

[![PyPI version](https://badge.fury.io/py/nombre-normalizer-es.svg)](https://badge.fury.io/py/nombre-normalizer-es)
[![Python](https://img.shields.io/pypi/pyversions/nombre-normalizer-es.svg)](https://pypi.org/project/nombre-normalizer-es/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Una biblioteca completa para normalizar nombres y apellidos en español con redistribución inteligente y detección de patrones avanzada.

## Características principales

🎯 **Redistribución inteligente**: Detecta y redistribuye apellidos mezclados en el campo nombre
🔍 **Detección de patrones**: Reconoce nombres compuestos tradicionales españoles
🔤 **Manejo de tildes**: Normaliza automáticamente acentos y caracteres especiales
📊 **Procesamiento masivo**: Procesa DataFrames completos de forma eficiente
🚨 **Detección de casos problemáticos**: Identifica registros que requieren revisión manual
⚡ **Alto rendimiento**: Optimizado para grandes volúmenes de datos

## Instalación

```bash
pip install nombre-normalizer-es
```

## Uso básico

### Normalización simple

```python
from nombre_normalizer import NombreNormalizer

# Crear instancia del normalizador
normalizador = NombreNormalizer()

# Normalizar un nombre simple
resultado = normalizador.normalizar_registro("JUAN CARLOS GARCIA LOPEZ")
print(resultado['nombres'])    # "Juan Carlos"
print(resultado['apellidos'])  # "García López"

# Con redistribución inteligente
resultado = normalizador.normalizar_registro(
    nombre="Maria del Carmen Fernandez Rodriguez",
    apellido="Martinez"
)
print(resultado['nombres'])    # "María del Carmen"
print(resultado['apellidos'])  # "Fernández Rodríguez Martínez"
```

### Función de conveniencia

```python
from nombre_normalizer import normalizar_nombre_simple

resultado = normalizar_nombre_simple("jose maria de la cruz")
print(resultado['nombres'])    # "José María de la Cruz"
print(resultado['apellidos'])  # ""
```

### Procesamiento de DataFrames

```python
import pandas as pd
from nombre_normalizer import NombreNormalizer

# Crear datos de ejemplo
df = pd.DataFrame({
    'nombre_completo': [
        'JUAN CARLOS GARCIA LOPEZ',
        'maria del carmen rodriguez',
        'JOSE LUIS DE LA TORRE MARTINEZ'
    ]
})

# Procesar DataFrame
normalizador = NombreNormalizer()
df_procesado = normalizador.procesar_dataframe(
    df, 
    col_nombre='nombre_completo'
)

# Ver resultados
print(df_procesado[['nombres_norm', 'apellidos_norm']])
```

### Procesamiento de archivos CSV

```python
from nombre_normalizer import procesar_csv

# Procesar archivo CSV completo
procesar_csv(
    archivo_entrada='datos_originales.csv',
    archivo_salida='datos_normalizados.csv',
    col_nombre='nombre',
    col_apellido='apellido'  # Opcional
)
```

## Características avanzadas

### Detección de nombres compuestos

La biblioteca reconoce automáticamente nombres compuestos tradicionales españoles:

```python
normalizador = NombreNormalizer()

# Nombres compuestos con partículas
resultado = normalizador.normalizar_registro("MARIA DE LOS ANGELES GARCIA")
print(resultado['nombres'])    # "María de los Ángeles"
print(resultado['apellidos'])  # "García"

# Nombres dobles tradicionales
resultado = normalizador.normalizar_registro("JOSE MARIA FERNANDEZ LOPEZ")
print(resultado['nombres'])    # "José María"
print(resultado['apellidos'])  # "Fernández López"
```

### Manejo de partículas

Las partículas se mantienen en minúscula según las reglas del español:

```python
resultado = normalizador.normalizar_registro("juan de la torre")
print(resultado['nombres'])    # "Juan"
print(resultado['apellidos'])  # "de la Torre"
```

### Detección de casos problemáticos

```python
normalizador = NombreNormalizer()

# Procesar varios registros
registros = [
    "NOMBRE COMPLEJO CON MUCHAS PALABRAS QUE ES DIFICIL DE SEPARAR",
    "JUAN CARLOS GARCIA LOPEZ",
    "X Y Z"  # Caso problemático
]

for registro in registros:
    resultado = normalizador.normalizar_registro(registro)
    if resultado['es_problematico']:
        print(f"⚠️  Revisar: {registro}")

# Obtener todos los casos problemáticos
casos_problema = normalizador.obtener_casos_problema()
print(f"Encontrados {len(casos_problema)} casos problemáticos")

# Exportar casos problemáticos a CSV
normalizador.exportar_casos_problema("revision_manual.csv")
```

## Ejemplos de casos de uso

### 1. Limpieza de base de datos de clientes

```python
import pandas as pd
from nombre_normalizer import NombreNormalizer

# Cargar datos
df = pd.read_csv('clientes.csv')

# Normalizar
normalizador = NombreNormalizer()
df_limpio = normalizador.procesar_dataframe(
    df, 
    col_nombre='nombre_cliente',
    col_apellido='apellido_cliente'
)

# Guardar resultado
df_limpio.to_csv('clientes_normalizados.csv', index=False)

# Revisar casos problemáticos
if normalizador.casos_problema:
    print(f"⚠️  {len(normalizador.casos_problema)} casos requieren revisión")
    normalizador.exportar_casos_problema('clientes_revisar.csv')
```

### 2. Procesamiento de formularios web

```python
from nombre_normalizer import normalizar_nombre_simple

def procesar_formulario(datos_formulario):
    """Procesa y normaliza datos de un formulario web"""
    
    resultado = normalizar_nombre_simple(
        nombre=datos_formulario.get('nombre_completo', ''),
        apellido=datos_formulario.get('apellidos', '')
    )
    
    return {
        'nombres_normalizados': resultado['nombres'],
        'apellidos_normalizados': resultado['apellidos'],
        'requiere_revision': resultado['es_problematico']
    }

# Ejemplo de uso
datos = {'nombre_completo': 'maria del carmen garcia lopez'}
resultado = procesar_formulario(datos)
print(resultado)
```

### 3. Análisis de datos con pandas

```python
import pandas as pd
from nombre_normalizer import NombreNormalizer

# Cargar datos
df = pd.read_excel('empleados.xlsx')

# Normalizar nombres
normalizador = NombreNormalizer()
df = normalizador.procesar_dataframe(df, 'nombre_completo')

# Análisis post-normalización
print("Estadísticas de normalización:")
print(f"- Total registros: {len(df)}")
print(f"- Casos problemáticos: {df['es_problematico'].sum()}")
print(f"- Nombres únicos: {df['nombres_norm'].nunique()}")

# Encontrar posibles duplicados por nombre
duplicados = df.groupby(['nombres_norm', 'apellidos_norm']).size()
duplicados = duplicados[duplicados > 1]
print(f"- Posibles duplicados: {len(duplicados)}")
```

## API Reference

### Clase NombreNormalizer

#### `__init__()`
Inicializa el normalizador con diccionarios predefinidos de nombres, apellidos y partículas españolas.

#### `normalizar_registro(nombre: str, apellido: str = "") -> Dict`
Normaliza un registro individual.

**Parámetros:**
- `nombre` (str): Campo nombre (puede incluir apellidos)
- `apellido` (str): Campo apellido (opcional)

**Retorna:**
- `dict` con claves: `nombres`, `apellidos`, `es_problematico`, `original_nombre`, `original_apellido`

#### `procesar_dataframe(df: DataFrame, col_nombre: str, col_apellido: str = None, inplace: bool = False) -> DataFrame`
Procesa un DataFrame completo.

**Parámetros:**
- `df` (DataFrame): DataFrame a procesar
- `col_nombre` (str): Nombre de la columna con nombres
- `col_apellido` (str): Nombre de la columna con apellidos (opcional)
- `inplace` (bool): Si modificar el DataFrame original

**Retorna:**
- `DataFrame` con columnas adicionales: `nombres_norm`, `apellidos_norm`, `es_problematico`

#### `obtener_casos_problema() -> List[Dict]`
Retorna la lista de casos problemáticos detectados durante el procesamiento.

#### `exportar_casos_problema(archivo: str = "casos_problema.csv")`
Exporta los casos problemáticos a un archivo CSV para revisión manual.

### Funciones de conveniencia

#### `normalizar_nombre_simple(nombre: str, apellido: str = "") -> Dict`
Función de conveniencia para normalizar un nombre simple sin crear una instancia de la clase.

#### `procesar_csv(archivo_entrada: str, archivo_salida: str, col_nombre: str, col_apellido: str = None)`
Función de conveniencia para procesar un archivo CSV completo.

## Casos especiales manejados

### Nombres compuestos reconocidos
- María del Carmen, María de los Ángeles, José María, Juan Carlos, etc.
- Nombres con partículas religiosas: María del Socorro, María de la Paz
- Nombres dobles tradicionales: Ana María, José Luis, Miguel Ángel

### Partículas manejadas
- `de`, `del`, `de la`, `de los`, `de las`
- `y`, `e`, `i`
- `van`, `von`, `da`, `dos`, `das`, `do`
- `san`, `santa`, `santo`
- `mc`, `mac`, `o`, `di`, `du`, `le`, `lo`

### Normalización de acentos
- Manejo automático de tildes y caracteres especiales
- Reconocimiento de variantes con y sin acentos
- Normalización Unicode completa

## Requisitos

- Python 3.8+
- pandas >= 1.3.0
- unicodedata2 >= 15.0.0 (para Python < 3.13)

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Soporte

Si encuentras algún problema o tienes sugerencias:

- Abre un [issue](https://github.com/KeepCoding/normalize_tools/issues)
- Contacta al mantenedor: rmr@keepcoding.io

## Changelog

### v1.0.0
- Versión inicial
- Normalización inteligente de nombres y apellidos españoles
- Redistribución automática de apellidos
- Detección de casos problemáticos
- Soporte para procesamiento masivo con pandas