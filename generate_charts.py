import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

# 確保結果目錄存在
RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

# --- 1. 圖二：不同安全檢測方法的 F1 分數對比 ---
def generate_f1_score_chart():
    """生成圖二：不同安全檢測方法的 F1 分數對比"""
    
    # 論文中提供的數據 (表一)
    data = {
        "方法": ["本框架 (多模態)", "本框架 (單模態)", "Slither", "Mythril", "Securify"],
        "F1 分數": [0.765, 0.700, 0.674, 0.565, 0.610]
    }
    df = pd.DataFrame(data)
    
    # 繪圖
    plt.figure(figsize=(10, 6))
    bars = plt.bar(df["方法"], df["F1 分數"], color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'])
    
    # 添加數值標籤
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.01, round(yval, 3), ha='center', va='bottom')

    plt.ylim(0.0, 0.9)
    plt.title("圖二：不同安全檢測方法的 F1 分數對比", fontproperties='SimHei')
    plt.ylabel("F1 分數", fontproperties='SimHei')
    plt.xlabel("檢測方法", fontproperties='SimHei')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # 儲存圖片
    chart_path = os.path.join(RESULTS_DIR, "Figure_2_F1_Score_Comparison.png")
    plt.savefig(chart_path)
    plt.close()
    print(f"Generated chart: {chart_path}")
    return chart_path

# --- 2. 圖四：不同規模合約的處理時間與不同方法的吞吐量對比 ---
def generate_processing_time_chart():
    """生成圖四：不同規模合約的處理時間與不同方法的吞吐量對比"""
    
    # 模擬數據 (基於論文描述)
    # 處理時間 (左軸)
    contract_sizes = [50, 100, 200, 400, 800] # 行數
    framework_time = [0.15, 0.25, 0.45, 0.85, 1.5] # 秒
    slither_time = [0.05, 0.08, 0.12, 0.20, 0.35] # 秒 (更快)
    
    # 吞吐量 (右軸)
    methods = ["本框架", "Slither", "Mythril"]
    throughput = [6000, 15000, 10000] # 合約/小時
    
    # 繪圖 - 處理時間 (左軸)
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    ax1.plot(contract_sizes, framework_time, marker='o', label='本框架 (處理時間)', color='blue')
    ax1.plot(contract_sizes, slither_time, marker='s', label='Slither (處理時間)', color='green')
    ax1.set_xlabel("合約規模 (行數)", fontproperties='SimHei')
    ax1.set_ylabel("平均處理時間 (秒)", color='blue', fontproperties='SimHei')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.grid(axis='y', linestyle='--', alpha=0.5)
    ax1.legend(loc='upper left', prop={'family':'SimHei'})
    
    # 繪圖 - 吞吐量 (右軸)
    ax2 = ax1.twinx()
    bar_width = 50
    x_pos = [200, 400, 600] # 錯開位置
    
    bars = ax2.bar(x_pos, throughput, bar_width, alpha=0.6, color='red', label='吞吐量 (合約/小時)')
    ax2.set_ylabel("吞吐量 (合約/小時)", color='red', fontproperties='SimHei')
    ax2.tick_params(axis='y', labelcolor='red')
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(methods, fontproperties='SimHei')
    ax2.legend(loc='upper right', prop={'family':'SimHei'})
    
    plt.title("圖四：不同規模合約的處理時間與不同方法的吞吐量對比", fontproperties='SimHei')
    
    # 儲存圖片
    chart_path = os.path.join(RESULTS_DIR, "Figure_4_Processing_Time_Throughput.png")
    plt.savefig(chart_path)
    plt.close()
    print(f"Generated chart: {chart_path}")
    return chart_path

if __name__ == "__main__":
    # 檢查是否安裝了 SimHei 字體 (用於中文顯示)
    try:
        from matplotlib.font_manager import FontProperties
        FontProperties(fname='/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc')
    except:
        print("Warning: SimHei font not found. Charts may not display Chinese characters correctly.")
        # Fallback to default font
        plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False

    generate_f1_score_chart()
    generate_processing_time_chart()
