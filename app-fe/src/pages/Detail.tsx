import React, { useEffect, useState } from 'react';
import './Detail.scss';

function App() {
  const [result, setResult] = useState<string>('');

  useEffect(() => {
    fetch('/api/news-fetch?dateRange=1&website=1')
      .then(response => response.json())
      .then(data => {
        setResult(data)
      })
      .catch(error => console.error('Error fetching news:', error));
  }, []);

  return (
    <div className="App">
      <pre>
        {JSON.stringify(result, null, 2)}
      </pre>
    </div>
  );
}


export default App;
