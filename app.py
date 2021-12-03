import requests
from flask import Flask
from flask import render_template,request
from twilio.rest import Client
import requests
import requests_cache
account_sid = 'AC4efb0791005c4f5613f6c8f5bb197e6f'
auth_token = 'fdb91cf151ecff9dc7257c9bb336835e'
client = Client(account_sid, auth_token)
app = Flask(__name__,static_url_path='/static')

@app.route('/')
def registration_form():
    return render_template('login.html')
@app.route('/login',methods=['POST','GET'])
def login_details():
    first_name=request.form['fname']
    last_name = request.form['lname']
    email_id = request.form['email']
    source_st = request.form['state']
    source_dt=request.form['district']
    dest_st = request.form['dest_state']
    dest_dt=request.form['dest_place']
    phone_no = request.form['phone']
    id_proof=request.form['aadhaar']
    date = request.form['date']
    full_name=first_name+"."+last_name
    r=requests.get("https://api.covid19india.org/v4/data.json")
    json_data=r.json()
    cnt=json_data[dest_st]['districts'][dest_dt]['total']['confirmed']
    pop=json_data[dest_st]['districts'][dest_dt]['meta']['population']
    travel_pass=((cnt/pop)*100)
    if(travel_pass < 30 and request.method == 'POST'):
        status="confirmed"
        client.messages.create(to="whatsapp:+7997684684",from_="whatsapp:+14155238886",
                              body="Hello"+" "+full_name+" "+"your travel from"+" "+source_dt+" "+"to"+" "+dest_dt+" "+"has"+status+" "+"on"+" "+date+" "+".")
        return render_template('reg_details.html',var1=full_name,var2=email_id,var3=id_proof,var4=source_st,var5=source_dt,var6=dest_st,var7=dest_dt,var8=phone_no,var9=date,var10=status)
    else:
        status="not confirmed"
        client.messages.create(to="whatsapp:+7997684684", from_="whatsapp:+1456835893",
                              body="Hello" + " " + full_name + " " + "your travel from" + " " + source_dt + " " + "to" + " " + dest_dt + " " + "has" + status + " " + "on" + " " + date + " " + ",Apply late")
        return render_template('reg_details.html', var1=full_name, var2=email_id, var3=id_proof, var4=source_st,
                               var5=source_dt, var6=dest_st, var7=dest_dt, var8=phone_no, var9=date, var10=status)


if __name__ == '__main__':
    app.run(port=9001,debug=True)
