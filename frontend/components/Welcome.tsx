import React from 'react'

const Welcome: React.FC = () => {
    const handleLogin = () => {
        window.location.href = 'http://localhost:8889/login';
    };

    return (
    <div style={{ textAlign: 'center', marginTop: '20px' }}>
      <h1>Welcome to ListenUP</h1>
      <p>
        ListenUP helps you transfer your playlists between Spotify and YouTube Music seamlessly.
      </p>
      <button onClick={handleLogin} style={{ padding: '10px 20px', fontSize: '16px', cursor: 'pointer' }}>
        Login with Spotify
      </button>
    </div>
    );
};

export default Welcome;