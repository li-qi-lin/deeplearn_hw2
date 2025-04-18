import pdfplumber
import re
class PDFReferenceParser:
    def __init__(self, file_path):
        self.file_path = file_path

    def extract_text(self):
        text = ""
        with pdfplumber.open(self.file_path) as pdf:
            for page in pdf.pages:
                page_width = page.width
                # 计算左右栏的边界
                mid_width = page_width / 2
                left_text = page.crop((0, 0, mid_width, page.height)).extract_text()
                right_text = page.crop((mid_width, 0, page_width, page.height)).extract_text()
                if left_text:
                    text += left_text
                if right_text:
                    text += right_text
            # print(text)
        return text
    def clean_reference_content(self, references):
        """
        去除参考文献内容中的换行符
        :param references: 包含参考文献内容的列表，列表中的每个元素是一个字典，
                           字典包含'编号'、'作者'、'标题'、'期刊'、'年份'等键
        :return: 处理后的包含参考文献内容的列表
        """
        for ref in references:
            for key in ref:
                if isinstance(ref[key], str):
                    ref[key] = ref[key].replace('\n', '')
        return references

    def parse_references(self):
        text = self.extract_text()
        # 预处理文本，统一换行符格式
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        # 查找参考文献部分
        start_index = text.find("References")
        if start_index == -1:
            print("未找到参考文献部分")
            return []
        references_text = text[start_index + len("References"):].strip()
        # 对提取出的参考文献文本单独处理换行符
        references_text = references_text.replace('\n', ' ')
        references_text = references_text.replace('- ', '')
        references_text = references_text.replace('[', '\n[')
        # print(references_text)

        parsed_references = []
        # 按行分割参考文献文本，每行是一个参考文献
        lines = references_text.strip().split('\n')
        for line in lines:
            if line:
                number_part = line.split(']')
                parts = number_part[1].split('.')
                ref = {}
                # 提取编号
                ref['编号'] = number_part[0].strip('[]')
                # 提取作者
                ref['作者'] = parts[0].strip()
                # 提取文章名称
                ref['文章名称'] = parts[1].strip()
                ref['期刊'] = parts[2].strip()
                parsed_references.append(ref)

        return parsed_references

file_path = "/home/houjunlin/llq/deep/hw/deep_hw2/2312.12470v3.pdf"
parser = PDFReferenceParser(file_path)
# parser.parse_references()
references = parser.parse_references()
for ref in references:
    print(ref)
