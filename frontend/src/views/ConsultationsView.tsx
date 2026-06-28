import React, { useEffect, useState } from 'react';
import {
  Stethoscope, Plus, Search, Filter, Activity,
  CheckCircle2, ChevronRight, Loader2, Trash2, AlertCircle
} from 'lucide-react';
import { consultationAPI } from '../services/api';
import { Consultation } from '../types';

interface ConsultationsViewProps {
  onNavigate: (view: string, id?: number) => void;
}

const ConsultationsView: React.FC<ConsultationsViewProps> = ({ onNavigate }) => {
  const [consultations, setConsultations] = useState<Consultation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState<'all' | 'active' | 'completed'>('all');

  useEffect(() => {
    consultationAPI.list()
      .then(setConsultations)
      .catch(() => setError('Failed to load consultations.'))
      .finally(() => setLoading(false));
  }, []);

  const handleDelete = async (id: number, e: React.MouseEvent) => {
    e.stopPropagation();
    if (!confirm('Delete this consultation? This action cannot be undone.')) return;
    try {
      await consultationAPI.delete(id);
      setConsultations(p => p.filter(c => c.id !== id));
    } catch {
      setError('Failed to delete consultation.');
    }
  };

  const filtered = consultations
    .filter(c => statusFilter === 'all' || c.status === statusFilter)
    .filter(c =>
      c.patient_name.toLowerCase().includes(search.toLowerCase()) ||
      c.patient_gender.toLowerCase().includes(search.toLowerCase())
    );

  return (
    <div className="p-6 max-w-6xl mx-auto space-y-5">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-white">Consultations</h2>
          <p className="text-sm text-slate-500 mt-0.5">{consultations.length} total patient sessions</p>
        </div>
        <button
          onClick={() => onNavigate('dashboard')}
          className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-gradient-to-r from-cyan-600 to-blue-600
            text-white text-sm font-semibold hover:from-cyan-500 hover:to-blue-500 transition-all shadow-lg shadow-cyan-500/20"
        >
          <Plus size={15} />
          New Consultation
        </button>
      </div>

      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-3">
        <div className="relative flex-1">
          <Search size={15} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500" />
          <input
            type="text"
            value={search}
            onChange={e => setSearch(e.target.value)}
            placeholder="Search patients…"
            className="w-full pl-10 pr-4 py-2.5 bg-[#161F30] border border-white/8 rounded-xl text-sm text-white placeholder-slate-500
              focus:outline-none focus:border-cyan-500/40 focus:ring-1 focus:ring-cyan-500/10 transition-all"
          />
        </div>
        <div className="flex items-center gap-2">
          <Filter size={14} className="text-slate-500 flex-shrink-0" />
          {(['all', 'active', 'completed'] as const).map(f => (
            <button
              key={f}
              onClick={() => setStatusFilter(f)}
              className={`px-3.5 py-2 rounded-lg text-xs font-semibold capitalize transition-all ${
                statusFilter === f
                  ? 'bg-cyan-600/20 text-cyan-400 border border-cyan-500/25'
                  : 'text-slate-400 hover:bg-white/5 border border-transparent'
              }`}
            >
              {f}
            </button>
          ))}
        </div>
      </div>

      {/* Error */}
      {error && (
        <div className="flex items-center gap-3 bg-red-500/10 border border-red-500/20 rounded-xl px-4 py-3">
          <AlertCircle size={16} className="text-red-400" />
          <p className="text-sm text-red-300">{error}</p>
        </div>
      )}

      {/* Table */}
      <div className="bg-[#161F30] border border-white/5 rounded-2xl overflow-hidden">
        {loading ? (
          <div className="flex items-center justify-center py-20 gap-3 text-slate-500">
            <Loader2 size={18} className="animate-spin" />
            <span className="text-sm">Loading…</span>
          </div>
        ) : filtered.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-20 text-slate-500">
            <Stethoscope size={36} className="mb-3 text-slate-700" />
            <p className="text-sm font-medium">No consultations found</p>
            <p className="text-xs text-slate-600 mt-1">Adjust filters or create a new consultation.</p>
          </div>
        ) : (
          <>
            {/* Table header */}
            <div className="hidden sm:grid grid-cols-12 gap-4 px-5 py-2.5 border-b border-white/5 text-xs font-semibold text-slate-500 uppercase tracking-wider">
              <div className="col-span-4">Patient</div>
              <div className="col-span-2">Age / Gender</div>
              <div className="col-span-2">Status</div>
              <div className="col-span-3">Created</div>
              <div className="col-span-1"></div>
            </div>
            <div className="divide-y divide-white/5">
              {filtered.map(c => (
                <button
                  key={c.id}
                  onClick={() => onNavigate('consultation', c.id)}
                  className="w-full grid sm:grid-cols-12 gap-4 px-5 py-3.5 hover:bg-white/3 transition-colors text-left items-center"
                >
                  <div className="sm:col-span-4 flex items-center gap-3">
                    <div className="w-8 h-8 rounded-lg bg-cyan-600/15 border border-cyan-500/15 flex items-center justify-center flex-shrink-0">
                      <Stethoscope size={14} className="text-cyan-400" />
                    </div>
                    <div className="min-w-0">
                      <p className="text-sm font-semibold text-white truncate">{c.patient_name}</p>
                      <p className="text-xs text-slate-500 sm:hidden">{c.patient_age} y/o · {c.patient_gender}</p>
                    </div>
                  </div>
                  <div className="hidden sm:block sm:col-span-2 text-sm text-slate-400">
                    {c.patient_age} y/o · {c.patient_gender}
                  </div>
                  <div className="hidden sm:block sm:col-span-2">
                    <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-semibold ${
                      c.status === 'active'
                        ? 'bg-emerald-500/15 text-emerald-400 border border-emerald-500/20'
                        : 'bg-slate-500/15 text-slate-400 border border-slate-500/20'
                    }`}>
                      {c.status === 'active' ? <Activity size={9} /> : <CheckCircle2 size={9} />}
                      {c.status}
                    </span>
                  </div>
                  <div className="hidden sm:block sm:col-span-3 text-xs text-slate-500">
                    {new Date(c.created_at).toLocaleString()}
                  </div>
                  <div className="hidden sm:flex sm:col-span-1 items-center gap-1 justify-end">
                    <button
                      onClick={e => handleDelete(c.id, e)}
                      className="p-1.5 rounded-lg hover:bg-red-500/10 text-slate-600 hover:text-red-400 transition-colors"
                    >
                      <Trash2 size={13} />
                    </button>
                    <ChevronRight size={14} className="text-slate-600" />
                  </div>
                </button>
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default ConsultationsView;
