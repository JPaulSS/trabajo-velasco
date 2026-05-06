from conexion import *
import pytest
import requests

class Test_editoriales:

    def setup_class(self):
        self.url = "http://localhost:5083/editoriales"
        sql_pais = "INSERT IGNORE INTO paises (idPais, nombre, continente) VALUES ('CO', 'Colombia', 'America')"
        mi_cursor.execute(sql_pais)
        mi_db.commit()
        sql = "INSERT IGNORE INTO editoriales (idEditorial, nombre, idPais) VALUES ('ED01', 'Editorial Prueba', 'CO')"
        mi_cursor.execute(sql)
        mi_db.commit()

    def teardown_class(self):
        sql = "DELETE FROM editoriales WHERE idEditorial='ED01'"
        mi_cursor.execute(sql)
        mi_db.commit()

    def test_lista_editoriales(self):
        esperado = "editoriales"
        calculado = requests.get(self.url)
        assert calculado.status_code == 200
        assert calculado.json()["mensaje"] == esperado

    @pytest.mark.parametrize(
        ["nuevo_entrada", "esperado_entrada"],
        [
            ({"id": "ED99", "nombre": "Nueva Editorial", "idPais": "CO"}, "Editorial agregada con éxito"),
            ({"id": "ED01", "nombre": "Editorial Prueba", "idPais": "CO"}, "Id de editorial ya existe"),
        ]
    )
    def test_agregar(self, nuevo_entrada, esperado_entrada):
        calculado = requests.post(self.url, json=nuevo_entrada)
        assert calculado.status_code == 200
        assert esperado_entrada == calculado.json()["mensaje"]

    @pytest.mark.parametrize(
        ["id_entrada", "esperado_entrada"],
        [("ED01", "Editorial encontrada"), ("XXXX", "Editorial no encontrada")]
    )
    def test_busqueda(self, id_entrada, esperado_entrada):
        calculado = requests.get(f"{self.url}/{id_entrada}")
        assert calculado.status_code == 200
        assert esperado_entrada in calculado.json()["mensaje"]

    def test_modifica1(self):
        id = "ED01"
        nuevo = {"nombre": "Editorial Modificada", "idPais": "CO"}
        calculado = requests.put(f"{self.url}/{id}", json=nuevo)
        assert calculado.status_code == 200
        assert "Editorial modificada con éxito" in calculado.json()["mensaje"]

    def test_modifica2(self):
        id = "NOEXISTE"
        nuevo = {"nombre": "Nadie", "idPais": "CO"}
        calculado = requests.put(f"{self.url}/{id}", json=nuevo)
        assert calculado.status_code == 200
        assert "Editorial no existe" in calculado.json()["mensaje"]

    @pytest.mark.parametrize(
        ["id_entrada", "esperado_entrada"],
        [("ED99", "Editorial eliminada con éxito!"), ("NOEXISTE", "Editorial no existe")]
    )
    def test_elimina(self, id_entrada, esperado_entrada):
        calculado = requests.delete(f"{self.url}/{id_entrada}")
        assert calculado.status_code == 200
        assert esperado_entrada in calculado.json()["mensaje"]
