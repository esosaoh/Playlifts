import { Header } from './Header'
import { Sidebar } from './Sidebar'

export const AppLayout = ({ children }: { children: React.ReactNode }) => (
  <div className="flex min-h-screen bg-gray-50 dark:bg-gray-900">
    <Sidebar />
    <div className="flex-1 flex flex-col">
      <Header />
      <main className="flex-1 p-4">{children}</main>
    </div>
  </div>
)
