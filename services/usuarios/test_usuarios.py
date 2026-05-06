from conexion import *
import pytest
import requests
import hashlib

class Test_usuarios:

    def setup_class(self):
        self.url = "http://localhost:5080/usuarios"
        id = "final881"
        nombre = "Fidel Nalisco"
        contra = hashlib.sha512("4321".encode("UTF-8")).hexdigest()
        sql = f"INSERT IGNORE INTO usuarios (idUsuario,nombre,contrasena) VALUES ('{id}','{nombre}','{contra}')"
        mi_cursor.execute(sql)
        mi_db.commit()

    def teardown_class(self):
        sql = f"DELETE FROM usuarios WHERE idUsuario='final881'"
        mi_cursor.execute(sql)
        mi_db.commit()

    def test_lista_usuarios(self):
        esperado = "usuarios"
        calculado = requests.get(self.url)
        assert calculado.status_code == 200
        assert calculado.json()["mensaje"] == esperado
    
    @pytest.mark.parametrize(
        ["nuevo_entrada","esperado_entrada"],
        [({"id":"test2026", "nombre":"Usuario Pruebas","contrasena":"6666"},"Usuario agregado con éxito"),
         ({"id":"final881", "nombre":"Fidel Nalisco", "contrasena":"1111"},"Id de usuario ya existe")]
    )
    def test_agregar(self,nuevo_entrada,esperado_entrada):
        contra = hashlib.sha512(nuevo_entrada["contrasena"].encode("UTF-8")).hexdigest()
        nuevo_entrada["contrasena"] = contra
        calculado = requests.post(self.url,json=nuevo_entrada)
        assert calculado.status_code == 200
        assert esperado_entrada == calculado.json()["mensaje"]

    @pytest.mark.parametrize(
        ["id_entrada","contra_entrada","esperado_entrada"],
        [("final881","4321",{"mensaje":"Bienvenido Fidel Nalisco"}),
         ("final881","1234",{"mensaje":"Credenciales inválidas"}),
         ("118final","hgtr",{"mensaje":"Credenciales inválidas"})]
    )
    def test_login(self,id_entrada,contra_entrada,esperado_entrada):
        id = id_entrada
        contra = hashlib.sha512(contra_entrada.encode("UTF-8")).hexdigest()
        usuario = {"id":id, "contra":contra}
        calculado = requests.post(f"{self.url}/{id}",json=usuario)
        assert calculado.status_code == 200
        assert calculado.json() == esperado_entrada

    @pytest.mark.parametrize(
        ["id_entrada","esperado_entrada"],
        [("final881","Usuario encontrado"), ("118final","Usuario no encontrado")]
    )
    def test_busqueda(self,id_entrada,esperado_entrada):
        calculado = requests.get(f"{self.url}/{id_entrada}")
        assert calculado.status_code == 200
        assert esperado_entrada in calculado.json()["mensaje"]

    def test_modifica1(self):
        id = "final881"
        nombre = "Fidelino Nalisco"
        contra = hashlib.sha512("4321".encode("UTF-8")).hexdigest()
        nuevo = {"id":id, "nombre":nombre, "contrasena":contra}
        calculado = requests.put(f"{self.url}/{id}",json=nuevo)
        assert calculado.status_code == 200
        assert "Usuario modificado con éxito" in calculado.json()["mensaje"]

    def test_modifica2(self):
        id = "testfail"
        nombre = "Fidelino Nalisco"
        contra = hashlib.sha512("9876".encode("UTF-8")).hexdigest()
        nuevo = {"id":id, "nombre":nombre, "contrasena":contra}
        calculado = requests.put(f"{self.url}/{id}",json=nuevo)
        assert calculado.status_code == 200
        assert "Usuario no existe" in calculado.json()["mensaje"]

    @pytest.mark.parametrize(
        ["id_entrada","esperado_entrada"],
        [("test2026","Usuario eliminado con éxito!"), ("testfail","Usuario no existe")]
    )
    def test_elimina(self,id_entrada, esperado_entrada):
        calculado = requests.delete(f"{self.url}/{id_entrada}")
        assert calculado.status_code == 200
        assert esperado_entrada in calculado.json()["mensaje"]
