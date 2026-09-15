from flask import Flask, render_template, request, redirect, url_for
from database import get_connection, init_database

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

# Create database tables if they don't exist
init_database()


@app.route("/")
def dashboard():
    connection = get_connection()

    campaigns = connection.execute(
        """
        SELECT
            c.id,
            c.name,
            c.subject,
            c.created_at,
            COUNT(r.id) AS total_sent,
            SUM(
                CASE WHEN r.clicked = 1 THEN 1 ELSE 0 END
            ) AS clicked,
            SUM(
                CASE WHEN r.credential_submitted = 1
                THEN 1 ELSE 0 END
            ) AS credentials_captured
        FROM campaigns c
        LEFT JOIN recipients r
            ON c.id = r.campaign_id
        GROUP BY c.id
        ORDER BY c.id DESC
        """
    ).fetchall()

    events = connection.execute(
        """
        SELECT
            ce.clicked_at,
            ce.ip_address,
            ce.user_agent,
            ce.location,
            r.name AS recipient_name,
            r.email AS recipient_email,
            c.name AS campaign_name
        FROM click_events ce
        JOIN recipients r
            ON ce.recipient_id = r.id
        JOIN campaigns c
            ON r.campaign_id = c.id
        ORDER BY ce.id DESC
        """
    ).fetchall()

    connection.close()

    # Convert database rows into dashboard data
    campaign_data = []

    total_sent = 0
    total_clicked = 0
    total_credentials = 0

    for campaign in campaigns:

        sent = campaign["total_sent"] or 0
        clicked = campaign["clicked"] or 0
        credentials = campaign["credentials_captured"] or 0

        if sent > 0:
            click_rate = round((clicked / sent) * 100, 1)
        else:
            click_rate = 0

        # Awareness risk calculation
        if credentials > 0:
            risk = "HIGH"
        elif click_rate >= 30:
            risk = "MEDIUM"
        else:
            risk = "LOW"

        campaign_data.append({
            "id": campaign["id"],
            "name": campaign["name"],
            "subject": campaign["subject"],
            "created_at": campaign["created_at"],
            "total_sent": sent,
            "clicked": clicked,
            "credentials_captured": credentials,
            "click_rate": click_rate,
            "risk": risk
        })

        total_sent += sent
        total_clicked += clicked
        total_credentials += credentials

    if total_sent > 0:
        overall_rate = round(
            (total_clicked / total_sent) * 100,
            1
        )
    else:
        overall_rate = 0

    return render_template(
        "dashboard.html",
        campaigns=campaign_data,
        events=events,
        total_sent=total_sent,
        total_clicked=total_clicked,
        total_credentials=total_credentials,
        overall_rate=overall_rate
    )


@app.route("/campaign/new", methods=["GET", "POST"])
def create_campaign():

    if request.method == "POST":
        campaign_name = request.form["campaign_name"]
        subject = request.form["subject"]
        recipient_name = request.form["recipient_name"]
        recipient_email = request.form["recipient_email"]

        connection = get_connection()
        cursor = connection.cursor()

        # Create campaign
        cursor.execute(
            """
            INSERT INTO campaigns (name, subject)
            VALUES (?, ?)
            """,
            (campaign_name, subject)
        )

        campaign_id = cursor.lastrowid

        # Create mock recipient
        cursor.execute(
            """
            INSERT INTO recipients
            (campaign_id, name, email)
            VALUES (?, ?, ?)
            """,
            (campaign_id, recipient_name, recipient_email)
        )

        connection.commit()
        connection.close()

        return redirect(url_for("email_preview", campaign_id=campaign_id))

    return render_template("campaign.html")


@app.route("/campaign/<int:campaign_id>/preview")
def email_preview(campaign_id):

    connection = get_connection()

    campaign = connection.execute(
        "SELECT * FROM campaigns WHERE id = ?",
        (campaign_id,)
    ).fetchone()

    recipient = connection.execute(
        "SELECT * FROM recipients WHERE campaign_id = ? LIMIT 1",
        (campaign_id,)
    ).fetchone()

    connection.close()

    if not campaign or not recipient:
        return "Campaign or recipient not found", 404

    tracking_link = url_for(
        "simulate",
        campaign_id=campaign_id,
        recipient_id=recipient["id"],
        _external=True
    )

    return render_template(
        "email_preview.html",
        campaign=campaign,
        recipient=recipient,
        tracking_link=tracking_link
    )


@app.route(
    "/simulate/<int:campaign_id>/<int:recipient_id>",
    methods=["GET", "POST"]
)
def simulate(campaign_id, recipient_id):

    connection = get_connection()

    recipient = connection.execute(
        """
        SELECT * FROM recipients
        WHERE id = ? AND campaign_id = ?
        """,
        (recipient_id, campaign_id)
    ).fetchone()

    if not recipient:
        connection.close()
        return "Recipient not found", 404

    # Handle mock credential submission
    if request.method == "POST":

        # IMPORTANT:
        # We deliberately do NOT read or store the password.

        connection.execute(
            """
            UPDATE recipients
            SET credential_submitted = 1
            WHERE id = ?
            """,
            (recipient_id,)
        )

        connection.commit()
        connection.close()

        return render_template(
            "simulation.html",
            campaign_id=campaign_id,
            recipient_id=recipient_id,
            submitted=True
        )

    # Record click only once
    already_clicked = connection.execute(
        """
        SELECT id FROM click_events
        WHERE recipient_id = ?
        LIMIT 1
        """,
        (recipient_id,)
    ).fetchone()

    if not already_clicked:

        ip_address = "127.0.0.1"
        user_agent = request.headers.get(
            "User-Agent",
            "Unknown"
        )
        location = "Localhost (simulated)"

        connection.execute(
            """
            INSERT INTO click_events
            (recipient_id, ip_address, user_agent, location)
            VALUES (?, ?, ?, ?)
            """,
            (
                recipient_id,
                ip_address,
                user_agent,
                location
            )
        )

        connection.execute(
            """
            UPDATE recipients
            SET clicked = 1
            WHERE id = ?
            """,
            (recipient_id,)
        )

        connection.commit()

    connection.close()

    return render_template(
        "simulation.html",
        campaign_id=campaign_id,
        recipient_id=recipient_id,
        submitted=False
    )

if __name__ == "__main__":
    app.run(debug=True)