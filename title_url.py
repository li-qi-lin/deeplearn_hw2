import re
import requests
from bs4 import BeautifulSoup
from serpapi import GoogleSearch
import json

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
                query_result["query_url"] = self.result[index]['search_metadata']['google_scholar_url']
                query_result["title"] = self.result[index]["organic_results"][0]["title"]
                result_dict[index] = query_result
            js = json.dumps(result_dict, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False)
            print(js)
        except requests.RequestException as e:
            print(f"请求出错: {e}")
            return None, None
    
    def search_citations(self):
        """
        在 Google Scholar 上查询给定关键词引用量
        :return: 查询结果的标题和链接
        """
        citations_dict = {}
        try:
            # 遍历 params 列表中的每个查询字典
            for index, params_dict in enumerate(self.params):
                query_result = {}
                query_result["cited_num"] = self.result[index]["organic_results"][0]["inline_links"]["cited_by"]["total"]
                citations_dict[index] = query_result
            js = json.dumps(citations_dict, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False)
            print(js)
        except requests.RequestException as e:
            print(f"请求出错: {e}")
            return None, None

    def download_pdf(self):
        """
        在 Google Scholar 上查询给定关键词的pdf下载链接
        :return: 查询结果的标题和链接
        """
        downloadpdf_dict = {}
        try:
            # 遍历 params 列表中的每个查询字典
            for index, params_dict in enumerate(self.params):
                query_result = {}
                query_result["cited_num"] = self.result[index]["organic_results"][0]["resources"][0]["link"]
                downloadpdf_dict[index] = query_result
            js = json.dumps(downloadpdf_dict, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False)
            print(js)
        except requests.RequestException as e:
            print(f"请求出错: {e}")
            return None, None

ref_list = [{'编号': '1', '作者': 'ZhaoweiCai,GukyeongKwon,AvinashRavichandran,ErhanBas,ZhuowenTu,RahulBhotika,andStefan0Soatto', 
  '文章名称': 'X-detr: A versatile architecture for instance-wise visionlanguagetasks', '期刊': 'ArXiv,abs/2204'},
   {'编号': '2', '作者': 'Ding-Jie Chen, Songhao Jia, Yi-Chen Lo, Hwann-Tzong Chen, and Tyng-Luh Liu', '文章名称': 'See-through-text'
  ' grouping for referring image segmentation', '期刊': 'In Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV),2019'}] 
handler = ReferenceInfoHandler(ref_list)
handler.search_title_and_url_on_google_scholar()
handler.search_citations()
handler.download_pdf()