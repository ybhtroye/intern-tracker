import requests
import datetime
import json

def fetch_jobs_from_api():
    # ReliefWeb 官方开放API：查询带 'law' 或 'legal' 的 'internship' 岗位
    url = "https://api.reliefweb.int/v1/jobs"
    params = {
        "appname": "intern-tracker",
        "query[value]": '(title:"law" OR title:"legal" OR body:"international law") AND (title:"intern" OR title:"internship")',
        "profile": "full",
        "limit": 20, # 获取最近的20个岗位
        "sort[]": "date:desc"
    }
    
    jobs =[]
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if 'data' in data:
            for item in data['data']:
                fields = item.get('fields', {})
                jobs.append({
                    'title': fields.get('title', 'Unknown Title'),
                    'link': fields.get('url', '#'),
                    'organization': fields.get('source', [{'name': 'Unknown'}])[0]['name'],
                    'closing_date': fields.get('date', {}).get('closing', 'N/A')[:10],
                    'country': fields.get('country', [{'name': 'Various/Remote'}])[0]['name']
                })
    except Exception as e:
        print(f"API请求失败: {e}")
        
    return jobs

def generate_html(jobs):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    html = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>⚖️ 国际法 & 国际组织实习动态追踪</title>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; color: #333; line-height: 1.6; background-color: #f4f7f6; }}
            .header {{ text-align: center; margin-bottom: 40px; }}
            h1 {{ color: #2c3e50; font-size: 1.8em; }}
            .update-time {{ color: #7f8c8d; font-size: 0.9em; }}
            .job-card {{ background: #fff; border-left: 5px solid #2980b9; padding: 20px; margin-bottom: 20px; border-radius: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); transition: transform 0.2s; }}
            .job-card:hover {{ transform: translateY(-3px); box-shadow: 0 4px 10px rgba(0,0,0,0.1); }}
            .job-title {{ font-size: 1.25em; font-weight: 600; margin-bottom: 10px; }}
            .job-title a {{ text-decoration: none; color: #2980b9; }}
            .job-title a:hover {{ text-decoration: underline; color: #1a5276; }}
            .job-meta {{ font-size: 0.9em; color: #555; display: flex; flex-wrap: wrap; gap: 15px; margin-top: 10px; }}
            .badge {{ background: #ecf0f1; padding: 4px 8px; border-radius: 4px; font-size: 0.85em; color: #2c3e50; font-weight: 500; }}
            .footer {{ margin-top: 40px; text-align: center; font-size: 0.85em; color: #95a5a6; }}
            
            /* 重点国际组织直达链接区 */
            .quick-links {{ background: #fff; padding: 20px; border-radius: 6px; margin-bottom: 30px; border: 1px solid #e1e8ed; }}
            .quick-links h3 {{ margin-top: 0; color: #d35400; font-size: 1.1em; }}
            .quick-links ul {{ margin: 0; padding-left: 20px; }}
            .quick-links li {{ margin-bottom: 8px; }}
            .quick-links a {{ color: #d35400; text-decoration: none; }}
            .quick-links a:hover {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>⚖️ 国际法学 & 国际组织实习岗位更新</h1>
            <div class="update-time">页面每天自动从国际组织开放数据源抓取最新未截止岗位。<br><strong>最后更新时间:</strong> {now} (UTC)</div>
        </div>
        
        <div class="quick-links">
            <h3>📌 长期滚动招募的核心机构 (建议定期查看)</h3>
            <ul>
                <li><a href="https://www.icc-cpi.int/jobs/internships-and-visiting-professionals" target="_blank">国际刑事法院 (ICC) - 实习与访问学者页面</a></li>
                <li><a href="https://pca-cpa.org/en/about/employment/internship-program/" target="_blank">常设仲裁法院 (PCA) - 助理法律顾问实习</a></li>
                <li><a href="https://careers.un.org/" target="_blank">联合国秘书处法律事务厅 (UN OLA) - 请在系统中搜索 Legal Internship</a></li>
                <li><a href="https://www.itlos.org/en/main/the-registry/training-and-internship-programmes/" target="_blank">国际海洋法法庭 (ITLOS) - 实习项目</a></li>
            </ul>
        </div>
        
        <h2>📡 最新抓取的活跃岗位 (距截止日期较近)</h2>
        <div id="jobs">
    """
    
    if not jobs:
        html += "<p style='text-align:center; color:#7f8c8d; padding:20px;'>今天暂未从API获取到新的对口实习岗位，请查看上方长期招募链接。</p>"
    else:
        for job in jobs:
            html += f"""
            <div class="job-card">
                <div class="job-title"><a href="{job['link']}" target="_blank">{job['title']}</a></div>
                <div class="job-meta">
                    <span class="badge">🏛️ 机构: {job['organization']}</span>
                    <span class="badge">📍 地点: {job['country']}</span>
                    <span class="badge" style="color:#c0392b;">⏳ 截止日期: {job['closing_date']}</span>
                </div>
            </div>
            """
            
    html += """
        </div>
        <div class="footer">
            Built with Python & GitHub Actions | Data Source: ReliefWeb API
        </div>
    </body>
    </html>
    """
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    jobs = fetch_jobs_from_api()
    generate_html(jobs)
