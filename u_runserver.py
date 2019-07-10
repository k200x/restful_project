from apps import app



if __name__ == '__main__':
    # objectId = cheek("project_m|token|ec67d1b38e2a48a286242f44c15e5cea")
                      # "project_m|token|ec67d1b38e2a48a286242f44c15e5cea"
    # mongo_cheek(objectId)
    app.run(host="127.0.0.1",port=9112,debug=True)