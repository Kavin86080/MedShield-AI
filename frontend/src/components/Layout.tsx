import React, { useState } from 'react';
import { 
  Shield, LayoutDashboard, Stethoscope, LogOut, 
  ChevronLeft, ChevronRight, User, Menu, X, Moon, Sun
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

interface LayoutProps {
  children: React.ReactNode;
  currentView: string;
  onNavigate: (view: string) => void;
}

const navItems = [
  { id: 'dashboard',      label: 'Dashboard',      icon: LayoutDashboard },
  { id: 'consultations',  label: 'Consultations',   icon: Stethoscope },
  { id: 'profile',        label: 'My Profile',      icon: User },
];

const Layout: React.FC<LayoutProps> = ({ children, currentView, onNavigate }) => {
  const { doctor, logout } = useAuth();
  const [collapsed, setCollapsed] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [darkMode, setDarkMode] = useState(true);

  const toggleTheme = () => {
    setDarkMode(prev => {
      const next = !prev;
      document.documentElement.classList.toggle('dark', next);
      return next;
    });
  };

  const sidebarW = collapsed ? 'w-16' : 'w-60';

  return (
    <div className="flex h-screen overflow-hidden bg-[#0B0F19] text-slate-100">

      {/* Mobile overlay */}
      {mobileOpen && (
        <div className="fixed inset-0 z-30 bg-black/60 lg:hidden" onClick={() => setMobileOpen(false)} />
      )}

      {/* Sidebar */}
      <aside
        className={`
          fixed lg:relative z-40 inset-y-0 left-0 flex flex-col
          ${sidebarW} bg-[#161F30] border-r border-white/5 transition-all duration-300
          ${mobileOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
        `}
      >
        {/* Brand */}
        <div className="flex items-center justify-between px-4 py-5 border-b border-white/5">
          {!collapsed && (
            <div className="flex items-center gap-2 min-w-0">
              <div className="flex-shrink-0 w-8 h-8 rounded-lg bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center">
                <Shield size={16} className="text-white" />
              </div>
              <div className="truncate">
                <p className="text-sm font-bold text-white truncate">MedShield-X</p>
                <p className="text-[10px] text-slate-500 truncate">Clinical AI Platform</p>
              </div>
            </div>
          )}
          {collapsed && (
            <div className="mx-auto w-8 h-8 rounded-lg bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center">
              <Shield size={16} className="text-white" />
            </div>
          )}
          <button
            onClick={() => setCollapsed(p => !p)}
            className="hidden lg:flex ml-auto flex-shrink-0 p-1 rounded-md hover:bg-white/5 text-slate-400"
          >
            {collapsed ? <ChevronRight size={15} /> : <ChevronLeft size={15} />}
          </button>
        </div>

        {/* Nav items */}
        <nav className="flex-1 px-2 py-4 space-y-1 overflow-y-auto">
          {navItems.map(item => {
            const Icon = item.icon;
            const active = currentView === item.id;
            return (
              <button
                key={item.id}
                onClick={() => { onNavigate(item.id); setMobileOpen(false); }}
                className={`
                  w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all duration-150
                  ${active
                    ? 'bg-gradient-to-r from-cyan-600/30 to-blue-600/20 text-cyan-400 border border-cyan-500/20'
                    : 'text-slate-400 hover:bg-white/5 hover:text-slate-200'
                  }
                `}
              >
                <Icon size={17} className="flex-shrink-0" />
                {!collapsed && <span className="truncate">{item.label}</span>}
              </button>
            );
          })}
        </nav>

        {/* Doctor footer */}
        <div className="px-2 py-3 border-t border-white/5">
          {!collapsed && (
            <div className="px-3 py-2 mb-2 rounded-xl bg-white/5">
              <p className="text-xs font-semibold text-white truncate">{doctor?.full_name}</p>
              <p className="text-[10px] text-slate-500 truncate">{doctor?.specialty ?? 'General Practitioner'}</p>
            </div>
          )}
          <button
            onClick={logout}
            className="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm text-slate-400 hover:bg-red-500/10 hover:text-red-400 transition-all duration-150"
          >
            <LogOut size={16} className="flex-shrink-0" />
            {!collapsed && <span>Logout</span>}
          </button>
        </div>
      </aside>

      {/* Main content */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* Topbar */}
        <header className="flex items-center justify-between px-5 h-14 bg-[#0B0F19] border-b border-white/5 flex-shrink-0">
          <div className="flex items-center gap-3">
            <button
              className="lg:hidden p-1.5 rounded-lg hover:bg-white/5 text-slate-400"
              onClick={() => setMobileOpen(p => !p)}
            >
              {mobileOpen ? <X size={18} /> : <Menu size={18} />}
            </button>
            <h1 className="text-sm font-semibold text-slate-200 capitalize">
              {navItems.find(n => n.id === currentView)?.label ?? currentView}
            </h1>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={toggleTheme}
              className="p-2 rounded-lg hover:bg-white/5 text-slate-400 transition-colors"
              title="Toggle theme"
            >
              {darkMode ? <Moon size={16} /> : <Sun size={16} />}
            </button>
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center text-xs font-bold text-white">
              {doctor?.full_name?.charAt(0).toUpperCase() ?? 'D'}
            </div>
          </div>
        </header>

        {/* Page content */}
        <main className="flex-1 overflow-y-auto">
          {children}
        </main>
      </div>
    </div>
  );
};

export default Layout;
