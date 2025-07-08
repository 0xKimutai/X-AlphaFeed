import axios from 'axios';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import TweetCard from '../components/TweetCard';
import SearchBar from '../components/SearchBar';

export default function SearchPage() {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(true); // Added
  const router = useRouter();
  const query = router.query.q;

  useEffect(() => {
    if (query) {
      setLoading(true);
      axios.get(`https://x-alphafeed.onrender.com/search?q=${encodeURIComponent(query)}`)
        .then(res => setResults(res.data.data))
        .catch(err => console.error('Search failed:', err))
        .finally(() => setLoading(false));
    }
  }, [query]);

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">🔍 Search Results for “{query}” in 𝕏-Alpha</h1>
      <SearchBar />
      {loading ? (
        <p>Searching...</p>
      ) : results.length > 0 ? (
        results.map((tweet, index) => (
          <TweetCard key={index} tweet={tweet} />
        ))
      ) : (
        <p>No results found.</p>
      )}
    </div>
  );
}
