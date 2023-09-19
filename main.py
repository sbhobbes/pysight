from pysight import fpp3

# fpp3.chapter_5.section_5_2.some_simple_forecasting_methods.some_simple_forecasting_methods()
df = fpp3.chapter_5.section_5_2.some_simple_forecasting_methods.get_data('1992 Q1', '2006 Q4', 'Beer')
# mean_df = fpp3.chapter_5.section_5_2.some_simple_forecasting_methods.get_forecast(df, 'Bricks', 'Quarter_date', 'mEAN', 25, 'QS')
# fpp3.chapter_5.section_5_2.some_simple_forecasting_methods.plot_mean_ts(df, 25, 'mean_bricks', 'Quarter_date', 'QS')
# fc_df = fpp3.chapter_5.section_5_2.some_simple_forecasting_methods.get_forecast(df, 'Bricks', 'Quarter_date', 'Naive', 25, 'QS')
# fpp3.chapter_5.section_5_2.some_simple_forecasting_methods.plot_naive_ts(df, fc_df, 'Bricks', 'naive_bricks')
fpp3.chapter_5.section_5_2.some_simple_forecasting_methods.plot_all(df, 24, 'mean_beer', 'Quarter_date', 'QS', 'Beer', 'Beer', '11/01/2000')
