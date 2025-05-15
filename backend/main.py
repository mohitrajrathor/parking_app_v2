# main app program

# imports
from app import create_app

# app instance
app = create_app()


if __name__ == "__main__":
    # running debugging server
    app.run(debug=True, port=1234)
