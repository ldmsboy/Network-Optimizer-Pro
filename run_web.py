from network_optimizer.web.server import app

if __name__ == '__main__':
    # Run the Flask web server
    app.run(host='0.0.0.0', port=5000, debug=True)
