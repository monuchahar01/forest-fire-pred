import pickle
from flask import Flask, request, app, jsonify, url_for, render_template
import numpy as np
import pandas as pd
from mongodb import db_ops

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))


@app.route('/')
def home():
    # return 'Hello World'
    return render_template('home.html')


@app.route('/predict_api', methods=['POST'])
def predict_api():
    data = request.json['data']
    print(data)
    new_data = [list(data.values())]
    output = model.predict(new_data)[0]
    return jsonify(output)


@app.route('/predict', methods=['POST'])
def predict():
    data = [float(x) for x in request.form.values()]
    final_features = [np.array(data)]
    print(data)

    output = model.predict(final_features)[0]
    print(output)
    # output = round(prediction[0], 2)
    return render_template('home.html', prediction_text="Forest Fire Prediction is  {}".format(output))


@app.route('/predict_all', methods=['POST'])
def predict_all():
    data = [x for x in request.form.values()]
    #[np.array(data)]
    database=''.join(data[-2:-1])
    collection=''.join(data[-1:])
    print(database,collection)

    db_obj = db_ops(database, collection)
    df = db_obj.load_df()
    print(df)
    if type(df) == str:
        return render_template('home.html', Error=df)
    else:
        #Test transformation
        X=df[[x for x in df.columns if x != 'Classes']]
        print(X)
        my_prediction=model.predict(X.values)
        my_prediction=my_prediction.tolist()
        return render_template('home.html',prediction = my_prediction)


if __name__ == "__main__":
    app.run(debug=True)


