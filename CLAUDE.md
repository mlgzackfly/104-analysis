# CLAUDE.md - AI Assistant Guide for 104-analysis

## Project Overview

**104-analysis** is a Python-based tool for visualizing job relationship networks from 104.com.tw (Taiwan's largest job bank). The project creates network graphs showing how different job postings are related to each other, helping users understand job market connections and related opportunities.

### Project Purpose
- Scrape related job data from 104.com.tw API
- Build a network graph of job relationships
- Visualize job connections using NetworkX and Matplotlib
- Support customizable depth for relationship traversal

### Primary Language
- **Code**: Python 3.x
- **Documentation**: Traditional Chinese (繁體中文)

---

## Codebase Structure

```
104-analysis/
├── README.md                      # Main documentation (Chinese)
├── requirements.txt               # Python dependencies
├── .gitignore                     # Git ignore rules
├── main.py                        # Entry point (currently minimal/incomplete)
├── related_jobs_network.py        # Main implementation
├── example/                       # Sample API response JSONs
│   ├── applyAnalysisToJob.json
│   ├── content.json
│   └── similarJobs.json
└── img/                          # Output visualizations
    └── node.png                  # Example graph output
```

### Key Files

#### `related_jobs_network.py` (Primary Implementation)
- **Class**: `RelatedJobsGraph`
- **Purpose**: Main class for building and visualizing job relationship graphs
- **Key Methods**:
  - `__init__(start_job_id, max_depth)`: Initialize graph with starting job
  - `get_job_name(job_id)`: Extract job title from 104.com.tw
  - `get_related_jobs(job_id, depth, parent_node)`: Recursive method to fetch related jobs
  - `draw_graph()`: Visualize the network using matplotlib

#### `main.py` (Incomplete/Legacy)
- Contains stub functions for API endpoints
- Not currently functional
- May be intended for future API utilities

#### `example/` Directory
Contains sample JSON responses from 104.com.tw APIs for reference and testing

---

## Key Components

### RelatedJobsGraph Class

```python
class RelatedJobsGraph:
    def __init__(self, start_job_id='83ix3', max_depth=3)
```

**Attributes**:
- `start_job_id`: Initial job posting ID to analyze
- `max_depth`: Maximum depth for recursive relationship traversal
- `G`: NetworkX Graph object storing job relationships
- `headers`: HTTP headers with Referer for API requests

**Workflow**:
1. Initialize with starting job ID
2. Recursively fetch related jobs up to max_depth
3. Build NetworkX graph with job names as nodes
4. Visualize using Spring Layout algorithm

---

## Dependencies & Setup

### Python Dependencies (requirements.txt)
```
matplotlib==3.7.2   # Graph visualization
networkx==3.1       # Network graph construction
requests==2.31.0    # HTTP API requests
```

### Installation Steps
```bash
# Clone repository
git clone https://github.com/mlgzackfly/104-analysis.git
cd 104-analysis

# Install dependencies
pip install -r requirements.txt
```

### Running the Tool
```bash
python related_jobs_network.py
```

**Interactive Prompts**:
- Enter starting job ID (default: 83ix3)
- Enter max depth (default: 3)

---

## API Integration

### 104.com.tw Endpoints Used

#### 1. Job Content Endpoint
```
https://www.104.com.tw/job/{job_id}
```
- **Purpose**: Fetch job title from HTML page
- **Extraction**: Regex pattern `<title>(.*?)｜` to get job name

#### 2. Similar Jobs API
```
https://www.104.com.tw/job/ajax/similarJobs/{job_id}
```
- **Purpose**: Get list of related job postings
- **Response Format**: JSON with job list, pagination info
- **Key Fields**:
  - `data.list[]`: Array of related jobs
  - `jobNo`: Job number
  - `name`: Job title
  - `link.job`: Relative URL to job posting
  - `custName`: Company name
  - `area`: Location
  - `salaryDesc`: Salary information

#### 3. Headers Required
```python
headers = {
    "Referer": f"https://www.104.com.tw/jobs/apply/analysis/{job_id}?jobsource=my104_apply"
}
```

---

## Code Conventions

### Style Guidelines

1. **Language**: Code comments and strings in Traditional Chinese
2. **Indentation**: 4 spaces (Python standard)
3. **Class Names**: PascalCase (e.g., `RelatedJobsGraph`)
4. **Function Names**: snake_case (e.g., `get_job_name`)
5. **Variable Names**: snake_case (e.g., `start_job_id`)

### Best Practices Observed

1. **Font Configuration**: Uses Microsoft YaHei for Chinese character support
   ```python
   plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
   plt.rcParams['axes.unicode_minus'] = False
   ```

2. **HTML Decoding**: Uses `html.unescape()` for job names with HTML entities

3. **Warning Suppression**: Filters UserWarning from matplotlib
   ```python
   warnings.filterwarnings("ignore", category=UserWarning)
   ```

4. **Regex for Job ID Extraction**: Pattern `r"//www\.104\.com\.tw/job/(\w+)"`

5. **Graph Visualization Settings**:
   - Layout: Spring Layout with 500 iterations
   - Node size: 10000
   - Font size: 16
   - Color map: 'tab20c' for varied node colors
   - Figure size: (50, 50) for large graphs

### Error Handling
- Fallback to job_id if job name extraction fails
- No explicit exception handling for API requests (could be improved)

---

## Development Workflows

### Adding New Features

1. **Modify Graph Algorithm**:
   - Edit `related_jobs_network.py`
   - Update `get_related_jobs()` for traversal logic
   - Modify `draw_graph()` for visualization changes

2. **Add New API Endpoints**:
   - Reference `example/` JSON files for response structure
   - Add new methods to `RelatedJobsGraph` class
   - Update headers if needed

3. **Testing**:
   - Use small max_depth (1-2) for quick testing
   - Verify graph output in generated matplotlib window
   - Check console for "未找到工作ID" (job ID not found) errors

### Common Modifications

1. **Change Layout Algorithm**:
   ```python
   # Current: Spring Layout
   pos = nx.spring_layout(self.G, iterations=500)

   # Alternatives:
   # pos = nx.kamada_kawai_layout(self.G)
   # pos = nx.circular_layout(self.G)
   ```

2. **Adjust Visualization**:
   - `node_size`: Adjust for readability
   - `font_size`: Currently 16, increase for better visibility
   - `figsize`: (50, 50) can be reduced for smaller graphs

3. **Filter Jobs**:
   - Add conditions in `get_related_jobs()` to filter by salary, location, etc.

---

## Git Workflow

### Recent Commit Pattern

Analysis of recent commits shows:
```
feat: update graph image
feat: add custom node colors to the graph
feat: use Spring Layout for graph visualization
style: change fontsize to 16
fix: correct the initial node name issue
```

### Commit Conventions

- **feat**: New features
- **fix**: Bug fixes
- **style**: Code style changes (formatting, font size)
- **docs**: Documentation updates

### Branching Strategy

- **Main Branch**: Primary development branch
- **Feature Branches**: Named with `claude/` prefix for AI-assisted development
  - Example: `claude/claude-md-mi5e2hiio7ptoj7h-01SEUDEV5Wx6QmDwqmBcW4Y9`

---

## Common AI Assistant Tasks

### 1. Fixing Encoding Issues
```python
# If characters display incorrectly, ensure:
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # Or other Chinese fonts
```

### 2. Improving API Error Handling
```python
def get_related_jobs(self, job_id, depth, parent_node=None):
    try:
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print(f"API請求失敗: {e}")
        return
```

### 3. Adding Rate Limiting
```python
import time

# Add delay between requests
time.sleep(0.5)  # 500ms delay
```

### 4. Saving Graph to File
```python
# In draw_graph() method, replace plt.show() with:
plt.savefig('output_graph.png', dpi=300, bbox_inches='tight')
```

### 5. Adding Progress Indicators
```python
print(f"正在處理深度 {depth}/{self.max_depth}, 節點: {parent_node}")
```

---

## Important Notes for AI Assistants

### When Modifying Code

1. **Preserve Chinese Comments**: Keep all Chinese language comments intact
2. **Test with Default Job ID**: Use '83ix3' for consistency with documentation
3. **Check Font Availability**: Microsoft YaHei may not be available on all systems
4. **API Rate Limits**: 104.com.tw may have rate limiting; add delays if needed
5. **Graph Memory**: Large depth values (>4) can create very large graphs

### Code Quality Checks

1. **Verify API Responses**: Check that job IDs are correctly extracted
2. **Handle Missing Data**: Job names may not always be retrievable
3. **Unicode Handling**: Ensure proper encoding for Chinese characters
4. **Graph Visualization**: Test with different node counts

### File Modifications

- **Never modify**: `example/` JSON files (reference data)
- **Update when adding features**: `README.md` (keep in Chinese)
- **Auto-generated**: `img/node.png` (visualization output)
- **Git ignore**: `.idea/` (IDE files)

---

## Troubleshooting

### Common Issues

1. **Font Not Found Warning**
   - Install Microsoft YaHei or modify to use available Chinese font
   - On Linux: `sudo apt-get install fonts-wqy-zenhei`

2. **API Request Failures**
   - Check internet connection
   - Verify job ID exists on 104.com.tw
   - Add error handling and retries

3. **Graph Not Displaying**
   - Ensure matplotlib backend is configured
   - On headless systems, save to file instead of showing

4. **Slow Performance**
   - Reduce max_depth
   - Add request caching
   - Implement parallel requests (carefully)

---

## Future Enhancements

### Potential Improvements

1. **Command Line Arguments**: Replace input() with argparse
2. **Data Persistence**: Save graph data to JSON/pickle
3. **Interactive Visualization**: Use plotly or networkx with D3.js
4. **Job Details**: Include salary, location in node tooltips
5. **Export Formats**: Support GraphML, GEXF for external analysis
6. **Caching**: Store API responses to reduce redundant requests
7. **Testing**: Add unit tests for graph construction
8. **Configuration**: Use config file for visualization parameters

### API Endpoint Stubs (main.py)

The `main.py` file contains incomplete function definitions:
- `applyAnalysisToJob(job_no)`: Could fetch job application analytics
- `similarJobs(job_id)`: Already implemented in `RelatedJobsGraph`
- `content(job_id)`: Could fetch detailed job content

These could be developed into a separate API utility module.

---

## Quick Reference

### Run the Tool
```bash
python related_jobs_network.py
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Example Job IDs
- Default: `83ix3`
- Format: Alphanumeric (e.g., `7fe9t`, `70dww`, `7sjd4`)

### Default Configuration
- **Starting Job**: 83ix3
- **Max Depth**: 3
- **Layout**: Spring (500 iterations)
- **Node Size**: 10000
- **Font Size**: 16
- **Color Map**: tab20c

---

## Maintainer Notes

- **Primary Language**: Traditional Chinese for user-facing content
- **Target Users**: Job seekers in Taiwan
- **Data Source**: 104.com.tw (requires internet access)
- **Visualization**: Desktop display required (or modify for file output)

Last Updated: 2025-11-19
