import os
import smtplib
from email.message import EmailMessage

from flask import flash, redirect, render_template, request, url_for

from main import app

MAIL_TO_DEFAULT = "pintorhaun35@gmail.com"


def _send_contact_email(nome: str, email_remetente: str, mensagem: str) -> None:
    mail_server = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    mail_port = int(os.getenv("MAIL_PORT", "587"))
    mail_user = os.getenv("MAIL_USERNAME", "").strip()
    mail_pass = os.getenv("MAIL_PASSWORD", "").strip()
    destino = os.getenv("MAIL_TO", MAIL_TO_DEFAULT).strip() or MAIL_TO_DEFAULT

    if not mail_user or not mail_pass:
        raise RuntimeError(
            "SMTP não configurado. Defina MAIL_USERNAME e MAIL_PASSWORD no ambiente."
        )

    assunto = f"[Portfólio] Contato de {nome}"
    corpo = (
        f"Nome: {nome}\n"
        f"E-mail para resposta: {email_remetente}\n\n"
        f"Mensagem:\n{mensagem}"
    )

    msg = EmailMessage()
    msg["Subject"] = assunto
    msg["From"] = mail_user
    msg["To"] = destino
    msg.set_content(corpo)

    with smtplib.SMTP(mail_server, mail_port, timeout=30) as smtp:
        smtp.starttls()
        smtp.login(mail_user, mail_pass)
        smtp.send_message(msg)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/enviar-contato", methods=["POST"])
def enviar_contato():
    nome = (request.form.get("nome") or "").strip()
    email_remetente = (request.form.get("email") or "").strip()
    mensagem = (request.form.get("mensagem") or "").strip()

    if len(nome) > 200 or len(email_remetente) > 320 or len(mensagem) > 8000:
        flash("Texto muito longo. Encurte e tente de novo.", "error")
        return redirect(url_for("index") + "#contato")

    if not nome or not email_remetente or not mensagem:
        flash("Preencha nome, e-mail e mensagem.", "error")
        return redirect(url_for("index") + "#contato")

    if "@" not in email_remetente:
        flash("Digite um e-mail válido.", "error")
        return redirect(url_for("index") + "#contato")

    try:
        _send_contact_email(nome, email_remetente, mensagem)
    except RuntimeError as e:
        flash(str(e), "error")
        return redirect(url_for("index") + "#contato")
    except smtplib.SMTPException as e:
        flash(f"Falha ao enviar e-mail: {e!s}", "error")
        return redirect(url_for("index") + "#contato")
    except OSError as e:
        flash(f"Erro de rede ao enviar: {e!s}", "error")
        return redirect(url_for("index") + "#contato")

    flash("Mensagem enviada! Em breve retorno o contato.", "success")
    return redirect(url_for("index") + "#contato")
