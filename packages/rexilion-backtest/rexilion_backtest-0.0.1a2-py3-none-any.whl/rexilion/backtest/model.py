from pathlib import Path
import pandas as pd
import os
import numpy as np
from rexilion.backtest import diagram, util, entryexitlogic, formula

def mean_normalize_backtesting(df, rolling_window, threshold, fees, sr_multiplier, backtest_mode):
    df["processed_data"] = formula.rolling_mean_normalize(df["data"].values, rolling_window)
    df["pos"] = entryexitlogic.entry_exit_threshold(df, rolling_window, threshold, backtest_mode)
    report = util.generate_report(df, rolling_window, threshold, fees, sr_multiplier)
    return report

def mean_normalize(df, backtest_mode_list, rolling_window_range, threshold_range, fees, sr_multiplier):
    if (isinstance(rolling_window_range,(np.generic, np.ndarray)) and isinstance(threshold_range,(np.generic, np.ndarray))):
        for backtest_mode in backtest_mode_list:
            all_report = []
            print(f"Mean_Normalize-backtest mode: {backtest_mode}")
            try:
                for rolling_window in rolling_window_range:
                    for threshold in threshold_range:
                        report = mean_normalize_backtesting(
                            df=df,
                            rolling_window=rolling_window,
                            threshold=threshold,
                            fees=fees,
                            sr_multiplier=sr_multiplier,
                            backtest_mode=backtest_mode,
                        )
                        all_report.append(report)
            except Exception as e:
                print(f"Error occurred: {e}")
                continue
            report_df = pd.DataFrame(all_report)
            file_name = f"Mean_Normalize-{backtest_mode}.csv" # modify file name, e.g f"{backtest_mode}-premium_index.csv" or f"{backtest_mode}-blablabla.csv". only modify blablabla
            file_path = Path(os.path.join(r"result\Mean_Normalize", file_name))
            file_path.parent.mkdir(parents=True, exist_ok=True)
            report_df.to_csv(file_path) 
            diagram.plot_heatmap(report_df)
    else:
        all_report = []
        print(f"Mean_Normalize-backtest mode: {backtest_mode_list}")
        report = mean_normalize_backtesting(
            df=df,
            rolling_window=rolling_window_range,
            threshold=threshold_range,
            fees=fees,
            sr_multiplier=sr_multiplier,
            backtest_mode=backtest_mode_list,
        )
        all_report.append(report)
        report_df = pd.DataFrame(all_report)
        file_name = f"Mean_Normalize-{backtest_mode_list}.csv" # modify file name, e.g f"{backtest_mode_list}-premium_index.csv" or f"{backtest_mode_list}-blablabla.csv". only modify blablabla
        file_path = Path(os.path.join(r"result\Mean_Normalize", file_name))
        file_path.parent.mkdir(parents=True, exist_ok=True)
        report_df.to_csv(file_path) 
        file_name1 = f"Mean_Normalize-Position-{backtest_mode_list}.csv" # modify file name, e.g f"{backtest_mode_list}-premium_index.csv" or f"{backtest_mode_list}-blablabla.csv". only modify blablabla
        file_path1 = Path(os.path.join(r"result\Mean_Normalize", file_name1))
        file_path1.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(file_path1)
        diagram.plot_single_diagram(df, report_df)

def bollinger_bands_backtesting(df, rolling_window, multiplier, fees, sr_multiplier, backtest_mode):
    # models
    formula.rolling_bollinger_bands(df, rolling_window, multiplier)
    df["pos"] = entryexitlogic.entry_exit_band(df, rolling_window, backtest_mode)
    report = util.generate_report(df, rolling_window, multiplier, fees, sr_multiplier)
    return report

def bollinger_bands(df, backtest_mode_list, rolling_window_range, threshold_range, fees, sr_multiplier):
    if (isinstance(rolling_window_range,(np.generic, np.ndarray)) and isinstance(threshold_range,(np.generic, np.ndarray))):
        for backtest_mode in backtest_mode_list:
            all_report = []
            print(f"Bollinger_Bands-backtest mode: {backtest_mode}")
            try:
                for rolling_window in rolling_window_range:
                    for threshold in threshold_range:
                        report = bollinger_bands_backtesting(
                            df=df,
                            rolling_window=rolling_window,
                            multiplier=threshold,
                            fees=fees,
                            sr_multiplier=sr_multiplier,
                            backtest_mode=backtest_mode,
                        )
                        all_report.append(report)
            except Exception as e:
                print(f"Error occurred: {e}")
                continue
            report_df = pd.DataFrame(all_report)
            file_name = f"Bollinger_Bands-{backtest_mode}.csv" # modify file name, e.g f"{backtest_mode}-premium_index.csv" or f"{backtest_mode}-blablabla.csv". only modify blablabla
            file_path = Path(os.path.join(r"result\Bollinger_Bands", file_name))
            file_path.parent.mkdir(parents=True, exist_ok=True)
            report_df.to_csv(file_path) 
            diagram.plot_heatmap(report_df)
    else:
        all_report = []
        print(f"Bollinger_Bands-backtest mode: {backtest_mode_list}")
        report = bollinger_bands_backtesting(
            df=df,
            rolling_window=rolling_window_range,
            multiplier=threshold_range,
            fees=fees,
            sr_multiplier=sr_multiplier,
            backtest_mode=backtest_mode_list,
        )
        all_report.append(report)
        report_df = pd.DataFrame(all_report)
        file_name = f"Bollinger_Bands-{backtest_mode_list}.csv" # modify file name, e.g f"{backtest_mode_list}-premium_index.csv" or f"{backtest_mode_list}-blablabla.csv". only modify blablabla
        file_path = Path(os.path.join(r"result\Bollinger_Bands", file_name))
        file_path.parent.mkdir(parents=True, exist_ok=True)
        report_df.to_csv(file_path) 
        file_name1 = f"Bollinger_Bands-Position-{backtest_mode_list}.csv" # modify file name, e.g f"{backtest_mode_list}-premium_index.csv" or f"{backtest_mode_list}-blablabla.csv". only modify blablabla
        file_path1 = Path(os.path.join(r"result\Bollinger_Bands", file_name1))
        file_path1.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(file_path1)
        diagram.plot_single_diagram(df, report_df)
        
def rsi_backtesting(df, rolling_window, threshold, fees, sr_multiplier, backtest_mode):
    formula.rolling_rsi(df, rolling_window)
    df["pos"] = entryexitlogic.entry_exit_threshold(df, rolling_window, threshold, backtest_mode)
    report = util.generate_report(df, rolling_window, threshold, fees, sr_multiplier)
    return report

def rsi(df, backtest_mode_list, rolling_window_range, threshold_range, fees, sr_multiplier):
    if (isinstance(rolling_window_range,(np.generic, np.ndarray)) and isinstance(threshold_range,(np.generic, np.ndarray))):
        for backtest_mode in backtest_mode_list:
            all_report = []
            print(f"RSI-backtest mode: {backtest_mode}")
            try:
                for rolling_window in rolling_window_range:
                    for threshold in threshold_range:
                        report = rsi_backtesting(
                            df=df,
                            rolling_window=rolling_window,
                            threshold=threshold,
                            fees=fees,
                            sr_multiplier=sr_multiplier,
                            backtest_mode=backtest_mode,
                        )
                        all_report.append(report)
            except Exception as e:
                print(f"Error occurred: {e}")
                continue
            report_df = pd.DataFrame(all_report)
            file_name = f"RSI-{backtest_mode}.csv" # modify file name, e.g f"{backtest_mode}-premium_index.csv" or f"{backtest_mode}-blablabla.csv". only modify blablabla
            file_path = Path(os.path.join(r"result\RSI", file_name))
            file_path.parent.mkdir(parents=True, exist_ok=True)
            report_df.to_csv(file_path) 
            diagram.plot_heatmap(report_df)
    else:
        all_report = []
        print(f"RSI-backtest mode: {backtest_mode_list}")
        report = rsi_backtesting(
            df=df,
            rolling_window=rolling_window_range,
            threshold=threshold_range,
            fees=fees,
            sr_multiplier=sr_multiplier,
            backtest_mode=backtest_mode_list,
        )
        all_report.append(report)
        report_df = pd.DataFrame(all_report)
        file_name = f"RSI-{backtest_mode_list}.csv" # modify file name, e.g f"{backtest_mode_list}-premium_index.csv" or f"{backtest_mode_list}-blablabla.csv". only modify blablabla
        file_path = Path(os.path.join(r"result\RSI", file_name))
        file_path.parent.mkdir(parents=True, exist_ok=True)
        report_df.to_csv(file_path) 

        file_name1 = f"RSI-Position-{backtest_mode_list}.csv" # modify file name, e.g f"{backtest_mode_list}-premium_index.csv" or f"{backtest_mode_list}-blablabla.csv". only modify blablabla
        file_path1 = Path(os.path.join(r"result\RSI", file_name1))
        file_path1.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(file_path1)
        diagram.plot_single_diagram(df, report_df)
        
def zscore_backtesting(df, rolling_window, threshold, fees, sr_multiplier, backtest_mode):
    df["processed_data"] = formula.rolling_zscore(df["data"].values, rolling_window)
    df["pos"] = entryexitlogic.entry_exit_threshold(df, rolling_window, threshold, backtest_mode)
    report = util.generate_report(df, rolling_window, threshold, fees, sr_multiplier)
    return report

def zscore(df, backtest_mode_list, rolling_window_range, threshold_range, fees, sr_multiplier):
    if (isinstance(rolling_window_range,(np.generic, np.ndarray)) and isinstance(threshold_range,(np.generic, np.ndarray))):
        for backtest_mode in backtest_mode_list:
            all_report = []
            print(f"ZScore-backtest mode: {backtest_mode}")
            try: 
                for rolling_window in rolling_window_range:
                    for threshold in threshold_range:
                        report = zscore_backtesting(
                            df=df,
                            rolling_window=rolling_window,
                            threshold=threshold,
                            fees=fees,
                            sr_multiplier=sr_multiplier,
                            backtest_mode=backtest_mode,
                        )
                        all_report.append(report)
            except Exception as e:
                print(f"Error occurred: {e}")
                continue
            report_df = pd.DataFrame(all_report)
            file_name = f"ZScore-{backtest_mode}.csv" # modify file name, e.g f"{backtest_mode}-premium_index.csv" or f"{backtest_mode}-blablabla.csv". only modify blablabla
            file_path = Path(os.path.join(r"result\ZScore", file_name))
            file_path.parent.mkdir(parents=True, exist_ok=True)
            report_df.to_csv(file_path) 
            diagram.plot_heatmap(report_df)
    else:
        all_report = []
        print(f"ZScore-backtest mode: {backtest_mode_list}")
        report = zscore_backtesting(
            df=df,
            rolling_window=rolling_window_range,
            threshold=threshold_range,
            fees=fees,
            sr_multiplier=sr_multiplier,
            backtest_mode=backtest_mode_list,
        )
        all_report.append(report)
        report_df = pd.DataFrame(all_report)
        file_name = f"ZScore-{backtest_mode_list}.csv" # modify file name, e.g f"{backtest_mode_list}-premium_index.csv" or f"{backtest_mode_list}-blablabla.csv". only modify blablabla
        file_path = Path(os.path.join(r"result\ZScore", file_name))
        file_path.parent.mkdir(parents=True, exist_ok=True)
        report_df.to_csv(file_path)
        file_name1 = f"ZScore-Position-{backtest_mode_list}.csv" # modify file name, e.g f"{backtest_mode_list}-premium_index.csv" or f"{backtest_mode_list}-blablabla.csv". only modify blablabla
        file_path1 = Path(os.path.join(r"result\ZScore", file_name1))
        file_path1.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(file_path1)
        diagram.plot_single_diagram(df, report_df)
        
def macd_backtesting(df, rolling_window1, rolling_window2, fees, sr_multiplier):
    formula.calculate_macd(df, rolling_window1, rolling_window2)
    df["pos"] = entryexitlogic.entry_exit_macd(df, rolling_window1, rolling_window2)
    report = util.generate_report(df, rolling_window1, rolling_window2, fees, sr_multiplier)
    return report

def macd(df, rolling_window1, rolling_window2, fees, sr_multiplier):
    if (isinstance(rolling_window1,(np.generic, np.ndarray)) and isinstance(rolling_window2,(np.generic, np.ndarray))):
        all_report = []
        print(f"MACD-backtest")
        for rolling1 in rolling_window1:
            for rolling2 in rolling_window2:                
                report = macd_backtesting(
                    df=df,
                    rolling_window1=rolling1,
                    rolling_window2=rolling2,
                    fees=fees,
                    sr_multiplier=sr_multiplier,
                )
                all_report.append(report)
        report_df = pd.DataFrame(all_report)
        file_name = f"MACD.csv" # modify file name, e.g f"{backtest_mode}-premium_index.csv" or f"{backtest_mode}-blablabla.csv". only modify blablabla
        file_path = Path(os.path.join(r"result\MACD", file_name))
        file_path.parent.mkdir(parents=True, exist_ok=True)
        report_df.to_csv(file_path) 
        diagram.plot_heatmap(report_df)
    else:
        all_report = []
        print(f"MACD-backtest")
        report = macd_backtesting(
            df=df,
            rolling_window1=rolling_window1,
            rolling_window2=rolling_window2,
            fees=fees,
            sr_multiplier=sr_multiplier,
        )
        all_report.append(report)
        report_df = pd.DataFrame(all_report)
        file_name = f"MACD.csv" # modify file name, e.g f"{backtest_mode}-premium_index.csv" or f"{backtest_mode}-blablabla.csv". only modify blablabla
        file_path = Path(os.path.join(r"result\MACD", file_name))
        file_path.parent.mkdir(parents=True, exist_ok=True)
        report_df.to_csv(file_path)
        file_name1 = f"MACD-Position.csv" # modify file name, e.g f"{backtest_mode_list}-premium_index.csv" or f"{backtest_mode_list}-blablabla.csv". only modify blablabla
        file_path1 = Path(os.path.join(r"result\MACD", file_name1))
        file_path1.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(file_path1)
        diagram.plot_single_diagram(df, report_df)
        
def minmax_normalize_backtesting(df, rolling_window, threshold, fees, sr_multiplier, backtest_mode):
    df["processed_data"] = formula.rolling_minmax_normalize(df["data"].values, rolling_window)
    df["pos"] = entryexitlogic.entry_exit_threshold(df, rolling_window, threshold, backtest_mode)
    report = util.generate_report(df, rolling_window, threshold, fees, sr_multiplier)
    return report

def minmax_normalize(df, backtest_mode_list, rolling_window_range, threshold_range, fees, sr_multiplier):
    if (isinstance(rolling_window_range,(np.generic, np.ndarray)) and isinstance(threshold_range,(np.generic, np.ndarray))):
        for backtest_mode in backtest_mode_list:
            all_report = []
            print(f"MinMax-backtest mode: {backtest_mode}")
            try:
                for rolling_window in rolling_window_range:
                    for threshold in threshold_range:
                        report = minmax_normalize_backtesting(
                            df=df,
                            rolling_window=rolling_window,
                            threshold=threshold,
                            fees=fees,
                            sr_multiplier=sr_multiplier,
                            backtest_mode=backtest_mode,
                        )
                        all_report.append(report)
            except Exception as e:
                print(f"Error occurred: {e}")
                continue
            report_df = pd.DataFrame(all_report)
            file_name = f"MinMax-{backtest_mode}.csv" # modify file name, e.g f"{backtest_mode}-premium_index.csv" or f"{backtest_mode}-blablabla.csv". only modify blablabla
            file_path = Path(os.path.join(r"result\MinMax", file_name))
            file_path.parent.mkdir(parents=True, exist_ok=True)
            report_df.to_csv(file_path) 
            diagram.plot_heatmap(report_df)
    else:
        all_report = []
        print(f"MinMax-backtest mode: {backtest_mode_list}")
        report = minmax_normalize_backtesting(
            df=df,
            rolling_window=rolling_window_range,
            threshold=threshold_range,
            fees=fees,
            sr_multiplier=sr_multiplier,
            backtest_mode=backtest_mode_list,
        )
        all_report.append(report)
        report_df = pd.DataFrame(all_report)
        file_name = f"MinMax-{backtest_mode_list}.csv" # modify file name, e.g f"{backtest_mode_list}-premium_index.csv" or f"{backtest_mode_list}-blablabla.csv". only modify blablabla
        file_path = Path(os.path.join(r"result\MinMax", file_name))
        file_path.parent.mkdir(parents=True, exist_ok=True)
        report_df.to_csv(file_path) 
        file_name1 = f"MinMax-Position-{backtest_mode_list}.csv" # modify file name, e.g f"{backtest_mode_list}-premium_index.csv" or f"{backtest_mode_list}-blablabla.csv". only modify blablabla
        file_path1 = Path(os.path.join(r"result\MinMax", file_name1))
        file_path1.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(file_path1)
        diagram.plot_single_diagram(df, report_df)
        
def zscore_mean_backtesting(df, rolling_window, threshold, fees, sr_multiplier, backtest_mode):
    df["processed_data"] = formula.rolling_zscore_mean(df["data"].values, rolling_window)
    df["pos"] = entryexitlogic.entry_exit_threshold(df, rolling_window, threshold, backtest_mode)
    report = util.generate_report(df, rolling_window, threshold, fees, sr_multiplier)
    return report

def zscore_mean(df, backtest_mode_list, rolling_window_range, threshold_range, fees, sr_multiplier):
    if (isinstance(rolling_window_range,(np.generic, np.ndarray)) and isinstance(threshold_range,(np.generic, np.ndarray))):
        for backtest_mode in backtest_mode_list:
            all_report = []
            print(f"zscore_mean-backtest mode: {backtest_mode}")
            try: 
                for rolling_window in rolling_window_range:
                    for threshold in threshold_range:
                        report = zscore_mean_backtesting(
                            df=df,
                            rolling_window=rolling_window,
                            threshold=threshold,
                            fees=fees,
                            sr_multiplier=sr_multiplier,
                            backtest_mode=backtest_mode,
                        )
                        all_report.append(report)
            except Exception as e:
                print(f"Error occurred: {e}")
                continue
            report_df = pd.DataFrame(all_report)
            file_name = f"zscore_mean-{backtest_mode}.csv" # modify file name, e.g f"{backtest_mode}-premium_index.csv" or f"{backtest_mode}-blablabla.csv". only modify blablabla
            file_path = Path(os.path.join(r"result\zscore_mean", file_name))
            file_path.parent.mkdir(parents=True, exist_ok=True)
            report_df.to_csv(file_path) 
            diagram.plot_heatmap(report_df)
    else:
        all_report = []
        print(f"zscore_mean-backtest mode: {backtest_mode_list}")
        report = zscore_mean_backtesting(
            df=df,
            rolling_window=rolling_window_range,
            threshold=threshold_range,
            fees=fees,
            sr_multiplier=sr_multiplier,
            backtest_mode=backtest_mode_list,
        )
        all_report.append(report)
        report_df = pd.DataFrame(all_report)
        file_name = f"zscore_mean-{backtest_mode_list}.csv" # modify file name, e.g f"{backtest_mode_list}-premium_index.csv" or f"{backtest_mode_list}-blablabla.csv". only modify blablabla
        file_path = Path(os.path.join(r"result\zscore_mean", file_name))
        file_path.parent.mkdir(parents=True, exist_ok=True)
        report_df.to_csv(file_path)
        file_name1 = f"zscore_mean-Position-{backtest_mode_list}.csv" # modify file name, e.g f"{backtest_mode_list}-premium_index.csv" or f"{backtest_mode_list}-blablabla.csv". only modify blablabla
        file_path1 = Path(os.path.join(r"result\zscore_mean", file_name1))
        file_path1.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(file_path1)
        diagram.plot_single_diagram(df, report_df)
        
def tanh_estimator_backtesting(df, rolling_window, threshold, fees, sr_multiplier, backtest_mode):
    df["processed_data"] = formula.rolling_tanh_estimator(df["data"].values, rolling_window)
    df["pos"] = entryexitlogic.entry_exit_threshold(df, rolling_window, threshold, backtest_mode)
    report = util.generate_report(df, rolling_window, threshold, fees, sr_multiplier)
    return report

def tanh_estimator(df, backtest_mode_list, rolling_window_range, threshold_range, fees, sr_multiplier):
    if (isinstance(rolling_window_range,(np.generic, np.ndarray)) and isinstance(threshold_range,(np.generic, np.ndarray))):
        for backtest_mode in backtest_mode_list:
            all_report = []
            print(f"tanh_estimator-backtest mode: {backtest_mode}")
            try: 
                for rolling_window in rolling_window_range:
                    for threshold in threshold_range:
                        report = tanh_estimator_backtesting(
                            df=df,
                            rolling_window=rolling_window,
                            threshold=threshold,
                            fees=fees,
                            sr_multiplier=sr_multiplier,
                            backtest_mode=backtest_mode,
                        )
                        all_report.append(report)
            except Exception as e:
                print(f"Error occurred: {e}")
                continue
            report_df = pd.DataFrame(all_report)
            file_name = f"tanh_estimator-{backtest_mode}.csv" # modify file name, e.g f"{backtest_mode}-premium_index.csv" or f"{backtest_mode}-blablabla.csv". only modify blablabla
            file_path = Path(os.path.join(r"result\tanh_estimator", file_name))
            file_path.parent.mkdir(parents=True, exist_ok=True)
            report_df.to_csv(file_path) 
            diagram.plot_heatmap(report_df)
    else:
        all_report = []
        print(f"tanh_estimator-backtest mode: {backtest_mode_list}")
        report = tanh_estimator_backtesting(
            df=df,
            rolling_window=rolling_window_range,
            threshold=threshold_range,
            fees=fees,
            sr_multiplier=sr_multiplier,
            backtest_mode=backtest_mode_list,
        )
        all_report.append(report)
        report_df = pd.DataFrame(all_report)
        file_name = f"tanh_estimator-{backtest_mode_list}.csv" # modify file name, e.g f"{backtest_mode_list}-premium_index.csv" or f"{backtest_mode_list}-blablabla.csv". only modify blablabla
        file_path = Path(os.path.join(r"result\tanh_estimator", file_name))
        file_path.parent.mkdir(parents=True, exist_ok=True)
        report_df.to_csv(file_path)
        file_name1 = f"tanh_estimator-Position-{backtest_mode_list}.csv" # modify file name, e.g f"{backtest_mode_list}-premium_index.csv" or f"{backtest_mode_list}-blablabla.csv". only modify blablabla
        file_path1 = Path(os.path.join(r"result\tanh_estimator", file_name1))
        file_path1.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(file_path1)
        diagram.plot_single_diagram(df, report_df)
        
def sigmoid_zscore_backtesting(df, rolling_window, threshold, fees, sr_multiplier, backtest_mode):
    df["processed_data"] = formula.rolling_sigmoid_zscore(df["data"].values, rolling_window)
    df["pos"] = entryexitlogic.entry_exit_threshold(df, rolling_window, threshold, backtest_mode)
    report = util.generate_report(df, rolling_window, threshold, fees, sr_multiplier)
    return report

def sigmoid_zscore(df, backtest_mode_list, rolling_window_range, threshold_range, fees, sr_multiplier):
    if (isinstance(rolling_window_range,(np.generic, np.ndarray)) and isinstance(threshold_range,(np.generic, np.ndarray))):
        for backtest_mode in backtest_mode_list:
            all_report = []
            print(f"sigmoid_zscore-backtest mode: {backtest_mode}")
            try: 
                for rolling_window in rolling_window_range:
                    for threshold in threshold_range:
                        report = sigmoid_zscore_backtesting(
                            df=df,
                            rolling_window=rolling_window,
                            threshold=threshold,
                            fees=fees,
                            sr_multiplier=sr_multiplier,
                            backtest_mode=backtest_mode,
                        )
                        all_report.append(report)
            except Exception as e:
                print(f"Error occurred: {e}")
                continue
            report_df = pd.DataFrame(all_report)
            file_name = f"sigmoid_zscore-{backtest_mode}.csv" # modify file name, e.g f"{backtest_mode}-premium_index.csv" or f"{backtest_mode}-blablabla.csv". only modify blablabla
            file_path = Path(os.path.join(r"result\sigmoid_zscore", file_name))
            file_path.parent.mkdir(parents=True, exist_ok=True)
            report_df.to_csv(file_path) 
            diagram.plot_heatmap(report_df)
    else:
        all_report = []
        print(f"sigmoid_zscore-backtest mode: {backtest_mode_list}")
        report = sigmoid_zscore_backtesting(
            df=df,
            rolling_window=rolling_window_range,
            threshold=threshold_range,
            fees=fees,
            sr_multiplier=sr_multiplier,
            backtest_mode=backtest_mode_list,
        )
        all_report.append(report)
        report_df = pd.DataFrame(all_report)
        file_name = f"sigmoid_zscore-{backtest_mode_list}.csv" # modify file name, e.g f"{backtest_mode_list}-premium_index.csv" or f"{backtest_mode_list}-blablabla.csv". only modify blablabla
        file_path = Path(os.path.join(r"result\sigmoid_zscore", file_name))
        file_path.parent.mkdir(parents=True, exist_ok=True)
        report_df.to_csv(file_path)
        file_name1 = f"sigmoid_zscore-Position-{backtest_mode_list}.csv" # modify file name, e.g f"{backtest_mode_list}-premium_index.csv" or f"{backtest_mode_list}-blablabla.csv". only modify blablabla
        file_path1 = Path(os.path.join(r"result\sigmoid_zscore", file_name1))
        file_path1.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(file_path1)
        diagram.plot_single_diagram(df, report_df)
        
def sigmoid_backtesting(df, rolling_window, threshold, fees, sr_multiplier, backtest_mode):
    df["processed_data"] = formula.rolling_sigmoid(df["data"].values, rolling_window)
    df["pos"] = entryexitlogic.entry_exit_threshold(df, rolling_window, threshold, backtest_mode)
    report = util.generate_report(df, rolling_window, threshold, fees, sr_multiplier)
    return report

def softmax_backtesting(df, rolling_window, threshold, fees, sr_multiplier, backtest_mode):
    df["processed_data"] = formula.rolling_softmax(df["data"].values, rolling_window)
    df["pos"] = entryexitlogic.entry_exit_threshold(df, rolling_window, threshold, backtest_mode)
    report = util.generate_report(df, rolling_window, threshold, fees, sr_multiplier)
    return report

def softmax(df, backtest_mode_list, rolling_window_range, threshold_range, fees, sr_multiplier):
    if (isinstance(rolling_window_range,(np.generic, np.ndarray)) and isinstance(threshold_range,(np.generic, np.ndarray))):
        for backtest_mode in backtest_mode_list:
            all_report = []
            print(f"softmax-backtest mode: {backtest_mode}")
            try: 
                for rolling_window in rolling_window_range:
                    for threshold in threshold_range:
                        report = softmax_backtesting(
                            df=df,
                            rolling_window=rolling_window,
                            threshold=threshold,
                            fees=fees,
                            sr_multiplier=sr_multiplier,
                            backtest_mode=backtest_mode,
                        )
                        all_report.append(report)
            except Exception as e:
                print(f"Error occurred: {e}")
                continue
            report_df = pd.DataFrame(all_report)
            file_name = f"softmax-{backtest_mode}.csv" # modify file name, e.g f"{backtest_mode}-premium_index.csv" or f"{backtest_mode}-blablabla.csv". only modify blablabla
            file_path = Path(os.path.join(r"result\softmax", file_name))
            file_path.parent.mkdir(parents=True, exist_ok=True)
            report_df.to_csv(file_path) 
            diagram.plot_heatmap(report_df)
    else:
        all_report = []
        print(f"softmax-backtest mode: {backtest_mode_list}")
        report = softmax_backtesting(
            df=df,
            rolling_window=rolling_window_range,
            threshold=threshold_range,
            fees=fees,
            sr_multiplier=sr_multiplier,
            backtest_mode=backtest_mode_list,
        )
        all_report.append(report)
        report_df = pd.DataFrame(all_report)
        file_name = f"softmax-{backtest_mode_list}.csv" # modify file name, e.g f"{backtest_mode_list}-premium_index.csv" or f"{backtest_mode_list}-blablabla.csv". only modify blablabla
        file_path = Path(os.path.join(r"result\softmax", file_name))
        file_path.parent.mkdir(parents=True, exist_ok=True)
        report_df.to_csv(file_path)
        file_name1 = f"softmax-Position-{backtest_mode_list}.csv" # modify file name, e.g f"{backtest_mode_list}-premium_index.csv" or f"{backtest_mode_list}-blablabla.csv". only modify blablabla
        file_path1 = Path(os.path.join(r"result\softmax", file_name1))
        file_path1.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(file_path1)
        diagram.plot_single_diagram(df, report_df)
        
def l1_normalization_backtesting(df, rolling_window, threshold, fees, sr_multiplier, backtest_mode):
    df["processed_data"] = formula.rolling_l1_normalization(df["data"].values, rolling_window)
    df["pos"] = entryexitlogic.entry_exit_threshold(df, rolling_window, threshold, backtest_mode)
    report = util.generate_report(df, rolling_window, threshold, fees, sr_multiplier)
    return report

def l1_normalization(df, backtest_mode_list, rolling_window_range, threshold_range, fees, sr_multiplier):
    if (isinstance(rolling_window_range,(np.generic, np.ndarray)) and isinstance(threshold_range,(np.generic, np.ndarray))):
        for backtest_mode in backtest_mode_list:
            all_report = []
            print(f"l1_normalization-backtest mode: {backtest_mode}")
            try: 
                for rolling_window in rolling_window_range:
                    for threshold in threshold_range:
                        report = l1_normalization_backtesting(
                            df=df,
                            rolling_window=rolling_window,
                            threshold=threshold,
                            fees=fees,
                            sr_multiplier=sr_multiplier,
                            backtest_mode=backtest_mode,
                        )
                        all_report.append(report)
            except Exception as e:
                print(f"Error occurred: {e}")
                continue
            report_df = pd.DataFrame(all_report)
            file_name = f"l1_normalization-{backtest_mode}.csv" # modify file name, e.g f"{backtest_mode}-premium_index.csv" or f"{backtest_mode}-blablabla.csv". only modify blablabla
            file_path = Path(os.path.join(r"result\l1_normalization", file_name))
            file_path.parent.mkdir(parents=True, exist_ok=True)
            report_df.to_csv(file_path) 
            diagram.plot_heatmap(report_df)
    else:
        all_report = []
        print(f"l1_normalization-backtest mode: {backtest_mode_list}")
        report = l1_normalization_backtesting(
            df=df,
            rolling_window=rolling_window_range,
            threshold=threshold_range,
            fees=fees,
            sr_multiplier=sr_multiplier,
            backtest_mode=backtest_mode_list,
        )
        all_report.append(report)
        report_df = pd.DataFrame(all_report)
        file_name = f"l1_normalization-{backtest_mode_list}.csv" # modify file name, e.g f"{backtest_mode_list}-premium_index.csv" or f"{backtest_mode_list}-blablabla.csv". only modify blablabla
        file_path = Path(os.path.join(r"result\l1_normalization", file_name))
        file_path.parent.mkdir(parents=True, exist_ok=True)
        report_df.to_csv(file_path)
        file_name1 = f"l1_normalization-Position-{backtest_mode_list}.csv" # modify file name, e.g f"{backtest_mode_list}-premium_index.csv" or f"{backtest_mode_list}-blablabla.csv". only modify blablabla
        file_path1 = Path(os.path.join(r"result\l1_normalization", file_name1))
        file_path1.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(file_path1)
        diagram.plot_single_diagram(df, report_df)

def Michael_backtesting(df, rolling_window, threshold, fees, sr_multiplier, backtest_mode):
    df["processed_data"] = df["data"]
    df["pos"] = entryexitlogic.entry_exit_threshold(df, rolling_window, threshold, backtest_mode)
    report = util.generate_report(df, rolling_window, threshold, fees, sr_multiplier)
    return report

def Michael(df, backtest_mode_list, rolling_window_range, threshold_range, fees, sr_multiplier):
    if (isinstance(rolling_window_range,(np.generic, np.ndarray)) and isinstance(threshold_range,(np.generic, np.ndarray))):
        for backtest_mode in backtest_mode_list:
            all_report = []
            print(f"Michael-backtest mode: {backtest_mode}")
            try:
                for rolling_window in rolling_window_range:
                    for threshold in threshold_range:
                        report = Michael_backtesting(
                            df=df,
                            rolling_window=rolling_window,
                            threshold=threshold,
                            fees=fees,
                            sr_multiplier=sr_multiplier,
                            backtest_mode=backtest_mode,
                        )
                        all_report.append(report)
            except Exception as e:
                print(f"Error occurred: {e}")
                continue
            report_df = pd.DataFrame(all_report)
            file_name = f"Michael-{backtest_mode}.csv"
            file_path = Path(os.path.join(r"result\Michael", file_name))
            file_path.parent.mkdir(parents=True, exist_ok=True)
            report_df.to_csv(file_path) 
            diagram.plot_heatmap(report_df)
    else:
        all_report = []
        print(f"Michael-backtest mode: {backtest_mode_list}")
        report = Michael_backtesting(
            df=df,
            rolling_window=rolling_window_range,
            threshold=threshold_range,
            fees=fees,
            sr_multiplier=sr_multiplier,
            backtest_mode=backtest_mode_list,
        )
        all_report.append(report)
        report_df = pd.DataFrame(all_report)
        file_name = f"Michael-{backtest_mode_list}.csv" # modify file name, e.g f"{backtest_mode_list}-premium_index.csv" or f"{backtest_mode_list}-blablabla.csv". only modify blablabla
        file_path = Path(os.path.join(r"result\Michael", file_name))
        file_path.parent.mkdir(parents=True, exist_ok=True)
        report_df.to_csv(file_path) 
        file_name1 = f"Michael-Position-{backtest_mode_list}.csv" # modify file name, e.g f"{backtest_mode_list}-premium_index.csv" or f"{backtest_mode_list}-blablabla.csv". only modify blablabla
        file_path1 = Path(os.path.join(r"result\Michael", file_name1))
        file_path1.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(file_path1)
        diagram.plot_single_diagram(df, report_df)