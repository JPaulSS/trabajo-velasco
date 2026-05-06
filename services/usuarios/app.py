from conexion import *
from usuarios import mis_usuarios

programa = Flask(__name__)
api = Api(programa)

class ListaUsuarios(Resource):
    def get(self):
        usuarios = mis_usuarios.listar()
        return jsonify({"mensaje": "usuarios","data": usuarios})
    def post(self):
        nuevo=request.json
        resultado = mis_usuarios.consultar(nuevo["id"])
        if len(resultado)==0:
            mis_usuarios.agregar(nuevo["id"],nuevo["nombre"],nuevo["contrasena"])
            return jsonify({"mensaje":"Usuario agregado con éxito"})
        else:
            return jsonify({"mensaje":"Id de usuario ya existe"})

class Usuario(Resource):
    def get(self,id):
        resultado = mis_usuarios.consultar(id)
        if len(resultado)==0:
            return jsonify({"mensaje":"Usuario no encontrado"})
        else:
            return jsonify({"mensaje":"Usuario encontrado","usuario":resultado[0]})
    def put(self,id):
        nuevo=request.json
        resultado = mis_usuarios.consultar(id)
        if len(resultado)==0:
            return jsonify({"mensaje":"Usuario no existe"})
        else:
            mis_usuarios.modificar(nuevo["id"],nuevo["nombre"],nuevo["contrasena"])
            return jsonify({"mensaje":"Usuario modificado con éxito"})
    def delete(self,id):
        resultado = mis_usuarios.consultar(id)
        if len(resultado)==0:
            return jsonify({"mensaje":"Usuario no existe"})
        else:
            mis_usuarios.eliminar(id)
            return jsonify({"mensaje":"Usuario eliminado con éxito!"})
    def post(self,id):
        nuevo=request.json
        resultado = mis_usuarios.login(nuevo["id"],nuevo["contra"])
        if resultado["entra"]:
            return jsonify({"mensaje":"Bienvenido "+resultado["nombre"]})
        else:
            return jsonify({"mensaje":"Credenciales inválidas"})
    
api.add_resource(ListaUsuarios, "/usuarios")
api.add_resource(Usuario,"/usuarios/<id>")

if __name__=="__main__":
    programa.run(host="0.0.0.0",debug=True,port=5080)