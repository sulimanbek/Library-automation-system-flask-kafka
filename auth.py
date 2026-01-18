from functools import wraps
import jwt
from flask import request, jsonify

SECRET_KEY = '21p4p'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')  # Example: http://localhost:27017/route?token=xxxxxx

        if not token:
            return jsonify({'message': 'Token is missing!'}), 403

        try:
            # Ensure you specify the algorithm used to sign the token
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 403

        # Token is valid, continue
        return f(*args, **kwargs)

    return decorated
