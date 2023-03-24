"""
Run the server.
"""

from sql_injection_demo import app
import sql_injection_demo.server
# import sql_injection_demo.models

app.run(host="0.0.0.0", port=8777, debug=True)
