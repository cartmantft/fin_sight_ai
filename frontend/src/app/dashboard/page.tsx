"use client"; // Data fetching and state management require client component

import { useState, useEffect } from 'react';

// Define an interface for the Material data based on backend response
interface Material {
  id: string;
  title: string;
  url?: string;
  pdf_file?: string;
  youtube_link?: string;
  created_at: string;
}

async function fetchRecentMaterials(): Promise<Material[]> {
  try {
    const response = await fetch('http://localhost:8000/materials/recent?limit=5'); // Fetch recent 5 items
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Failed to fetch recent materials:", error);
    return []; // Return empty array on error
  }
}

export default function DashboardPage() {
  const [recentMaterials, setRecentMaterials] = useState<Material[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadMaterials() {
      setIsLoading(true);
      setError(null);
      const materials = await fetchRecentMaterials();
      if (materials.length === 0 && !error) {
         // Check if fetch failed silently
         // setError("Could not load recent materials."); // Optional: show error message
      }
      setRecentMaterials(materials);
      setIsLoading(false);
    }
    loadMaterials();
  }, []); // Empty dependency array means this runs once on mount

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Dashboard</h1>

      <section>
        <h2 className="text-xl font-semibold mb-2">Recent Updates</h2>
        {isLoading && <p>Loading recent materials...</p>}
        {error && <p className="text-red-500">{error}</p>}
        {!isLoading && !error && recentMaterials.length === 0 && (
          <p>No recent materials found.</p>
        )}
        {!isLoading && !error && recentMaterials.length > 0 && (
          <ul className="space-y-3">
            {recentMaterials.map((material) => (
              <li key={material.id} className="p-4 border rounded shadow-sm hover:shadow-md transition-shadow">
                <h3 className="font-semibold text-lg mb-1">{material.title}</h3>
                {/* Display source type based on available fields */}
                {material.url && <p className="text-sm text-gray-600">Type: URL</p>}
                {material.pdf_file && <p className="text-sm text-gray-600">Type: PDF</p>}
                {material.youtube_link && <p className="text-sm text-gray-600">Type: YouTube</p>}
                <p className="text-xs text-gray-500 mt-1">
                  Added: {new Date(material.created_at).toLocaleString()}
                </p>
                {/* TODO: Add link to detail view, summary snippet */}
              </li>
            ))}
          </ul>
        )}
      </section>

      {/* TODO: Implement Folder/Tag views */}
      {/* TODO: Implement Monitoring status */}
    </div>
  );
}
