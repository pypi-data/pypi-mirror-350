"""
Normalizador de Nombres y Apellidos en Español
==============================================

Módulo para normalizar nombres y apellidos en español, separando correctamente
nombres de apellidos y aplicando las reglas de capitalización apropiadas.

Autor: Assistant
Versión: 1.1.0 - Mejorado con soporte completo para tildes
"""

import re
import unicodedata
from typing import Dict, List, Tuple, Optional, Union
import pandas as pd


class NombreNormalizer:
    """
    Clase principal para normalizar nombres y apellidos en español.
    
    Versión mejorada que incluye:
    - Redistribución inteligente de apellidos desde el campo nombre
    - Detección de patrones de apellidos con partículas
    - Combinación inteligente de apellidos sin duplicación
    """
    
    def __init__(self):
        """Inicializa el normalizador con diccionarios y reglas predefinidas."""
        self.particulas = self._load_particulas()
        self.nombres_comunes = self._load_nombres_comunes()
        self.apellidos_comunes = self._load_apellidos_comunes()
        self.nombres_compuestos = self._load_nombres_compuestos()
        self.casos_problema = []
    
    def _crear_variantes_tildes(self, palabras: List[str]) -> set:
        """
        Crea un conjunto que incluye tanto las versiones con tildes como sin tildes.
        
        Args:
            palabras (List[str]): Lista de palabras base
            
        Returns:
            set: Conjunto con todas las variantes
        """
        resultado = set()
        
        for palabra in palabras:
            # Agregar versión original
            resultado.add(palabra.lower())
            
            # Agregar versión sin tildes
            sin_tildes = unicodedata.normalize('NFKD', palabra.lower())
            sin_tildes = ''.join(c for c in sin_tildes if not unicodedata.combining(c))
            resultado.add(sin_tildes)
            
            # Agregar versiones con tildes comunes para palabras sin tildes
            if palabra.lower() == sin_tildes:  # Si la palabra original no tenía tildes
                variantes_con_tildes = self._generar_variantes_con_tildes(palabra)
                resultado.update(variantes_con_tildes)
        
        return resultado
    
    def _generar_variantes_con_tildes(self, palabra: str) -> List[str]:
        """
        Genera variantes comunes con tildes para una palabra.
        
        Args:
            palabra (str): Palabra sin tildes
            
        Returns:
            List[str]: Lista de variantes con tildes
        """
        # Mapeo de vocales sin tilde a con tilde
        mapeo_tildes = {
            'a': ['á'], 'e': ['é'], 'i': ['í'], 'o': ['ó'], 'u': ['ú']
        }
        
        variantes = []
        palabra_lower = palabra.lower()
        
        # Para nombres comunes conocidos, generar variantes específicas
        variantes_especificas = {
            'jesus': ['jesús'],
            'angel': ['ángel'],
            'adrian': ['adrián'],
            'oscar': ['óscar'],
            'raul': ['raúl'],
            'ruben': ['rubén'],
            'ivan': ['iván'],
            'angeles': ['ángeles'],
            'monica': ['mónica'],
            'andrea': ['andrea', 'andrés'],  # Andrés como variante masculina
            'lucia': ['lucía'],
            'maria': ['maría'],
            'jose': ['josé'],
            'antonio': ['antonio', 'antônio'],
            'ramon': ['ramón'],
            'simon': ['simón'],
            'tomas': ['tomás'],
            'nicolas': ['nicolás'],
            'sebastian': ['sebastián'],
            'martin': ['martín'],
            'german': ['germán'],
            'julian': ['julián'],
            'fabian': ['fabián'],
            'adrian': ['adrián'],
            'dario': ['darío'],
            'mario': ['mario', 'mário'],
            'victor': ['víctor'],
            'hector': ['héctor'],
            'nestor': ['néstor'],
            'cesar': ['césar'],
            'felix': ['félix']
        }
        
        if palabra_lower in variantes_especificas:
            variantes.extend(variantes_especificas[palabra_lower])
        
        return variantes
    
    def _load_particulas(self) -> set:
        """
        Carga el conjunto de partículas que deben ir en minúscula.
        
        Returns:
            set: Conjunto de partículas en español
        """
        particulas_base = [
            'de', 'del', 'de la', 'de los', 'de las', 'y', 'e', 'i',
            'van', 'von', 'da', 'dos', 'das', 'do', 'san', 'santa',
            'santo', 'ben', 'ibn', 'al', 'el', 'la', 'los', 'las',
            'mc', 'mac', 'o', 'di', 'du', 'le', 'lo'
        ]
        
        return self._crear_variantes_tildes(particulas_base)
    
    def _load_nombres_comunes(self) -> set:
        """
        Carga diccionario de nombres comunes en español con variantes de tildes.
        
        Returns:
            set: Conjunto de nombres frecuentes
        """
        nombres_base = [
            # Nombres masculinos
            'josé', 'jose', 'maría', 'maria', 'antonio', 'francisco', 'manuel', 'david',
            'juan', 'javier', 'daniel', 'carlos', 'miguel', 'rafael',
            'pedro', 'ángel', 'angel', 'alejandro', 'fernando', 'sergio', 'pablo',
            'jorge', 'alberto', 'luis', 'álvaro', 'alvaro', 'adrián', 'adrian', 'óscar', 'oscar',
            'roberto', 'rubén', 'ruben', 'iván', 'ivan', 'raúl', 'raul', 'jesús', 'jesus', 'marcos',
            'diego', 'gabriel', 'eduardo', 'ricardo', 'santiago', 'andrés', 'andres',
            'ramón', 'ramon', 'simón', 'simon', 'tomás', 'tomas', 'nicolás', 'nicolas',
            'sebastián', 'sebastian', 'martín', 'martin', 'germán', 'german',
            'julián', 'julian', 'fabián', 'fabian', 'darío', 'dario', 'mario',
            'víctor', 'victor', 'héctor', 'hector', 'néstor', 'nestor', 'césar', 'cesar',
            'félix', 'felix', 'ignacio', 'emilio', 'agustín', 'agustin', 'esteban',
            
            # Nombres femeninos
            'ana', 'carmen', 'dolores', 'pilar', 'teresa', 'ángeles', 'angeles',
            'mercedes', 'rosario', 'francisca', 'antonia', 'isabel',
            'cristina', 'marta', 'elena', 'concepción', 'concepcion', 'laura',
            'josefa', 'manuela', 'rosa', 'montserrat', 'margarita',
            'esperanza', 'amparo', 'remedios', 'encarnación', 'encarnacion', 'asunción', 'asuncion',
            'mónica', 'monica', 'andrea', 'lucía', 'lucia', 'patricia', 'raquel',
            'silvia', 'beatriz', 'natalia', 'rocío', 'rocio', 'gloria', 'inmaculada',
            'verónica', 'veronica', 'susana', 'yolanda', 'nuria', 'soledad',
            'irene', 'guadalupe', 'milagros', 'aurora', 'consuelo', 'victoria',
            'celia', 'sonia', 'alicia', 'nerea', 'claudia', 'sandra'
        ]
        
        return self._crear_variantes_tildes(nombres_base)

    def _load_nombres_compuestos(self) -> set:
        """Carga nombres compuestos tradicionales con variantes de tildes."""
        nombres_compuestos_base = [
            'maría del carmen', 'maria del carmen',
            'maría de los angeles', 'maria de los angeles', 'maría de los ángeles', 'maria de los ángeles',
            'maría del rosario', 'maria del rosario',
            'maría del pilar', 'maria del pilar',
            'maría de la cruz', 'maria de la cruz',
            'maría de los dolores', 'maria de los dolores',
            'maría del socorro', 'maria del socorro',
            'maría de la paz', 'maria de la paz',
            'maría de las mercedes', 'maria de las mercedes',
            'josé maría', 'jose maria', 'josé maría', 'jose maría',
            'juan carlos', 'luis miguel', 'carlos alberto',
            'ana maría', 'ana maria', 'ana isabel', 'maría josé', 'maria jose', 'maría elena', 'maria elena',
            'francisco javier', 'juan antonio', 'josé luis', 'jose luis', 'josé manuel', 'jose manuel',
            'miguel ángel', 'miguel angel', 'rafael ángel', 'rafael angel', 'diego alejandro', 'pedro pablo',
            'maría teresa', 'maria teresa', 'maría cristina', 'maria cristina', 
            'maría fernanda', 'maria fernanda', 'maría victoria', 'maria victoria',
            'juan josé', 'juan jose', 'carlos andrés', 'carlos andres',
            'luis fernando', 'josé antonio', 'jose antonio', 'maría guadalupe', 'maria guadalupe'
        ]
        
        return self._crear_variantes_tildes(nombres_compuestos_base)

    def _load_apellidos_comunes(self) -> set:
        """
        Carga diccionario de apellidos comunes en español con variantes de tildes.
        
        Returns:
            set: Conjunto de apellidos frecuentes
        """
        apellidos_base = [
            'garcía', 'garcia', 'rodríguez', 'rodriguez', 'martínez', 'martinez', 
            'lópez', 'lopez', 'gonzález', 'gonzalez',
            'hernández', 'hernandez', 'pérez', 'perez', 'sánchez', 'sanchez', 
            'ramírez', 'ramirez', 'cruz',
            'flores', 'gómez', 'gomez', 'díaz', 'diaz', 'reyes', 'morales', 'jiménez', 'jimenez',
            'ruiz', 'gutiérrez', 'gutierrez', 'ortiz', 'torres', 'méndez', 'mendez', 'vargas',
            'castillo', 'álvarez', 'alvarez', 'herrera', 'vázquez', 'vazquez', 'ramos',
            'moreno', 'romero', 'medina', 'soto', 'contreras',
            'aguilar', 'guerrero', 'rojas', 'mendoza', 'vega',
            'muñoz', 'munoz', 'marín', 'marin', 'delgado', 'castro', 'ortega',
            'rubio', 'núñez', 'nunez', 'iglesias', 'calvo', 'prieto',
            'peña', 'pena', 'león', 'leon', 'serrano', 'blanco', 'suárez', 'suarez',
            'ramos', 'vidal', 'molina', 'lozano', 'pardo', 'silva',
            'durán', 'duran', 'cortés', 'cortes', 'domínguez', 'dominguez',
            'garrido', 'carrasco', 'fernández', 'fernandez', 'torre', 'torres'
        ]
        
        return self._crear_variantes_tildes(apellidos_base)
    
    def limpiar_texto(self, texto: str) -> str:
        """
        Limpia y normaliza el texto de entrada.
        
        Args:
            texto (str): Texto a limpiar
            
        Returns:
            str: Texto limpio y normalizado
        """
        if not isinstance(texto, str):
            return ""
        
        # Normalizar unicode y eliminar acentos para comparaciones
        texto = unicodedata.normalize('NFKC', texto.strip())
        # Eliminar espacios múltiples
        texto = re.sub(r'\s+', ' ', texto)
        # Eliminar caracteres especiales excepto guiones y apostrofes
        texto = re.sub(r'[^\w\s\-\'\.]', '', texto, flags=re.UNICODE)
        
        return texto.strip()
    
    def capitalizar_palabra(self, palabra: str, es_inicio: bool = False) -> str:
        """
        Capitaliza una palabra según las reglas del español.
        
        Args:
            palabra (str): Palabra a capitalizar
            es_inicio (bool): Si es el inicio de la cadena
            
        Returns:
            str: Palabra correctamente capitalizada
        """
        if not palabra:
            return palabra
        
        palabra_lower = palabra.lower()
        
        # Si es una partícula, mantenerla en minúscula
        if palabra_lower in self.particulas and not es_inicio:
            return palabra_lower
        
        # Casos especiales con guiones o apostrofes
        if '-' in palabra:
            partes = palabra.split('-')
            return '-'.join([self.capitalizar_palabra(parte) for parte in partes])
        
        if "'" in palabra:
            partes = palabra.split("'")
            return "'".join([parte.capitalize() for parte in partes])
        
        # Caso normal: primera letra mayúscula
        return palabra_lower.capitalize()
    
    def capitalizar_nombre_completo(self, nombre_completo: str, es_inicio: bool = False) -> str:
        """
        Capitaliza un nombre completo respetando las partículas.
        
        Args:
            nombre_completo (str): Nombre completo a capitalizar
            es_inicio (bool): Si es el inicio de la cadena (para partículas)
            
        Returns:
            str: Nombre correctamente capitalizado
        """
        if not nombre_completo:
            return ""
        
        palabras = nombre_completo.strip().split()
        if not palabras:
            return ""
        
        resultado = []
        for i, palabra in enumerate(palabras):
            # La primera palabra siempre se capitaliza, incluso si es partícula
            if i == 0 and es_inicio:
                resultado.append(self.capitalizar_palabra(palabra.capitalize(), es_inicio))
            else:
                resultado.append(self.capitalizar_palabra(palabra))
        
        return ' '.join(resultado)
    
    def es_probable_nombre(self, palabra: str) -> float:
        """
        Calcula la probabilidad de que una palabra sea un nombre.
        
        Args:
            palabra (str): Palabra a evaluar
            
        Returns:
            float: Probabilidad (0-1) de que sea un nombre
        """
        palabra_lower = palabra.lower()
        
        # Comparar tanto con tildes como sin tildes
        if palabra_lower in self.nombres_comunes:
            return 0.9
        elif palabra_lower in self.apellidos_comunes:
            return 0.2
        elif palabra_lower in self.particulas:
            return 0.1
        else:
            # Heurísticas adicionales
            if len(palabra) <= 3:
                return 0.3  # Nombres cortos menos probables
            elif palabra.endswith(('ez', 'az', 'oz', 'is')):
                return 0.3  # Terminaciones típicas de apellidos
            else:
                return 0.5  # Neutral
    
    def encontrar_punto_corte_apellidos(self, palabras: List[str]) -> Optional[int]:
        """
        NUEVA FUNCIÓN: Encuentra el punto óptimo para separar apellidos del campo nombre.
        
        Args:
            palabras (List[str]): Lista de palabras del campo nombre
            
        Returns:
            Optional[int]: Índice donde cortar, o None si no se encuentra
        """
        if len(palabras) <= 1:
            return None
        
        # Patrón 1: Partícula + Apellido al final
        for i in range(len(palabras) - 1, 0, -1):
            palabra_actual = palabras[i].lower()
            if palabra_actual in self.apellidos_comunes:
                # Verificar si hay partícula antes
                if i > 0 and palabras[i-1].lower() in self.particulas:
                    return i - 1  # Cortar antes de la partícula
                else:
                    return i  # Cortar antes del apellido
        
        # Patrón 2: Secuencia de apellidos al final
        contador_apellidos_consecutivos = 0
        for i in range(len(palabras) - 1, -1, -1):
            if palabras[i].lower() in self.apellidos_comunes:
                contador_apellidos_consecutivos += 1
            else:
                break
        
        if contador_apellidos_consecutivos >= 1:
            return len(palabras) - contador_apellidos_consecutivos
        
        # Patrón 3: Heurística por posición y probabilidades
        if len(palabras) > 3:
            prob_penultima = self.es_probable_nombre(palabras[-2])
            prob_ultima = self.es_probable_nombre(palabras[-1])
            
            if prob_penultima < 0.4 and prob_ultima < 0.4:
                return len(palabras) - 2
            elif prob_ultima < 0.3:
                return len(palabras) - 1
        
        return None
    
    def combinar_apellidos(self, apellidos_del_nombre: str, apellidos_originales: str) -> str:
        """
        NUEVA FUNCIÓN: Combina apellidos evitando duplicaciones.
        
        Args:
            apellidos_del_nombre (str): Apellidos extraídos del campo nombre
            apellidos_originales (str): Apellidos del campo apellido original
            
        Returns:
            str: Apellidos combinados sin duplicación
        """
        if not apellidos_del_nombre.strip():
            return apellidos_originales
        
        if not apellidos_originales.strip():
            return apellidos_del_nombre
        
        # Verificar si hay traslape/duplicación
        apellidos_del_nombre_palabras = apellidos_del_nombre.lower().split()
        apellidos_originales_palabras = apellidos_originales.lower().split()
        
        # Buscar duplicados
        hay_duplicados = False
        for palabra in apellidos_del_nombre_palabras:
            if palabra in apellidos_originales_palabras:
                hay_duplicados = True
                break
        
        if hay_duplicados:
            # Mantener solo los apellidos originales para evitar confusión
            return apellidos_originales
        else:
            # Combinar: apellidos del nombre + apellidos originales
            return f"{apellidos_del_nombre} {apellidos_originales}".strip()
    
    def _verificar_nombre_compuestos(self, palabras, length):
        for i in range(len(palabras) - length + 1):
            nombre_2_palabras = ' '.join(palabras[i:i+length]).lower()
            if nombre_2_palabras in self.nombres_compuestos:
                if i == 0:  # Al inicio
                    nombres = ' '.join(palabras[:i+length])
                    apellidos = ' '.join(palabras[i+length:]) if i+length < len(palabras) else ""
                    return nombres, apellidos
        return None
    
    def separar_nombre_apellidos(self, nombre_completo: str) -> Tuple[str, str, bool]:
        """Versión mejorada que reconoce nombres compuestos con tildes."""
        palabras = nombre_completo.strip().split()
        
        if len(palabras) <= 1:
            return nombre_completo, "", len(palabras) == 1
        
        if len(palabras) == 2:
            nombres_compuestos = self._verificar_nombre_compuestos(palabras, 2)
            if nombres_compuestos:
                return nombres_compuestos[0], "", False
            else:
                return palabras[0], palabras[1], False
        
        # NUEVA LÓGICA: Buscar nombres compuestos conocidos (ahora con soporte para tildes)
        texto_lower = nombre_completo.lower()
        
        # Verificar nombres compuestos de 2 palabras
        for i in range(2, 5):
            nombres_compuestos = self._verificar_nombre_compuestos(palabras, i)
            if nombres_compuestos:
                nombres, apellidos = nombres_compuestos
                return nombres, apellidos, False
            
        for i in range(len(palabras) - 1):
            nombre_2_palabras = ' '.join(palabras[i:i+2]).lower()
            if nombre_2_palabras in self.nombres_compuestos:
                if i == 0:  # Al inicio
                    nombres = ' '.join(palabras[:i+2])
                    apellidos = ' '.join(palabras[i+2:]) if i+2 < len(palabras) else ""
                    return nombres, apellidos, False
        
        # Verificar nombres compuestos de 3 palabras
        for i in range(len(palabras) - 2):
            nombre_3_palabras = ' '.join(palabras[i:i+3]).lower()
            if nombre_3_palabras in self.nombres_compuestos:
                if i == 0:  # Al inicio
                    nombres = ' '.join(palabras[:i+3])
                    apellidos = ' '.join(palabras[i+3:]) if i+3 < len(palabras) else ""
                    return nombres, apellidos, False
        
        # Verificar nombres compuestos de 4 palabras
        for i in range(len(palabras) - 3):
            nombre_4_palabras = ' '.join(palabras[i:i+4]).lower()
            if nombre_4_palabras in self.nombres_compuestos:
                if i == 0:  # Al inicio
                    nombres = ' '.join(palabras[:i+4])
                    apellidos = ' '.join(palabras[i+4:]) if i+4 < len(palabras) else ""
                    return nombres, apellidos, False
        # Si no hay nombres compuestos, usar lógica original mejorada
        return self._separar_con_heuristicas(palabras)
    
    def _separar_con_heuristicas(self, palabras: List[str]) -> Tuple[str, str, bool]:
        """Lógica de heurísticas mejorada."""
        probabilidades = [self.es_probable_nombre(palabra) for palabra in palabras]
        
        # NUEVA HEURÍSTICA: Si tenemos patrón [nombre_alto] [partícula] [nombre_alto] [apellido_bajo]
        # Considerar los primeros 3 como nombres
        if len(palabras) >= 4:
            if (probabilidades[0] > 0.8 and  # Nombre común
                palabras[1].lower() in self.particulas and  # Partícula
                probabilidades[2] > 0.8 and  # Otro nombre común
                probabilidades[3] < 0.5):    # Probable apellido
                
                nombres = ' '.join(palabras[:3])
                apellidos = ' '.join(palabras[3:])
                return nombres, apellidos, False
        
        # Lógica original como fallback
        mejor_corte = 1
        mejor_score = 0
        
        for i in range(1, len(palabras)):
            score_nombres = sum(probabilidades[:i]) / i
            score_apellidos = sum(1 - p for p in probabilidades[i:]) / (len(palabras) - i)
            score_total = score_nombres + score_apellidos
            
            if score_total > mejor_score:
                mejor_score = score_total
                mejor_corte = i
        
        nombres = ' '.join(palabras[:mejor_corte])
        apellidos = ' '.join(palabras[mejor_corte:])
        es_problematico = mejor_score < 1.0 or len(palabras) > 4
        
        return nombres, apellidos, es_problematico
    
    def normalizar_registro(self, nombre: str, apellido: str = "") -> Dict[str, Union[str, bool]]:
        """
        FUNCIÓN MEJORADA: Normaliza un registro con redistribución inteligente.
        
        Args:
            nombre (str): Campo nombre (puede incluir apellidos)
            apellido (str): Campo apellido (opcional)
            
        Returns:
            Dict: Diccionario con nombres y apellidos normalizados
        """
        # Limpiar entradas
        nombre_limpio = self.limpiar_texto(nombre)
        apellido_limpio = self.limpiar_texto(apellido)
        
        # NUEVA LÓGICA: Analizar redistribución incluso con apellido existente
        if apellido_limpio:
            # Analizar si el campo nombre tiene apellidos al final
            partes_nombre = nombre_limpio.split()
            
            # Buscar punto de corte óptimo en el campo nombre
            punto_corte = self.encontrar_punto_corte_apellidos(partes_nombre)
            
            if punto_corte is not None:
                # Redistribuir
                nombres_reales = ' '.join(partes_nombre[:punto_corte])
                apellidos_del_nombre = ' '.join(partes_nombre[punto_corte:])
                
                # Combinar apellidos: los del nombre + los del campo apellido
                apellidos_combinados = self.combinar_apellidos(apellidos_del_nombre, apellido_limpio)
                
                nombres_final = self.capitalizar_nombre_completo(nombres_reales, True)
                apellidos_final = self.capitalizar_nombre_completo(apellidos_combinados, True)
                es_problematico = False
            else:
                # No hay redistribución necesaria, usar lógica original
                nombres_final = self.capitalizar_nombre_completo(nombre_limpio, True)
                apellidos_final = self.capitalizar_nombre_completo(apellido_limpio, True)
                es_problematico = False
        else:
            # Lógica original para cuando no hay apellido separado
            nombres_sep, apellidos_sep, es_problematico = self.separar_nombre_apellidos(nombre_limpio)
            nombres_final = self.capitalizar_nombre_completo(nombres_sep, True)
            apellidos_final = self.capitalizar_nombre_completo(apellidos_sep, True)
        
        resultado = {
            'nombres': nombres_final,
            'apellidos': apellidos_final,
            'es_problematico': es_problematico,
            'original_nombre': nombre,
            'original_apellido': apellido
        }
        
        if es_problematico:
            self.casos_problema.append(resultado)
        
        return resultado
    
    def procesar_dataframe(self, df: pd.DataFrame, col_nombre: str, 
                          col_apellido: str = None, inplace: bool = False) -> pd.DataFrame:
        """
        Procesa un DataFrame completo normalizando nombres y apellidos.
        
        Args:
            df (pd.DataFrame): DataFrame a procesar
            col_nombre (str): Nombre de la columna con nombres
            col_apellido (str): Nombre de la columna con apellidos (opcional)
            inplace (bool): Si modificar el DataFrame original
            
        Returns:
            pd.DataFrame: DataFrame con columnas normalizadas
        """
        if not inplace:
            df = df.copy()
        
        # Resetear casos problema
        self.casos_problema = []
        
        # Procesar cada fila
        resultados = []
        for idx, row in df.iterrows():
            nombre = row[col_nombre] if pd.notna(row[col_nombre]) else ""
            apellido = row[col_apellido] if col_apellido and pd.notna(row[col_apellido]) else ""
            
            resultado = self.normalizar_registro(nombre, apellido)
            resultados.append(resultado)
        
        # Agregar columnas normalizadas
        df['nombres_norm'] = [r['nombres'] for r in resultados]
        df['apellidos_norm'] = [r['apellidos'] for r in resultados]
        df['es_problematico'] = [r['es_problematico'] for r in resultados]
        
        return df
    
    def obtener_casos_problema(self) -> List[Dict]:
        """
        Retorna la lista de casos problemáticos detectados.
        
        Returns:
            List[Dict]: Lista de casos que requieren revisión manual
        """
        return self.casos_problema
    
    def exportar_casos_problema(self, archivo: str = "casos_problema.csv"):
        """
        Exporta los casos problemáticos a un archivo CSV.
        
        Args:
            archivo (str): Nombre del archivo de salida
        """
        if self.casos_problema:
            df_problemas = pd.DataFrame(self.casos_problema)
            df_problemas.to_csv(archivo, index=False, encoding='utf-8')
            print(f"Exportados {len(self.casos_problema)} casos problemáticos a {archivo}")
        else:
            print("No hay casos problemáticos para exportar")


# Funciones de conveniencia para uso directo
def normalizar_nombre_simple(nombre: str, apellido: str = "") -> Dict[str, str]:
    """
    Función de conveniencia para normalizar un nombre simple.
    
    Args:
        nombre (str): Nombre a normalizar
        apellido (str): Apellido (opcional)
        
    Returns:
        Dict[str, str]: Resultado normalizado
    """
    normalizador = NombreNormalizer()
    return normalizador.normalizar_registro(nombre, apellido)


def procesar_csv(archivo_entrada: str, archivo_salida: str, 
                col_nombre: str, col_apellido: str = None) -> None:
    """
    Función de conveniencia para procesar un archivo CSV completo.
    
    Args:
        archivo_entrada (str): Ruta del archivo CSV de entrada
        archivo_salida (str): Ruta del archivo CSV de salida
        col_nombre (str): Nombre de la columna con nombres
        col_apellido (str): Nombre de la columna con apellidos (opcional)
    """
    # Leer CSV
    df = pd.read_csv(archivo_entrada, encoding='utf-8')
    
    # Procesar
    normalizador = NombreNormalizer()
    df_procesado = normalizador.procesar_dataframe(df, col_nombre, col_apellido)
    
    # Guardar resultado
    df_procesado.to_csv(archivo_salida, index=False, encoding='utf-8')
    
    # Exportar casos problema si los hay
    if normalizador.casos_problema:
        archivo_problemas = archivo_salida.replace('.csv', '_problemas.csv')
        normalizador.exportar_casos_problema(archivo_problemas)
    
    print(f"Procesamiento completado. Resultado guardado en {archivo_salida}")



if __name__ == "__main__":
    # Ejemplo de uso mejorado con tildes
    print("=== Normalizador de Nombres y Apellidos (v1.1.0) ===")
    
    # Pruebas con tildes
    casos_prueba = [
        "juan carlos garcía de la torre",
        "maría josé lópez martínez", 
        "jesús miguel ángel rodríguez",
        "josé maría fernández pérez",
        "ana maría de los ángeles gonzález"
    ]
    
    normalizador = NombreNormalizer()
    
    for caso in casos_prueba:
        resultado = normalizar_nombre_simple(caso)
        print(f"\nEntrada: '{caso}'")
        print(f"Nombres: {resultado['nombres']}")
        print(f"Apellidos: {resultado['apellidos']}")
        print(f"Problemático: {resultado['es_problematico']}")
    
    # Mostrar tamaños de diccionarios
    print(f"\n=== Estadísticas de Diccionarios ===")
    print(f"Nombres comunes: {len(normalizador.nombres_comunes)} entradas")
    print(f"Apellidos comunes: {len(normalizador.apellidos_comunes)} entradas")
    print(f"Nombres compuestos: {len(normalizador.nombres_compuestos)} entradas")
    print(f"Partículas: {len(normalizador.particulas)} entradas")