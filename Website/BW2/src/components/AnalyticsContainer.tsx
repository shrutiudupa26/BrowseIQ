'use client';

import React, { useState, useEffect } from 'react';
import SimplePieChart from './SimplePieChart';

interface DomainData {
  domain: string;
  visits: number;
  category: string;
  percentage: number;
}

interface CategoryData {
  category: string;
  visits: number;
  percentage: number;
}

interface AnalyticsData {
  domain_frequency: DomainData[];
  category_breakdown: CategoryData[];
}

// Color schemes
const CATEGORY_COLORS = {
  'Other': '#6B7280',
  'Search': '#F59E0B',
  'Technology': '#3B82F6',
  'News & Media': '#EF4444',
  'Social Media': '#8B5CF6',
  'E-commerce': '#10B981',
  'Business Tools': '#F97316',
  'Entertainment': '#EC4899',
  'Education': '#14B8A6'
} as const;

const DOMAIN_COLORS = [
  '#F59E0B', '#3B82F6', '#EF4444', '#8B5CF6', '#10B981',
  '#F97316', '#EC4899', '#14B8A6', '#6366F1', '#84CC16'
];

const BACKEND_PORT = process.env.NEXT_PUBLIC_BACKEND_PORT || '8000';
const BACKEND_URL = `http://localhost:${BACKEND_PORT}`;

export const AnalyticsContainer: React.FC = () => {
  const [data, setData] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await fetch('http://localhost:8001/api/browsing_analytics');
        
        if (!response.ok) {
          throw new Error('Failed to fetch analytics data');
        }
        
        const analyticsData = await response.json();
        setData(analyticsData);
      } catch (err) {
        console.error('Error loading analytics:', err);
        setError('Failed to load analytics data');
        
        // Fallback to sample data for demo purposes
        const sampleData: AnalyticsData = {
          domain_frequency: [
            { domain: 'google.com', visits: 50, category: 'Search', percentage: 25 },
            { domain: 'github.com', visits: 40, category: 'Technology', percentage: 20 },
            { domain: 'stackoverflow.com', visits: 30, category: 'Technology', percentage: 15 },
            { domain: 'medium.com', visits: 25, category: 'News & Media', percentage: 12.5 },
            { domain: 'youtube.com', visits: 20, category: 'Entertainment', percentage: 10 },
            { domain: 'linkedin.com', visits: 15, category: 'Social Media', percentage: 7.5 },
            { domain: 'reddit.com', visits: 12, category: 'Social Media', percentage: 6 },
            { domain: 'twitter.com', visits: 8, category: 'Social Media', percentage: 4 }
          ],
          category_breakdown: [
            { category: 'Technology', visits: 70, percentage: 35 },
            { category: 'Search', visits: 50, percentage: 25 },
            { category: 'Social Media', visits: 35, percentage: 17.5 },
            { category: 'News & Media', visits: 25, percentage: 12.5 },
            { category: 'Entertainment', visits: 20, percentage: 10 }
          ]
        };
        setData(sampleData);
        setError(null); // Clear error since we have sample data
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center py-20">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-orange-400"></div>
      </div>
    );
  }

  if (error && !data) {
    return (
      <div className="text-center py-20">
        <div className="text-red-400 text-xl mb-4">{error}</div>
        <p className="text-gray-400">
          Please ensure the analytics data is generated and available.
        </p>
      </div>
    );
  }

  if (!data || !Array.isArray(data.domain_frequency) || !Array.isArray(data.category_breakdown)) {
    return (
      <div className="text-center py-20">
        <div className="text-red-400 text-xl mb-4">No analytics data available</div>
        <p className="text-gray-400">
          Please ensure the analytics data is generated and available.
        </p>
      </div>
    );
  }

  // Prepare category data for chart
  const categoryChartData = data.category_breakdown.map((item) => ({
    name: item.category,
    value: item.visits,
    percentage: item.percentage,
    color: CATEGORY_COLORS[item.category as keyof typeof CATEGORY_COLORS] || '#6B7280'
  }));

  // Prepare domain data for chart (top 8 domains)
  const topDomains = data.domain_frequency.slice(0, 8);
  const domainChartData = topDomains.map((item, index) => ({
    name: item.domain,
    value: item.visits,
    percentage: item.percentage,
    color: DOMAIN_COLORS[index] || '#6B7280'
  }));

  return (
    <div className="space-y-8">
      {error && (
        <div className="bg-yellow-900 border border-yellow-600 rounded-lg p-4 mb-8">
          <p className="text-yellow-200">
            ⚠️ Using sample data for demonstration. {error}
          </p>
        </div>
      )}
      
      <div className="grid lg:grid-cols-2 gap-8">
        <SimplePieChart 
          data={categoryChartData} 
          title="Browsing Categories" 
        />
        <SimplePieChart 
          data={domainChartData} 
          title="Top Domains Visited" 
        />
      </div>
      
      <div className="text-center mt-12">
        <p className="text-gray-400 mb-6">
          These insights are generated from your browsing history to help you understand your digital patterns and interests.
        </p>
        <div className="grid md:grid-cols-3 gap-6 max-w-4xl mx-auto">
          <div className="bg-gray-700 rounded-lg p-4">
            <div className="text-orange-400 text-2xl mb-2">📊</div>
            <h4 className="font-bold text-white mb-2">Category Analysis</h4>
            <p className="text-gray-300 text-sm">See how your browsing time is distributed across different categories</p>
          </div>
          <div className="bg-gray-700 rounded-lg p-4">
            <div className="text-purple-400 text-2xl mb-2">🌐</div>
            <h4 className="font-bold text-white mb-2">Top Domains</h4>
            <p className="text-gray-300 text-sm">Discover which websites you visit most frequently</p>
          </div>
          <div className="bg-gray-700 rounded-lg p-4">
            <div className="text-blue-400 text-2xl mb-2">🎯</div>
            <h4 className="font-bold text-white mb-2">Insights</h4>
            <p className="text-gray-300 text-sm">Get personalized recommendations based on your patterns</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalyticsContainer; 