'use client';

import Image from "next/image";
import Link from "next/link";
import dynamic from "next/dynamic";
import DatePickerInsights from "@/components/DatePickerInsights";

// Dynamically import AnalyticsContainer to avoid SSR hydration issues
const AnalyticsContainer = dynamic(() => import("@/components/AnalyticsContainer"), {
  ssr: false,
  loading: () => (
    <div className="flex justify-center items-center py-20">
      <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-orange-400"></div>
    </div>
  )
});

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Header */}
      <header className="bg-gray-800 border-b border-gray-700">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="text-2xl font-bold bg-gradient-to-r from-orange-400 to-purple-600 bg-clip-text text-transparent">
              BIQ
            </div>
            <nav className="hidden md:flex space-x-8">
              <Link href="#features" className="hover:text-orange-400 transition-colors">Features</Link>
              <Link href="#how-it-works" className="hover:text-orange-400 transition-colors">How It Works</Link>
              <Link href="#analytics" className="hover:text-orange-400 transition-colors">Analytics</Link>
              <Link href="#team" className="hover:text-orange-400 transition-colors">Our Team</Link>
            </nav>
            <Link
              href="https://www.joindex.com/"
              target="_blank"
              rel="noopener noreferrer"
              className="bg-gradient-to-r from-orange-500 to-purple-600 px-6 py-2 rounded-lg font-semibold hover:shadow-lg transition-all"
            >
              Join Dex
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
        <div className="relative z-10 text-center max-w-5xl mx-auto px-6">
          <h1 className="text-6xl md:text-8xl font-bold mb-8">
            <span className="bg-gradient-to-r from-orange-400 via-purple-500 to-pink-500 bg-clip-text text-transparent">
              BrowseIQ
            </span>
          </h1>
          <p className="text-xl md:text-2xl text-gray-300 mb-12 leading-relaxed max-w-4xl mx-auto">
            Meet BrowseIQ, a privacy-first Dex Chrome Extension feature that transforms your 
            search history into an AI-powered, personalized insight story and content 
            recommendation system!
          </p>
          <div className="flex flex-col sm:flex-row gap-6 justify-center">
            <Link
              href="https://www.joindex.com/"
              target="_blank"
              rel="noopener noreferrer"
              className="bg-gradient-to-r from-orange-500 to-purple-600 px-8 py-4 rounded-lg text-lg font-semibold hover:shadow-2xl hover:scale-105 transition-all"
            >
              Join Dex
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 bg-gray-800">
        <div className="max-w-6xl mx-auto px-6">
          <h2 className="text-4xl font-bold text-center mb-16">
            Check out our top three elements!
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-gray-700 rounded-xl p-8 text-center hover:bg-gray-600 transition-colors">
              <div className="w-16 h-16 mx-auto mb-6 bg-orange-500 rounded-lg flex items-center justify-center text-2xl">
                📊
              </div>
              <h3 className="text-2xl font-bold mb-4">Ranking your top interests!</h3>
              <p className="text-gray-300">You can learn about your top 5 interests, activities, or websites visited</p>
            </div>
            <div className="bg-gray-700 rounded-xl p-8 text-center hover:bg-gray-600 transition-colors">
              <div className="w-16 h-16 mx-auto mb-6 bg-purple-500 rounded-lg flex items-center justify-center text-2xl">
                📈
              </div>
              <h3 className="text-2xl font-bold mb-4">Graphing your personality!</h3>
              <p className="text-gray-300">Find out what's most important to you, compare the intensity of your interest</p>
            </div>
            <div className="bg-gray-700 rounded-xl p-8 text-center hover:bg-gray-600 transition-colors">
              <div className="w-16 h-16 mx-auto mb-6 bg-blue-500 rounded-lg flex items-center justify-center text-2xl">
                🕒
              </div>
              <h3 className="text-2xl font-bold mb-4">Go back in time, relive your history!</h3>
              <p className="text-gray-300">State a time period and you will receive a summary of your work completed in the time frame</p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" className="py-20 bg-gray-900">
        <div className="max-w-6xl mx-auto px-6">
          <h2 className="text-4xl font-bold text-center mb-16">
            How It Works
          </h2>
          <p className="text-xl text-gray-400 text-center mb-12">Simple steps to get started</p>
          <div className="grid md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 mx-auto mb-6 bg-orange-500 rounded-full flex items-center justify-center text-xl font-bold">
                1
              </div>
              <h3 className="text-xl font-bold mb-3">Sign Up</h3>
              <p className="text-gray-300">Join Dex / Sign up on the waitlist today!</p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 mx-auto mb-6 bg-orange-500 rounded-full flex items-center justify-center text-xl font-bold">
                2
              </div>
              <h3 className="text-xl font-bold mb-3">Top Interests</h3>
              <p className="text-gray-300">Search with queries like "Generate browsing analytics" to view rankings</p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 mx-auto mb-6 bg-orange-500 rounded-full flex items-center justify-center text-xl font-bold">
                3
              </div>
              <h3 className="text-xl font-bold mb-3">Graphing</h3>
              <p className="text-gray-300">Search "Graph Interests" or "Visualization" to view charts</p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 mx-auto mb-6 bg-orange-500 rounded-full flex items-center justify-center text-xl font-bold">
                4
              </div>
              <h3 className="text-xl font-bold mb-3">History</h3>
              <p className="text-gray-300">Search "History" or "Time Frame" to view your work summaries</p>
            </div>
          </div>
        </div>
      </section>

      {/* Analytics Section */}
      <section id="analytics" className="py-20 bg-gray-800">
        <div className="max-w-7xl mx-auto px-6">
          <h2 className="text-4xl font-bold text-center mb-16">
            <span className="bg-gradient-to-r from-orange-400 to-purple-600 bg-clip-text text-transparent">
              Your Browsing Analytics
            </span>
          </h2>
          <div className="mb-12">
            <DatePickerInsights />
          </div>
          <AnalyticsContainer />
        </div>
      </section>

      {/* Team Section */}
      <section id="team" className="py-20 bg-gray-900">
        <div className="max-w-6xl mx-auto px-6">
          <h2 className="text-4xl font-bold text-center mb-16">
            What Our Creators Say
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="bg-gray-700 rounded-xl p-6 text-center">
              <div className="w-16 h-16 mx-auto mb-4 bg-gradient-to-r from-orange-400 to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-xl">
                A
              </div>
              <h4 className="font-bold mb-2">Ananya</h4>
              <p className="text-orange-400 text-sm mb-4">Frontend / ML</p>
              <p className="text-gray-300 text-sm">"BIQ has completely transformed how I understand my digital habits. The insights are incredible!"</p>
            </div>
            <div className="bg-gray-700 rounded-xl p-6 text-center">
              <div className="w-16 h-16 mx-auto mb-4 bg-gradient-to-r from-orange-400 to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-xl">
                N
              </div>
              <h4 className="font-bold mb-2">Nishan</h4>
              <p className="text-orange-400 text-sm mb-4">Frontend / ML</p>
              <p className="text-gray-300 text-sm">"BrowseIQ highlights your top topics and groups related content so you never lose key insights."</p>
            </div>
            <div className="bg-gray-700 rounded-xl p-6 text-center">
              <div className="w-16 h-16 mx-auto mb-4 bg-gradient-to-r from-orange-400 to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-xl">
                S
              </div>
              <h4 className="font-bold mb-2">Shruti</h4>
              <p className="text-orange-400 text-sm mb-4">Backend / ML</p>
              <p className="text-gray-300 text-sm">"BIQ helps you understand your productivity! A great tool!"</p>
            </div>
            <div className="bg-gray-700 rounded-xl p-6 text-center">
              <div className="w-16 h-16 mx-auto mb-4 bg-gradient-to-r from-orange-400 to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-xl">
                I
              </div>
              <h4 className="font-bold mb-2">Isabella</h4>
              <p className="text-orange-400 text-sm mb-4">Backend / ML</p>
              <p className="text-gray-300 text-sm">"The personalization features are outstanding. It really understands my workflow patterns."</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gray-800">
        <div className="max-w-4xl mx-auto text-center px-6">
          <h2 className="text-4xl font-bold mb-4">Ready to join BrowseIQ?</h2>
          <p className="text-xl text-gray-400 mb-8">Start your journey today and learn more about yourself!</p>
          <Link
            href="https://www.joindex.com/"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center px-8 py-4 bg-gradient-to-r from-orange-500 to-purple-600 rounded-full text-white font-semibold hover:from-orange-600 hover:to-purple-700 transition-all transform hover:scale-105"
          >
            Join Dex
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-800 border-t border-gray-700 py-12">
        <div className="max-w-6xl mx-auto px-6">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="text-2xl font-bold bg-gradient-to-r from-orange-400 to-purple-600 bg-clip-text text-transparent mb-4 md:mb-0">
              BIQ
            </div>
            <div className="text-gray-400 text-sm">
              © 2025 BIQ. All rights reserved.
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

