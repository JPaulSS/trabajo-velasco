from conexion import *
from autores import mis_autores

programa = Flask(__name__)
api = Api(programa)

class ListaAutores(Resource):

    def get(self):
        # Retorna todos los autores
        autores = mis_autores.listar()
        return jsonify({"mensaje": "autores", "data": autores})

    def post(self):
        # Agrega un nuevo autor si el id no existe
        nuevo = request.json
        resultado = mis_autores.consultar(nuevo["id"])
        if len(resultado) == 0:
            mis_autores.agregar(nuevo["id"], nuevo["nombre"], nuevo["email"], nuevo["idPais"])
            return jsonify({"mensaje": "Autor agregado con éxito"})
        else:
            return jsonify({"mensaje": "Id de autor ya existe"})


class Autor(Resource):

    def get(self, id):
        # Busca un autor por id
        resultado = mis_autores.consultar(id)
        if len(resultado) == 0:
            return jsonify({"mensaje": "Autor no encontrado"})
        else:
            return jsonify({"mensaje": "Autor encontrado", "autor": resultado[0]})

    def put(self, id):
        # Modifica un autor existente
        nuevo = request.json
        resultado = mis_autores.consultar(id)
        if len(resultado) == 0:
            return jsonify({"mensaje": "Autor no existe"})
        else:
            mis_autores.modificar(id, nuevo["nombre"], nuevo["email"], nuevo["idPais"])
            return jsonify({"mensaje": "Autor modificado con éxito"})

    def delete(self, id):
        # Elimina un autor existente
        resultado = mis_autores.consultar(id)
        if len(resultado) == 0:
            return jsonify({"mensaje": "Autor no existe"})
        else:
            mis_autores.eliminar(id)
            return jsonify({"mensaje": "Autor eliminado con éxito!"})


api.add_resource(ListaAutores, "/autores")
api.add_resource(Autor, "/autores/<id>")

if __name__ == "__main__":
    programa.run(host="0.0.0.0", debug=True, port=5081)
