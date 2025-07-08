// TweetCard.jsx
import React from 'react';

const TweetCard = ({ tweet }) => {
  return (
    <div className="border rounded-xl p-4 shadow-sm mb-4 hover:bg-gray-50 transition">
      <p className="text-sm text-gray-500 mb-1">{tweet.keyword}</p>
      <p className="text-base font-medium">{tweet.snippet}</p>
      <a
        href={tweet.url}
        target="_blank"
        rel="noopener noreferrer"
        className="text-blue-600 text-sm underline mt-2 block"
      >
        View Tweet →
      </a>
      <p className="text-xs text-gray-400 mt-1">{new Date(tweet.timestamp).toLocaleString()}</p>
    </div>
  );
};

export default TweetCard;
