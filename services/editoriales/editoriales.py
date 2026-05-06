from conexion import *

class Editoriales:

    def listar(self):
        # Trae todas las editoriales de la base de datos
        sql = "SELECT * FROM editoriales"
        mi_cursor.execute(sql)
        resultado = mi_cursor.fetchall()
        return resultado

    def consultar(self, id):
        # Busca una editorial por su idEditorial
        sql = f"SELECT * FROM editoriales WHERE idEditorial='{id}'"
        mi_cursor.execute(sql)
        resultado = mi_cursor.fetchall()
        return resultado

    def agregar(self, id, nombre, idPais):
        # Inserta una nueva editorial en la tabla
        sql = f"INSERT INTO editoriales (idEditorial, nombre, idPais) VALUES ('{id}', '{nombre}', '{idPais}')"
        mi_cursor.execute(sql)
        mi_db.commit()

    def modificar(self, id, nombre, idPais):
        # Actualiza los datos de una editorial existente
        sql = f"UPDATE editoriales SET nombre='{nombre}', idPais='{idPais}' WHERE idEditorial='{id}'"
        mi_cursor.execute(sql)
        mi_db.commit()
        return self.consultar(id)

    def eliminar(self, id):
        # Elimina una editorial de la tabla
        sql = f"DELETE FROM editoriales WHERE idEditorial='{id}'"
        mi_cursor.execute(sql)
        mi_db.commit()

# Instancia global del modelo
mis_editoriales = Editoriales()
