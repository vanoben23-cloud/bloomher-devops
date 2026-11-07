
from datetime import date, timedelta
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    error = None

    if request.method == "POST":
        try:
            last_period = date.fromisoformat(
                request.form["last_period"]
            )
            cycle_length = int(
                request.form["cycle_length"]
            )

            if last_period > date.today():
                raise ValueError("Date cannot be in the future.")

            if not 21 <= cycle_length <= 45:
                raise ValueError(
                    "Cycle length must be between 21 and 45 days."
                )

            next_period = last_period + timedelta(
                days=cycle_length
            )
            ovulation = next_period - timedelta(days=14)

            result = {
                "next_period": next_period.isoformat(),
                "ovulation": ovulation.isoformat(),
                "fertile_start": (
                    ovulation - timedelta(days=5)
                ).isoformat(),
                "fertile_end": (
                    ovulation + timedelta(days=1)
                ).isoformat()
            }

        except (ValueError, KeyError) as exc:
            error = str(exc)

    return render_template(
        "index.html",
        result=result,
        error=error
    )

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
