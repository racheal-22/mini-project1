from flask import Flask, request, render_template
from flasgger import Swagger
from flasgger.utils import swag_from
from models import db, RequestRecord
import json
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sum_records.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Swagger(app)
db.init_app(app)

# Create DB tables
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/compute', methods=['GET', 'POST'])
@swag_from({
    'tags': ['Sum Calculator'],
    'consumes': ['application/x-www-form-urlencoded'],
    'parameters': [
        {
            'name': 'numbers',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Comma-separated numbers (e.g. 10, 20, 30)'
        }
    ],
    'responses': {
        200: {'description': 'Sum computed or retrieved from cache'},
        400: {'description': 'Invalid input format'}
    }
})
def compute():
    if request.method == 'POST':
        numbers_input = request.form.get('numbers', '').strip()

        if not numbers_input:
            return render_template('compute.html', error="Please enter some numbers.")

        items = [item.strip() for item in numbers_input.split(',')]
        numbers = []

        for i in items:
            if i == '':
                continue
            # allow negative numbers too
            if not (i.lstrip('-').isdigit()):
                return render_template('compute.html', error=f"Invalid input: '{i}' is not a number.")
            numbers.append(int(i))

        if not numbers:
            return render_template('compute.html', error="No valid numbers provided.")

        numbers_str = json.dumps(sorted(numbers))
        existing = RequestRecord.query.filter_by(numbers=numbers_str).first()

        if existing:
            return render_template('compute.html', result=existing.result, cached=True,
                                   txn_id=existing.id, timestamp=existing.timestamp)
        else:
            result = sum(numbers)
            new_record = RequestRecord(numbers=numbers_str, result=result)
            db.session.add(new_record)
            db.session.commit()
            return render_template('compute.html', result=result, cached=False,
                                   txn_id=new_record.id, timestamp=new_record.timestamp)

    return render_template('compute.html')


@app.route('/transaction', methods=['GET', 'POST'])
@swag_from({
    'tags': ['Transaction Lookup'],
    'consumes': ['application/x-www-form-urlencoded'],
    'parameters': [
        {
            'name': 'txn_id',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Transaction ID to retrieve the cached result'
        }
    ],
    'responses': {
        200: {
            'description': 'Transaction retrieved successfully'
        },
        404: {
            'description': 'Transaction ID not found'
        }
    }
})
def transaction():
    if request.method == 'POST':
        txn_id = request.form.get('txn_id')
        record = RequestRecord.query.filter_by(id=txn_id).first()
        if record:
            return render_template('transaction.html',
                                   numbers=json.loads(record.numbers),
                                   result=record.result,
                                   timestamp=record.timestamp)
        else:
            return render_template('transaction.html', error="Transaction ID not found.")
    return render_template('transaction.html')


@app.route('/about')
def about():
    return "<h2>Smart Sum Calculator - Built with Flask + SQLite</h2>"



if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)

