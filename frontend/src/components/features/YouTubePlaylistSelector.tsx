import { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../ui/Card";
import { Button } from "../ui/Button";
import { motion } from "framer-motion";
import { Youtube } from "lucide-react";

interface Playlist {
  id: string;
  title: string;
}

interface YouTubePlaylistSelectorProps {
  onPlaylistSelect: (playlistId: string | null, playlistName?: string) => void;
  selectedPlaylistId: string | null;
}

export const YouTubePlaylistSelector = ({ onPlaylistSelect, selectedPlaylistId }: YouTubePlaylistSelectorProps) => {
  const [playlists, setPlaylists] = useState<Playlist[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchPlaylists();
  }, []);

  const fetchPlaylists = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const timestamp = Date.now()
      const response = await fetch(`https://api.playlifts.com/youtube/playlists?t=${timestamp}`, {
        credentials: "include"
      });
      
      if (response.ok) {
        const data = await response.json();
        setPlaylists(data.playlists);
      } else if (response.status === 401) {
        setError("Please log in to YouTube to access your playlists");
      } else {
        setError("Failed to load YouTube playlists");
      }
    } catch (err) {
      setError("Could not load YouTube playlists");
    } finally {
      setLoading(false);
    }
  };

  const handlePlaylistSelect = (playlistId: string, playlistName: string) => {
    onPlaylistSelect(playlistId, playlistName);
  };

  if (loading) {
    return (
      <Card className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm border-0 shadow-2xl">
        <CardContent className="p-6">
          <div className="flex items-center justify-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-green-600"></div>
            <span className="ml-3 text-gray-600 dark:text-gray-300">Loading YouTube playlists...</span>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm border-0 shadow-2xl">
        <CardContent className="p-6">
          <div className="text-center text-red-600 dark:text-red-400">
            {error}
            <Button onClick={fetchPlaylists} variant="outline" className="ml-4">
              Retry
            </Button>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm border-0 shadow-2xl">
      <CardHeader className="text-center pb-4">
        <CardTitle className="text-xl font-bold text-gray-900 dark:text-white">
          Select YouTube Playlist
        </CardTitle>
        <CardDescription className="text-gray-600 dark:text-gray-300">
          Choose where to transfer your songs
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="max-h-60 overflow-y-auto space-y-2">
          {playlists.map((playlist) => (
            <motion.div
              key={playlist.id}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              <Button
                onClick={() => handlePlaylistSelect(playlist.id, playlist.title)}
                variant={selectedPlaylistId === playlist.id ? "default" : "outline"}
                className="w-full justify-start p-4 h-auto"
              >
                <Youtube className="w-5 h-5 mr-3" />
                <div className="text-left">
                  <div className="font-semibold">{playlist.title}</div>
                  <div className="text-sm opacity-70">
                    YouTube playlist
                  </div>
                </div>
              </Button>
            </motion.div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}; 