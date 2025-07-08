export const Sidebar = () => (
  <aside className="w-64 bg-gray-100 dark:bg-gray-900 p-4 hidden md:block">
    {/* Navigation, playlist selection, etc. */}
    <nav>
      <ul>
        <li className="mb-2">
          <a href="/" className="text-gray-800 dark:text-gray-200">
            Transfer
          </a>
        </li>
      </ul>
    </nav>
  </aside>
)
