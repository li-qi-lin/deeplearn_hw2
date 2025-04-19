import re
import requests
from bs4 import BeautifulSoup
from serpapi import GoogleSearch
import json
import matplotlib.pyplot as plt

class ReferenceInfoHandler:
    def __init__(self, references):
        self.references = references
        self.article_titles = []  # 用于存储文章名称的列表
        self.params = []  # 用于存储访问的列表
        for ref in self.references:
            if '文章名称' in ref:
                self.article_titles.append(ref['文章名称'][0:50])
        for title in self.article_titles:
            # 构建字典，并将其添加到 params 列表
            params_dict = {
                'engine': 'google_scholar',
                'q': title,  # 每个文章标题作为 q 的值
                'api_key': '05769a47f0c9c04832b5669b540947598d4a703ba9460408335e88f7b28f8938'
            }
            self.params.append(params_dict)
        self.result = {} #保存网页信息的字典
        self.ref_result = {} #保存参考文献信息的字典
        # 遍历 params 列表中的每个查询字典
        for index, params_dict in enumerate(self.params):
            # 创建 GoogleSearch 对象
            search = GoogleSearch(params_dict)
            # 获取返回的字典数据
            query_result = search.get_dict()
            self.result[index] = query_result
        # print(self.result)
       
    def search_title_and_url_on_google_scholar(self):
        """
        在 Google Scholar 上查询给定关键词的相关信息
        :return: 查询结果的标题和链接
        """
        result_dict = {}
        try:
            # 遍历 params 列表中的每个查询字典
            for index, params_dict in enumerate(self.params):
                query_result = {}
                # 检查 'search_metadata' 是否存在
                if 'search_metadata' in self.result[index]:
                    query_result["query_url"] = self.result[index]['search_metadata'].get('google_scholar_url', 'URL not found')
                    # 检查 'organic_results' 是否存在，并且确保它不为空
                    if 'organic_results' in self.result[index] and len(self.result[index]['organic_results']) > 0:
                        query_result["title"] = self.result[index]["organic_results"][0]["title"]
                    else:
                        query_result["title"] = "Title not found"

                    result_dict[index] = query_result
                else:
                    print(f"Skipping index {index}: 'search_metadata' not found.")
            js = json.dumps(result_dict, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False)
            print(js)
        except requests.RequestException as e:
            print(f"请求出错: {e}")
            return None, None
    
    def search_citations(self):
        """
        在 Google Scholar 上查询给定关键词引用量
        :return: 查询结果的引用量
        """
        citations_dict = {}
        try:
            # 遍历 params 列表中的每个查询字典
            for index, params_dict in enumerate(self.params):
                query_result = {}

                # 检查 'organic_results' 是否存在，并且它的长度大于 0
                if 'organic_results' in self.result[index] and len(self.result[index]['organic_results']) > 0:
                    # 获取引用量
                    cited_by = self.result[index]["organic_results"][0]["inline_links"].get("cited_by", {})
                    cited_num = cited_by.get("total", 0)  # 如果没有 "cited_by" 信息，则默认为 0
                    query_result["cited_num"] = cited_num
                    citations_dict[index] = query_result
                else:
                    print(f"Skipping index {index}: 'organic_results' not found or empty.")

            js = json.dumps(citations_dict, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False)
            print(js)
            return citations_dict
        except requests.RequestException as e:
            print(f"请求出错: {e}")
            return None, None

    def download_pdf(self):
        """
        在 Google Scholar 上查询给定关键词的pdf下载链接
        :return: 查询结果的pdf下载链接
        """
        downloadpdf_dict = {}
        try:
            # 遍历 params 列表中的每个查询字典
            for index, params_dict in enumerate(self.params):
                query_result = {}

                # 检查 'organic_results' 是否存在，并且它的长度大于 0
                if 'organic_results' in self.result[index] and len(self.result[index]['organic_results']) > 0:
                    # 检查 'resources' 是否存在并且它的长度大于 0
                    if 'resources' in self.result[index]["organic_results"][0] and len(self.result[index]["organic_results"][0]["resources"]) > 0:
                        # 获取 PDF 下载链接
                        query_result["pdf_download"] = self.result[index]["organic_results"][0]["resources"][0].get("link", "Link not found")
                        downloadpdf_dict[index] = query_result
                    else:
                        print(f"Skipping index {index}: 'resources' not found or empty.")
                else:
                    print(f"Skipping index {index}: 'organic_results' not found or empty.")
            
            js = json.dumps(downloadpdf_dict, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False)
            print(js)
        except requests.RequestException as e:
            print(f"请求出错: {e}")
            return None, None
        
    def citations_api_code(self):
        """
        在 Google Scholar 上查询给定关键词的引用格式下载的API code
        :return: 查询结果的引用格式下载的API code
        """
        citations_api_code = {}
        try:
            # 遍历 params 列表中的每个查询字典
            for index, params_dict in enumerate(self.params):
                query_result = {}

                # 检查 'organic_results' 是否存在，并且它的长度大于 0
                if 'organic_results' in self.result[index] and len(self.result[index]['organic_results']) > 0:
                    # 检查 'result_id' 是否存在
                    if 'result_id' in self.result[index]["organic_results"][0]:
                        # 获取引用 API 代码
                        query_result["citations_api_code"] = self.result[index]["organic_results"][0]["result_id"]
                        citations_api_code[index] = query_result
                    else:
                        print(f"Skipping index {index}: 'result_id' not found.")
                else:
                    print(f"Skipping index {index}: 'organic_results' not found or empty.")
            
            js = json.dumps(citations_api_code, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False)
            print(js)
        except requests.RequestException as e:
            print(f"请求出错: {e}")
            return None, None
        
    def plot_citations(self):
        """
        根据引用量绘制柱状图
        """
        # 获取引用量数据
        citations_dict = self.search_citations()

        if citations_dict is None:
            print("没有获取到引用量数据")
            return
        # 按引用量从高到低排序
        sorted_citations = sorted(citations_dict.items(), key=lambda x: x[1]["cited_num"], reverse=True)

        indices = [item[0] for item in sorted_citations]  # 文献编号
        cited_nums = [item[1]["cited_num"] for item in sorted_citations]  # 引用量

        max_citations = 150000
        cited_nums = [min(cited_num, max_citations) for cited_num in cited_nums]

        plt.figure(figsize=(10, 6))
        plt.bar(indices, cited_nums, color='skyblue')
        plt.title("Citation Counts of References", fontsize=16)
        plt.xlabel("Reference Index", fontsize=12)
        plt.ylabel("Number of Citations", fontsize=12)
        plt.ylim(0, max_citations)
        plt.xticks(indices, rotation=45)  # 旋转横坐标标签，避免重叠
        plt.show()

handler = ReferenceInfoHandler(ref_list)
handler.search_title_and_url_on_google_scholar()
handler.search_citations()
handler.download_pdf()
handler.citations_api_code()
handler.plot_citations()