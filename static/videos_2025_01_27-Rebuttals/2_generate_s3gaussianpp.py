import os
import shutil

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def check_file_exists(filepath):
    exists = os.path.exists(filepath)
    print(f"Checking {filepath}: {'exists' if exists else 'does not exist'}")
    return exists

# 基础路径
base_src = "/lustre/qingpo.wuwu/3_Rebuttal/1_Ours/s3gaussianpp/work_dirs/2025_01_27-Rebuttals/dynamic-4gpus"
base_dst = "/lustre/qingpo.wuwu/3_Rebuttal/videos_2025_01_27-Rebuttals"

# 创建目标目录
for offset in ["0.5m", "1.0m", "1.5m"]:
    ensure_dir(f"{base_dst}/LaneChangeOffset-{offset}/ours/left")
    ensure_dir(f"{base_dst}/LaneChangeOffset-{offset}/ours/right")
ensure_dir(f"{base_dst}/UnchangedGT/ours")

# 场景ID列表
scenes = ["053", "080", "089", "323", "546", "640"]

# 首先复制所有GT视频（只需要从一个offset文件夹复制即可）
for scene in scenes:
    exp_name = f"{scene}_recon_tdim32_gdim4_maxnum200w_dense_depth_skymodel_deniter15000_negativetime_no_fine_hexplane_features_usehexplane_time_smoothness_weight0.0_do_2025_01_28_11_18_35-ok"
    src_base = f"{base_src}/LaneChangeOffset-0.5m/{exp_name}/eval"
    gt_src = f"{src_base}/full_videos/50000_gt_rgbs.mp4"
    gt_dst = f"{base_dst}/UnchangedGT/ours/{scene}.mp4"
    if check_file_exists(gt_src) and not os.path.exists(gt_dst):
        shutil.copy2(gt_src, gt_dst)
        print(f"Copied GT: {gt_src} -> {gt_dst}")

# 然后复制所有novel view视频
for scene in scenes:
    for offset in ["0.5", "1.0", "1.5"]:  # 移除'm'后缀
        offset_with_m = f"{offset}m"  # 用于目标路径
        exp_name = f"{scene}_recon_tdim32_gdim4_maxnum200w_dense_depth_skymodel_deniter15000_negativetime_no_fine_hexplane_features_usehexplane_time_smoothness_weight0.0_do_2025_01_28_11_18_35-ok"
        src_base = f"{base_src}/LaneChangeOffset-{offset_with_m}/{exp_name}/eval"
        print(f"\nProcessing scene {scene} with offset {offset}")
        
        # 复制左视角视频
        left_src = f"{src_base}/full_videos-novel_left-{offset}/50000_rgbs.mp4"
        left_dst = f"{base_dst}/LaneChangeOffset-{offset_with_m}/ours/left/{scene}.mp4"
        if check_file_exists(left_src) and not os.path.exists(left_dst):
            shutil.copy2(left_src, left_dst)
            print(f"Copied Left: {left_src} -> {left_dst}")
        
        # 复制右视角视频
        right_src = f"{src_base}/full_videos-novel_right-{offset}/50000_rgbs.mp4"
        right_dst = f"{base_dst}/LaneChangeOffset-{offset_with_m}/ours/right/{scene}.mp4"
        if check_file_exists(right_src) and not os.path.exists(right_dst):
            shutil.copy2(right_src, right_dst)
            print(f"Copied Right: {right_src} -> {right_dst}")