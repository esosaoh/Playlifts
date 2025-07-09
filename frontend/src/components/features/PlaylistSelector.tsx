import { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../ui/Card";
import { Button } from "../ui/Button";
import { motion } from "framer-motion";
import { Music, Heart } from "lucide-react";

interface Playlist {
  id: string;
  name: string;
  tracks_count: number;
  owner: string;
  public: boolean;
  cover_image: string | null;
}

interface PlaylistSelectorProps {
  onPlaylistSelect: (playlistId: string | null, playlistName?: string, playlistImage?: string | null) => void;
  selectedPlaylistId: string | null;
}

export const PlaylistSelector = ({ onPlaylistSelect, selectedPlaylistId }: PlaylistSelectorProps) => {
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
      const response = await fetch(`http://localhost:8889/get-playlists?t=${timestamp}`, {
        credentials: "include"
      });
      
      if (response.ok) {
        const data = await response.json();
        setPlaylists(data.playlists);
      } else if (response.status === 401) {
        setError("Please log in to access your playlists");
      } else {
        setError("Failed to load playlists");
      }
    } catch (err) {
      setError("Could not load playlists");
    } finally {
      setLoading(false);
    }
  };

  const handleLikedSongsSelect = () => {
    onPlaylistSelect(null);
  };

  const handlePlaylistSelect = (playlistId: string, playlistName: string, playlistImage: string | null) => {
    onPlaylistSelect(playlistId, playlistName, playlistImage);
  };

  if (loading) {
    return (
      <Card className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm border-0 shadow-2xl">
        <CardContent className="p-6">
          <div className="flex items-center justify-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-green-600"></div>
            <span className="ml-3 text-gray-600 dark:text-gray-300">Loading playlists...</span>
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
          Choose Destination
        </CardTitle>
        <CardDescription className="text-gray-600 dark:text-gray-300">
          Select where to add your songs
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Liked Songs Option */}
        <motion.div
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
        >
          <Button
            onClick={handleLikedSongsSelect}
            variant={selectedPlaylistId === null ? "default" : "outline"}
            className="w-full justify-start p-4 h-auto"
          >
            <Heart className="w-5 h-5 mr-3 text-red-500" />
            <div className="text-left">
              <div className="font-semibold">Liked Songs</div>
              <div className="text-sm opacity-70">Add to your liked songs</div>
            </div>
          </Button>
        </motion.div>

        {/* User Playlists */}
        <div className="space-y-2">
          <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300">Your Playlists</h3>
          <div className="max-h-60 overflow-y-auto space-y-2">
            {playlists.map((playlist) => (
              <motion.div
                key={playlist.id}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                <Button
                  onClick={() => handlePlaylistSelect(playlist.id, playlist.name, playlist.cover_image)}
                  variant={selectedPlaylistId === playlist.id ? "default" : "outline"}
                  className="w-full justify-start p-4 h-auto"
                >
                  {playlist.cover_image ? (
                    <img 
                      src={playlist.cover_image} 
                      alt={playlist.name}
                      className="w-10 h-10 rounded-lg object-cover mr-3"
                    />
                  ) : (
                    <Music className="w-5 h-5 mr-3" />
                  )}
                  <div className="text-left">
                    <div className="font-semibold">{playlist.name}</div>
                    <div className="text-sm opacity-70">
                      {playlist.tracks_count} tracks • {playlist.owner} • {playlist.public ? 'Public' : 'Private'}
                    </div>
                  </div>
                </Button>
              </motion.div>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}; 