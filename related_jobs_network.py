import requests
import networkx as nx
import matplotlib.pyplot as plt
import re
import warnings
import html


class RelatedJobsGraph:
    def __init__(self, start_job_id='83ix3', max_depth=3):
        warnings.filterwarnings("ignore", category=UserWarning)  # 忽略警告
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        plt.rcParams['axes.unicode_minus'] = False

        self.start_job_id = start_job_id
        self.max_depth = max_depth
        self.headers = {
            "Referer": f"https://www.104.com.tw/jobs/apply/analysis/{start_job_id}?jobsource=my104_apply"
        }
        self.G = nx.Graph()
        self.start_job_name = self.get_job_name(start_job_id)
        self.G.add_node(self.get_job_name(start_job_id))

    def get_job_name(self, job_id):
        url = f"https://www.104.com.tw/job/{job_id}"
        response = requests.get(url, headers=self.headers)
        match = re.search(r'<title>(.*?)｜', response.text)
        if match:
            job_name = match.group(1)
            return html.unescape(job_name)
        return job_id  # 如果無法獲取名稱，使用工作 ID 作為名稱

    def get_related_jobs(self, job_id, depth, parent_node=None):
        if depth > self.max_depth:
            return
        if depth == 1:
            parent_node = self.get_job_name(job_id)
        url = f"https://www.104.com.tw/job/ajax/similarJobs/{job_id}"
        response = requests.get(url, headers=self.headers)
        data = response.json()
        similar_jobs = data['data']['list']
        for job in similar_jobs:
            related_job_id = job['link']['job']
            related_job_name = job['name']

            job_id_match = re.search(r"//www\.104\.com\.tw/job/(\w+)", related_job_id)
            if job_id_match:
                job_id = job_id_match.group(1)

                # 將新的節點添加到圖中，並使用工作名稱作為節點名稱
                self.G.add_node(related_job_name)
                self.G.add_edge(parent_node, related_job_name)  # 連接父節點和新節點

                # 遞迴深入下一層
                self.get_related_jobs(job_id, depth + 1, related_job_name)
            else:
                print("未找到工作ID")

    def draw_graph(self):
        # 使用 Fruchterman-Reingold 布局算法
        pos = nx.fruchterman_reingold_layout(self.G)

        # 設置圖的大小，根據節點數量自動調整
        plt.figure(figsize=(50, 50))

        # 繪製關聯網路圖
        nx.draw(self.G, pos, with_labels=True, node_size=10000, node_color='skyblue', font_size=28)
        plt.show()


if __name__ == "__main__":
    # 提示用戶輸入工作 ID 和深度
    start_job_id = input("請輸入起始工作 ID（預設為 83ix3）：") or "83ix3"
    max_depth = int(input("請輸入最大深度（預設為 3）：") or 3)

    # 創建 RelatedJobsGraph 類別的實例
    graph = RelatedJobsGraph(start_job_id, max_depth)

    # 開始遞迴獲取相關工作
    graph.get_related_jobs(start_job_id, 1)

    # 繪製關聯網路圖
    graph.draw_graph()
