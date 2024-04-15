import { useState } from 'react';
import { useNavigate } from "react-router-dom";
import './Search.scss';
import { Button, TextField } from '@mui/material';

function SearchPage() {
  const [searchValue, setSearchValue] = useState('');
  const navigate = useNavigate();

  const handleSearch = () => {
    navigate({ pathname: '/detail', search: `?symbol=${searchValue}` });
  };

  return (
    <div className="app">
      <div className='center-search'>
        <TextField id="search-input" label="Input symbol here" variant="outlined"
          value={searchValue}
          onChange={(e) => setSearchValue(e.target.value)}
          onKeyPress={(e) => {
            if (e.key === 'Enter') {
              handleSearch();
            }
          }}
          placeholder="Input here..." />

        <Button id='search-button' variant="contained" onClick={handleSearch}>Search</Button>
      </div>
    </div>
  );
}

export default SearchPage;