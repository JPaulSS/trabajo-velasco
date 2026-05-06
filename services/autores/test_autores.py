from conexion import *
import pytest
import requests

class Test_autores:

    def setup_class(self):
        self.url = "http://localhost:5081/autores"
        
        sql_pais = "INSERT IGNORE INTO paises (idPais, nombre, continente) VALUES ('CO', 'Colombia', 'America')"
        mi_cursor.execute(sql_pais)
        mi_db.commit()
        
        sql = "INSERT IGNORE INTO autores (idAutor, nombre, email, idPais) VALUES ('AU001', 'Autor de Prueba', 'prueba@test.com', 'CO')"
        mi_cursor.execute(sql)
        mi_db.commit()


    def test_lista_autores(self):
        esperado = "autores"
        # Ejecutar la prueba
        calculado = requests.get(self.url)
        # Verificación
        assert calculado.status_code == 200
        assert calculado.json()["mensaje"] == esperado

    @pytest.mark.parametrize(
        ["nuevo_entrada", "esperado_entrada"],
        [
            # Caso exitoso: autor nuevo
            ({"id": "AU999", "nombre": "Nuevo Autor", "email": "nuevo@test.com", "idPais": "CO"}, "Autor agregado con éxito"),
            # Caso fallido: autor ya existe
            ({"id": "AU001", "nombre": "Autor de Prueba", "email": "prueba@test.com", "idPais": "CO"}, "Id de autor ya existe"),
        ]
    )
    def test_agregar(self, nuevo_entrada, esperado_entrada):
        # Ejecutar la prueba
        calculado = requests.post(self.url, json=nuevo_entrada)
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado_entrada == calculado.json()["mensaje"]

    @pytest.mark.parametrize(
        ["id_entrada", "esperado_entrada"],
        [
            ("AU001", "Autor encontrado"),   # Existe
            ("XXXX",  "Autor no encontrado"), # No existe
        ]
    )
    def test_busqueda(self, id_entrada, esperado_entrada):
        id = id_entrada
        esperado = esperado_entrada
        # Ejecutar la prueba
        calculado = requests.get(f"{self.url}/{id}")
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado in calculado.json()["mensaje"]

    def test_modifica1(self):
        id = "AU001"
        nombre = "Autor Modificado"
        email = "modificado@test.com"
        idPais = "CO"
        nuevo = {"nombre": nombre, "email": email, "idPais": idPais}
        esperado = "Autor modificado con éxito"
        # Ejecutar la prueba
        calculado = requests.put(f"{self.url}/{id}", json=nuevo)
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado in calculado.json()["mensaje"]
        # Verificar en la base de datos que el cambio quedó guardado
        sql = f"SELECT * FROM autores WHERE idAutor='{id}'"
        mi_cursor.execute(sql)
        datos = mi_cursor.fetchall()[0]
        assert nombre == datos[1] and email == datos[2]

    def test_modifica2(self):
        id = "NOEXISTE"
        nuevo = {"nombre": "Nadie", "email": "nadie@test.com", "idPais": "CO"}
        esperado = "Autor no existe"
        # Ejecutar la prueba
        calculado = requests.put(f"{self.url}/{id}", json=nuevo)
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado in calculado.json()["mensaje"]

    @pytest.mark.parametrize(
        ["id_entrada", "esperado_entrada"],
        [
            ("AU999",    "Autor eliminado con éxito!"), # Existe (se creó en test_agregar)
            ("NOEXISTE", "Autor no existe"),             # No existe
        ]
    )
    def test_elimina(self, id_entrada, esperado_entrada):
        id = id_entrada
        esperado = esperado_entrada
        # Ejecutar la prueba
        calculado = requests.delete(f"{self.url}/{id}")
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado in calculado.json()["mensaje"]
        # Si se eliminó, verificar que ya no esté en la BD
        if "éxito" in esperado_entrada:
            mi_db.commit()
            sql = f"SELECT * FROM autores WHERE idAutor='{id}'"
            mi_cursor.execute(sql)
            datos = mi_cursor.fetchall()
            assert len(datos) == 0
