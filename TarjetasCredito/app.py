from datetime import date
from flask import Flask, render_template, request, redirect, url_for,flash
from bdd import *
from tarjeta_credito import TarjetaCredito
from sqlite3 import IntegrityError


app = Flask(__name__)
app.secret_key = "key_para_flash_123"


inicializar_bd()

@app.route("/")
def inicio():
    tarjetas = obtener_tarjetas()
    return render_template("index.html", tarjetas=tarjetas)


#endpoints menu principal
@app.route("/crear_tarjeta", methods=["GET", "POST"])
def crear():
    """
    Endpoint para crear una nueva tarjeta de crédito. 
    Usa un formulario para recoger los datos
    """

    if request.method == "POST":
        try:
            titular = request.form["titular"]
            nif = request.form["nif"]
            pin = request.form["pin"]
            limite = float(request.form["limite"])
            numero = request.form["numero"]
            if not titular or not nif or not pin or not numero:
                flash("Todos los campos son obligatorios", "danger")
                return render_template("crear_tarjeta.html")

            t = TarjetaCredito(titular, nif, pin, limite, numero)
            insert_tarjeta(t)

            flash("Tarjeta creada con éxito", "success")
            return redirect(url_for("inicio"))

        except IntegrityError:
            flash("Error: ya existe una tarjeta con ese NIF o número", "danger")
            return render_template("crear_tarjeta.html")
    return render_template("crear_tarjeta.html")


#
@app.route("/ver_tarjeta/<nif>")
def ver_tarjeta(nif):
    """
    Endpoint para ver los detalles de una tarjeta de crédito, incluyendo sus movimientos y el total gastado.
    """
    t = buscar_tarjeta_por_nif(nif)

    if t is None:
        flash("Tarjeta no encontrada", "danger")
        return redirect(url_for("inicio"))


    movimientos = obtener_movimientos(t.numero_tarjeta)
    total_movimientos = sum(m.cantidad for m in movimientos)


    return render_template(
        "detalle_tarjeta.html",
        tarjeta=t,
        movimientos=movimientos,
        total_movimientos=total_movimientos
    )

@app.route("/eliminar/<nif>", methods=["GET", "POST"])
def eliminar(nif):
    """
    Endpoint para eliminar una tarjeta de crédito. Pide confirmación.
    """
    t = buscar_tarjeta_por_nif(nif)

    if t is None:
        flash("Tarjeta no encontrada", "danger")
        return redirect(url_for("inicio"))


    if request.method == "POST":
        eliminar_tarjeta_por_nif(nif)
        flash("Tarjeta eliminada con éxito", "warning")
        return redirect(url_for("inicio"))

    return render_template("confirmacion_eliminar.html", tarjeta=t)


@app.route("/gastos")
def gastos():
    """
    Endpoint para mostrar el total de gastos acumulados de todas las tarjetas.
    """
    total = gastos_totales_bd()

    return render_template("gastos.html", total=total)


#endpoints submenu tarjeta
@app.route("/pagar/<nif>", methods=["GET", "POST"])
def pagar(nif):
    """
    Emdpoint para gestionar un pago.
    """
    tarjeta = buscar_tarjeta_por_nif(nif)
    if tarjeta is None:
        flash("Tarjeta no encontrada", "danger")
        return redirect(url_for("inicio"))

    if request.method == "POST":
        concepto = request.form["concepto"]

        try:
            cantidad = float(request.form["cantidad"])
        except ValueError:
            flash("Cantidad no válida", "danger")
            return redirect(url_for("pagar", nif=nif))

        if cantidad <= 0:
            flash("La cantidad debe ser mayor que 0", "danger")
            return redirect(url_for("pagar", nif=nif))

        if cantidad > tarjeta.limite:
            flash("Supera el límite de la tarjeta", "danger")
            return redirect(url_for("pagar", nif=nif))

        movimiento = Movimiento(cantidad=cantidad, concepto=concepto)
        insertar_movimiento(tarjeta, movimiento)

        flash("Pago realizado con éxito", "success")
        return redirect(url_for("ver_tarjeta", nif=nif))

    return render_template("pagar.html", nif=nif)


@app.route("/cambiar_pin/<nif>", methods=["GET", "POST"])
def cambiar_pin(nif):
    """
    Endpoint para cambiar el PIN de una tarjeta.
    """
    tarjeta = buscar_tarjeta_por_nif(nif)
    if tarjeta is None:
        flash("Tarjeta no encontrada", "danger")
        return redirect(url_for("inicio"))

    if request.method == "POST":
        nuevo_pin = request.form["pin"]

        if not nuevo_pin.isdigit():
            flash("El PIN debe ser numérico", "danger")
            return redirect(url_for("cambiar_pin", nif=nif))

        if len(nuevo_pin) < 4:
            flash("El PIN debe tener al menos 4 dígitos", "danger")
            return redirect(url_for("cambiar_pin", nif=nif))

        tarjeta.pin = nuevo_pin
        update_pin(tarjeta)

        flash("PIN actualizado con éxito", "success")
        return redirect(url_for("ver_tarjeta", nif=nif))

    return render_template("cambiar_pin.html", tarjeta=tarjeta)

if __name__ == "__main__":
    app.run(debug=True)

