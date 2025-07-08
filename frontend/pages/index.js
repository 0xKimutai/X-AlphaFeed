import axios from 'axios';
import { useEffect, useState } from 'react';
import TweetCard from '../components/TweetCard';
import SearchBar from '../components/SearchBar';

export default function Home() {
  const [tweets, setTweets] = useState([]);
  const [loading, setLoading] = useState(true); // Track loading status

  useEffect(() => {
    axios.get('https://x-alphafeed.onrender.com/feed')
      .then(res => setTweets(res.data.data))
      .catch(err => console.error('Failed to fetch feed:', err))
      .finally(() => setLoading(false)); // Mark as loaded whether success or failure
  }, []);

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">📊 X-Alpha Feed</h1>
      <SearchBar />
      {loading ? (
        <p>Loading tweets...</p> // Show this while waiting
      ) : tweets.length > 0 ? (
        tweets.map((tweet, index) => (
          <TweetCard key={index} tweet={tweet} />
        ))
      ) : (
        <p>No tweets found.</p>
      )}
    </div>
  );
}
