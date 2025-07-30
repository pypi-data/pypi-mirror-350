import pandas as pd


def add_binary_variable(
    ori_df: pd.DataFrame,
    var_name,
    start_col,
    end_col,
    start_timedelta=pd.Timedelta(days=0),
    end_timedelta=pd.Timedelta(days=0),
):
    print("Loading medical records file...")
    medical_df = read_aurum.read_file(
        file_path=os.path.join(VARIABLE_EXTRACTION_DIR, f"{var_name}_medical.txt"),
        table_name="observation",
    )
    medical_df = medical_df.dropna(subset=["value"])
    print(f"Original medical_df: {medical_df.shape}")

    # 合并ori_df和身高记录
    print("Merging ori_df and medical records...")
    merged_df = pd.merge(
        ori_df, medical_df[["patid", "obsdate", "value"]], on="patid", how="left"
    )
    print(f"merged_df: {merged_df.shape}")

    # 计算时间条件
    # 过滤出日期在指定期间的记录
    print("Processing...")
    merged_df = merged_df[
        (merged_df["obsdate"] >= (merged_df[start_col] + start_timedelta))
        & (merged_df["obsdate"] <= (merged_df[end_col] + end_timedelta))
    ]
    # merged_df["within_period"] = (
    #     merged_df["obsdate"] >= (merged_df[start_col] + start_timedelta)
    # ) & (merged_df["obsdate"] <= (merged_df[end_col] + end_timedelta))

    # 排序：优先级升序，期间内按事件时间降序
    merged_df_sorted = merged_df.sort_values(
        ["pregid", "obsdate"],
        ascending=[True, False],
    )

    # 提取每个pregid的第一条有效记录 (日期最晚的记录)
    merged_df_squeezed = merged_df_sorted.groupby("pregid").first().reset_index()

    # 合并回原始ori_df
    ori_df = ori_df.merge(
        merged_df_squeezed[["pregid", "value", "obsdate"]], on="pregid", how="left"
    )
    print(f"Finished df: {ori_df.shape}")
    # 将 'value' 修改为对应variable名称
    ori_df.rename(
        columns={"value": var_name, "obsdate": f"{var_name}_date"}, inplace=True
    )

    return ori_df
