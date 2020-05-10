import mongoDB_services

class analysis():
    def __init__(self, db_name):
        self.db = mongoDB_services.connect_db_nopwd('localhost', '27017', db_name)

    def get_keys(self, collection_name):
        sample_data = mongoDB_services.get_one_sample_data(self.db, collection_name)
        self.header = list(sample_data.keys())


if __name__ == '__main__':
    A = analysis('企业')
    A.get_keys('IT桔子全人工智能企业')
