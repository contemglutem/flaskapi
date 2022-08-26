from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'flaskapp'

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Fecth form data
        userDatails = request.form
        country_name = userDatails['name']
        cur = mysql.connection.cursor()
        cur.execute(
            "select a.Country_Name, a.Country_Code, a.Indicator_Name, a.Date, a.Value, m.Region from api_ny as a "
            "left join metadata_coutry as m on a.Country_Code = m.Country_Code "
            "WHERE a.Country_Name like %s and a.Value is not null or a.Country_Code like %s and a.Value is not null",
            (country_name, country_name))
        mysql.connection.commit()
        data = cur.fetchall()

        if len(data) == 0 and country_name == 'all':
            cur.execute(
                "select a.Country_Name, a.Country_Code, a.Indicator_Name, a.Date, a.Value, m.Region from api_ny as a "
                "left join metadata_coutry as m on a.Country_Code = m.Country_Code "
                "WHERE a.Value is not null")
            mysql.connection.commit()
            data = cur.fetchall()
        return render_template('index.html', data=data)

    return render_template('index.html')


@app.route('/PIB', methods=['GET', 'POST'])
def pib():
    if request.method == 'POST':
        # Fecth form data
        userDatails = request.form
        region = userDatails['name']
        cur = mysql.connection.cursor()
        cur.execute(
            "select a.Country_Name, a.Country_Code, a.Indicator_Name, sum(a.Value), m.Region from api_ny as a "
            "left join metadata_coutry as m on a.Country_Code = m.Country_Code "
            "WHERE m.Region like %s and a.Value is not null "
            "group by a.Country_Name, a.Country_Code, a.Indicator_Name, m.Region "
            "order by a.Country_Name asc;", [region])
        mysql.connection.commit()
        data = cur.fetchall()
        if len(data) == 0 and region == 'all':
            cur.execute(
                "select a.Country_Name, a.Country_Code, a.Indicator_Name, sum(a.Value), m.Region from api_ny as a "
                "left join metadata_coutry as m on a.Country_Code = m.Country_Code "
                "WHERE a.Value is not null "
                "group by a.Country_Name, a.Country_Code, a.Indicator_Name, m.Region "
                "order by a.Country_Name asc;")
            mysql.connection.commit()
            data = cur.fetchall()
        return render_template('pib.html', data=data)
    return render_template('pib.html')


@app.route('/TOP10', methods=['GET', 'POST'])
def TOP10():
    if request.method == 'POST':
        # Fecth form data
        userDatails = request.form
        inicio = userDatails['inicio'],
        fim = userDatails['fim']
        cur = mysql.connection.cursor()
        cur.execute(
            "select a.Country_Name, a.Country_Code, a.Indicator_Name, sum(a.Value), m.Region from api_ny as a "
            "left join metadata_coutry as m on a.Country_Code = m.Country_Code "
            "WHERE a.Date > %s and a.Date < %s and a.Value is not null "
            "group by a.Country_Name, a.Country_Code, a.Indicator_Name, m.Region "
            "order by sum(a.Value) desc "
            "limit 10;", (inicio, fim))
        mysql.connection.commit()
        data = cur.fetchall()

        cur.execute(
            "select a.Country_Name, a.Country_Code, a.Indicator_Name, sum(a.Value), m.Region from api_ny as a "
            "left join metadata_coutry as m on a.Country_Code = m.Country_Code "
            "WHERE a.Date > %s and a.Date < %s and a.Value is not null "
            "group by a.Country_Name, a.Country_Code, a.Indicator_Name, m.Region "
            "order by sum(a.Value) asc "
            "limit 10;", (inicio, fim))
        mysql.connection.commit()
        values = cur.fetchall()
        if len(data) == 0 and inicio == 'all':
            cur.execute(
                "select a.Country_Name, a.Country_Code, a.Indicator_Name, a.Date, a.Value, m.Region from api_ny")
            mysql.connection.commit()
            data = cur.fetchall()
        return render_template('toppib.html', data=data, values=values)

    return render_template('toppib.html')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
