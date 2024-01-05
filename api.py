from flask import Flask, request, jsonify

from fixed_point_iteration import fixed_point_iteration
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/fixed-point-iteration', methods=['POST'])
def api_fixed_point_iteration():
    """
    Bu endpoint, Fixed-Point Iteration yöntemini kullanarak bir fonksiyonun kökünü bulur.
    ---
    parameters:
      - name: function
        in: body
        type: string
        required: true
        description: "Kökünü bulmak istediğiniz fonksiyon, 'x' bağımsız değişkenini içermelidir."
        example: "x**2 - 4"
      - name: initial_guess
        in: body
        type: float
        required: true
        description: "Iteratif sürecin başlangıç tahmini."
        example: 2.0
      - name: tolerance
        in: body
        type: float
        required: true
        description: "İterasyonları durdurmak için çok yakın bir sıfır değeri."
        example: 0.001
      - name: max_iterations
        in: body
        type: int
        required: true
        description: "Maksimum iterasyon sayısı."
        example: 50
    responses:
      200:
        description: Başarılı işlem
        schema:
          type: object
          properties:
            root:
              type: float
              description: "Bulunan kök değeri."
            iterations:
              type: int
              description: "Yapılan iterasyon sayısı."
    """
    data = request.get_json()
    f = lambda x: eval(data['function'])
    x_0 = data['initial_guess']
    tol = data['tolerance']
    max_iter = data['max_iterations']

    result = fixed_point_iteration(f, x_0, tol, max_iter)

    # Plotting

    return jsonify(result)

if __name__ == '__main__':
    app.run("localhost", port="8008")
