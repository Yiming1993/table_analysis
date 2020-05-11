from pymongo import MongoClient
from bson import ObjectId

'''
用于操作mongo数据库，包括登录，获取数据，保存数据和更新数据
'''

def connect_db(host, port, user_name, password, db_name):
    host = host
    port = port
    user_name = user_name
    user_pwd = password
    db_name = db_name
    uri = "mongodb://" + user_name + ":" + user_pwd + "@" + host + ":" + port + "/" + db_name
    client = MongoClient(uri, connect=True)
    db = client[db_name]
    return db

def connect_db_nopwd(host, port, db_name):
    host = host
    port = port
    db_name = db_name
    uri = "mongodb://" + host + ":" + port + "/" + db_name
    client = MongoClient(uri, connect=True)
    db = client[db_name]
    return db

def get_data(db, collection_name, find_rule, data_tag):
    data = db[collection_name].find(find_rule)
    for doc in data:
        if type(data_tag) == str:
            yield doc[data_tag]
        if type(data_tag) == list:
            single_data = []
            for tag in data_tag:
                single_data.append(doc[tag])
            yield single_data

def get_full_data(db, collection_name, find_rule):
    data = db[collection_name].find(find_rule)
    for doc in data:
        yield doc

def save_data(db, collection_name, data, exist_detect_tag = 'name', exist_detect = True):
    if exist_detect == True:
        exist = db[collection_name].find({exist_detect_tag: data[exist_detect_tag]}).count()
        if exist == 0:
            db[collection_name].insert(data)
            print('data {} is saved'.format(data[exist_detect_tag]))
        else:
            pass
            # print('data {} exists'.format(data[exist_detect_tag]))
    else:
        db[collection_name].insert(data)
        print('data {} is saved'.format(data[exist_detect_tag]))

def update_data(db, collection_name, id, data):
    db[collection_name].update({"_id":ObjectId(id)},{"$set":data}, True, True)
    print('data {} is updated with data {}'.format(id, data))

def connect_db_ssh(host_ssh, user_name_ssh, password_ssh, host, port, user_name, db_name, password):
    from sshtunnel import SSHTunnelForwarder
    server_addr = (host_ssh, 22)  ##服务器地址
    server_user = user_name_ssh  ##登录服务器的用户
    server_password = password_ssh  ##登录服务器的密码
    remote_bind_address =  (host, port)  ##云mongodb地址
    mongo_port = port  # mongo端口，一般默认27017
    mongo_user = user_name  ## 访问数据库的用户名
    mongo_password = password  # 访问数据库的密码
    mongo_database = db_name

    server = SSHTunnelForwarder(
        ssh_address_or_host=server_addr,
        ssh_password=server_password,
        ssh_username=server_user,
        remote_bind_address=remote_bind_address)
    server.start()

    client = MongoClient('127.0.0.1', server.local_bind_port)  ## 这里一定要填入ssh映射到本地的端口
    db = client[mongo_database]
    db.authenticate(mongo_user, mongo_password)

    return client

def data_transfer(db_1, collection_1, db_2, collection_2):
    data = db_2[collection_2].find({})
    for i in data:
        save_data(db_1, collection_1, i, exist_detect = False, exist_detect_tag="title")

def get_one_sample_data(db, collection):
    data = db[collection].find_one()

    return data

def get_one_sample_data_with_search(db, collection_name, find_tag, find_rule):
    data = db[collection_name].find_one({find_tag:{"$regex":find_rule}})
    return data