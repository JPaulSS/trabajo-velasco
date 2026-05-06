from conexion import *

class Paises:

    def listar(self):
        # Trae todos los países de la base de datos
        sql = "SELECT * FROM paises"
        mi_cursor.execute(sql)
        resultado = mi_cursor.fetchall()
        return resultado

    def consultar(self, id):
        # Busca un país por su idPais
        sql = f"SELECT * FROM paises WHERE idPais='{id}'"
        mi_cursor.execute(sql)
        resultado = mi_cursor.fetchall()
        return resultado

    def agregar(self, id, nombre, continente):
        # Inserta un nuevo país en la tabla
        sql = f"INSERT INTO paises (idPais, nombre, continente) VALUES ('{id}', '{nombre}', '{continente}')"
        mi_cursor.execute(sql)
        mi_db.commit()

    def modificar(self, id, nombre, continente):
        # Actualiza los datos de un país existente
        sql = f"UPDATE paises SET nombre='{nombre}', continente='{continente}' WHERE idPais='{id}'"
        mi_cursor.execute(sql)
        mi_db.commit()
        return self.consultar(id)

    def eliminar(self, id):
        # Elimina un país de la tabla
        sql = f"DELETE FROM paises WHERE idPais='{id}'"
        mi_cursor.execute(sql)
        mi_db.commit()

# Instancia global del modelo
mis_paises = Paises()
