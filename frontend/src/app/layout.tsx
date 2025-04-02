import type { Metadata } from 'next';
import { Geist, Geist_Mono } from 'next/font/google';
import Header from '@/components/Header'; // Import Header component
import './globals.css';

const geistSans = Geist({
  variable: '--font-geist-sans',
  subsets: ['latin'],
});

const geistMono = Geist_Mono({
  variable: '--font-geist-mono',
  subsets: ['latin'],
});

export const metadata: Metadata = {
  title: 'FinSight AI', // Updated title
  description: 'AI-powered Investment Research Assistant', // Updated description
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased flex flex-col min-h-screen`}
      >
        <Header />
        <main className="flex-grow container mx-auto p-4">{children}</main>
        <footer className="bg-gray-200 text-center p-4 mt-auto">
          © {new Date().getFullYear()} FinSight AI. All rights reserved.
        </footer>
      </body>
    </html>
  );
}
