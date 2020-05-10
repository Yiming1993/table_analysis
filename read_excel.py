import xlrd
import mongoDB_services

class read_excel():
    def __init__(self):
        pass

    def read_excel_sheets(self, file_path):
        book = xlrd.open_workbook(file_path)
        num_sheets = len(book.sheets())
        print('number of sheets is {}, as follows\n{}'.format(num_sheets, book.sheet_names()))
        self.sheets = book.sheets()

    def merge_cell(self,sheet):
        rt = {}
        if sheet.merged_cells:
            # exists merged cell
            for item in sheet.merged_cells:
                for row in range(item[0], item[1]):
                    for col in range(item[2], item[3]):
                        rt.update({(row, col): (item[0], item[2])})
        return rt

    def read_sheet_content(self, sheet_index):
        sheet = self.sheets[sheet_index]
        nrows = sheet.nrows
        ncols = sheet.ncols
        print('number of rows: {}'.format(nrows))
        print('number of cols: {}'.format(ncols))
        excelhead = []
        for i in range(ncols):
            excel_head_values = sheet.col_values(i)
            excelhead.append(excel_head_values[0])
        print(excelhead)
        rows = sheet.nrows
        # 如果sheet为空，那么rows是0
        merged = self.merge_cell(sheet)
        if rows:
            for row in range(1,rows):
                data = sheet.row_values(row)  # 单行数据
                for index, content in enumerate(data):
                    if merged.get((row, index)):
                        # 这是合并后的单元格，需要重新取一次数据
                        data[index] = sheet.cell_value(*merged.get((row, index)))
                saved_data = {excelhead[x]:data[x] for x in range(len(excelhead))}
                yield saved_data

    def xls2xlsx(self, file_path):
        import pandas as pd

        file_name = file_path.split('.')
        file_new_name = file_name[0] + '.xlsx'
        data = pd.read_excel(file_path)
        data.to_excel(file_new_name, index=False)

    def save_data(self, db, collection, data, tag):
        mongoDB_services.save_data(db, collection, data, exist_detect_tag=tag, exist_detect=False)


if __name__ == '__main__':
    R = read_excel()
    file_path = '/Users/Yiming/PycharmProject/data_tools/人工智能领域公司数据包-20200407.xlsx'
    file_type = file_path.split('.')
    db = mongoDB_services.connect_db_nopwd('localhost','27017', '企业')
    if file_type == 'xls':
        R.xls2xlsx(file_path)
    else:
        R.read_excel_sheets(file_path)
        for data in R.read_sheet_content(1):
            R.save_data(db, 'IT桔子全人工智能企业_无融资',data,'公司名称')







