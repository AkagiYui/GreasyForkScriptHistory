import json
import requests
import matplotlib.pyplot as plt
import pandas as pd
import mplcyberpunk
from pathlib import Path
import matplotlib.font_manager as fm

def get_script_info(script_id):
    # 获取脚本基本信息
    info_response = requests.get(f'https://greasyfork.org/zh-CN/scripts/{script_id}.json')
    script_info = json.loads(info_response.text)
    script_name = script_info['name']
    print(json.dumps(script_info, indent=4, ensure_ascii=False))
    
    # 获取安装统计数据
    stats_response = requests.get(f'https://greasyfork.org/zh-CN/scripts/{script_id}/stats.json')
    stats_json = json.loads(stats_response.text)
    
    return script_name, stats_json

def plot_install_history(script_id):
    script_name, stats_json = get_script_info(script_id)
    
    star_date = []
    star_installs = []
    star_temp = 0
    
    for date in stats_json:
        star_date.append(str(date))
        star_temp += stats_json[date]['installs']
        star_installs.append(star_temp)
    
    font_path = Path(__file__).parent.parent / 'fonts' / 'HYWenHei.ttf'
    font = fm.FontProperties(fname=font_path)

    plt.style.use("cyberpunk")
    plt.figure(figsize=(20, 10), dpi=100)
    
    # 修改字体大小的设置方式
    plt.title(script_name, fontproperties=font, size=30)
    plt.xlabel("时间", fontproperties=font, size=30)
    plt.ylabel("总安装数（Greasy Fork）", fontproperties=font, size=30)
    plt.xticks(fontproperties=font, size=20)
    plt.yticks(fontproperties=font, size=20)
    plt.plot(pd.to_datetime(star_date), star_installs, linewidth=4.0)
    plt.savefig('history.png')

print(plt.style.available)
if __name__ == "__main__":
    script_id = "500519"  # 可以根据需要修改脚本ID
    plot_install_history(script_id)
