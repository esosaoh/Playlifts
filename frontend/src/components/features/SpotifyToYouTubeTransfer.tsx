import { useState } from "react";
import { Button } from "../ui/Button";
import { Input } from "../ui/Input";
import { SongPreview } from "./SongPreview";
import { YouTubePlaylistSelector } from "./YouTubePlaylistSelector";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../ui/Card";
import { motion } from "framer-motion";
import { Youtube, Music2 } from "lucide-react";

export const SpotifyToYouTubeTransfer = () => {
  const [spotifyUrl, setSpotifyUrl] = useState("");
  const [selectedYouTubePlaylistId, setSelectedYouTubePlaylistId] = useState<string | null>(null);
  const [selectedYouTubePlaylistName, setSelectedYouTubePlaylistName] = useState<string | null>(null);
  const [showYouTubePlaylistSelector, setShowYouTubePlaylistSelector] = useState(false);
  const [isTransferring, setIsTransferring] = useState(false);
  const [songs, setSongs] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);

  const extractSpotifyPlaylistId = (url: string) => {
    try {
      const urlObj = new URL(url);
      if (urlObj.hostname !== 'open.spotify.com') {
        return null;
      }
      
      const pathParts = urlObj.pathname.split('/');
      if (pathParts[1] === 'playlist' && pathParts[2]) {
        return pathParts[2];
      }
      return null;
    } catch {
      return null;
    }
  };

  const handleTransfer = async () => {
    if (!spotifyUrl || !selectedYouTubePlaylistId) {
      setError("Please provide a Spotify playlist URL and select a YouTube destination");
      return;
    }

    const spotifyPlaylistId = extractSpotifyPlaylistId(spotifyUrl);
    if (!spotifyPlaylistId) {
      setError("Invalid Spotify playlist URL. Please use a URL like: https://open.spotify.com/playlist/...");
      return;
    }

    setIsTransferring(true);
    setError(null);
    setSongs([]);

    try {
      const res = await fetch("https://api.playlifts.com/spotify/transfer", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          spotify_playlist_id: spotifyPlaylistId,
          youtube_playlist_id: selectedYouTubePlaylistId
        }),
        credentials: "include",
      });
      const data = await res.json();

      console.log('Transfer response:', { status: res.status, data });

      if (res.status === 202 && data.task_id) {
        // start polling
        pollTaskStatus(data.task_id);
      } else if (res.ok) {
        const allSongs = [
          ...data.success.songs.map((s: any) => ({ ...s, status: "success" })),
          ...data.failed.songs.map((s: any) => ({ ...s, status: "failed", reason: s.reason })),
        ];
        setSongs(allSongs);
        
        if (data.success.count > 0) {
          setError(null);
        } else {
          setError("No songs were successfully transferred. Please check your Spotify playlist URL and try again.");
        }
      } else {
        setError(`Transfer failed: ${data.error || 'Unknown error'}`);
      }
    } catch (e: any) {
      console.error('Transfer error:', e);
      setError("Could not process this transfer. Please check your Spotify playlist URL and try again.");
      setIsTransferring(false);
    }
  };

  const pollTaskStatus = async (taskId: string) => {
    let pollCount = 0;
    const maxPolls = 300; // 10 minutes at 1-second intervals
    
    const pollInterval = setInterval(async () => {
      pollCount++;
      
      try {
        const response = await fetch(`https://api.playlifts.com/tasks/status/${taskId}`, {
          credentials: 'include'
        });
        
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        console.log('Task status:', data.state);

        if (data.state === 'PENDING') { 
          console.log('Task pending, continuing to poll...');
        } else if (data.state === 'PROGRESS') {
          console.log('Task in progress, continuing to poll...');
        } else if (data.state === 'SUCCESS') {
          clearInterval(pollInterval);
          setIsTransferring(false);
          
          const result = data.result;
          const allSongs = [
            ...result.success.tracks.map((s: any) => ({ ...s, status: "success" })),
            ...result.failed.tracks.map((s: any) => ({ ...s, status: "failed", reason: s.reason })),
          ];
          setSongs(allSongs);
          
          if (result.success.count > 0) {
            setError(null);
          } else {
            setError("No songs were successfully transferred. Please check your Spotify playlist URL and try again.");
          }
        } else if (data.state === 'FAILURE') {
          clearInterval(pollInterval);
          setIsTransferring(false);
          const errorMessage = data.status || data.error || 'Unknown error occurred during transfer';
          setError(`Transfer failed: ${errorMessage}`);
        }
        
        if (pollCount >= maxPolls) {
          clearInterval(pollInterval);
          setIsTransferring(false);
          setError("Transfer timed out. Please try again with a smaller playlist.");
        }
        
      } catch (error) {
        console.error('Polling error:', error);
        
        if (pollCount > 5) {
          clearInterval(pollInterval);
          setIsTransferring(false);
          setError("Failed to check transfer status. Please try again.");
        }
      }
    }, 1000);

    return () => {
      clearInterval(pollInterval);
    };
  };

  const handleYouTubePlaylistSelect = (playlistId: string | null, playlistName?: string) => {
    setSelectedYouTubePlaylistId(playlistId);
    setSelectedYouTubePlaylistName(playlistName || null);
    setShowYouTubePlaylistSelector(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-100 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      <div className="container mx-auto px-4 py-12">
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: "easeOut" }}
          className="max-w-4xl mx-auto"
        >
          {/* Main Transfer Card */}
          <Card className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm border-0 shadow-2xl">
            <CardHeader className="text-center pb-4 flex flex-col items-center">
              <CardTitle className="text-2xl font-bold text-gray-900 dark:text-white w-full text-center">
                Spotify to YouTube Music Transfer
              </CardTitle>
              <CardDescription className="text-gray-600 dark:text-gray-300 w-full text-center">
                Paste your Spotify playlist URL below to get started
              </CardDescription>
            </CardHeader>

            <CardContent className="space-y-6 flex flex-col items-center w-full">
              <div className="space-y-4 w-full">
                {/* Spotify Playlist URL Input */}
                <Input
                  label="Spotify Playlist URL"
                  value={spotifyUrl}
                  onChange={e => setSpotifyUrl(e.target.value)}
                  placeholder="https://open.spotify.com/playlist/..."
                  disabled={isTransferring}
                  className="text-lg h-14 px-6 w-full border-2 border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 focus:outline-none focus:ring-2 focus:ring-green-500 transition rounded-lg"
                />

                {/* YouTube Playlist Selection */}
                <div className="space-y-2">
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                    Destination YouTube Playlist
                  </label>
                  <Button
                    onClick={() => setShowYouTubePlaylistSelector(!showYouTubePlaylistSelector)}
                    variant="outline"
                    className="w-full justify-start p-4 h-auto border-2 border-gray-300 dark:border-gray-700"
                  >
                    <Youtube className="w-5 h-5 mr-3" />
                    <div className="text-left">
                      <div className="font-semibold">{selectedYouTubePlaylistName || "Select YouTube playlist"}</div>
                      <div className="text-sm opacity-70">
                        Click to select destination playlist
                      </div>
                    </div>
                  </Button>
                </div>

                {/* YouTube Playlist Selector */}
                {showYouTubePlaylistSelector && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: "auto" }}
                    exit={{ opacity: 0, height: 0 }}
                    className="w-full"
                  >
                    <YouTubePlaylistSelector
                      onPlaylistSelect={handleYouTubePlaylistSelect}
                      selectedPlaylistId={selectedYouTubePlaylistId}
                    />
                  </motion.div>
                )}

                <Button
                  onClick={handleTransfer}
                  loading={isTransferring}
                  disabled={!spotifyUrl || !selectedYouTubePlaylistId || isTransferring}
                  size="lg"
                  className="w-full text-lg py-4 bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 shadow-lg"
                >
                  <Music2 className="w-5 h-5" />
                  {isTransferring ? "Transferring..." : "Transfer to YouTube"}
                  <Youtube className="w-5 h-5" />
                </Button>
              </div>

              {isTransferring && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: "auto" }}
                  className="space-y-4 w-full"
                >
                  <div className="flex items-center justify-center space-x-3 p-6 bg-gray-50 dark:bg-gray-800 rounded-lg">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-green-600"></div>
                    <div className="text-center">
                      <div className="text-sm font-medium text-gray-700 dark:text-gray-300">
                        Transferring your playlist to {selectedYouTubePlaylistName}...
                      </div>
                      <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                        This may take a few minutes for large playlists
                      </div>
                    </div>
                  </div>
                </motion.div>
              )}

              {error && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  className="p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg text-red-700 dark:text-red-300 text-center w-full"
                >
                  {error}
                </motion.div>
              )}

              {songs.length > 0 && songs.some(s => s.status === "success") && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  className="p-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg text-green-700 dark:text-green-300 text-center w-full"
                >
                  Successfully transferred {songs.filter(s => s.status === "success").length} songs to {selectedYouTubePlaylistName}!
                </motion.div>
              )}

              {songs.length > 0 && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="space-y-3 w-full"
                >
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                    Transfer Results
                  </h3>
                  <div className="space-y-2 max-h-96 overflow-y-auto">
                    {songs.map((song, idx) => (
                      <SongPreview key={idx} song={song} />
                    ))}
                  </div>
                </motion.div>
              )}
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </div>
  );
}; 