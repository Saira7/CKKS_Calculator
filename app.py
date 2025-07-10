from flask import Flask, request, jsonify, render_template
import tenseal as ts

app = Flask(__name__)

# Create context once
context = ts.context(
    ts.SCHEME_TYPE.CKKS,
    poly_modulus_degree=8192,
    coeff_mod_bit_sizes=[40, 20, 40]
)
context.global_scale = 2 ** 20
context.generate_galois_keys()

@app.route('/ckks-calc', methods=['POST'])
def ckks_calc():
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Missing or invalid JSON body."}), 400
    # Accept comma-separated vectors
    num1_raw = data.get('num1')
    num2_raw = data.get('num2')
    operation = data.get('operation', '').strip().lower()

    try:
        vec1_plain = [float(x.strip()) for x in str(num1_raw).split(',') if x.strip()]
        vec2_plain = [float(x.strip()) for x in str(num2_raw).split(',') if x.strip()]
    except Exception:
        return jsonify({"error": "Invalid vector input. Use comma-separated numbers."}), 400

    if len(vec1_plain) != len(vec2_plain):
        return jsonify({"error": "Vectors must be the same length."}), 400

    # Encrypt numbers
    vec1 = ts.ckks_vector(context, vec1_plain)
    vec2 = ts.ckks_vector(context, vec2_plain)

    # Perform encrypted computation
    if operation == "add":
        result = vec1 + vec2
        op_str = "Sum"
        actual_result = [a + b for a, b in zip(vec1_plain, vec2_plain)]
    elif operation == "multiply":
        result = vec1 * vec2
        op_str = "Product"
        actual_result = [a * b for a, b in zip(vec1_plain, vec2_plain)]
    else:
        return jsonify({"error": "Invalid operation. Use 'add' or 'multiply'."}), 400

    # Decrypt and prepare proof
    decrypted = result._decrypt()
    encrypted_repr = str(result.serialize())[:100]  # Show first 100 chars as proof

    # Track precision loss
    abs_errors = [abs(float(d) - float(a)) for d, a in zip(decrypted, actual_result)]
    max_error = max(abs_errors) if abs_errors else 0.0
    avg_error = sum(abs_errors) / len(abs_errors) if abs_errors else 0.0
    precision_loss = {
        "max_abs_error": max_error,
        "avg_abs_error": avg_error
    }

    return jsonify({
        "operation": op_str,
        "decrypted_result": decrypted,
        "actual_result": actual_result,
        "encrypted_sample": encrypted_repr,
        "precision_loss": precision_loss
    })

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
