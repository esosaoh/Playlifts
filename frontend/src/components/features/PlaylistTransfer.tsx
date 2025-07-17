import { useState } from "react";
import { Button } from "../ui/Button";
import { Input } from "../ui/Input";
import { SongPreview } from "./SongPreview";
import { PlaylistSelector } from "./PlaylistSelector";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../ui/Card";
import { motion } from "framer-motion";
import { Music, Youtube, Music2, Heart } from "lucide-react";

export const PlaylistTransfer = () => {
  const [url, setUrl] = useState("");
  const [selectedPlaylistId, setSelectedPlaylistId] = useState<string | null>(null);
  const [selectedPlaylistName, setSelectedPlaylistName] = useState<string | null>(null);
  const [selectedPlaylistImage, setSelectedPlaylistImage] = useState<string | null>(null);
  const [showPlaylistSelector, setShowPlaylistSelector] = useState(false);
  const [isTransferring, setIsTransferring] = useState(false);
  const [songs, setSongs] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);

  const handleTransfer = async () => {
    setIsTransferring(true);
    setError(null);
    setSongs([]);

    try {
      const res = await fetch("https://api.playlifts.com/process-youtube", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          url,
          playlist_id: selectedPlaylistId 
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
          setError("No songs were successfully transferred. Please check your YouTube Music link and try again.");
        }
      } else {
        setError(`Transfer failed: ${data.error || 'Unknown error'}`);
      }
    } catch (e: any) {
      console.error('Transfer error:', e);
      setError("Could not process this playlist. Please check your YouTube Music link and try again.");
      setIsTransferring(false);
    }
  };

  const pollTaskStatus = async (taskId: string) => {
    let pollCount = 0;
    const maxPolls = 300; // 10 minutes at 1-second intervals
    
    const pollInterval = setInterval(async () => {
      pollCount++;
      
      try {
        const response = await fetch(`https://api.playlifts.com/task-status/${taskId}`, {
          credentials: "include"
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
            ...result.success.songs.map((s: any) => ({ ...s, status: "success" })),
            ...result.failed.songs.map((s: any) => ({ ...s, status: "failed", reason: s.reason })),
          ];
          setSongs(allSongs);
          
          if (result.success.count > 0) {
            setError(null);
          } else {
            setError("No songs were successfully transferred. Please check your YouTube Music link and try again.");
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

  const handlePlaylistSelect = (playlistId: string | null, playlistName?: string, playlistImage?: string | null) => {
    setSelectedPlaylistId(playlistId);
    setSelectedPlaylistName(playlistName || null);
    setSelectedPlaylistImage(playlistImage || null);
    setShowPlaylistSelector(false);
  };

  const getDestinationText = () => {
    if (selectedPlaylistId === null) return "Liked Songs";
    return selectedPlaylistName || "Selected Playlist";
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
          {/* Hero Section */}
          <div className="text-center mb-12">
            <motion.div
              initial={{ scale: 0.8 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.2, duration: 0.5 }}
              className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-green-500 to-emerald-600 rounded-2xl mb-6 shadow-lg"
            >
              <Music className="w-8 h-8 text-white" />
            </motion.div>
            <h1 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-4">
              Transfer Your Music
            </h1>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-lg mx-auto">
              Seamlessly move your YouTube Music playlists to Spotify with our
              intelligent transfer system
            </p>
          </div>

          {/* Main Transfer Card */}
          <Card className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm border-0 shadow-2xl">
            <CardHeader className="text-center pb-4 flex flex-col items-center">
              <CardTitle className="text-2xl font-bold text-gray-900 dark:text-white w-full text-center">
                YouTube Music to Spotify Transfer
              </CardTitle>
              <CardDescription className="text-gray-600 dark:text-gray-300 w-full text-center">
                Paste your YouTube Music playlist URL below to get started
              </CardDescription>
            </CardHeader>

            <CardContent className="space-y-6 flex flex-col items-center w-full">
              <div className="space-y-4 w-full">
                <Input
                  label="YouTube Music Playlist URL"
                  value={url}
                  onChange={e => setUrl(e.target.value)}
                  placeholder="https://music.youtube.com/playlist?list=..."
                  disabled={isTransferring}
                  className="text-lg h-14 px-6 w-full border-2 border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 focus:outline-none focus:ring-2 focus:ring-green-500 transition rounded-lg"
                />

                {/* Destination Selection */}
                <div className="space-y-2">
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                    Destination
                  </label>
                  <Button
                    onClick={() => setShowPlaylistSelector(!showPlaylistSelector)}
                    variant="outline"
                    className="w-full justify-start p-4 h-auto border-2 border-gray-300 dark:border-gray-700"
                  >
                    {selectedPlaylistId === null ? (
                      <Heart className="w-5 h-5 mr-3 text-red-500" />
                    ) : selectedPlaylistImage ? (
                      <img 
                        src={selectedPlaylistImage} 
                        alt={selectedPlaylistName || "Selected playlist"}
                        className="w-5 h-5 rounded object-cover mr-3"
                      />
                    ) : (
                      <Music2 className="w-5 h-5 mr-3" />
                    )}
                    <div className="text-left">
                      <div className="font-semibold">{getDestinationText()}</div>
                      <div className="text-sm opacity-70">
                        Click to change destination
                      </div>
                    </div>
                  </Button>
                </div>

                {/* Playlist Selector */}
                {showPlaylistSelector && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: "auto" }}
                    exit={{ opacity: 0, height: 0 }}
                    className="w-full"
                  >
                    <PlaylistSelector
                      onPlaylistSelect={handlePlaylistSelect}
                      selectedPlaylistId={selectedPlaylistId}
                    />
                  </motion.div>
                )}

                <Button
                  onClick={handleTransfer}
                  loading={isTransferring}
                  disabled={!url || isTransferring}
                  size="lg"
                  className="w-full text-lg py-4 bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 shadow-lg"
                >
                  <Youtube className="w-5 h-5" />
                  {isTransferring ? "Transferring..." : "Transfer to Spotify"}
                  <Music2 className="w-5 h-5" />
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
                        Transferring your playlist to {getDestinationText()}...
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
                  Successfully transferred {songs.filter(s => s.status === "success").length} songs to {getDestinationText()}!
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
