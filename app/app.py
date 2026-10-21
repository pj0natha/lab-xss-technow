import secrets
import sqlite3
import threading

from flask import Flask, abort, make_response, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

FLAG_1 = f"flag{{xss_1_{secrets.token_hex(4)}}}"
FLAG_2 = f"flag{{xss_2_{secrets.token_hex(4)}}}"
FLAG_3 = f"flag{{xss_3_{secrets.token_hex(4)}}}"
FLAG_4 = f"flag{{xss_4_{secrets.token_hex(4)}}}"
FLAG_5 = f"flag{{xss_5_{secrets.token_hex(4)}}}"
FLAG_6 = f"flag{{xss_6_{secrets.token_hex(4)}}}"

DB_LOCK = threading.Lock()
conn = sqlite3.connect(":memory:", check_same_thread=False)
conn.row_factory = sqlite3.Row


def preparar_banco():
    with DB_LOCK:
        conn.execute(
            """
            CREATE TABLE posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT,
                categoria TEXT,
                resumo TEXT,
                corpo TEXT
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE comentarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id INTEGER,
                autor TEXT,
                corpo TEXT
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE contato_mensagens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                mensagem TEXT
            )
            """
        )

        posts = [
            (
                "Nova GPU promete dobrar desempenho em jogos",
                "Hardware",
                "Fabricante anuncia nova linha de placas de video com arquitetura renovada.",
                "A nova geracao de placas de video chega prometendo ganhos de ate 90% em "
                "benchmarks populares, segundo a fabricante. O lancamento oficial esta previsto "
                "para o proximo trimestre, com precos que devem variar bastante entre regioes.",
            ),
            (
                "Vazamento de dados afeta aplicativo popular de mensagens",
                "Seguranca",
                "Pesquisadores encontraram um banco de dados exposto com informacoes de usuarios.",
                "Um banco de dados mal configurado deixou exposto por semanas um conjunto de "
                "registros de usuarios de um aplicativo de mensagens amplamente usado. A empresa "
                "afirma ter corrigido a configuracao apos ser notificada por pesquisadores "
                "independentes.",
            ),
            (
                "Startup brasileira lanca assistente de codigo com IA",
                "Software",
                "Ferramenta promete sugerir trechos de codigo direto no editor.",
                "Uma startup brasileira apresentou um assistente que se integra a editores de "
                "codigo populares e sugere trechos com base no contexto do projeto. A equipe diz "
                "que o foco inicial sao equipes pequenas e desenvolvedores autonomos.",
            ),
            (
                "Fabricante anuncia novo chip para notebooks ultrafinos",
                "Hardware",
                "Novo processador promete mais autonomia de bateria sem perder desempenho.",
                "O novo chip deve chegar a notebooks ultrafinos no segundo semestre, com foco em "
                "eficiencia energetica. Fabricantes parceiros ja confirmaram modelos que vao usar "
                "o novo processador.",
            ),
            (
                "Pesquisadores demonstram novo metodo de computacao quantica",
                "Ciencia",
                "Experimento reduz taxa de erro em operacoes quanticas basicas.",
                "Um grupo de pesquisa publicou resultados mostrando uma reducao significativa na "
                "taxa de erro de operacoes quanticas basicas, usando uma abordagem diferente de "
                "correcao de erros. O trabalho ainda esta em fase experimental.",
            ),
        ]
        conn.executemany(
            "INSERT INTO posts (titulo, categoria, resumo, corpo) VALUES (?, ?, ?, ?)",
            posts,
        )
        conn.commit()


@app.route("/")
def index():
    posts = conn.execute(
        "SELECT id, titulo, categoria, resumo FROM posts ORDER BY id"
    ).fetchall()
    return render_template("index.html", posts=posts)


@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def post_detalhe(post_id):
    post = conn.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
    if post is None:
        abort(404)

    if request.method == "POST":
        autor = request.form.get("autor", "")
        corpo = request.form.get("corpo", "")
        with DB_LOCK:
            conn.execute(
                "INSERT INTO comentarios (post_id, autor, corpo) VALUES (?, ?, ?)",
                (post_id, autor, corpo),
            )
            conn.commit()
        return redirect(url_for("post_detalhe", post_id=post_id))

    comentarios = conn.execute(
        "SELECT autor, corpo FROM comentarios WHERE post_id = ? ORDER BY id",
        (post_id,),
    ).fetchall()

    resposta = make_response(
        render_template("post.html", post=post, comentarios=comentarios)
    )
    resposta.set_cookie("flag2", FLAG_2, path="/post", httponly=False)
    resposta.set_cookie("flag6", FLAG_6, path="/post", httponly=False)
    return resposta


@app.route("/buscar")
def buscar():
    q = request.args.get("q", "")
    resultados = []
    if q:
        resultados = conn.execute(
            "SELECT id, titulo, categoria FROM posts WHERE titulo LIKE ?",
            (f"%{q}%",),
        ).fetchall()

    resposta = make_response(render_template("busca.html", q=q, resultados=resultados))
    resposta.set_cookie("flag1", FLAG_1, path="/buscar", httponly=False)
    return resposta


@app.route("/categoria/<nome>")
def categoria(nome):
    posts = conn.execute(
        "SELECT id, titulo, categoria FROM posts WHERE categoria = ?",
        (nome,),
    ).fetchall()

    resposta = make_response(render_template("categoria.html", nome=nome, posts=posts))
    resposta.set_cookie("flag5", FLAG_5, path="/categoria", httponly=False)
    return resposta


@app.route("/contato", methods=["GET", "POST"])
def contato():
    if request.method == "POST":
        nome = request.form.get("nome", "")
        mensagem = request.form.get("mensagem", "")
        with DB_LOCK:
            conn.execute(
                "INSERT INTO contato_mensagens (nome, mensagem) VALUES (?, ?)",
                (nome, mensagem),
            )
            conn.commit()
        return redirect(url_for("contato"))

    mensagens = conn.execute(
        "SELECT nome, mensagem FROM contato_mensagens ORDER BY id"
    ).fetchall()

    resposta = make_response(render_template("contato.html", mensagens=mensagens))
    resposta.set_cookie("flag4", FLAG_4, path="/contato", httponly=False)
    return resposta


@app.errorhandler(404)
def nao_encontrado(erro):
    resposta = make_response(render_template("404.html", caminho=request.path), 404)
    resposta.set_cookie("flag3", FLAG_3, path=request.path, httponly=False)
    return resposta


if __name__ == "__main__":
    preparar_banco()
    app.run(host="0.0.0.0", port=80, threaded=False)
