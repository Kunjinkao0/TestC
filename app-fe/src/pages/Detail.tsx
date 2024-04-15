import { useEffect, useState } from 'react';
import './Detail.scss';
import HighchartsReact from 'highcharts-react-official';
import Highcharts from 'highcharts/highstock';
import zaxios from '../zrequest';
import { Box, Button, Grid, Tab, Tabs, TextField, styled } from '@mui/material';
import { fNum } from '../utils';

function Detail() {
  const symbol = new URLSearchParams(window.location.search).get('symbol');
  const [priceData, setPriceData] = useState<any>([]);
  const [detail, setDetail] = useState<any>(null);
  const [indicators, setIndicators] = useState<any>({});
  const [tab, setTab] = useState(0);

  useEffect(() => {
    const getIndicators = async () => {
      try {
        const data: any = await zaxios.get(`/api/ticker-detail?symbol=${symbol}`);
        const indicators = {
          "OPEN": fNum(data.open),
          "PREV CLOSE": fNum(data.previousClose),
          "HIGH": fNum(data.dayHigh),
          "LOW": fNum(data.dayLow),
          "VOLUMN": fNum(data.volume),
          "TURNOVER": fNum(data.regularMarketVolume),
          '52 WEEK HIGH': fNum(data.fiftyTwoWeekHigh),
          '52 WEEK LOW': fNum(data.fiftyTwoWeekLow),
          "MARKET CAP": fNum(data.marketCap),
          "P/E (TTM)": fNum(data.trailingPE)
        };
        setDetail({ ...data, currentTime: new Date().toLocaleString() });
        setIndicators(indicators);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    const getPriceData = async () => {
      try {
        const res = await zaxios.get(`/api/price-info?symbol=${symbol}`);
        setPriceData(res);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    Promise.all([getIndicators(), getPriceData()]).then();
  }, []);

  const options = {
    title: {
      text: `${symbol} Stock Price`
    },
    series: [
      { name: `${symbol}`, data: priceData }
    ]
  };

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTab(newValue);
  };

  const WhitedTextFiled = styled(TextField)(() => ({
    '& label.Mui-focused': {
      color: 'white',
    },
    '& .MuiInput-underline:after': {
      borderBottomColor: 'white',
    },
    '& .MuiOutlinedInput-root': {
      '& fieldset': {
        borderColor: 'white',
      },
      '&:hover fieldset': {
        borderColor: 'white',
      },
      '&.Mui-focused fieldset': {
        borderColor: 'white',
      },
    },
  }));

  return (
    <>
      <div id='TopSection'>
        <Grid container spacing={2}>
          <Grid item md={2} style={{ "display": 'flex', "flexDirection": "row" }}>
            <span style={{ fontSize: '40px' }}>{symbol}</span>
            <div style={{ "display": 'flex', "flexDirection": "column", justifyContent: 'center', marginLeft: '16px' }}>
              <span id='CompanyNameHead'>{detail?.shortName || '--'}</span>
              <span id='ChannelHead'>NASDAQ</span>
            </div>
          </Grid>

          <Grid item md={10}>
            <WhitedTextFiled label="Input symbol here" variant="outlined"
              style={{ width: '100%' }}
              InputProps={{ style: { color: 'white' } }}
              InputLabelProps={{ style: { color: 'white' } }} />
          </Grid>
        </Grid>

        <Grid id='TopDetails' style={{ marginTop: '16px' }}>
          {detail && <div>
            <div style={{
              display: 'flex', alignItems: 'center',
              color: detail.currentPrice - detail.previousClose > 0 ? 'green' : 'red'
            }}>
              <span style={{ fontSize: '24px' }}>
                {detail.currentPrice - detail.previousClose > 0 ? '▲' : '▼'}
              </span>
              <div style={{ display: 'flex', alignItems: 'center', marginLeft: '16px' }}>
                <span style={{ fontSize: '32px' }}>
                  {detail.currentPrice}
                </span>
                <span style={{ marginLeft: '16px', fontSize: '0.8rem' }}>
                  {(detail.currentPrice - detail.previousClose).toFixed(2)}<br />
                  {((detail.currentPrice - detail.previousClose) / detail.previousClose * 100).toFixed(2)}%
                </span>
              </div>
            </div>

            <div>
              <span style={{ fontSize: '0.8rem', marginLeft: '40px' }}>Last update: {detail.currentTime}</span>
            </div>

            <div style={{ marginTop: '16px' }}>
              <Button id='search-button' variant="contained">Trade Stocks</Button>
              <Button id='search-button' variant="outlined" style={{ marginLeft: '16px' }}>Trade Options</Button>
            </div>
          </div>}

          <Grid container id='Indicators' columnSpacing={4}>
            {Object.entries(indicators).map(([k, v]) => (
              <Grid item md={6} key={k}>
                <div className='IndicatorItem'>
                  <span>{k}</span>
                  <span>{v as string}</span>
                </div>
              </Grid>
            ))}
          </Grid>
        </Grid >
      </div >

      <div>
        <HighchartsReact
          highcharts={Highcharts}
          options={options}
        />
      </div>

      <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Tabs value={tab} onChange={handleTabChange} aria-label="basic tabs example">
          <Tab label="Item One" value="1" />
          <Tab label="Item Two" value="2" />
          <Tab label="Item Three" value="3" />
        </Tabs>
      </Box>
    </>
  );
}

export default Detail;
