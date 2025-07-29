"""
Tests unitarios para el normalizador de nombres usando pytest.
"""

import pytest
import pandas as pd
from nombre_normalizer import NombreNormalizer, normalizar_nombre_simple


class TestNombreNormalizer:
    """Tests para la clase NombreNormalizer."""
    
    @pytest.fixture
    def normalizador(self):
        """Fixture para crear una instancia del normalizador."""
        return NombreNormalizer()
    
    @pytest.mark.parametrize("entrada,esperado", [
        ("  Juan   Carlos  ", "Juan Carlos"),
        ("José-María", "José-María"),
        ("Juan@Carlos#", "JuanCarlos"),
        ("", ""),
        ("María José", "María José")
    ])
    def test_limpiar_texto(self, normalizador, entrada, esperado):
        """Test de limpieza de texto."""
        resultado = normalizador.limpiar_texto(entrada)
        assert resultado == esperado
    
    @pytest.mark.parametrize("entrada,esperado", [
        ("juan", "Juan"),
        ("MARIA", "Maria"),
        ("de", "de"),  # Partícula
        ("del", "del"),  # Partícula
        ("van", "van"),  # Partícula
        ("García", "García"),
        ("o'connor", "O'Connor"),
        ("jean-claude", "Jean-Claude")
    ])
    def test_capitalizar_palabra(self, normalizador, entrada, esperado):
        """Test de capitalización de palabras individuales."""
        resultado = normalizador.capitalizar_palabra(entrada)
        assert resultado == esperado
    
    @pytest.mark.parametrize("entrada,esperado,es_inicio", [
        ("juan carlos", "Juan Carlos", True),
        ("garcia de la torre", "Garcia de la Torre", True),
        ("de la cruz", "De la Cruz", True),  # Inicio
        ("maria jose", "Maria Jose", True),
        ("van der berg", "Van Der Berg", True)
    ])
    def test_capitalizar_nombre_completo(self, normalizador, entrada, esperado, es_inicio):
        """Test de capitalización de nombres completos."""
        resultado = normalizador.capitalizar_nombre_completo(entrada, es_inicio)
        assert resultado == esperado
    
    def test_es_probable_nombre(self, normalizador):
        """Test de detección de probabilidad de nombres."""
        # Nombres comunes deberían tener alta probabilidad
        assert normalizador.es_probable_nombre("Juan") > 0.8
        assert normalizador.es_probable_nombre("María") > 0.8
        
        # Apellidos comunes deberían tener baja probabilidad como nombres
        assert normalizador.es_probable_nombre("García") < 0.5
        assert normalizador.es_probable_nombre("López") < 0.5
        
        # Partículas deberían tener muy baja probabilidad
        assert normalizador.es_probable_nombre("de") < 0.2
        assert normalizador.es_probable_nombre("del") < 0.2
    
    @pytest.mark.parametrize("entrada,nom_esp,ape_esp,prob_esp", [
        ("Juan García", "Juan", "García", False),
        ("María José López", "María José", "López", False),
        ("Juan Carlos García Pérez", "Juan Carlos", "García Pérez", False),
        ("Pedro de la Torre", "Pedro", "de la Torre", False),
        ("Ana María García de la Cruz", "Ana María", "García de la Cruz", False)
    ])
    def test_separar_nombre_apellidos(self, normalizador, entrada, nom_esp, ape_esp, prob_esp):
        """Test de separación de nombres y apellidos."""
        nombres, apellidos, es_prob = normalizador.separar_nombre_apellidos(entrada)
        assert nombres == nom_esp
        assert apellidos == ape_esp
        # No verificamos es_prob exactamente porque depende de heurísticas
    
    @pytest.mark.parametrize("nombre,apellido,nom_esp,ape_esp", [
        ("juan carlos garcia", "", "Juan Carlos", "Garcia"),
        ("maria jose", "lopez perez", "Maria Jose", "Lopez Perez"),
        ("pedro de la torre", "", "Pedro", "De la Torre"),
        ("ANA MARIA", "GARCIA DE LA CRUZ", "Ana Maria", "Garcia de la Cruz")
    ])
    def test_normalizar_registro(self, normalizador, nombre, apellido, nom_esp, ape_esp):
        """Test de normalización completa de registro."""
        resultado = normalizador.normalizar_registro(nombre, apellido)
        assert resultado['nombres'] == nom_esp
        assert resultado['apellidos'] == ape_esp
        assert 'es_problematico' in resultado
        assert 'original_nombre' in resultado
    
    def test_procesar_dataframe(self, normalizador):
        """Test de procesamiento de DataFrame."""
        # Crear DataFrame de prueba
        data = {
            'nombre': ['juan carlos', 'maria jose garcia', 'pedro de la torre'],
            'apellido': ['garcia perez', '', 'martinez']
        }
        df = pd.DataFrame(data)
        
        # Procesar
        resultado = normalizador.procesar_dataframe(df, 'nombre', 'apellido')
        
        # Verificar estructura
        assert 'nombres_norm' in resultado.columns
        assert 'apellidos_norm' in resultado.columns
        assert 'es_problematico' in resultado.columns
        
        # Verificar contenido
        assert resultado.loc[0, 'nombres_norm'] == 'Juan Carlos'
        assert resultado.loc[0, 'apellidos_norm'] == 'Garcia Perez'
        assert resultado.loc[2, 'nombres_norm'] == 'Pedro de'
        assert resultado.loc[2, 'apellidos_norm'] == 'La Torre Martinez'
    
    @pytest.mark.parametrize("entrada,nom_esp,ape_esp", [
        ("", "", ""),  # Vacío
        ("Juan", "Juan", ""),  # Solo nombre
        ("de la Cruz", "De", "La Cruz"),  # Solo apellido con partícula
        ("María-José", "María-José", ""),  # Nombre con guión
        ("O'Connor", "O'Connor", ""),  # Nombre con apóstrofe
        ("Jean-Claude van Damme", "Jean-Claude", "Van Damme")  # Complejo
    ])
    def test_casos_especiales(self, normalizador, entrada, nom_esp, ape_esp):
        """Test de casos especiales y edge cases."""
        resultado = normalizador.normalizar_registro(entrada)
        assert resultado['nombres'] == nom_esp
        assert resultado['apellidos'] == ape_esp


class TestFuncionesConveniencia:
    """Tests para las funciones de conveniencia."""
    
    def test_normalizar_nombre_simple(self):
        """Test de la función de normalización simple."""
        resultado = normalizar_nombre_simple("juan carlos garcia de la torre")
        
        assert 'nombres' in resultado
        assert 'apellidos' in resultado
        assert 'es_problematico' in resultado
        assert resultado['nombres'] == 'Juan Carlos'
        assert resultado['apellidos'] == 'Garcia de la Torre'
    
    def test_normalizar_con_apellido_separado(self):
        """Test con nombre y apellido ya separados."""
        resultado = normalizar_nombre_simple("juan carlos", "garcia de la torre")
        
        assert resultado['nombres'] == 'Juan Carlos'
        assert resultado['apellidos'] == 'Garcia de la Torre'
        assert resultado['es_problematico'] is False


class TestCasosReales:
    """Tests con casos reales típicos."""
    
    @pytest.fixture
    def normalizador(self):
        """Fixture para crear una instancia del normalizador."""
        return NombreNormalizer()
    
    @pytest.mark.parametrize("entrada,nom_esp,ape_esp", [
        ("josé maría garcía rodríguez", "José María", "García Rodríguez"),
        ("ana isabel lópez de la fuente", "Ana Isabel", "López de la Fuente"),
        ("francisco javier martínez", "Francisco Javier", "Martínez"),
        ("maría del carmen santos", "María del Carmen", "Santos"),  # Nombre compuesto tradicional
        ("juan antonio fernández", "Juan Antonio", "Fernández")
    ])
    def test_nombres_españoles_tipicos(self, normalizador, entrada, nom_esp, ape_esp):
        """Test con nombres españoles típicos."""
        resultado = normalizador.normalizar_registro(entrada)
        assert resultado['nombres'] == nom_esp
        assert resultado['apellidos'] == ape_esp
    
    @pytest.mark.parametrize("entrada,nom_esp,ape_esp", [
        ("carlos alberto mendoza", "Carlos Alberto", "Mendoza"),
        ("ana lucia rodriguez", "Ana Lucia", "Rodriguez"),
        ("josé luis hernández", "José Luis", "Hernández"),
        ("maría elena vargas", "María Elena", "Vargas"),
        ("diego alejandro castillo", "Diego Alejandro", "Castillo")
    ])
    def test_nombres_latinoamericanos(self, normalizador, entrada, nom_esp, ape_esp):
        """Test con nombres latinoamericanos típicos."""
        resultado = normalizador.normalizar_registro(entrada)
        assert resultado['nombres'] == nom_esp
        assert resultado['apellidos'] == ape_esp
    
    @pytest.mark.parametrize("entrada,nom_esp,ape_esp", [
        ("pedro de la cruz y morales", "Pedro", "De la Cruz y Morales"),
        ("ana maría de los santos", "Ana María", "De los Santos"),
        ("juan carlos van der berg", "Juan Carlos", "Van Der Berg"),
        ("maría josé da silva", "María José", "Da Silva"),
        ("francisco de las heras", "Francisco", "De las Heras")
    ])
    def test_nombres_con_particulas_complejas(self, normalizador, entrada, nom_esp, ape_esp):
        """Test con partículas complejas."""
        resultado = normalizador.normalizar_registro(entrada)
        assert resultado['nombres'] == nom_esp
        assert resultado['apellidos'] == ape_esp


# Tests adicionales para funcionalidades específicas de pytest
class TestErrorHandling:
    """Tests para manejo de errores."""
    
    @pytest.fixture
    def normalizador(self):
        return NombreNormalizer()
    
    def test_normalizar_con_none(self, normalizador):
        """Test con valores None."""
        
        resultado = normalizador.normalizar_registro(None)
        assert resultado['nombres'] == ''
        assert resultado['apellidos'] == ''
    
    def test_dataframe_columnas_inexistentes(self, normalizador):
        """Test con columnas que no existen en el DataFrame."""
        df = pd.DataFrame({'col1': ['test']})
        with pytest.raises(KeyError):
            normalizador.procesar_dataframe(df, 'nombre_inexistente', 'apellido_inexistente')


class TestTildesYAcentos:
    """Tests específicos para verificar conservación de tildes."""
    
    @pytest.fixture
    def normalizador(self):
        return NombreNormalizer()
    
    @pytest.mark.parametrize("entrada,nombres_esperados,apellidos_esperados", [
        ("josé maría", "José María", ""),
        ("maria jose", "Maria Jose", ""),
        ("josé luis hernández", "José Luis", "Hernández"),
        ("maria elena garcia", "Maria Elena", "Garcia"),
        ("andrés gonzález", "Andrés", "González"),
        ("jose antonio lopez", "Jose Antonio", "Lopez"),
    ])
    def test_conservacion_tildes(self, normalizador, entrada, nombres_esperados, apellidos_esperados):
        """Test para verificar que se conservan las tildes."""
        resultado = normalizador.normalizar_registro(entrada)
        assert resultado['nombres'] == nombres_esperados
        assert resultado['apellidos'] == apellidos_esperados
    
    def test_limpiar_texto_conserva_tildes(self, normalizador):
        """Test específico para la función limpiar_texto."""
        casos = [
            ("josé maría", "josé maría"),
            ("MARÍA JOSÉ", "MARÍA JOSÉ"),  
            ("José-María", "José-María"),
            ("  José   María  ", "José María"),
        ]
        
        for entrada, esperado in casos:
            resultado = normalizador.limpiar_texto(entrada)
            assert resultado == esperado, f"Entrada: '{entrada}' -> Esperado: '{esperado}' -> Obtenido: '{resultado}'"


# Markers para categorizar tests
@pytest.mark.slow
class TestRendimiento:
    """Tests de rendimiento - marcados como lentos."""
    
    @pytest.fixture
    def normalizador(self):
        return NombreNormalizer()
    
    def test_procesamiento_lote_grande(self, normalizador):
        """Test con un lote grande de nombres."""
        # Crear DataFrame grande
        nombres = ['juan carlos'] * 1000
        apellidos = ['garcia perez'] * 1000
        df = pd.DataFrame({'nombre': nombres, 'apellido': apellidos})
        
        resultado = normalizador.procesar_dataframe(df, 'nombre', 'apellido')
        assert len(resultado) == 1000
        assert all(resultado['nombres_norm'] == 'Juan Carlos')


class TestNombresCompuestos:
    """Tests específicos para nombres compuestos."""
    
    @pytest.fixture
    def normalizador(self):
        return NombreNormalizer()
    
    @pytest.mark.parametrize("entrada,nombres_esperados,apellidos_esperados", [
        ("maría del carmen santos", "María del Carmen", "Santos"),
        ("jose maria garcia", "Jose Maria", "Garcia"),
        ("ana maria lopez", "Ana Maria", "Lopez"),
        ("juan carlos perez", "Juan Carlos", "Perez"),
        ("luis miguel hernández", "Luis Miguel", "Hernández"),
        ("maria de los angeles torres", "Maria de los Angeles", "Torres"),
        ("francisco javier martínez lópez", "Francisco Javier", "Martínez López"),
        ("maria del rosario garcia de la cruz", "Maria del Rosario", "Garcia de la Cruz"),
    ])
    def test_nombres_compuestos_tradicionales(self, normalizador, entrada, nombres_esperados, apellidos_esperados):
        """Test para nombres compuestos tradicionales."""
        resultado = normalizador.normalizar_registro(entrada)
        assert resultado['nombres'] == nombres_esperados
        assert resultado['apellidos'] == apellidos_esperados
        assert not resultado['es_problematico']  # No deberían ser problemáticos
    
    def test_patron_nombre_particula_nombre_apellido(self, normalizador):
        """Test para patrón [nombre] [partícula] [nombre] [apellidos]."""
        casos = [
            ("pedro de la cruz martínez", "Pedro", "De la Cruz Martínez"),
            ("ana del carmen lopez", "Ana del Carmen", "Lopez"),
            ("carlos de los santos perez", "Carlos", "De los Santos Perez"),
        ]
        
        for entrada, nombres_esp, apellidos_esp in casos:
            resultado = normalizador.normalizar_registro(entrada)
            assert resultado['nombres'] == nombres_esp
            assert resultado['apellidos'] == apellidos_esp


if __name__ == '__main__':
    # Para ejecutar los tests
    pytest.main([__file__, '-v'])