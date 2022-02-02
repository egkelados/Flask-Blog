from FlaskBlogApp import app


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
    #host: the server is online for every address on the localhost!
    #port: changing the port of the server! 