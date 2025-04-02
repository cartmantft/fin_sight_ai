"use client"; // Needs client-side interaction for form handling

import { useState } from 'react';

export default function UploadPage() {
  const [inputType, setInputType] = useState('url'); // 'url', 'pdf', 'youtube'
  const [url, setUrl] = useState('');
  const [youtubeLink, setYoutubeLink] = useState('');
  const [pdfFile, setPdfFile] = useState<File | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setPdfFile(event.target.files[0]);
    }
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    // TODO: Implement API call to POST /documents based on inputType
    console.log('Submitting:', { inputType, url, youtubeLink, pdfFile });
    // TODO: Implement API call to POST /documents based on inputType
    // console.log('Submitting:', { inputType, url, youtubeLink, pdfFile });
    // alert('Upload functionality not yet implemented.');

    let payload: any = {};
    let endpoint = 'http://localhost:8000/materials/';
    let requestOptions: RequestInit = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // TODO: Add Authorization header if auth is implemented
      },
    };

    try {
      if (inputType === 'url') {
        if (!url) throw new Error('URL is required.');
        payload = { title: url, url: url }; // Use URL as title for now
        requestOptions.body = JSON.stringify(payload);
      } else if (inputType === 'youtube') {
        if (!youtubeLink) throw new Error('YouTube Link is required.');
        payload = { title: youtubeLink, youtube_link: youtubeLink }; // Use link as title for now
        requestOptions.body = JSON.stringify(payload);
      } else if (inputType === 'pdf') {
        if (!pdfFile) throw new Error('PDF file is required.');
        // TODO: PDF upload needs backend adjustment.
        // Current backend expects pdf_file as string (path/url).
        // Option 1: Modify backend to accept file upload (e.g., using UploadFile).
        // Option 2: Upload file to storage first, then send path/url to backend.
        alert('PDF upload is not fully implemented yet due to backend constraints.');
        return; // Stop submission for PDF for now
        /*
        // Example using FormData (requires backend changes)
        const formData = new FormData();
        formData.append('file', pdfFile);
        // Need a way to pass title or extract it
        formData.append('title', pdfFile.name); // Use filename as title for now
        requestOptions.headers = {}; // Remove Content-Type for FormData
        requestOptions.body = formData;
        endpoint = 'http://localhost:8000/materials/upload_pdf/'; // Example new endpoint
        */
      } else {
        throw new Error('Invalid input type');
      }

      const response = await fetch(endpoint, requestOptions);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
        throw new Error(`HTTP error! status: ${response.status}, message: ${errorData.detail || 'Failed to submit'}`);
      }

      const result = await response.json();
      console.log('Submission successful:', result);
      alert('Material submitted successfully! Processing will start in the background.');
      // Optionally clear the form
      setUrl('');
      setYoutubeLink('');
      setPdfFile(null);
      // TODO: Redirect or update UI

    } catch (error: any) {
      console.error('Submission failed:', error);
      alert(`Submission failed: ${error.message}`);
    }
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Upload New Material</h1>
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2">
            Input Type
          </label>
          <select
            value={inputType}
            onChange={(e) => setInputType(e.target.value)}
            className="shadow border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          >
            <option value="url">URL</option>
            <option value="pdf">PDF File</option>
            <option value="youtube">YouTube Link</option>
          </select>
        </div>

        {inputType === 'url' && (
          <div className="mb-4">
            <label htmlFor="url" className="block text-gray-700 text-sm font-bold mb-2">
              Website URL
            </label>
            <input
              type="url"
              id="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://example.com"
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              required
            />
          </div>
        )}

        {inputType === 'pdf' && (
          <div className="mb-4">
            <label htmlFor="pdf" className="block text-gray-700 text-sm font-bold mb-2">
              PDF File
            </label>
            <input
              type="file"
              id="pdf"
              accept=".pdf"
              onChange={handleFileChange}
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              required
            />
          </div>
        )}

        {inputType === 'youtube' && (
          <div className="mb-4">
            <label htmlFor="youtube" className="block text-gray-700 text-sm font-bold mb-2">
              YouTube Link
            </label>
            <input
              type="url"
              id="youtube"
              value={youtubeLink}
              onChange={(e) => setYoutubeLink(e.target.value)}
              placeholder="https://www.youtube.com/watch?v=..."
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              required
            />
          </div>
        )}

        {/* TODO: Add options for summary template, folder selection etc. */}

        <button
          type="submit"
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
        >
          Start Processing
        </button>
      </form>
    </div>
  );
}
