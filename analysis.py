import mongoDB_services

class analysis():
    def __init__(self, db_name):
        self.db = mongoDB_services.connect_db_nopwd('localhost', '27017', db_name)

    def get_keys(self, collection_name):
        sample_data = mongoDB_services.get_one_sample_data(self.db, collection_name)
        self.header = list(sample_data.keys())

class data_merge():
    def __init__(self, merged_db_name, target_db_name):
        self.merged_db = mongoDB_services.connect_db_nopwd('localhost', '27017', merged_db_name)
        self.target_db = mongoDB_services.connect_db_nopwd('localhost', '27017', target_db_name)

    def tag_merge(self, merged_collection, merged_common_part_name, merged_tag_name, target_tag_collection, target_common_part_name, target_tag_name, merge_rule_collection):
        '''
        这里要求多对一的关系，即被merged的多个tag和唯一的目标tag对应，多对多时不能进行本操作
        '''

        for doc in mongoDB_services.get_data(self.target_db, target_tag_collection, {}, [target_common_part_name,target_tag_name]):
            common_part = doc[0]
            target_tag = doc[1]
            try:
                merged_data = mongoDB_services.get_one_sample_data_with_search(self.merged_db, merged_collection, merged_common_part_name,common_part)
                merged_tag = merged_data[merged_tag_name]
                tag_merge_rule = {"tag_name": target_tag, "coverd_tags": merged_tag}
                mongoDB_services.save_data(self.target_db, merge_rule_collection, tag_merge_rule,
                                           exist_detect_tag="tag_name", exist_detect=True)
            except:
                print('no matching find')


