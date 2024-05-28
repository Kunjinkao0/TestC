from darts.models import TSMixerModel
from darts.dataprocessing.transformers.scaler import Scaler
import pandas as pd
import json
from darts import concatenate, TimeSeries


if __name__ == "__main__":

    tsla_stock_data = pd.read_csv('/Users/willi/Workspace/fidchart/app-server/model/tsla_feature_data.csv')
    tsla_stock_data.tail(5)
    tsla_stock_data_ts = TimeSeries.from_dataframe(tsla_stock_data,
                                               time_col='Date',
                                               freq='30min')

    tsla_stock_data_ts_target = tsla_stock_data_ts['return']
    train = tsla_stock_data_ts_target.split_after(0.6)
    
    scaler = Scaler()  # default uses sklearn's MinMaxScaler
    train = scaler.fit_transform(train)
    # test = scaler.transform(test)
    tsla_stock_data_ts_target = scaler.transform(tsla_stock_data_ts_target)

    model = TSMixerModel.load('/Users/willi/Workspace/fidchart/app-server/model/tsla_tsm_0520.pkl', map_location="cpu")
    pred_series = model.predict(n=10*24, 
                                predict_likelihood_parameters=True)

    pred_test_unscaler = scaler.inverse_transform(pred_series)

    pdd = pred_test_unscaler.pd_dataframe().resample('1d').mean()
    print(pdd.head())

    pdd['return_q0.90'].to_csv('/Users/willi/Workspace/fidchart/app-server/model/prediction_90.csv')
