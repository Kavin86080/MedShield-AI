import React, { useEffect, useState } from 'react';
import {
  Plus, Stethoscope, Clock,
  Activity, Users, TrendingUp, ChevronRight, Loader2,
  AlertCircle, CheckCircle2
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { consultationAPI } from '../services/api';
import { Consultation } from '../types';

interface DashboardViewProps {
  onNavigate: (view: string, id?: number) => void;
}

const StatCard: React.FC<{ icon: React.ElementType; label: string; value: string | number; color: string; sub?: string }> = ({ icon: Icon, label, value, color, sub }) => (
  <div className="bg-[#161F30] border border-white/5 rounded-2xl p-5 flex items-start gap-4">
    <div className={`w-11 h-11 rounded-xl flex items-center justify-center flex-shrink-0 ${color}`}>
      <Icon size={20} className="text-white" />
    </div>
    <div>
      <p className="text-2xl font-bold text-white">{value}</p>
      <p className="text-xs text-slate-400 font-medium">{label}</p>
      {sub && <p className="text-xs text-slate-600 mt-0.5">{sub}</p>}
    </div>
  </div>
);

const StatusBadge: React.FC<{ status: string }> = ({ status }) => (
  <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold
    ${status === 'active'
      ? 'bg-emerald-500/15 text-emerald-400 border border-emerald-500/20'
      : 'bg-slate-500/15 text-slate-400 border border-slate-500/20'
    }`}>
    {status === 'active' ? <Activity size={10} /> : <CheckCircle2 size={10} />}
    {status.charAt(0).toUpperCase() + status.slice(1)}
  </span>
);

const DashboardView: React.FC<DashboardViewProps> = ({ onNavigate }) => {
  const { doctor } = useAuth();
  const [consultations, setConsultations] = useState<Consultation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showNewModal, setShowNewModal] = useState(false);
  const [creating, setCreating] = useState(false);
  const [newForm, setNewForm] = useState({ patient_name: '', patient_age: '', patient_gender: 'Male' });

  useEffect(() => {
    consultationAPI.list()
      .then(setConsultations)
      .catch(() => setError('Failed to load consultations.'))
      .finally(() => setLoading(false));
  }, []);

  const active = consultations.filter(c => c.status === 'active');
  const completed = consultations.filter(c => c.status === 'completed');
  const recent = [...consultations].sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime()).slice(0, 5);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newForm.patient_name || !newForm.patient_age) return;
    setCreating(true);
    try {
      const created = await consultationAPI.create({
        patient_name: newForm.patient_name,
        patient_age: parseInt(newForm.patient_age),
        patient_gender: newForm.patient_gender,
      });
      setConsultations(p => [created, ...p]);
      setShowNewModal(false);
      setNewForm({ patient_name: '', patient_age: '', patient_gender: 'Male' });
      onNavigate('consultation', created.id);
    } catch {
      setError('Failed to create consultation.');
    } finally {
      setCreating(false);
    }
  };

  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-white">
            Good day, <span className="text-cyan-400">{doctor?.full_name?.split(' ')[0]}</span>
          </h2>
          <p className="text-sm text-slate-500 mt-0.5">Your clinical workspace is active and ready.</p>
        </div>
        <button
          id="new-consultation-btn"
          onClick={() => setShowNewModal(true)}
          className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-cyan-600 to-blue-600
            hover:from-cyan-500 hover:to-blue-500 text-white text-sm font-semibold
            transition-all duration-200 shadow-lg shadow-cyan-500/20 flex-shrink-0"
        >
          <Plus size={16} />
          New Consultation
        </button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard icon={Users} label="Total Consultations" value={consultations.length} color="bg-gradient-to-br from-blue-500 to-blue-700" />
        <StatCard icon={Activity} label="Active Cases" value={active.length} color="bg-gradient-to-br from-emerald-500 to-emerald-700" />
        <StatCard icon={CheckCircle2} label="Completed" value={completed.length} color="bg-gradient-to-br from-slate-500 to-slate-700" />
        <StatCard icon={TrendingUp} label="AI Queries" value="—" color="bg-gradient-to-br from-violet-500 to-violet-700" sub="across all sessions" />
      </div>

      {/* Error */}
      {error && (
        <div className="flex items-center gap-3 bg-red-500/10 border border-red-500/20 rounded-xl px-4 py-3">
          <AlertCircle size={16} className="text-red-400" />
          <p className="text-sm text-red-300">{error}</p>
        </div>
      )}

      {/* Recent consultations */}
      <div className="bg-[#161F30] border border-white/5 rounded-2xl overflow-hidden">
        <div className="flex items-center justify-between px-5 py-4 border-b border-white/5">
          <h3 className="text-sm font-semibold text-white flex items-center gap-2">
            <Clock size={15} className="text-slate-400" />
            Recent Consultations
          </h3>
          <button
            onClick={() => onNavigate('consultations')}
            className="text-xs text-cyan-400 hover:text-cyan-300 font-medium flex items-center gap-1"
          >
            View all <ChevronRight size={12} />
          </button>
        </div>

        {loading ? (
          <div className="flex items-center justify-center py-16 gap-3 text-slate-500">
            <Loader2 size={18} className="animate-spin" />
            <span className="text-sm">Loading consultations…</span>
          </div>
        ) : recent.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-16 text-slate-500">
            <Stethoscope size={32} className="mb-3 text-slate-700" />
            <p className="text-sm font-medium">No consultations yet</p>
            <p className="text-xs text-slate-600 mt-1">Start by creating a new patient consultation.</p>
          </div>
        ) : (
          <div className="divide-y divide-white/5">
            {recent.map(c => (
              <button
                key={c.id}
                onClick={() => onNavigate('consultation', c.id)}
                className="w-full flex items-center gap-4 px-5 py-3.5 hover:bg-white/3 transition-colors text-left"
              >
                <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-cyan-600/20 to-blue-600/20 border border-cyan-500/15 flex items-center justify-center flex-shrink-0">
                  <Stethoscope size={16} className="text-cyan-400" />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-semibold text-white truncate">{c.patient_name}</p>
                  <p className="text-xs text-slate-500">{c.patient_age} y/o · {c.patient_gender}</p>
                </div>
                <div className="flex items-center gap-3 flex-shrink-0">
                  <StatusBadge status={c.status} />
                  <p className="text-xs text-slate-600 hidden sm:block">
                    {new Date(c.created_at).toLocaleDateString()}
                  </p>
                  <ChevronRight size={14} className="text-slate-600" />
                </div>
              </button>
            ))}
          </div>
        )}
      </div>

      {/* New Consultation Modal */}
      {showNewModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
          <div className="bg-[#161F30] border border-white/8 rounded-2xl w-full max-w-md p-7 shadow-2xl">
            <h3 className="text-lg font-bold text-white mb-1 flex items-center gap-2">
              <Stethoscope size={18} className="text-cyan-400" />
              New Consultation
            </h3>
            <p className="text-sm text-slate-500 mb-6">Enter patient details to start the clinical session.</p>

            <form onSubmit={handleCreate} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-2 uppercase tracking-wider">Patient Name</label>
                <input type="text" required value={newForm.patient_name}
                  onChange={e => setNewForm(p => ({ ...p, patient_name: e.target.value }))}
                  placeholder="Full patient name"
                  className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-sm text-white placeholder-slate-500
                    focus:outline-none focus:border-cyan-500/50 focus:ring-2 focus:ring-cyan-500/10 transition-all" />
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-400 mb-2 uppercase tracking-wider">Age</label>
                  <input type="number" required min={1} max={150} value={newForm.patient_age}
                    onChange={e => setNewForm(p => ({ ...p, patient_age: e.target.value }))}
                    placeholder="Age"
                    className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-sm text-white placeholder-slate-500
                      focus:outline-none focus:border-cyan-500/50 focus:ring-2 focus:ring-cyan-500/10 transition-all" />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-400 mb-2 uppercase tracking-wider">Gender</label>
                  <select value={newForm.patient_gender}
                    onChange={e => setNewForm(p => ({ ...p, patient_gender: e.target.value }))}
                    className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-sm text-white
                      focus:outline-none focus:border-cyan-500/50 focus:ring-2 focus:ring-cyan-500/10 transition-all cursor-pointer">
                    <option value="Male" className="bg-[#161F30]">Male</option>
                    <option value="Female" className="bg-[#161F30]">Female</option>
                    <option value="Other" className="bg-[#161F30]">Other</option>
                  </select>
                </div>
              </div>
              <div className="flex gap-3 pt-2">
                <button type="button" onClick={() => setShowNewModal(false)}
                  className="flex-1 py-2.5 rounded-xl border border-white/10 text-sm text-slate-400 hover:bg-white/5 transition-colors">
                  Cancel
                </button>
                <button type="submit" disabled={creating}
                  className="flex-1 flex items-center justify-center gap-2 py-2.5 rounded-xl bg-gradient-to-r from-cyan-600 to-blue-600
                    text-white text-sm font-semibold hover:from-cyan-500 hover:to-blue-500 transition-all disabled:opacity-50">
                  {creating ? <><Loader2 size={14} className="animate-spin" />Creating…</> : 'Start Consultation'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default DashboardView;
