from conexion import *
from editoriales import mis_editoriales

programa = Flask(__name__)
api = Api(programa)

class ListaEditoriales(Resource):

    def get(self):
        # Retorna todas las editoriales
        editoriales = mis_editoriales.listar()
        return jsonify({"mensaje": "editoriales", "data": editoriales})

    def post(self):
        # Agrega una nueva editorial si el id no existe
        nuevo = request.json
        resultado = mis_editoriales.consultar(nuevo["id"])
        if len(resultado) == 0:
            mis_editoriales.agregar(nuevo["id"], nuevo["nombre"], nuevo["idPais"])
            return jsonify({"mensaje": "Editorial agregada con éxito"})
        else:
            return jsonify({"mensaje": "Id de editorial ya existe"})


class Editorial(Resource):

    def get(self, id):
        # Busca una editorial por id
        resultado = mis_editoriales.consultar(id)
        if len(resultado) == 0:
            return jsonify({"mensaje": "Editorial no encontrada"})
        else:
            return jsonify({"mensaje": "Editorial encontrada", "editorial": resultado[0]})

    def put(self, id):
        # Modifica una editorial existente
        nuevo = request.json
        resultado = mis_editoriales.consultar(id)
        if len(resultado) == 0:
            return jsonify({"mensaje": "Editorial no existe"})
        else:
            mis_editoriales.modificar(id, nuevo["nombre"], nuevo["idPais"])
            return jsonify({"mensaje": "Editorial modificada con éxito"})

    def delete(self, id):
        # Elimina una editorial existente
        resultado = mis_editoriales.consultar(id)
        if len(resultado) == 0:
            return jsonify({"mensaje": "Editorial no existe"})
        else:
            mis_editoriales.eliminar(id)
            return jsonify({"mensaje": "Editorial eliminada con éxito!"})


api.add_resource(ListaEditoriales, "/editoriales")
api.add_resource(Editorial, "/editoriales/<id>")

if __name__ == "__main__":
    programa.run(host="0.0.0.0", debug=True, port=5083)
