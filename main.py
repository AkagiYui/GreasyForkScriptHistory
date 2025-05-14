import json
import requests
import matplotlib.pyplot as plt
import pandas as pd
import mplcyberpunk
from pathlib import Path
import matplotlib.font_manager as fm

def get_script_info(script_id: str) -> tuple[str, dict[str, dict[str, int]]]:
    # 获取脚本基本信息
    info_response = requests.get(f'https://greasyfork.org/zh-CN/scripts/{script_id}.json')
    script_info = json.loads(info_response.text)
    script_name = script_info['name']
    print(json.dumps(script_info, indent=4, ensure_ascii=False))
    
    # 获取安装统计数据
    stats_response = requests.get(f'https://greasyfork.org/zh-CN/scripts/{script_id}/stats.json')
    stats_json = json.loads(stats_response.text)
    
    return script_name, stats_json

def plot_install_history(script_id: str, output_dir: Path) -> None:
    script_name, stats_json = get_script_info(script_id)
    
    star_date: list[str] = []
    star_installs: list[int] = []
    star_temp: int = 0
    
    for date in stats_json:
        star_date.append(str(date))
        star_temp += stats_json[date]['installs']
        star_installs.append(star_temp)
    
    font_path = Path(__file__).parent / 'fonts' / 'HYWenHei.ttf'
    font = fm.FontProperties(fname=font_path)

    plt.style.use("cyberpunk")
    plt.figure(figsize=(20, 10), dpi=100)
    
    plt.title(script_name, fontproperties=font, size=30)
    plt.xlabel("时间", fontproperties=font, size=30)
    plt.ylabel("总安装数（Greasy Fork）", fontproperties=font, size=30)
    plt.xticks(fontproperties=font, size=20)
    plt.yticks(fontproperties=font, size=20)
    plt.plot(pd.to_datetime(star_date), star_installs, linewidth=4.0)
    
    # 保存到output目录，使用脚本ID作为文件名
    output_path = output_dir / f'history_{script_id}.png'
    plt.savefig(output_path)
    plt.close()  # 关闭图表，避免内存泄漏

def load_script_ids(config_file: str = 'script_ids.json') -> list[str]:
    """从配置文件加载脚本ID列表"""
    try:
        config_path = Path(__file__).parent / config_file
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config.get('script_ids', [])
    except FileNotFoundError:
        print(f"配置文件 {config_file} 不存在，将创建默认配置文件，请在修改完成后重新运行脚本")
        config = {"script_ids": ["500519"]}  # 默认只包含一个示例ID
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        return []
    except json.JSONDecodeError:
        print(f"配置文件 {config_file} 格式错误，请检查JSON格式")
        return []

def main() -> None:
    # 从配置文件加载脚本ID列表
    script_ids = load_script_ids()
    
    if not script_ids:
        print("没有找到有效的脚本ID，请检查配置文件")
        return
    
    # 创建output目录
    output_dir = Path(__file__).parent / 'output'
    output_dir.mkdir(exist_ok=True)
    
    # 为每个脚本生成图表
    for script_id in script_ids:
        try:
            print(f"正在生成脚本 {script_id} 的安装历史图表...")
            plot_install_history(script_id, output_dir)
            print(f"脚本 {script_id} 的图表已生成")
        except Exception as e:
            print(f"生成脚本 {script_id} 的图表时出错: {str(e)}")

if __name__ == "__main__":
    main()
