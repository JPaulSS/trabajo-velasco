
from conexion import *

class Autores:

    def listar(self):
        # Trae todos los autores de la base de datos
        sql = "SELECT * FROM autores"
        mi_cursor.execute(sql)
        resultado = mi_cursor.fetchall()
        return resultado

    def consultar(self, id):
        # Busca un autor por su idAutor
        sql = f"SELECT * FROM autores WHERE idAutor='{id}'"
        mi_cursor.execute(sql)
        resultado = mi_cursor.fetchall()
        return resultado

    def agregar(self, id, nombre, email, idPais):
        # Inserta un nuevo autor en la tabla
        sql = f"INSERT INTO autores (idAutor, nombre, email, idPais) VALUES ('{id}', '{nombre}', '{email}', '{idPais}')"
        mi_cursor.execute(sql)
        mi_db.commit()

    def modificar(self, id, nombre, email, idPais):
        # Actualiza los datos de un autor existente
        sql = f"UPDATE autores SET nombre='{nombre}', email='{email}', idPais='{idPais}' WHERE idAutor='{id}'"
        mi_cursor.execute(sql)
        mi_db.commit()
        return self.consultar(id)

    def eliminar(self, id):
        # Elimina un autor de la tabla
        sql = f"DELETE FROM autores WHERE idAutor='{id}'"
        mi_cursor.execute(sql)
        mi_db.commit()

# Instancia global del modelo
mis_autores = Autores()
