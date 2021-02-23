from flask import Flask, render_template, redirect, url_for, request, json, session
import datetime
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234567890'

import os

API_TOKEN = ''
API_URL = os.getenv('API_URL') or 'https://bankapi-demo.bill24.net/'


@app.route('/')
def index():
    return redirect(url_for('listbank'))


@app.route('/listbank')
def listbank():
    return render_template("listbank/bank.html")


@app.route('/inquiry',methods=['GET'])
def inquiry():
    bank_id = request.args.get('bank_id')
    img=request.args.get('img')
    token=request.args.get('token')
    return render_template('inquiry/inquery.html', action_url=(url_for('comfirm')),bank_id=bank_id,img=img)

@app.route('/comfirm', methods=(['POST']))
def comfirm():
        form = request.form
        token = '3c81cc406c554b7a90030efed8a4c23b'
        session['token'] = token

        url = '%s//payment/v3/inquiry/single' % API_URL
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'token': token
        }
        payload = {
            'bill_code': form['cus_code'],
            'customer_code': form['cus_code']
        }
        response = requests.post(url=url, headers=headers, json=payload, verify=False)
        response_body = json.loads(response.content)

        if response.status_code == 200 and response_body['code']=='SUCCESS':
            supplier=response_body ['data']['supplier']
            customer=response_body ['data']['customer']
            balance=response_body ['data']['balance']
            return redirect(url_for('fee'))
        else:
            error_code = response_body['code']
            error_message = response_body['message']
            return render_template(
                '/inquiry/fail.html',
                error_code=error_code,
                error_message=error_message
            )

@app.route('/fee')
def fee(response_body,supplier):
    print(response_body)

@app.route('/comfirm/success')
def comfirm_success():
    return render_template("inquiry/success.html")

@app.route('/fail')
def fail():
    return render_template("inquiry/fail.html")
if __name__ == '__main__':
    app.run(debug=True)
