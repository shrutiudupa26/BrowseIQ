'use client';

import React, { useState, useEffect } from 'react';

interface PieData {
  name: string;
  value: number;
  percentage: number;
  color: string;
}

interface SimplePieChartProps {
  data: PieData[];
  title: string;
}

export const SimplePieChart: React.FC<SimplePieChartProps> = ({ data, title }) => {
  const [mounted, setMounted] = useState(false);
  const [RechartsComponents, setRechartsComponents] = useState<any>(null);

  useEffect(() => {
    setMounted(true);
    
    // Dynamically import Recharts to avoid SSR issues
    import('recharts').then((recharts) => {
      setRechartsComponents(recharts);
    });
  }, []);

  if (!mounted || !RechartsComponents) {
    return (
      <div className="bg-gray-800 rounded-xl p-6">
        <h3 className="text-2xl font-bold text-white mb-4 text-center">{title}</h3>
        <div className="h-80 flex items-center justify-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-orange-400"></div>
        </div>
      </div>
    );
  }

  const { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } = RechartsComponents;

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-gray-800 border border-gray-600 rounded-lg p-3 shadow-lg">
          <p className="text-white font-semibold">{data.name}</p>
          <p className="text-orange-400">
            Visits: <span className="font-bold">{data.value}</span>
          </p>
          <p className="text-purple-400">
            Percentage: <span className="font-bold">{data.percentage}%</span>
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="bg-gray-800 rounded-xl p-6">
      <h3 className="text-2xl font-bold text-white mb-4 text-center">{title}</h3>
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ name, percentage }: { name: string; percentage: number }) => 
                `${name}: ${percentage}%`
              }
              outerRadius={100}
              fill="#8884d8"
              dataKey="value"
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
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

export default SimplePieChart; 