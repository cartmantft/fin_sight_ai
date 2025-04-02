import Link from 'next/link';

export default function Header() {
  return (
    <header className="bg-gray-800 text-white p-4">
      <nav className="container mx-auto flex justify-between items-center">
        <Link href="/" className="text-xl font-bold">
          FinSight AI
        </Link>
        <ul className="flex space-x-4">
          <li>
            <Link href="/dashboard" className="hover:text-gray-300">
              Dashboard
            </Link>
          </li>
          <li>
            <Link href="/upload" className="hover:text-gray-300">
              Upload
            </Link>
          </li>
          <li>
            <Link href="/schedules" className="hover:text-gray-300">
              Schedules
            </Link>
          </li>
          {/* Add Auth links later */}
        </ul>
      </nav>
    </header>
  );
}
