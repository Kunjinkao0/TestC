import { useEffect, useRef, useState } from 'react';
import './Detail.scss';
import HighchartsReact from 'highcharts-react-official';
import Highcharts from 'highcharts/highstock';
import zaxios from '../zrequest';
import { Box, Button, CircularProgress, Grid, Tab, Tabs, TextField, styled } from '@mui/material';
import { fNum } from '../utils';

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

function Detail() {
  const _symbol = new URLSearchParams(window.location.search).get('symbol')!.toLocaleUpperCase();
  const [currentSymbol, setCurrentSymbol] = useState<string>(_symbol);
  const [searchValue, setSearchValue] = useState<string>('');
  const [priceData, setPriceData] = useState<any>([]);
  const [pridictData, setPridictData] = useState<any>([]);
  const [detail, setDetail] = useState<any>(null);
  const [indicators, setIndicators] = useState<any>({});
  const [tab, setTab] = useState('Analysis');
  const [loading, setLoading] = useState(false);

  const getTickerDetail = (symbol: string) => {
    const getIndicators = async () => {
      try {
        setLoading(true);
        const data: any = await zaxios.get(`/api/ticker-detail?symbol=${symbol}`);
        if (!data.open) return;

        setCurrentSymbol(symbol.toLocaleUpperCase());
        setSearchValue('');
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
      } finally {
        setLoading(false);
      }
    };

    const getPriceData = async () => {
      try {
        const res: string = await zaxios.get(`/api/price-info?symbol=${symbol}`);
        const priceData = JSON.parse(res); // FIXME
        setPriceData(priceData);

        const pridictData = priceData.map((d: any) => [d[0], d[1] + Math.random() * 10 - 5]);
        setPridictData(pridictData);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    Promise.all([getIndicators(), getPriceData()]).then();
  };

  useEffect(() => {
    getTickerDetail(currentSymbol);
  }, []);

  const handleSearch = () => {
    if (!searchValue) return;
    getTickerDetail(searchValue);
  };

  const options = {
    title: {
      text: `Stock Price`
    },
    xAxis: {
      type: 'datetime',
      labels: {
        format: '{value:%b %e}',
      },
    },
    series: [
      { name: `${currentSymbol} Stock`, data: priceData, color: '#0000ff' },
      { name: `Predicted`, data: pridictData, color: '#9999ee' }, // Choose a fixed color for prediction data
    ]
  };

  const handleTabChange = (_: React.SyntheticEvent, newValue: string) => {
    setTab(newValue);
  };

  return (
    <>
      <div id='TopSection'>
        <Grid container spacing={2}>
          <Grid item md={3} style={{ "display": 'flex', "flexDirection": "row" }}>
            <span style={{ fontSize: '40px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', maxWidth: '300px' }}>{currentSymbol}</span>
            <div style={{ "display": 'flex', "flexDirection": "column", justifyContent: 'center', marginLeft: '16px' }}>
              <span id='CompanyNameHead'>{detail?.shortName || '--'}</span>
              <span id='ChannelHead'>NASDAQ</span>
            </div>
          </Grid>

          <Grid item md={9}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <WhitedTextFiled
                label="Input symbol here" variant="outlined"
                InputProps={{ style: { color: 'white' } }}
                InputLabelProps={{ style: { color: 'white' } }}
                value={searchValue}
                onChange={(e) => setSearchValue(e.target.value)}
                onKeyPress={(e) => {
                  if (e.key === 'Enter') {
                    handleSearch();
                  }
                }}
                style={{ flex: 1 }} />
              <Button id='search-button'
                variant="contained"
                onClick={handleSearch}
                style={{ marginLeft: '16px' }}>Search</Button>
            </div>
          </Grid>
        </Grid>

        <Grid id='TopDetails' style={{ marginTop: '16px' }}>
          {detail && <div>
            <div style={{
              display: 'flex', alignItems: 'center',
              color: detail.currentPrice - detail.previousClose > 0 ? '#33FF88' : '#ff1a1a',
              textShadow: '0 0 2px #00000033',
            }}>
              <span style={{ fontSize: '32px' }}>
                {detail.currentPrice - detail.previousClose > 0 ? '▲' : '▼'}
              </span>
              <div style={{ display: 'flex', alignItems: 'center', marginLeft: '16px' }}>
                <span style={{ fontSize: '32px' }}>
                  {detail.currentPrice.toFixed(2)}
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

      <div id='ChartSection'>
        {detail && <Grid container spacing={8} style={{ height: '480px' }}>
          <Grid item md={8}>
            <HighchartsReact
              highcharts={Highcharts}
              options={options}
            />
          </Grid>
          <Grid item md={4} style={{ height: '100%', paddingBottom: '80px' }}>
            <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', height: '100%' }}>
              <span style={{ fontSize: '30px' }}>About {detail.shortName}</span><br />
              <span >{detail.longBusinessSummary.length > 500 ?
                detail.longBusinessSummary.slice(0, 500) + '...' :
                detail.longBusinessSummary}</span>
            </div>
          </Grid>
        </Grid >}

        <Box>
          <Tabs value={tab} onChange={handleTabChange} aria-label="basic tabs example">
            <Tab label="News" value="News" />
            <Tab label="Options" value="Options" />
            <Tab label="Financial" value="Financial" />
            <Tab label="Analysis" value="Analysis" />
          </Tabs>
        </Box>
      </div>

      {loading && <div style={{ height: '100%', width: '100%', background: '#ffffff99', position: 'fixed', top: '0', zIndex: 99999 }}>
        <CircularProgress size="5rem" style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)' }} />
      </div>
      }
    </>
  );
}

export default Detail;
