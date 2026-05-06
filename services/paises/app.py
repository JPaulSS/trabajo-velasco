from conexion import *
from paises import mis_paises

programa = Flask(__name__)
api = Api(programa)

class ListaPaises(Resource):

    def get(self):
        # Retorna todos los países
        paises = mis_paises.listar()
        return jsonify({"mensaje": "paises", "data": paises})

    def post(self):
        # Agrega un nuevo país si el id no existe
        nuevo = request.json
        resultado = mis_paises.consultar(nuevo["id"])
        if len(resultado) == 0:
            mis_paises.agregar(nuevo["id"], nuevo["nombre"], nuevo["continente"])
            return jsonify({"mensaje": "País agregado con éxito"})
        else:
            return jsonify({"mensaje": "Id de país ya existe"})


class Pais(Resource):

    def get(self, id):
        # Busca un país por id
        resultado = mis_paises.consultar(id)
        if len(resultado) == 0:
            return jsonify({"mensaje": "País no encontrado"})
        else:
            return jsonify({"mensaje": "País encontrado", "pais": resultado[0]})

    def put(self, id):
        # Modifica un país existente
        nuevo = request.json
        resultado = mis_paises.consultar(id)
        if len(resultado) == 0:
            return jsonify({"mensaje": "País no existe"})
        else:
            mis_paises.modificar(id, nuevo["nombre"], nuevo["continente"])
            return jsonify({"mensaje": "País modificado con éxito"})

    def delete(self, id):
        # Elimina un país existente
        resultado = mis_paises.consultar(id)
        if len(resultado) == 0:
            return jsonify({"mensaje": "País no existe"})
        else:
            mis_paises.eliminar(id)
            return jsonify({"mensaje": "País eliminado con éxito!"})


api.add_resource(ListaPaises, "/paises")
api.add_resource(Pais, "/paises/<id>")

if __name__ == "__main__":
    programa.run(host="0.0.0.0", debug=True, port=5082)
