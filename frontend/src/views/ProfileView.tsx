import React, { useState } from 'react';
import { User, Mail, Stethoscope, Save, Loader2, CheckCircle2, AlertCircle } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { doctorAPI } from '../services/api';

const SPECIALTIES = [
  'General Practitioner', 'Cardiology', 'Neurology', 'Radiology',
  'Oncology', 'Pathology', 'Pediatrics', 'Internal Medicine',
  'Emergency Medicine', 'Surgery', 'Orthopaedics', 'Pulmonology',
  'Endocrinology', 'Psychiatry', 'Dermatology',
];

const ProfileView: React.FC = () => {
  const { doctor } = useAuth();
  const [fullName, setFullName] = useState(doctor?.full_name ?? '');
  const [specialty, setSpecialty] = useState(doctor?.specialty ?? '');
  const [saving, setSaving] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState('');

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setSuccess(false);
    setError('');
    try {
      await doctorAPI.updateProfile({ full_name: fullName, specialty: specialty || undefined });
      setSuccess(true);
      setTimeout(() => setSuccess(false), 3000);
    } catch (err: any) {
      setError(err.response?.data?.detail ?? 'Failed to update profile.');
    } finally {
      setSaving(false);
    }
  };

  const inputCls = `w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-sm text-white placeholder-slate-500
    focus:outline-none focus:border-cyan-500/50 focus:ring-2 focus:ring-cyan-500/10 transition-all`;

  return (
    <div className="p-6 max-w-2xl mx-auto space-y-6">
      <div>
        <h2 className="text-xl font-bold text-white">Doctor Profile</h2>
        <p className="text-sm text-slate-500 mt-0.5">Manage your clinical workspace account details.</p>
      </div>

      {/* Avatar & identity card */}
      <div className="bg-[#161F30] border border-white/5 rounded-2xl p-6 flex items-center gap-5">
        <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center text-2xl font-bold text-white flex-shrink-0">
          {doctor?.full_name?.charAt(0).toUpperCase()}
        </div>
        <div>
          <p className="text-lg font-bold text-white">{doctor?.full_name}</p>
          <p className="text-sm text-slate-400">{doctor?.specialty ?? 'No specialty set'}</p>
          <p className="text-xs text-slate-600 mt-1">Member since {doctor?.created_at ? new Date(doctor.created_at).toLocaleDateString() : '—'}</p>
        </div>
      </div>

      {/* Feedback */}
      {success && (
        <div className="flex items-center gap-3 bg-emerald-500/10 border border-emerald-500/20 rounded-xl px-4 py-3">
          <CheckCircle2 size={16} className="text-emerald-400" />
          <p className="text-sm text-emerald-300">Profile updated successfully.</p>
        </div>
      )}
      {error && (
        <div className="flex items-center gap-3 bg-red-500/10 border border-red-500/20 rounded-xl px-4 py-3">
          <AlertCircle size={16} className="text-red-400" />
          <p className="text-sm text-red-300">{error}</p>
        </div>
      )}

      {/* Edit form */}
      <form onSubmit={handleSave} className="bg-[#161F30] border border-white/5 rounded-2xl p-6 space-y-5">
        <h3 className="text-sm font-semibold text-slate-300 border-b border-white/5 pb-3">Edit Information</h3>

        <div>
          <label className="flex items-center gap-2 text-xs font-semibold text-slate-400 mb-2 uppercase tracking-wider">
            <User size={12} /> Full Name
          </label>
          <input type="text" value={fullName} onChange={e => setFullName(e.target.value)}
            placeholder="Dr. Full Name" className={inputCls} />
        </div>

        <div>
          <label className="flex items-center gap-2 text-xs font-semibold text-slate-400 mb-2 uppercase tracking-wider">
            <Mail size={12} /> Email Address
          </label>
          <input type="email" value={doctor?.email ?? ''} disabled
            className={`${inputCls} opacity-50 cursor-not-allowed`} />
          <p className="text-xs text-slate-600 mt-1">Email cannot be changed after registration.</p>
        </div>

        <div>
          <label className="flex items-center gap-2 text-xs font-semibold text-slate-400 mb-2 uppercase tracking-wider">
            <Stethoscope size={12} /> Clinical Specialty
          </label>
          <select value={specialty} onChange={e => setSpecialty(e.target.value)} className={`${inputCls} cursor-pointer`}>
            <option value="" className="bg-[#161F30]">Select specialty</option>
            {SPECIALTIES.map(s => <option key={s} value={s} className="bg-[#161F30]">{s}</option>)}
          </select>
        </div>

        <button type="submit" disabled={saving}
          className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-cyan-600 to-blue-600
            hover:from-cyan-500 hover:to-blue-500 text-white text-sm font-semibold transition-all
            shadow-lg shadow-cyan-500/20 disabled:opacity-50 disabled:cursor-not-allowed">
          {saving ? <><Loader2 size={15} className="animate-spin" />Saving…</> : <><Save size={15} />Save Changes</>}
        </button>
      </form>
    </div>
  );
};

export default ProfileView;
