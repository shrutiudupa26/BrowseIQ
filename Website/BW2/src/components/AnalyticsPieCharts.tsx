'use client';

import React, { useState, useEffect } from 'react';
import dynamic from 'next/dynamic';
import { fetchAnalyticsData, getCategoryColor, getDomainColor } from '@/lib/analytics';
import type { AnalyticsData, CategoryData, DomainData } from '@/lib/analytics';

// Dynamically import the entire recharts module to avoid SSR issues
const RechartsComponents = dynamic(
  () => import('recharts'),
  { 
    ssr: false,
    loading: () => (
      <div className="h-80 flex items-center justify-center">
        <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-orange-400"></div>
      </div>
    )
  }
);

interface CustomTooltipProps {
  active?: boolean;
  payload?: Array<{
    payload: {
      name?: string;
      domain?: string;
      category?: string;
      visits: number;
      percentage: number;
    };
  }>;
  label?: string;
}

const CustomTooltip: React.FC<CustomTooltipProps> = ({ active, payload }) => {
  if (active && payload && payload.length) {
    const data = payload[0].payload;
    return (
      <div className="bg-gray-800 border border-gray-600 rounded-lg p-3 shadow-lg">
        <p className="text-white font-semibold">{data.name || data.domain || data.category}</p>
        <p className="text-orange-400">
          Visits: <span className="font-bold">{data.visits}</span>
        </p>
        <p className="text-purple-400">
          Percentage: <span className="font-bold">{data.percentage}%</span>
        </p>
      </div>
    );
  }
  return null;
};

const CategoryPieChart: React.FC<{ data: CategoryData[]; recharts: any }> = ({ data, recharts }) => {
  if (!recharts) {
    return (
      <div className="bg-gray-800 rounded-xl p-6">
        <h3 className="text-2xl font-bold text-white mb-4 text-center">
          Browsing Categories
        </h3>
        <div className="h-80 flex items-center justify-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-orange-400"></div>
        </div>
      </div>
    );
  }

  const { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } = recharts;
  
  const chartData = data.map((item) => ({
    name: item.category,
    visits: item.visits,
    percentage: item.percentage,
  }));

  return (
    <div className="bg-gray-800 rounded-xl p-6">
      <h3 className="text-2xl font-bold text-white mb-4 text-center">
        Browsing Categories
      </h3>
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={chartData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ name, percentage }: { name: string; percentage: number }) => `${name}: ${percentage}%`}
              outerRadius={100}
              fill="#8884d8"
              dataKey="visits"
            >
              {chartData.map((entry, index) => (
                <Cell 
                  key={`cell-${index}`} 
                  fill={getCategoryColor(entry.name)} 
                />
              ))}
            </Pie>
            <Tooltip content={<CustomTooltip />} />
            <Legend 
              wrapperStyle={{ color: '#fff' }}
              formatter={(value: string) => <span style={{ color: '#fff' }}>{value}</span>}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

const DomainPieChart: React.FC<{ data: DomainData[]; recharts: any }> = ({ data, recharts }) => {
  if (!recharts) {
    return (
      <div className="bg-gray-800 rounded-xl p-6">
        <h3 className="text-2xl font-bold text-white mb-4 text-center">
          Top Domains Visited
        </h3>
        <div className="h-80 flex items-center justify-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-orange-400"></div>
        </div>
      </div>
    );
  }

  const { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } = recharts;

  // Take top 8 domains for better visibility
  const topDomains = data.slice(0, 8);
  const chartData = topDomains.map((item) => ({
    name: item.domain,
    visits: item.visits,
    percentage: item.percentage,
    category: item.category,
  }));

  return (
    <div className="bg-gray-800 rounded-xl p-6">
      <h3 className="text-2xl font-bold text-white mb-4 text-center">
        Top Domains Visited
      </h3>
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={chartData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ percentage }: { percentage: number }) => `${percentage}%`}
              outerRadius={100}
              fill="#8884d8"
              dataKey="visits"
            >
              {chartData.map((entry, index) => (
                <Cell 
                  key={`cell-${index}`} 
                  fill={getDomainColor(index)} 
                />
              ))}
            </Pie>
            <Tooltip content={<CustomTooltip />} />
            <Legend 
              wrapperStyle={{ color: '#fff' }}
              formatter={(value: string) => <span style={{ color: '#fff' }}>{value}</span>}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export const AnalyticsPieCharts: React.FC = () => {
  const [data, setData] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [recharts, setRecharts] = useState<any>(null);

  useEffect(() => {
    // Load recharts dynamically
    import('recharts').then((rechartsModule) => {
      setRecharts(rechartsModule);
    });

    const loadData = async () => {
      try {
        setLoading(true);
        const analyticsData = await fetchAnalyticsData();
        if (analyticsData) {
          setData(analyticsData);
        } else {
          setError('Failed to load analytics data');
        }
      } catch (err) {
        setError('Error loading analytics data');
        console.error('Error loading analytics:', err);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  if (loading || !recharts) {
    return (
      <div className="flex justify-center items-center py-20">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-orange-400"></div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="text-center py-20">
        <div className="text-red-400 text-xl mb-4">
          {error || 'No analytics data available'}
        </div>
        <p className="text-gray-400">
          Please ensure the analytics data is generated and available.
        </p>
      </div>
    );
  }

  return (
    <div className="grid lg:grid-cols-2 gap-8">
      <CategoryPieChart data={data.category_breakdown} recharts={recharts} />
      <DomainPieChart data={data.domain_frequency} recharts={recharts} />
    </div>
  );
};

export default AnalyticsPieCharts; 