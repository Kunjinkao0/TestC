import { useEffect, useState } from 'react';
import './Detail.scss';
import HighchartsReact from 'highcharts-react-official';
import Highcharts from 'highcharts/highstock';
import zaxios from '../zrequest';

function Detail() {
  const symbol = new URLSearchParams(window.location.search).get('symbol');
  const [data, setData] = useState<any>([]);
  const [detail, setDetail] = useState<any>({});

  useEffect(() => {
    const getDetails = async () => {
      try {
        const res = await zaxios.get(`/api/ticker-detail?symbol=${symbol}`);
        setDetail(res);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };


    const getPriceData = async () => {
      try {
        const res = await zaxios.get(`/api/price-info?symbol=${symbol}`);
        setData(res);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    getDetails();
    getPriceData();
  }, []);

  const options = {
    title: {
      text: `${symbol} Stock Price`
    },
    series: [{
      name: `${symbol}`,
      data: data
    }]
  };

  return (
    <>
      <div className='TopDetails'>
        <h1>{detail.shortName}</h1>
      </div>

      <div>
        <HighchartsReact
          highcharts={Highcharts}
          options={options}
        />
      </div>
    </>
  );
}

export default Detail;
