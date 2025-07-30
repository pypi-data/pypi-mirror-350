import numpy as np
import matplotlib.pyplot as plt
import datetime
from hjnwtx.colormap import cmp_hjnwtx
from mpl_toolkits.axes_grid1 import make_axes_locatable

def radarcomP(base_up, base_down, name="radar_composite"):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    combined_data = np.concatenate([base_up, base_down], axis=0)
    num_frames = base_up.shape[0]  # 获取图像数量
    fig, axes = plt.subplots(
        2,  # 行数(上下两层)
        num_frames,  # 列数(每层图像数量)
        figsize=(10 * num_frames, 10),  # 动态调整宽度
        squeeze=False  # 确保总是2D数组
    )
    vmin, vmax = 0, 70
    for i in range(2):  # 上下两层
        for j in range(num_frames):  # 每层的图像数量
            data_index = i * num_frames + j
            im = axes[i, j].imshow(
                combined_data[data_index, :, :],
                vmin=vmin,
                vmax=vmax,
                cmap=cmp_hjnwtx["pre_tqw"]  #pre_tqw  radar_nmc
            )
            axes[i, j].axis('off')  # 关闭坐标轴
            divider = make_axes_locatable(axes[i, j])
            cax = divider.append_axes("right", size="5%", pad=0.1)
            plt.colorbar(im, cax=cax)
    plt.tight_layout()
    output_filename = f"{name}_{timestamp}.png"
    plt.savefig(output_filename, bbox_inches='tight', dpi=300)
    plt.close()    
    print(f"图像已保存为: {output_filename}")

import numpy as np
import matplotlib.pyplot as plt
import datetime
from hjnwtx.colormap import cmp_hjnwtx
from mpl_toolkits.axes_grid1 import make_axes_locatable

def comP(base_up, base_down, name="radar_composite",vmin=150,vmax=320,cmap='summer'):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    combined_data = np.concatenate([base_up, base_down], axis=0)
    num_frames = base_up.shape[0]  # 获取图像数量
    fig, axes = plt.subplots(
        2,  # 行数(上下两层)
        num_frames,  # 列数(每层图像数量)
        figsize=(10 * num_frames, 10),  # 动态调整宽度
        squeeze=False  # 确保总是2D数组
    )
    for i in range(2):  # 上下两层
        for j in range(num_frames):  # 每层的图像数量
            data_index = i * num_frames + j
            im = axes[i, j].imshow(
                combined_data[data_index, :, :],
                vmin=vmin,
                vmax=vmax,
                cmap=cmap  #pre_tqw  radar_nmc
            )
            axes[i, j].axis('off')  # 关闭坐标轴
            divider = make_axes_locatable(axes[i, j])
            cax = divider.append_axes("right", size="5%", pad=0.1)
            plt.colorbar(im, cax=cax)
    plt.tight_layout()
    output_filename = f"{name}_{timestamp}.png"
    plt.savefig(output_filename, bbox_inches='tight', dpi=300)
    plt.close()    
    print(f"图像已保存为: {output_filename}")

#使用示例:
#draw_radar_composite(upper_data, lower_data, "my_radar_image")
#comP(base_up, base_down, name="radar_composite",vmin=150,vmax=320,cmap='summer')