import { useState } from 'react';
import { useNavigate } from "react-router-dom";
import './Search.scss';
import { Button, TextField } from '@mui/material';

function SearchPage() {
  const [searchValue, setSearchValue] = useState('');
  const navigate = useNavigate();

  const handleSearch = () => {
    if (!searchValue) return;
    navigate({ pathname: '/detail', search: `?symbol=${searchValue}` });
  };

  return (
    <div id="App">
      <div id='CenterSearch'>
        <TextField id="SearchInput" label="Input symbol here" variant="outlined"
          value={searchValue}
          onChange={(e) => setSearchValue(e.target.value)}
          onKeyPress={(e) => {
            if (e.key === 'Enter') {
              handleSearch();
            }
          }} />

        <Button id='SearchButton' variant="contained" onClick={handleSearch}>Search</Button>
      </div>
    </div>
  );
}

export default SearchPage;