import React, { useState } from 'react';
import { AuthProvider, useAuth } from './context/AuthContext';
import Layout from './components/Layout';
import LoginView from './views/LoginView';
import RegisterView from './views/RegisterView';
import DashboardView from './views/DashboardView';
import ConsultationsView from './views/ConsultationsView';
import ConsultationDetailView from './views/ConsultationDetailView';
import ProfileView from './views/ProfileView';
import { Loader2 } from 'lucide-react';

type View = 'dashboard' | 'consultations' | 'consultation' | 'profile';

const AppContent: React.FC = () => {
  const { isAuthenticated, isLoading } = useAuth();
  const [authPage, setAuthPage] = useState<'login' | 'register'>('login');
  const [currentView, setCurrentView] = useState<View>('dashboard');
  const [activeConsultationId, setActiveConsultationId] = useState<number | null>(null);

  // Loading state while checking JWT session
  if (isLoading) {
    return (
      <div className="min-h-screen bg-[#0B0F19] flex items-center justify-center gap-3 text-slate-500">
        <Loader2 size={22} className="animate-spin" />
        <span className="text-sm">Loading MedShield-X…</span>
      </div>
    );
  }

  // Unauthenticated — show login or register
  if (!isAuthenticated) {
    return authPage === 'login'
      ? <LoginView onSwitchToRegister={() => setAuthPage('register')} />
      : <RegisterView onSwitchToLogin={() => setAuthPage('login')} />;
  }

  // Navigation handler
  const handleNavigate = (view: string, id?: number) => {
    if (view === 'consultation' && id != null) {
      setActiveConsultationId(id);
      setCurrentView('consultation');
    } else {
      setCurrentView(view as View);
      if (view !== 'consultation') setActiveConsultationId(null);
    }
  };

  // Render current view
  const renderView = () => {
    switch (currentView) {
      case 'dashboard':
        return <DashboardView onNavigate={handleNavigate} />;
      case 'consultations':
        return <ConsultationsView onNavigate={handleNavigate} />;
      case 'consultation':
        return activeConsultationId != null
          ? <ConsultationDetailView
              consultationId={activeConsultationId}
              onBack={() => { setCurrentView('consultations'); setActiveConsultationId(null); }}
            />
          : <ConsultationsView onNavigate={handleNavigate} />;
      case 'profile':
        return <ProfileView />;
      default:
        return <DashboardView onNavigate={handleNavigate} />;
    }
  };

  // Layout view label for topbar
  const layoutView = currentView === 'consultation' ? 'consultation' : currentView;

  return (
    <Layout currentView={layoutView} onNavigate={handleNavigate}>
      {renderView()}
    </Layout>
  );
};

const App: React.FC = () => (
  <AuthProvider>
    <AppContent />
  </AuthProvider>
);

export default App;
