import feedparser
import datetime

# 目标RSS订阅源 (这里以 UNjobs 的法律主题和国际法主题为例)
FEEDS =[
    "https://unjobs.org/themes/legal/feed",
    "https://unjobs.org/themes/international-law/feed"
]

# 筛选关键词：只看实习
KEYWORDS =['intern', 'internship', 'trainee', 'fellowship', 'stagiaire']

def fetch_jobs():
    jobs =[]
    for url in FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                title = entry.title.lower()
                # 判断标题中是否包含实习的关键词
                if any(keyword in title for keyword in KEYWORDS):
                    jobs.append({
                        'title': entry.title,
                        'link': entry.link,
                        'published': entry.published
                    })
        except Exception as e:
            print(f"抓取 {url} 失败: {e}")
            
    # 去重
    unique_jobs = {job['link']: job for job in jobs}.values()
    return list(unique_jobs)

def generate_html(jobs):
    # 生成一个极简的网页
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    html = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>国际法实习岗位自动追踪</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6; }}
            h1 {{ color: #2c3e50; }}
            .job-card {{ background: #f9f9f9; border-left: 4px solid #3498db; padding: 15px; margin-bottom: 15px; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
            .job-title {{ font-size: 1.2em; font-weight: bold; }}
            .job-title a {{ text-decoration: none; color: #2980b9; }}
            .job-title a:hover {{ text-decoration: underline; }}
            .job-date {{ color: #7f8c8d; font-size: 0.9em; margin-top: 5px; }}
            .footer {{ margin-top: 30px; font-size: 0.8em; color: #95a5a6; border-top: 1px solid #eee; padding-top: 10px; }}
        </style>
    </head>
    <body>
        <h1>⚖️ 国际法学 & 国际组织实习岗位更新</h1>
        <p>页面每天自动从UNJobs等平台抓取更新。</p>
        <p><strong>最后更新时间:</strong> {now} (UTC)</p>
        
        <div id="jobs">
    """
    
    if not jobs:
        html += "<p>今天没有抓取到新的法学实习岗位。</p>"
    else:
        for job in jobs:
            html += f"""
            <div class="job-card">
                <div class="job-title"><a href="{job['link']}" target="_blank">{job['title']}</a></div>
                <div class="job-date">发布时间/抓取标记: {job['published']}</div>
            </div>
            """
            
    html += """
        </div>
        <div class="footer">
            Built with Python & GitHub Actions
        </div>
    </body>
    </html>
    """
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    jobs = fetch_jobs()
    generate_html(jobs)
