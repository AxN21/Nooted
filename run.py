from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=False)  # Modify to 'True' in development mode
