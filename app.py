from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps

app = Flask(__name__)
app.secret_key = "chave_o_brownie_mania"


usuarios = []
sugestoes = []
encomendas = []


def login_obrigatorio(funcao):
    @wraps(funcao)
    def verificar_login(*args, **kwargs):

        if "usuario_id" not in session:
            flash("Faça login para acessar esta página.", "warning")
            return redirect(url_for("login"))

        return funcao(*args, **kwargs)

    return verificar_login



@app.route("/")
@login_obrigatorio
def index():
    return render_template("index.html")



@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "")

        if not email or not senha:
            flash("Preencha o e-mail e a senha.", "danger")
            return render_template("login.html")

        for usuario in usuarios:

            if usuario["email"] == email and usuario["senha"] == senha:

                session["usuario_id"] = usuario["id"]
                session["usuario_nome"] = usuario["nome"]

                return redirect(url_for("index"))

        flash("E-mail ou senha inválidos.", "danger")

    return render_template("login.html")



@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))



@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":

        nome = request.form["nome"]
        telefone = request.form["telefone"]
        data_nascimento = request.form["data_nascimento"]
        logradouro = request.form["logradouro"]
        bairro = request.form["bairro"]
        complemento = request.form["complemento"]
        numero = request.form["numero"]
        cep = request.form["cep"]
        cidade = request.form["cidade"]
        estado = request.form["estado"]
        email = request.form["email"]
        senha = request.form["senha"]
        confirmar_senha = request.form["confirmar_senha"]

        if senha != confirmar_senha:
            flash("As senhas não coincidem.", "danger")
            return redirect(url_for("cadastrar"))

        for usuario in usuarios:
            if usuario["email"] == email:
                flash("Este e-mail já está cadastrado.", "danger")
                return redirect(url_for("cadastrar"))

        usuario = {
            "id": len(usuarios) + 1,
            "nome": nome,
            "telefone": telefone,
            "data_nascimento": data_nascimento,
            "logradouro": logradouro,
            "bairro": bairro,
            "complemento": complemento,
            "numero": numero,
            "cep": cep,
            "cidade": cidade,
            "estado": estado,
            "email": email,
            "senha": senha
        }

        usuarios.append(usuario)

        flash("Cliente cadastrado com sucesso!", "success")
        return redirect(url_for("login"))

    return render_template("cadastro.html")


@app.route("/listagem")
@login_obrigatorio
def listagem():

    return render_template(
        "listagem.html",
        usuarios=usuarios
    )


@app.route("/cadastrar_sugestao", methods=["GET", "POST"])
@login_obrigatorio
def cadastrar_sugestao():

    if request.method == "POST":

        nome = request.form.get("nome", "").strip()
        sugestao = request.form.get("sugestao", "").strip()


        if not nome or not sugestao:

            flash("Preencha todos os campos.", "danger")

            return render_template(
                "cadastrar_sugestao.html",
                usuarios=usuarios
            )


        # Verifica se o cliente está cadastrado
        cliente_existe = False

        for usuario in usuarios:

            if usuario["nome"] == nome:
                cliente_existe = True
                break


        if not cliente_existe:

            flash(
                "O cliente informado não possui cadastro.",
                "danger"
            )

            return render_template(
                "cadastrar_sugestao.html",
                usuarios=usuarios
            )


        nova_sugestao = {

            "id": len(sugestoes) + 1,

            "nome": nome,

            "sugestao": sugestao

        }


        sugestoes.append(nova_sugestao)

        flash(
            "Sugestão cadastrada com sucesso!",
            "success"
        )

        return redirect(
            url_for("listar_sugestao")
        )


    return render_template(
        "cadastrar_sugestao.html",
        usuarios=usuarios
    )


@app.route("/listar_sugestao")
@login_obrigatorio
def listar_sugestao():

    return render_template(
        "listar_sugestao.html",
        sugestoes=sugestoes
    )


@app.route("/cadastrar_encomenda", methods=["GET", "POST"])
@login_obrigatorio
def cadastrar_encomenda():

    if request.method == "POST":

        nome = request.form.get("nome", "").strip()
        produto = request.form.get("produto", "").strip()
        data_entrega = request.form.get("data_entrega", "").strip()


        if not nome or not produto or not data_entrega:

            flash(
                "Preencha todos os campos.",
                "danger"
            )

            return render_template(
                "cadastrar_encomenda.html",
                usuarios=usuarios
            )


        # Verifica se o cliente está cadastrado
        cliente_existe = False

        for usuario in usuarios:

            if usuario["nome"] == nome:
                cliente_existe = True
                break


        if not cliente_existe:

            flash(
                "O cliente informado não possui cadastro.",
                "danger"
            )

            return render_template(
                "cadastrar_encomenda.html",
                usuarios=usuarios
            )


        nova_encomenda = {

            "id": len(encomendas) + 1,

            "nome": nome,

            "produto": produto,

            "data_entrega": data_entrega

        }


        encomendas.append(nova_encomenda)

        flash(
            "Encomenda cadastrada com sucesso!",
            "success"
        )

        return redirect(
            url_for("listar_encomenda")
        )


    return render_template(
        "cadastrar_encomenda.html",
        usuarios=usuarios
    )

@app.route("/listar_encomenda")
@login_obrigatorio
def listar_encomenda():

    return render_template(
        "listar_encomenda.html",
        encomendas=encomendas
    )



if __name__ == "__main__":

    app.run(debug=True)