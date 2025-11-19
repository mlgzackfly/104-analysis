#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
104 人力銀行相關工作網路圖視覺化工具

此工具可以從 104.com.tw 抓取相關職位資訊，並建立職位關聯網路圖。
支援自訂起始職位 ID 和搜尋深度。
"""

import requests
import networkx as nx
import matplotlib.pyplot as plt
import re
import warnings
import html
import argparse
import logging
import time
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass


# 配置類別
@dataclass
class GraphConfig:
    """圖形視覺化配置"""
    # 視覺化參數
    figure_size: Tuple[int, int] = (60, 40)
    node_size_base: int = 8000
    node_size_multiplier: int = 500
    edge_width: float = 1.5
    edge_alpha: float = 0.3
    font_size: int = 14
    font_size_title: int = 24
    title_pad: int = 20

    # 佈局參數
    spring_iterations: int = 1000
    spring_k: float = 0.5

    # 顏色配置
    color_scheme: str = 'viridis'  # 可選: 'viridis', 'plasma', 'rainbow', 'coolwarm'
    edge_color: str = '#CCCCCC'
    background_color: str = '#FAFAFA'

    # API 配置
    request_delay: float = 0.3  # 請求間隔（秒）
    max_retries: int = 3
    retry_delay: float = 1.0


class RelatedJobsGraph:
    """
    104 人力銀行相關工作網路圖類別

    此類別負責從 104.com.tw 抓取相關職位資訊，建立網路圖並進行視覺化。

    Attributes:
        start_job_id (str): 起始職位 ID
        max_depth (int): 最大搜尋深度
        config (GraphConfig): 圖形配置
        G (nx.Graph): NetworkX 圖形物件
        node_depths (Dict): 記錄每個節點的深度
    """

    def __init__(self, start_job_id: str = '83ix3', max_depth: int = 3,
                 config: Optional[GraphConfig] = None):
        """
        初始化相關工作圖形

        Args:
            start_job_id: 起始職位 ID
            max_depth: 最大搜尋深度
            config: 圖形配置物件
        """
        # 設定日誌
        self._setup_logging()

        # 忽略 matplotlib 警告
        warnings.filterwarnings("ignore", category=UserWarning)

        # 設定中文字體
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'WenQuanYi Micro Hei',
                                           'SimHei', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False

        self.start_job_id = start_job_id
        self.max_depth = max_depth
        self.config = config or GraphConfig()

        # 初始化圖形和資料結構
        self.G = nx.Graph()
        self.node_depths = {}  # 記錄每個節點的深度
        self.visited_jobs = set()  # 記錄已訪問的職位

        # 設定 HTTP headers
        self.headers = {
            "Referer": f"https://www.104.com.tw/jobs/apply/analysis/{start_job_id}?jobsource=my104_apply",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        # 初始化起始節點
        self.start_job_name = self._get_job_name_with_retry(start_job_id)
        if self.start_job_name:
            self.G.add_node(self.start_job_name)
            self.node_depths[self.start_job_name] = 0
            self.visited_jobs.add(start_job_id)
            logging.info(f"起始職位: {self.start_job_name} (ID: {start_job_id})")
        else:
            raise ValueError(f"無法獲取起始職位資訊: {start_job_id}")

    def _setup_logging(self):
        """設定日誌系統"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )

    def _get_job_name_with_retry(self, job_id: str) -> Optional[str]:
        """
        帶重試機制的職位名稱獲取

        Args:
            job_id: 職位 ID

        Returns:
            職位名稱，失敗則返回 None
        """
        for attempt in range(self.config.max_retries):
            try:
                name = self.get_job_name(job_id)
                if name:
                    return name
            except Exception as e:
                logging.warning(f"獲取職位名稱失敗 (嘗試 {attempt + 1}/{self.config.max_retries}): {e}")
                if attempt < self.config.max_retries - 1:
                    time.sleep(self.config.retry_delay * (attempt + 1))
        return None

    def get_job_name(self, job_id: str) -> Optional[str]:
        """
        從 104.com.tw 獲取職位名稱

        Args:
            job_id: 職位 ID

        Returns:
            職位名稱，失敗則返回 job_id
        """
        try:
            url = f"https://www.104.com.tw/job/{job_id}"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()

            match = re.search(r'<title>(.*?)｜', response.text)
            if match:
                job_name = match.group(1)
                return html.unescape(job_name)

            logging.warning(f"無法從 HTML 中提取職位名稱: {job_id}")
            return job_id

        except requests.RequestException as e:
            logging.error(f"請求職位頁面失敗 ({job_id}): {e}")
            return job_id

    def get_related_jobs(self, job_id: str, depth: int, parent_node: Optional[str] = None):
        """
        遞迴獲取相關職位

        Args:
            job_id: 職位 ID
            depth: 當前深度
            parent_node: 父節點名稱
        """
        # 檢查深度限制
        if depth > self.max_depth:
            return

        # 設定父節點
        if depth == 1:
            parent_node = self.get_job_name(job_id)

        # 檢查是否已訪問過此職位
        if job_id in self.visited_jobs and depth > 1:
            return

        try:
            # 獲取相關職位資料
            url = f"https://www.104.com.tw/job/ajax/similarJobs/{job_id}"
            logging.info(f"正在處理深度 {depth}/{self.max_depth}: {parent_node}")

            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            # 檢查回應資料
            if 'data' not in data or 'list' not in data['data']:
                logging.warning(f"無效的 API 回應格式: {job_id}")
                return

            similar_jobs = data['data']['list']
            logging.info(f"找到 {len(similar_jobs)} 個相關職位")

            # 處理每個相關職位
            for job in similar_jobs:
                try:
                    related_job_id = job.get('link', {}).get('job', '')
                    related_job_name = job.get('name', '')

                    if not related_job_id or not related_job_name:
                        continue

                    # 提取職位 ID
                    job_id_match = re.search(r"//www\.104\.com\.tw/job/(\w+)", related_job_id)
                    if not job_id_match:
                        continue

                    extracted_job_id = job_id_match.group(1)

                    # 避免重複處理
                    if extracted_job_id in self.visited_jobs:
                        continue

                    # 添加節點和邊
                    self.G.add_node(related_job_name)
                    self.G.add_edge(parent_node, related_job_name)
                    self.node_depths[related_job_name] = depth
                    self.visited_jobs.add(extracted_job_id)

                    # 添加請求延遲
                    time.sleep(self.config.request_delay)

                    # 遞迴處理下一層
                    self.get_related_jobs(extracted_job_id, depth + 1, related_job_name)

                except Exception as e:
                    logging.warning(f"處理相關職位時發生錯誤: {e}")
                    continue

        except requests.RequestException as e:
            logging.error(f"API 請求失敗 ({job_id}): {e}")
        except Exception as e:
            logging.error(f"處理職位時發生未預期的錯誤 ({job_id}): {e}")

    def draw_graph(self, output_file: Optional[str] = None):
        """
        繪製並顯示或儲存網路圖

        Args:
            output_file: 輸出檔案路徑，若為 None 則顯示圖形
        """
        if len(self.G.nodes()) == 0:
            logging.error("圖形中沒有節點，無法繪製")
            return

        logging.info(f"開始繪製圖形... (節點數: {len(self.G.nodes())}, 邊數: {len(self.G.edges())})")

        # 建立圖形
        fig, ax = plt.subplots(figsize=self.config.figure_size, facecolor=self.config.background_color)
        ax.set_facecolor(self.config.background_color)

        # 計算佈局
        pos = nx.spring_layout(
            self.G,
            iterations=self.config.spring_iterations,
            k=self.config.spring_k,
            seed=42  # 固定隨機種子以確保可重現性
        )

        # 根據深度設定節點顏色
        node_colors = [self.node_depths.get(node, 0) for node in self.G.nodes()]

        # 根據連接數設定節點大小
        node_sizes = [
            self.config.node_size_base + self.G.degree(node) * self.config.node_size_multiplier
            for node in self.G.nodes()
        ]

        # 繪製邊
        nx.draw_networkx_edges(
            self.G, pos,
            width=self.config.edge_width,
            alpha=self.config.edge_alpha,
            edge_color=self.config.edge_color,
            ax=ax
        )

        # 繪製節點
        nodes = nx.draw_networkx_nodes(
            self.G, pos,
            node_color=node_colors,
            node_size=node_sizes,
            cmap=plt.cm.get_cmap(self.config.color_scheme),
            vmin=0,
            vmax=self.max_depth,
            alpha=0.9,
            ax=ax
        )

        # 繪製標籤
        nx.draw_networkx_labels(
            self.G, pos,
            font_size=self.config.font_size,
            font_weight='bold',
            font_color='#333333',
            ax=ax
        )

        # 添加顏色條（圖例）
        if nodes:
            cbar = plt.colorbar(nodes, ax=ax, label='深度層級', shrink=0.8)
            cbar.set_ticks(range(self.max_depth + 1))
            cbar.ax.tick_params(labelsize=12)

        # 設定標題
        title = f"104 人力銀行職位關聯網路圖\n起始職位: {self.start_job_name}"
        plt.title(title, fontsize=self.config.font_size_title,
                 fontweight='bold', pad=self.config.title_pad)

        # 移除座標軸
        ax.axis('off')

        # 調整佈局
        plt.tight_layout()

        # 儲存或顯示圖形
        if output_file:
            logging.info(f"儲存圖形至: {output_file}")
            plt.savefig(output_file, dpi=300, bbox_inches='tight',
                       facecolor=self.config.background_color)
            logging.info("圖形已成功儲存")
        else:
            logging.info("顯示圖形...")
            plt.show()

    def get_statistics(self) -> Dict:
        """
        獲取圖形統計資訊

        Returns:
            包含統計資訊的字典
        """
        return {
            '節點總數': len(self.G.nodes()),
            '邊總數': len(self.G.edges()),
            '最大深度': self.max_depth,
            '實際深度': max(self.node_depths.values()) if self.node_depths else 0,
            '平均度數': sum(dict(self.G.degree()).values()) / len(self.G.nodes()) if len(self.G.nodes()) > 0 else 0,
            '已訪問職位數': len(self.visited_jobs)
        }

    def print_statistics(self):
        """列印圖形統計資訊"""
        stats = self.get_statistics()
        print("\n" + "="*50)
        print("圖形統計資訊")
        print("="*50)
        for key, value in stats.items():
            if isinstance(value, float):
                print(f"{key}: {value:.2f}")
            else:
                print(f"{key}: {value}")
        print("="*50 + "\n")


def parse_arguments():
    """解析命令列參數"""
    parser = argparse.ArgumentParser(
        description='104 人力銀行相關工作網路圖視覺化工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例:
  %(prog)s                          # 使用預設參數
  %(prog)s -j 83ix3 -d 3            # 指定職位 ID 和深度
  %(prog)s -j 83ix3 -o output.png   # 儲存為圖片
  %(prog)s -j 83ix3 --color plasma  # 使用不同配色
        """
    )

    parser.add_argument(
        '-j', '--job-id',
        type=str,
        default='83ix3',
        help='起始職位 ID (預設: 83ix3)'
    )

    parser.add_argument(
        '-d', '--depth',
        type=int,
        default=3,
        help='最大搜尋深度 (預設: 3)'
    )

    parser.add_argument(
        '-o', '--output',
        type=str,
        help='輸出圖片檔案路徑（不指定則顯示圖形）'
    )

    parser.add_argument(
        '--color',
        type=str,
        choices=['viridis', 'plasma', 'rainbow', 'coolwarm', 'spring', 'winter'],
        default='viridis',
        help='配色方案 (預設: viridis)'
    )

    parser.add_argument(
        '--no-stats',
        action='store_true',
        help='不顯示統計資訊'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='顯示詳細日誌'
    )

    return parser.parse_args()


def main():
    """主程式"""
    # 解析命令列參數
    args = parse_arguments()

    # 設定日誌級別
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # 顯示歡迎訊息
    print("="*60)
    print("104 人力銀行相關工作網路圖視覺化工具")
    print("="*60)
    print(f"起始職位 ID: {args.job_id}")
    print(f"搜尋深度: {args.depth}")
    print(f"配色方案: {args.color}")
    print("="*60 + "\n")

    try:
        # 建立配置
        config = GraphConfig(color_scheme=args.color)

        # 建立圖形物件
        graph = RelatedJobsGraph(
            start_job_id=args.job_id,
            max_depth=args.depth,
            config=config
        )

        # 開始抓取相關職位
        print("開始建立職位關聯網路...\n")
        graph.get_related_jobs(args.job_id, 1)

        # 顯示統計資訊
        if not args.no_stats:
            graph.print_statistics()

        # 繪製圖形
        graph.draw_graph(output_file=args.output)

        print("\n處理完成！")

    except KeyboardInterrupt:
        print("\n\n使用者中斷程式")
        logging.info("程式被使用者中斷")
    except Exception as e:
        print(f"\n發生錯誤: {e}")
        logging.error(f"程式執行失敗: {e}", exc_info=True)
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
