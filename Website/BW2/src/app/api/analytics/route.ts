import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

export async function GET() {
  try {
    // Path to the analytics file - going up from Website/BW2 to the project root
    const analyticsPath = path.join(process.cwd(), '..', '..', 'data', 'browsing_analytics.json');
    
    // Check if file exists
    if (!fs.existsSync(analyticsPath)) {
      return NextResponse.json(
        { error: 'Analytics data not found' },
        { status: 404 }
      );
    }

    // Read and parse the analytics data
    const data = fs.readFileSync(analyticsPath, 'utf8');
    const analyticsData = JSON.parse(data);

    return NextResponse.json(analyticsData);
  } catch (error) {
    console.error('Error reading analytics data:', error);
    return NextResponse.json(
      { error: 'Failed to load analytics data' },
      { status: 500 }
    );
  }
} 