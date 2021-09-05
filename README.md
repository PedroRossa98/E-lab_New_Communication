Já corrigi o html. 
Adcionei as pastas 'templates' e 'static' onde contem os ficheiros para o flask correr bem
Quanto ao app.py as alterações que fiz está  abaixo.


```python
...
app = Flask(__name__, template_folder='templates', static_folder='static')
...
}
```
```python
...
@app.route('/',methods=['GET'])
def HTML_exe():
    return render_template("index.html")
 ...
}





