# Deploy the classroom demo

In Render, choose New > Blueprint, connect this GitHub repository, and apply render.yaml. The configuration selects a Free Python web service, generates a stable SECRET_KEY, and starts the Flask factory with Gunicorn. After deployment, Render displays the public service URL.

This is a shared demonstration: anyone visiting can add, change, or delete requests. Use fictional data only. There are no user accounts or staff roles.

The Free service uses temporary storage. SQLite records are lost on service restart, redeployment or idle spin-down; three sample requests are recreated at startup. For lasting records, migrate to a durable database or configure a persistent disk on a suitable paid service. Free services may take about a minute to wake after inactivity.

Running locally remains unchanged: python app.py.
