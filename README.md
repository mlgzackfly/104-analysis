# 104 人力銀行 相關工作分析

**related_jobs_network** 是一個用於顯示 104 人力銀行相關工作的關聯圖的工具。你可以使用它來可視化與特定工作職位相關的其他工作，以幫助你更好地理解工作市場的關聯性。

## ✨ 功能特色

- 🔍 **自動抓取相關職位**：從 104.com.tw 自動抓取相關職位資訊
- 📊 **網路圖視覺化**：使用 NetworkX 和 Matplotlib 建立美觀的職位關聯圖
- 🎨 **多種配色方案**：支援 viridis、plasma、rainbow 等多種配色
- 📈 **深度控制**：可自訂搜尋深度，探索更多職位關聯
- 💾 **圖片輸出**：支援將圖形儲存為高解析度圖片
- 📊 **統計資訊**：自動顯示節點數、邊數、平均度數等統計資訊
- ⚡ **錯誤處理**：完善的錯誤處理和重試機制
- 📝 **日誌記錄**：詳細的執行日誌，方便追蹤處理進度

## 安裝

1. 使用 Git 將專案複製到本地：

   ```bash
   git clone https://github.com/mlgzackfly/104-analysis.git
   cd 104-analysis
   ```

2. 使用 pip 安裝相依套件：
   ```bash
   pip install -r requirements.txt
   ```

## 使用方式

### 基本使用

使用預設參數（起始職位 ID: 83ix3，深度: 3）：

```bash
python related_jobs_network.py
```

### 進階使用

#### 指定職位 ID 和深度

```bash
python related_jobs_network.py -j 83ix3 -d 3
```

#### 儲存圖片而不顯示

```bash
python related_jobs_network.py -j 83ix3 -o output.png
```

#### 使用不同的配色方案

```bash
# 使用 plasma 配色
python related_jobs_network.py --color plasma

# 使用 rainbow 配色
python related_jobs_network.py --color rainbow
```

#### 顯示詳細日誌

```bash
python related_jobs_network.py -v
```

#### 不顯示統計資訊

```bash
python related_jobs_network.py --no-stats
```

### 完整參數說明

```
使用方式: related_jobs_network.py [-h] [-j JOB_ID] [-d DEPTH] [-o OUTPUT]
                                   [--color {viridis,plasma,rainbow,coolwarm,spring,winter}]
                                   [--no-stats] [-v]

參數說明:
  -h, --help            顯示說明訊息
  -j, --job-id JOB_ID   起始職位 ID (預設: 83ix3)
  -d, --depth DEPTH     最大搜尋深度 (預設: 3)
  -o, --output OUTPUT   輸出圖片檔案路徑（不指定則顯示圖形）
  --color {viridis,plasma,rainbow,coolwarm,spring,winter}
                        配色方案 (預設: viridis)
  --no-stats            不顯示統計資訊
  -v, --verbose         顯示詳細日誌
```

### 使用範例

```bash
# 範例 1: 使用預設參數
python related_jobs_network.py

# 範例 2: 指定職位 ID 和深度
python related_jobs_network.py -j 7fe9t -d 2

# 範例 3: 儲存為高解析度圖片
python related_jobs_network.py -j 83ix3 -d 3 -o job_network.png

# 範例 4: 使用 plasma 配色並顯示詳細日誌
python related_jobs_network.py --color plasma -v

# 範例 5: 組合使用多個參數
python related_jobs_network.py -j 70dww -d 2 -o network.png --color coolwarm -v
```

## 示意圖

![示意圖](img/node.png)

## 程式碼架構

- **GraphConfig**: 圖形視覺化配置類別，包含所有視覺化參數
- **RelatedJobsGraph**: 主要類別，負責資料抓取和圖形建立
  - `get_job_name()`: 獲取職位名稱
  - `get_related_jobs()`: 遞迴獲取相關職位
  - `draw_graph()`: 繪製網路圖
  - `get_statistics()`: 獲取統計資訊

## 技術特點

### UI 美化
- ✨ 使用漸變色標示深度層級
- 📏 根據連接數動態調整節點大小
- 🎨 淺色背景提升可讀性
- 📊 添加顏色條圖例
- 🔤 優化字體大小和粗細

### 程式碼重構
- 🏗️ 使用 dataclass 管理配置
- 📝 完整的 type hints 和 docstrings
- ⚠️ 完善的錯誤處理機制
- 🔄 API 請求重試機制
- 📊 詳細的日誌記錄
- 🎯 命令列參數支援
- 🧪 避免重複訪問職位

## 相依套件

- matplotlib==3.7.2   # 圖形視覺化
- networkx==3.1       # 網路圖建構
- requests==2.31.0    # HTTP 請求

## 預設配置

預設的起始職位 ID 為 [83ix3](https://www.104.com.tw/job/83ix3?jobsource=apply_analyze)，深度為 3。你可以透過命令列參數自訂這些設定。

## 注意事項

- 搜尋深度越大，處理時間越長，建議從較小的深度開始測試
- API 請求之間有延遲（預設 0.3 秒），以避免對伺服器造成過大負擔
- 如果遇到網路錯誤，程式會自動重試最多 3 次

## 貢獻

如果你發現任何問題或想要改進這個工具，請隨時提交 issue 或提出 PR。

## 授權

MIT License