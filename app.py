from flask import Flask, render_template, request
import numpy as np
import sympy as sp

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    matrix_data = []
    size = 2
    selected_operation = "char_poly"

    if request.method == "POST":
        try:
            size = int(request.form["matrix_size"])
            selected_operation = request.form["operation"]
            matrix_data = [[request.form.get(f"a{i}_{j}", "") for j in range(size)] for i in range(size)]

            # Convert to integers
            matrix = [[int(matrix_data[i][j]) for j in range(size)] for i in range(size)]
            np_matrix = np.array(matrix)
            sp_matrix = sp.Matrix(matrix)

            if selected_operation == "char_poly":
                x = sp.Symbol('x')
                char_poly = sp_matrix.charpoly(x).as_expr()
                result = f"Characteristic Polynomial:\n{char_poly} = 0"

            elif selected_operation == "eigenvalues":
                eigen = np.linalg.eigvals(np_matrix)
                result = f"Eigenvalues:\n{np.round(eigen, 2)}"

            elif selected_operation == "rank":
                rank = np.linalg.matrix_rank(np_matrix)
                result = f"Rank of the Matrix: {rank}"

            elif selected_operation == "canonical":
                eigen = np.round(np.linalg.eigvals(np_matrix)).astype(int)
                canonical = " + ".join([f"({val}y{i+1}^2)" for i, val in enumerate(eigen)])
                result = f"Canonical Form:\n{canonical}"

            elif selected_operation == "quadratic":
                n = len(np_matrix)
                terms = []
                for i in range(n):
                    terms.append(f"({np_matrix[i][i]})x{i+1}^2")
                for i in range(n):
                    for j in range(i + 1, n):
                        terms.append(f"({2 * np_matrix[i][j]})x{i+1}x{j+1}")
                result = "Quadratic Form:\n" + " + ".join(terms)

        except Exception as e:
            result = f"❌ Error: {e}"

    return render_template("index.html",
                           result=result,
                           size=size,
                           matrix_data=matrix_data,
                           selected_operation=selected_operation)

if __name__ == "__main__":
    app.run(debug=True)
