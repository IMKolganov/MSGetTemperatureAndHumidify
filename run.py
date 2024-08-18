# run.py

from app.main import create_app, start_message_processing

app = create_app()

if __name__ == '__main__':
    start_message_processing(app)
    app.run(debug=True, host='0.0.0.0', port=5000)
