from conexion import *

class Usuarios:
    def listar(self):
        sql = "SELECT * FROM usuarios"
        mi_cursor.execute(sql)
        resultado = mi_cursor.fetchall()
        return resultado
    def consultar(self, id):
        sql = f"SELECT * FROM usuarios WHERE idUsuario='{id}'"
        mi_cursor.execute(sql)
        resultado = mi_cursor.fetchall()
        return resultado
    def agregar(self,id,nom,contra):
        sql = f"INSERT INTO usuarios (idUsuario,nombre,contrasena) VALUES ('{id}','{nom}','{contra}')"
        mi_cursor.execute(sql)
        mi_db.commit()
    def modificar(self, id, nom, contra):
        sql = f"UPDATE usuarios SET nombre='{nom}', contrasena='{contra}' WHERE idUsuario='{id}'"
        mi_cursor.execute(sql)
        mi_db.commit()
        return self.consultar(id)
    def eliminar(self, id):
        sql = f"DELETE FROM usuarios WHERE idUsuario='{id}'"
        mi_cursor.execute(sql)
        mi_db.commit()
    def login(self,id,contra):
        sql = f"SELECT * FROM usuarios WHERE idUsuario='{id}' AND contrasena='{contra}'"
        mi_cursor.execute(sql)
        resultado = mi_cursor.fetchall()
        if len(resultado)>0:
            retorno = {"entra":True, "id": id, "nombre": resultado[0][1]}
        else:
            retorno = {"entra":False, "mensaje": "Credenciales inválidas"}
        return retorno
    
mis_usuarios = Usuarios()
