import os
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

BASEPATH = os.getcwd()
result_folder_path = f'{BASEPATH}/results/2023-12-23-00-00to2024-02-06-00-00'
# start_date = datetime.strptime('2024-01-05-00-00', '%Y-%m-%d-%H-%M')
start_date = datetime.strptime('2023-12-24-00-00', '%Y-%m-%d-%H-%M')
# end_date = datetime.strptime('2023-12-15-23-00', '%Y-%m-%d-%H-%M')
end_date = datetime.strptime('2024-02-06-00-00', '%Y-%m-%d-%H-%M')

# 存储每个时间点的数据
data_per_time_upper = []
data_per_time_surface = []

# 列出目录中的所有 .npy 文件，并在日期范围内加载 "upper" 和 "surface" 文件
for file in os.listdir(result_folder_path):
    if file.endswith('.npy'):
        # 提取文件日期
        file_date_str = file.split('_')[2].split('.')[0]
        file_date = datetime.strptime(file_date_str, '%Y-%m-%d-%H-%M')

        # 检查文件日期是否在指定范围内
        if start_date <= file_date <= end_date:
            npy_file_path = os.path.join(result_folder_path, file)

            # 使用 numpy 加载 .npy 文件
            data = np.load(npy_file_path)

            # 存储数据，根据文件名中的关键字区分 "upper" 和 "surface"
            if 'upper' in file:
                data_per_time_upper.append((file_date, data))
            elif 'surface' in file:
                data_per_time_surface.append((file_date, data))

# 创建存放图像的文件夹
output_folder = f"img/{(start_date - timedelta(days=1)).strftime('%Y-%m-%d-%H-%M')}"
os.makedirs(output_folder, exist_ok=True)

# 设置字体大小
font_size = 18

upper_variables = ['geopotential', 'specific_humidity', 'temperature', 'u_component_of_wind', 'v_component_of_wind']
pressure_levels = ['1000', '925', '850', '700', '600', '500', '400', '300', '250', '200', '150', '100', '50']

# Specify the extent for the Asian region
lon_extent = [90, 160]
lat_extent = [5, 60]

# 循环每个时间点
for time, upper_data in data_per_time_upper:
    plt.close()  # 关闭先前的图
    fig = plt.figure(figsize=(12, 8))
    projection = ccrs.PlateCarree(central_longitude=105)
    ax = plt.axes(projection=projection)
    
    # Set the extent for the Asian region
    ax.set_extent([lon_extent[0], lon_extent[1], lat_extent[0], lat_extent[1]])

    lon = np.linspace(0, 360, upper_data.shape[3])
    lat = np.linspace(90, -90, upper_data.shape[2])
    lon_grid, lat_grid = np.meshgrid(lon, lat)

    # 计算850 hPa的温度数据
    temperature_850 = upper_data[upper_variables.index('temperature'), pressure_levels.index('850'), :, :] - 273.15

    # 计算500 hPa的geopotential height数据
    geopotential_height_500 = upper_data[upper_variables.index('geopotential'), pressure_levels.index('500'), :, :] / 10

    # 绘制地图背景
    ax.add_feature(cfeature.COASTLINE, edgecolor='lightgray')
    ax.add_feature(cfeature.BORDERS, linestyle=':')

    # 绘制850 hPa温度场的shading图
    cf_temperature = ax.contourf(lon_grid, lat_grid, temperature_850, transform=ccrs.PlateCarree(), cmap='viridis', levels=20)

    # 绘制500 hPa geopotential height的contour
    contour_geopotential_height = ax.contour(lon_grid, lat_grid, geopotential_height_500, transform=ccrs.PlateCarree(), colors='black', levels=20)

    # 添加 color bar
    cbar_ax_temperature = fig.add_axes([ax.get_position().x1 + 0.01, ax.get_position().y0, 0.02, ax.get_position().height])
    cbar_temperature = plt.colorbar(cf_temperature, cax=cbar_ax_temperature, orientation='vertical', extend='both')
    cbar_temperature.set_label('Temperature (°C)', fontsize=font_size)

    # 添加 contour labels
    plt.clabel(contour_geopotential_height, inline=True, fontsize=font_size, fmt='%1.0f')
    
    # # 查找相应时间的surface数据
    # surface_data = next(data for t, data in data_per_time_surface if t == time)

    # # 绘制海平面气压等高线
    # slp_contour = ax.contour(lon_grid, lat_grid, surface_data[0, :, :]/100,
    #                          transform=ccrs.PlateCarree(), colors='black', levels=20)
    
    # # 显示海平面气压的 contour labels
    # plt.clabel(slp_contour, inline=True, fontsize=font_size, fmt='%1.0f')

    # 添加网格线和标签
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                      linewidth=1, color='gray', alpha=0.5, linestyle='--')
    gl.top_labels = False
    gl.right_labels = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER

    # 设置字体大小
    gl.xlabel_style = {'size': font_size}
    gl.ylabel_style = {'size': font_size}

    # 获取子图的位置信息
    pos = ax.get_position()

    # 调整 title 位置
    fig.suptitle(f"850 hPa Temp. + 500 hPa GH at Time: {time}", fontsize=font_size, y=pos.y1 + 0.05)

    # 构建文件名，使用时间
    filename = f"{output_folder}/850T_500GH_{time.strftime('%Y%m%d_%H%M')}_asia.png"

    # 保存图像
    plt.savefig(filename, bbox_inches='tight', pad_inches=0.2)