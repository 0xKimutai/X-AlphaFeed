// pages/search.js
import axios from 'axios';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import TweetCard from '../components/TweetCard';
import SearchBar from '../components/SearchBar';

export default function SearchPage() {
  const [results, setResults] = useState([]);
  const router = useRouter();
  const query = router.query.q;

  useEffect(() => {
    if (query) {
      axios.get(`http://127.0.0.1:8000/search?q=${encodeURIComponent(query)}`)
        .then(res => setResults(res.data.data))
        .catch(err => console.error('Search failed:', err));
    }
  }, [query]);

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">🔍 Search Results for “{query}”</h1>
      <SearchBar />
      {results.length > 0 ? (
        results.map((tweet, index) => (
          <TweetCard key={index} tweet={tweet} />
        ))
      ) : (
        <p>No results found.</p>
      )}
    </div>
  );
}
