import requests

def applyAnalysisToJob(job_no):
    # 分析的 URL
    analysisURL = f'https://www.104.com.tw/jb/104i/applyAnalysisToJob/all?job_no={job_no}'

def similarJobs(job_id):
    similarJobs = f'https://www.104.com.tw/job/ajax/similarJobs/{job_id}'

def content(job_id):
    content = f'https://www.104.com.tw/job/ajax/content/{job_id}'


if __name__ == '__main__':
    applyAnalysisToJob()