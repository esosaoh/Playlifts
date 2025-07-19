import { motion } from 'framer-motion';
import { ArrowLeft } from 'lucide-react';
import { Link } from 'react-router-dom';
import { Button } from '../ui/Button';

export const PrivacyPolicy = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-100 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-2xl shadow-2xl p-8"
        >
          {/* Header */}
          <div className="mb-8">
            <Link to="/">
              <Button variant="outline" className="mb-6">
                <ArrowLeft className="w-4 h-4 mr-2" />
                Back to Home
              </Button>
            </Link>
            <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Privacy Policy
            </h1>
            <p className="text-gray-600 dark:text-gray-300">
              Last updated: {new Date().toLocaleDateString()}
            </p>
          </div>

          {/* Content */}
          <div className="prose prose-lg dark:prose-invert max-w-none">
            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4">
                Introduction
              </h2>
              <p className="text-gray-700 dark:text-gray-300 mb-4">
                Playlifts ("we", "our", or "us") is committed to protecting your privacy. This Privacy Policy explains how we collect, use, and safeguard your information when you use our service to transfer playlists between YouTube Music and Spotify.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4">
                Information We Collect
              </h2>
              
              <h3 className="text-xl font-medium text-gray-900 dark:text-white mb-3">
                Authentication Data
              </h3>
              <ul className="list-disc pl-6 text-gray-700 dark:text-gray-300 mb-4">
                <li><strong>OAuth Tokens:</strong> We store temporary access tokens from Spotify and YouTube Music to access your playlists and music library</li>
                <li><strong>User Profile Information:</strong> Basic profile data from your Spotify and YouTube Music accounts (username, display name, profile picture)</li>
                <li><strong>Session Data:</strong> Temporary session information to maintain your login state</li>
              </ul>

              <h3 className="text-xl font-medium text-gray-900 dark:text-white mb-3">
                Playlist and Music Data
              </h3>
              <ul className="list-disc pl-6 text-gray-700 dark:text-gray-300 mb-4">
                <li><strong>Playlist Information:</strong> Playlist names, descriptions, cover images, and track counts</li>
                <li><strong>Track Data:</strong> Song titles, artist names, album names, and track IDs</li>
                <li><strong>Transfer History:</strong> Information about which playlists you've transferred and when</li>
              </ul>

              <h3 className="text-xl font-medium text-gray-900 dark:text-white mb-3">
                Technical Data
              </h3>
              <ul className="list-disc pl-6 text-gray-700 dark:text-gray-300 mb-4">
                <li><strong>Usage Analytics:</strong> How you interact with our service (pages visited, features used)</li>
                <li><strong>Error Logs:</strong> Technical information when errors occur to help us improve the service</li>
                <li><strong>Device Information:</strong> Browser type, operating system, and IP address for security purposes</li>
              </ul>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4">
                How We Use Your Information
              </h2>
              <ul className="list-disc pl-6 text-gray-700 dark:text-gray-300 mb-4">
                <li><strong>Service Provision:</strong> To provide playlist transfer functionality between YouTube Music and Spotify</li>
                <li><strong>Authentication:</strong> To maintain your login sessions and verify your identity</li>
                <li><strong>Playlist Management:</strong> To read your playlists and create new ones on the destination platform</li>
                <li><strong>Service Improvement:</strong> To analyze usage patterns and improve our service</li>
                <li><strong>Technical Support:</strong> To troubleshoot issues and provide customer support</li>
                <li><strong>Security:</strong> To protect against fraud, abuse, and unauthorized access</li>
              </ul>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4">
                Data Sharing and Third Parties
              </h2>
              <p className="text-gray-700 dark:text-gray-300 mb-4">
                We do not sell, trade, or rent your personal information to third parties. We may share your information only in the following circumstances:
              </p>
              <ul className="list-disc pl-6 text-gray-700 dark:text-gray-300 mb-4">
                <li><strong>Service Providers:</strong> With trusted third-party services that help us operate our platform (hosting, analytics, etc.)</li>
                <li><strong>Legal Requirements:</strong> When required by law or to protect our rights and safety</li>
                <li><strong>API Integration:</strong> With Spotify and YouTube Music APIs as necessary to provide our service</li>
              </ul>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4">
                How to Revoke Access
              </h2>
              
              <h3 className="text-xl font-medium text-gray-900 dark:text-white mb-3">
                Spotify
              </h3>
              <ol className="list-decimal pl-6 text-gray-700 dark:text-gray-300 mb-4">
                <li>Go to <a href="https://www.spotify.com/account/apps/" className="text-blue-600 dark:text-blue-400 hover:underline" target="_blank" rel="noopener noreferrer">Spotify Account Apps</a></li>
                <li>Find "Playlifts" in the list of connected apps</li>
                <li>Click "REMOVE ACCESS" to revoke our access to your Spotify account</li>
              </ol>

              <h3 className="text-xl font-medium text-gray-900 dark:text-white mb-3">
                YouTube Music (Google)
              </h3>
              <ol className="list-decimal pl-6 text-gray-700 dark:text-gray-300 mb-4">
                <li>Go to <a href="https://myaccount.google.com/permissions" className="text-blue-600 dark:text-blue-400 hover:underline" target="_blank" rel="noopener noreferrer">Google Account Permissions</a></li>
                <li>Find "Playlifts" in the list of third-party apps</li>
                <li>Click on Playlifts and then click "Remove Access"</li>
                <li>Alternatively, you can revoke access through <a href="https://security.google.com/settings/security/permissions" className="text-blue-600 dark:text-blue-400 hover:underline" target="_blank" rel="noopener noreferrer">Google Security Settings</a></li>
              </ol>

              <p className="text-gray-700 dark:text-gray-300 mb-4">
                <strong>Note:</strong> Revoking access will immediately log you out of our service and prevent future playlist transfers until you re-authenticate.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4">
                Data Retention
              </h2>
              <ul className="list-disc pl-6 text-gray-700 dark:text-gray-300 mb-4">
                <li><strong>OAuth Tokens:</strong> Stored temporarily and automatically refreshed as needed</li>
                <li><strong>Session Data:</strong> Deleted when you log out or after a period of inactivity</li>
                <li><strong>Transfer History:</strong> Retained for up to 30 days to help with troubleshooting</li>
                <li><strong>Error Logs:</strong> Retained for up to 90 days for service improvement</li>
              </ul>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4">
                Your Rights
              </h2>
              <ul className="list-disc pl-6 text-gray-700 dark:text-gray-300 mb-4">
                <li><strong>Access:</strong> Request information about what data we have about you</li>
                <li><strong>Deletion:</strong> Request deletion of your personal data</li>
                <li><strong>Correction:</strong> Request correction of inaccurate data</li>
                <li><strong>Portability:</strong> Request a copy of your data in a portable format</li>
                <li><strong>Revocation:</strong> Revoke access to your accounts at any time</li>
              </ul>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4">
                Security
              </h2>
              <p className="text-gray-700 dark:text-gray-300 mb-4">
                We implement appropriate security measures to protect your information:
              </p>
              <ul className="list-disc pl-6 text-gray-700 dark:text-gray-300 mb-4">
                <li>Encryption of data in transit and at rest</li>
                <li>Secure OAuth 2.0 authentication flows</li>
                <li>Regular security audits and updates</li>
                <li>Limited access to personal data on a need-to-know basis</li>
              </ul>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4">
                Contact Information
              </h2>
              <p className="text-gray-700 dark:text-gray-300 mb-4">
                If you have any questions about this Privacy Policy or our data practices, please contact us:
              </p>
              <ul className="list-disc pl-6 text-gray-700 dark:text-gray-300 mb-4">
                <li><strong>Email:</strong> esosaohangbonswe@gmail.com</li>
                <li><strong>Website:</strong> <a href="https://playlifts.com" className="text-blue-600 dark:text-blue-400 hover:underline">playlifts.com</a></li>
              </ul>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4">
                Changes to This Policy
              </h2>
              <p className="text-gray-700 dark:text-gray-300 mb-4">
                We may update this Privacy Policy from time to time. We will notify you of any material changes by posting the new Privacy Policy on this page and updating the "Last updated" date.
              </p>
            </section>
          </div>
        </motion.div>
      </div>
    </div>
  );
}; 