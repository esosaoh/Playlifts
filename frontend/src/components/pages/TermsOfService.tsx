import { motion } from 'framer-motion';
import { ArrowLeft } from 'lucide-react';
import { Link } from 'react-router-dom';
import { Button } from '../ui/Button';

export const TermsOfService = () => {
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
              Terms of Service
            </h1>
            <p className="text-gray-600 dark:text-gray-300">
              Last updated: {new Date().toLocaleDateString()}
            </p>
          </div>

          {/* Content */}
          <div className="prose prose-lg dark:prose-invert max-w-none">
            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4">
                Agreement to Terms
              </h2>
              <p className="text-gray-700 dark:text-gray-300 mb-4">
                By accessing and using Playlifts ("the Service"), you accept and agree to be bound by the terms and provision of this agreement. If you do not agree to abide by the above, please do not use this service.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4">
                Description of Service
              </h2>
              <p className="text-gray-700 dark:text-gray-300 mb-4">
                Playlifts is a web-based service that allows users to transfer music playlists between YouTube Music and Spotify. The service acts as an intermediary to facilitate the transfer of playlist data between these two music streaming platforms.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4">
                User Accounts and Authentication
              </h2>
              <ul className="list-disc pl-6 text-gray-700 dark:text-gray-300 mb-4">
                <li>You must have valid accounts with both Spotify and YouTube Music to use our service</li>
                <li>You are responsible for maintaining the security of your authentication credentials</li>
                <li>You must authorize our service to access your music libraries through OAuth 2.0</li>
                <li>You can revoke access at any time through your respective platform settings</li>
              </ul>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4">
                Acceptable Use
              </h2>
              <p className="text-gray-700 dark:text-gray-300 mb-4">
                You agree to use the Service only for lawful purposes and in accordance with these Terms. You agree not to:
              </p>
              <ul className="list-disc pl-6 text-gray-700 dark:text-gray-300 mb-4">
                <li>Use the service for any illegal or unauthorized purpose</li>
                <li>Attempt to gain unauthorized access to our systems or other users' accounts</li>
                <li>Interfere with or disrupt the service or servers</li>
                <li>Use the service to transfer copyrighted content without proper authorization</li>
                <li>Exceed reasonable usage limits or attempt to abuse the service</li>
                <li>Use automated tools or scripts to access the service</li>
              </ul>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4">
                Service Limitations
              </h2>
              <ul className="list-disc pl-6 text-gray-700 dark:text-gray-300 mb-4">
                <li><strong>Transfer Limits:</strong> Spotify to YouTube transfers are limited to 15 songs per playlist due to YouTube API quotas</li>
                <li><strong>Availability:</strong> Service availability depends on the status of Spotify and YouTube Music APIs</li>
                <li><strong>Accuracy:</strong> We strive for accurate transfers but cannot guarantee perfect matches between platforms</li>
                <li><strong>Content:</strong> Some songs may not be available on the destination platform</li>
                <li><strong>Rate Limits:</strong> We may implement rate limiting to ensure fair usage</li>
              </ul>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4">
                Intellectual Property
              </h2>
              <ul className="list-disc pl-6 text-gray-700 dark:text-gray-300 mb-4">
                <li>You retain ownership of your playlists and music content</li>
                <li>We do not claim ownership of any music, playlists, or user-generated content</li>
                <li>Our service and website design are protected by intellectual property laws</li>
                <li>You must respect the intellectual property rights of music creators and platforms</li>
              </ul>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4">
                Privacy and Data Protection
              </h2>
              <p className="text-gray-700 dark:text-gray-300 mb-4">
                Your privacy is important to us. Please review our Privacy Policy, which also governs your use of the Service, to understand our practices regarding the collection and use of your information.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4">
                Third-Party Services
              </h2>
              <p className="text-gray-700 dark:text-gray-300 mb-4">
                Our service integrates with Spotify and YouTube Music. You acknowledge that:
              </p>
              <ul className="list-disc pl-6 text-gray-700 dark:text-gray-300 mb-4">
                <li>These platforms have their own terms of service and privacy policies</li>
                <li>We are not responsible for the content or policies of these third-party services</li>
                <li>Your use of these platforms is subject to their respective terms</li>
                <li>We may be limited by the APIs and policies of these platforms</li>
              </ul>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4">
                Disclaimers
              </h2>
              <p className="text-gray-700 dark:text-gray-300 mb-4">
                THE SERVICE IS PROVIDED "AS IS" AND "AS AVAILABLE" WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED. WE DISCLAIM ALL WARRANTIES, INCLUDING BUT NOT LIMITED TO:
              </p>
              <ul className="list-disc pl-6 text-gray-700 dark:text-gray-300 mb-4">
                <li>Warranties of merchantability and fitness for a particular purpose</li>
                <li>Warranties that the service will be uninterrupted or error-free</li>
                <li>Warranties regarding the accuracy or completeness of transferred data</li>
                <li>Warranties that the service will meet your specific requirements</li>
              </ul>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4">
                Limitation of Liability
              </h2>
              <p className="text-gray-700 dark:text-gray-300 mb-4">
                IN NO EVENT SHALL WE BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES, INCLUDING WITHOUT LIMITATION, LOSS OF PROFITS, DATA, USE, GOODWILL, OR OTHER INTANGIBLE LOSSES, RESULTING FROM YOUR USE OF THE SERVICE.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4">
                Indemnification
              </h2>
              <p className="text-gray-700 dark:text-gray-300 mb-4">
                You agree to defend, indemnify, and hold harmless Playlifts and its officers, directors, employees, and agents from and against any claims, damages, obligations, losses, liabilities, costs, or debt arising from your use of the Service.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4">
                Termination
              </h2>
              <ul className="list-disc pl-6 text-gray-700 dark:text-gray-300 mb-4">
                <li>We may terminate or suspend your access to the Service at any time, with or without cause</li>
                <li>You may stop using the Service at any time</li>
                <li>Upon termination, your right to use the Service will cease immediately</li>
                <li>Provisions of these Terms that by their nature should survive termination shall survive</li>
              </ul>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4">
                Governing Law
              </h2>
              <p className="text-gray-700 dark:text-gray-300 mb-4">
                These Terms shall be governed by and construed in accordance with the laws of the jurisdiction in which Playlifts operates, without regard to its conflict of law provisions.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4">
                Changes to Terms
              </h2>
              <p className="text-gray-700 dark:text-gray-300 mb-4">
                We reserve the right to modify these Terms at any time. We will notify users of any material changes by posting the new Terms on this page and updating the "Last updated" date. Your continued use of the Service after such modifications constitutes acceptance of the updated Terms.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4">
                Contact Information
              </h2>
              <p className="text-gray-700 dark:text-gray-300 mb-4">
                If you have any questions about these Terms of Service, please contact us:
              </p>
              <ul className="list-disc pl-6 text-gray-700 dark:text-gray-300 mb-4">
                <li><strong>Email:</strong> legal@playlifts.com</li>
                <li><strong>Website:</strong> <a href="https://playlifts.com" className="text-blue-600 dark:text-blue-400 hover:underline">playlifts.com</a></li>
              </ul>
            </section>
          </div>
        </motion.div>
      </div>
    </div>
  );
}; 