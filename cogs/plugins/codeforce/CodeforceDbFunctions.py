from util.db.UserConnection import UserDbConn

class CodeforceDbConn(UserDbConn):
    def __init__ (self):
        super().__init__()
    
    def get_handle(self, handle_name):
        query = "SELECT * FROM user_handle WHERE handle='{}';".format(handle_name)
        self.cur.execute(query)
        res = [i for i in self.cur]
        if res:
            return res[0]
        return None

    def remove_handle(self, handle_name):
        query = "DELETE FROM user_handle WHERE handle='{}';".format(handle_name)
        self.cur.execute(query)
        self.db.commit()

    def get_user_id(self, user_id):
        query = "SELECT * FROM user_handle WHERE user_id='{}';".format(user_id)
        self.cur.execute(query)
        res = [i for i in self.cur]
        if res:
            return res[0]
        return None


def setup(client):
    pass
