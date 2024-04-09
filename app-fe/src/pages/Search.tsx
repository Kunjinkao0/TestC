import { useState } from 'react';
import { useNavigate } from "react-router-dom";
import './Search.scss';

function SearchPage() {
  const [searchValue, setSearchValue] = useState('');
  const navigate = useNavigate();

  const handleSearch = () => {
    navigate({ pathname: '/detail', search: `?wd=searchValue` });
  };

  return (
    <div className="app">
      <div className='center-search'>
        <input
          type="text"
          id="search-input"
          value={searchValue}
          onChange={(e) => setSearchValue(e.target.value)}
          placeholder="Input here..." />
        <button id='search-button' onClick={handleSearch}>Search</button>
      </div>
    </div>
  );
}

export default SearchPage;