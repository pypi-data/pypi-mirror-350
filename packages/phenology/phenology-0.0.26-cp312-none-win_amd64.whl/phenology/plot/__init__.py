import numpy as np
import matplotlib.pyplot as plt


def set_rcParams(font_size=6.5,
                 axes_linewidth=0.5,
                 font_family='Arial',
                 svg_fonttype='none',
                 xtick_major_width=0.5,
                 ytick_major_width=0.5,
                 xtick_major_size=2,
                 ytick_major_size=2,
                 unicode_minus=False):
    """
    设置 matplotlib 的全局 rcParams 参数，方便统一调整图形样式。

    参数:
      font_size: 字体大小
      axes_linewidth: 坐标轴线宽
      font_family: 字体
      svg_fonttype: SVG 文件字体类型
      xtick_major_width: x 轴主刻度线宽
      ytick_major_width: y 轴主刻度线宽
      xtick_major_size: x 轴主刻度线长
      ytick_major_size: y 轴主刻度线长
      unicode_minus: 是否使用 Unicode 格式负号

    示例:
      set_rcParams(font_size=8, font_family='SimHei')
    """
    plt.rcParams['font.size'] = font_size
    plt.rcParams['axes.linewidth'] = axes_linewidth
    plt.rcParams['font.family'] = font_family
    plt.rcParams['svg.fonttype'] = svg_fonttype
    plt.rcParams['xtick.major.width'] = xtick_major_width
    plt.rcParams['ytick.major.width'] = ytick_major_width
    plt.rcParams['xtick.major.size'] = xtick_major_size
    plt.rcParams['ytick.major.size'] = ytick_major_size
    plt.rcParams['axes.unicode_minus'] = unicode_minus



# 定义一个初始化函数
def plt_init_start(width=3.33, height=3.33, dpi=300):
    plt.figure(figsize=(width/2.54, height/2.54), dpi=dpi)
    set_rcParams()
    plt.axes([0,0,1,1])
    fig = plt.gcf()
    return fig



# 定义一个初始化函数
def plt_init_end(pad=2, x_labelpad=3, y_labelpad=2):
    plt.gca().tick_params(axis='both', pad=pad)
    ylabel = plt.gca().get_ylabel()
    xlabel = plt.gca().get_xlabel()
    plt.ylabel(ylabel, labelpad=y_labelpad)
    plt.xlabel(xlabel, labelpad=x_labelpad)



def cmap_plot(cmap_name='BrBG', bins=50, dpi=200, marker_percentiles=None):
    """
    展示指定名称的颜色带，并分为指定数量的级别，同时标注级别。
    如果传入 marker_percentiles，则在对应百分位位置上方标记箭头。
    
    参数：
    - cmap_name (str): 颜色带名称，例如 'BrBG'。
    - bins (int): 分级数量，默认为 50。
    - marker_percentiles (list): 要标记的百分位数列表，范围 0~100，例如 [10, 50, 90]。
    - dpi (int): 图像分辨率，默认为 200。
    """
    cmap = plt.get_cmap(cmap_name)
    gradient1 = np.linspace(1/(bins*2), 1-1/(bins*2), bins)
    gradient2 = gradient1.reshape(1, -1)
    gradient2 = np.vstack((gradient2, gradient2))
    fig, ax = plt.subplots(figsize=(10, 0.8), dpi=dpi)
    
    # 显示颜色带
    ax.imshow(gradient2, aspect='auto', cmap=cmap)
    ax.set_title(f'{cmap_name} Colormap with {bins} Levels', fontsize=8)
    
    # 设置 x 轴刻度（每个颜色级别的中心）
    xlabels = [f'{int((p*100).round())}' for p in gradient1]
    plt.xticks(range(bins), xlabels, rotation=0, fontsize=7)
    plt.yticks([], [])
    
    # 如果传入了 marker_percentiles，则在对应位置上方添加箭头标记
    if marker_percentiles is not None:
        for p in marker_percentiles:
            # 根据百分位计算对应的 x 轴位置（范围 0~bins）
            x_marker = (p / 100) * bins
            ax.annotate(
                '',
                xy=(x_marker, 0.85),    # 箭头尖端位置（在颜色带上方）
                xytext=(x_marker, 1.18),  # 箭头尾部位置（紧贴颜色带顶部）
                zorder=24,
                arrowprops=dict(
                    arrowstyle='->',
                    color='black',  # 箭头填充颜色为黑色
                    lw=1,
                )
            )
            ax.annotate(
                '',
                xy=(x_marker, 0.8),    # 箭头尖端位置（在颜色带上方）
                xytext=(x_marker, 1.2),  # 箭头尾部位置（紧贴颜色带顶部）
                arrowprops=dict(
                    arrowstyle='->',
                    color='white',
                    lw=2.5),
                zorder=23
            )

    
    # 调整 y 轴范围，确保箭头能够显示
    ax.set_ylim(0, 1.2)
    
    # 隐藏上、左、右边框
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    
    plt.xlabel('Percentile (%)', fontsize=8)
    plt.show()
    plt.close()
    
    
    

def extract_colors_from_cmap(cmap_name, percentiles, show_cmap=False, show_plot=False, dpi=200):
    """
    从指定颜色带中提取对应于百分位数的颜色，并选择是否展示颜色。
    
    参数：
    - cmap_name (str): 颜色带名称，例如 'BrBG_r'。
    - percentiles (list): 分位数列表，范围 [1, 100]，例如 [10, 20, 30]。
    - show_plot (bool): 是否展示提取的颜色，默认为 False。
      
    返回：
    - colors (list): 提取的颜色列表，每个颜色为归一化的 RGB 值，范围 [0, 1]。
    """
    cmap = plt.get_cmap(cmap_name) # # 加载颜色带

    if show_cmap: cmap_plot(cmap_name, dpi=dpi, marker_percentiles=percentiles)

    percentiles_norm = [p / 100 for p in percentiles] # # 将百分位数转换为 [0, 1] 范围的比例值
    colors = [(round(r, 4), round(g, 4), round(b, 4)) for r, g, b, _ in [cmap(p) for p in percentiles_norm]] # # 提取分位数对应的颜色（忽略透明度通道 A）
    
    if not show_plot: return colors
    
    num_colors = len(colors)
    
    # 创建一个图形和轴对象
    fig, ax = plt.subplots(figsize=(num_colors*0.2, 0.5), dpi=dpi)
    
    # 绘制每个颜色的色块
    for i, color in enumerate(colors):
        color_with_alpha = (*color, 1)  # 确保有alpha通道
        ax.add_patch(plt.Rectangle((i, 0), 1, 1, color=color_with_alpha))
        # ax.text(i + 0.5, -0.2, f'{percentiles[i]}%', ha='center', va='center', fontsize=10, color='black')
    
    # 设置轴属性
    ax.set_xlim([0, num_colors])
    plt.xticks(np.arange(num_colors)+0.5, percentiles, fontsize=7)
    plt.yticks([], [])
    # 去除上边框，左右边框
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    # plt.xlabel('Percentile (%)', fontsize=8)
    plt.show()
    plt.close()
    return colors