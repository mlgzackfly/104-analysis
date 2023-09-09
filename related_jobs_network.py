import requests
import networkx as nx
import matplotlib.pyplot as plt
import re
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

def get_related_jobs(job_id, depth, max_depth, graph, headers, parent_node=None):
    if depth > max_depth:
        return
    if depth == 1:
        parent_node = job_id
    url = f"https://www.104.com.tw/job/ajax/similarJobs/{job_id}"
    response = requests.get(url, headers=headers)
    data = response.json()
    similar_jobs = data['data']['list']
    for job in similar_jobs:
        related_job_id = job['link']['job']
        related_job_name = job['name']

        job_id_match = re.search(r"//www\.104\.com\.tw/job/(\w+)", related_job_id)
        if job_id_match:
            job_id = job_id_match.group(1)

            # 將新的節點添加到圖中，並使用工作名稱作為節點名稱
            graph.add_node(related_job_name)
            graph.add_edge(parent_node, related_job_name)  # 連接父節點和新節點

            # 遞迴深入下一層
            get_related_jobs(job_id, depth + 1, max_depth, graph, headers, related_job_name)
        else:
            print("未找到工作ID")

# 起始工作 ID 和深度限制
start_job_id = "83ix3"
max_depth = 3  # 限制獲取相關工作的深度

# 設置 Referer 標頭
headers = {
    "Referer": "https://www.104.com.tw/jobs/apply/analysis/83ix3?jobsource=my104_apply"
}

# 創建一個空的關聯網路圖
G = nx.Graph()

# 將起始工作節點添加到圖中
G.add_node(start_job_id)

# 開始遞迴獲取相關工作
get_related_jobs(start_job_id, 1, max_depth, G, headers)

# 使用 Fruchterman-Reingold 布局算法
pos = nx.fruchterman_reingold_layout(G)

# 設置圖的大小，根據節點數量自動調整
plt.figure(figsize=(50, 50))

# 繪製關聯網路圖
nx.draw(G, pos, with_labels=True, node_size=900, node_color='skyblue', font_size=28)
plt.show()
