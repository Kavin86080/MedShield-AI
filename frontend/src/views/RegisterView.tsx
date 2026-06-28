import React, { useState } from 'react';
import { Shield, Eye, EyeOff, Loader2, AlertCircle } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

interface RegisterViewProps {
  onSwitchToLogin: () => void;
}

const SPECIALTIES = [
  'General Practitioner', 'Cardiology', 'Neurology', 'Radiology',
  'Oncology', 'Pathology', 'Pediatrics', 'Internal Medicine',
  'Emergency Medicine', 'Surgery', 'Orthopaedics', 'Pulmonology',
  'Endocrinology', 'Psychiatry', 'Dermatology',
];

const RegisterView: React.FC<RegisterViewProps> = ({ onSwitchToLogin }) => {
  const { register } = useAuth();
  const [form, setForm] = useState({ full_name: '', email: '', password: '', specialty: '' });
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const set = (k: string) => (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) =>
    setForm(p => ({ ...p, [k]: e.target.value }));

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (form.password.length < 8) {
      setError('Password must be at least 8 characters.');
      return;
    }
    setError('');
    setLoading(true);
    try {
      await register(form.email, form.password, form.full_name, form.specialty || undefined);
    } catch (err: any) {
      setError(err.response?.data?.detail ?? 'Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const inputCls = `w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-sm text-white placeholder-slate-500
    focus:outline-none focus:border-cyan-500/50 focus:ring-2 focus:ring-cyan-500/10 transition-all`;

  return (
    <div className="min-h-screen bg-[#0B0F19] flex items-center justify-center p-4">
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -left-40 w-96 h-96 rounded-full bg-blue-600/10 blur-3xl" />
        <div className="absolute -bottom-40 -right-40 w-96 h-96 rounded-full bg-cyan-600/10 blur-3xl" />
      </div>

      <div className="relative w-full max-w-md">
        <div className="bg-[#161F30] border border-white/8 rounded-2xl p-8 shadow-2xl">
          
          <div className="text-center mb-7">
            <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-gradient-to-br from-cyan-500 to-blue-600 mb-4 shadow-lg shadow-cyan-500/25">
              <Shield size={26} className="text-white" />
            </div>
            <h1 className="text-2xl font-bold text-white mb-1">Register Portal</h1>
            <p className="text-sm text-slate-400">Create your doctor workspace account</p>
          </div>

          {error && (
            <div className="flex items-start gap-3 bg-red-500/10 border border-red-500/20 rounded-xl px-4 py-3 mb-5">
              <AlertCircle size={16} className="text-red-400 flex-shrink-0 mt-0.5" />
              <p className="text-sm text-red-300">{error}</p>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-400 mb-2 uppercase tracking-wider">Full Name</label>
              <input id="reg-name" type="text" required value={form.full_name} onChange={set('full_name')}
                placeholder="Dr. Jane Smith" className={inputCls} />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-400 mb-2 uppercase tracking-wider">Clinical Email</label>
              <input id="reg-email" type="email" required value={form.email} onChange={set('email')}
                placeholder="doctor@hospital.com" className={inputCls} />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-400 mb-2 uppercase tracking-wider">Specialty</label>
              <select id="reg-specialty" value={form.specialty} onChange={set('specialty')}
                className={`${inputCls} cursor-pointer`}
              >
                <option value="" className="bg-[#161F30]">Select specialty (optional)</option>
                {SPECIALTIES.map(s => <option key={s} value={s} className="bg-[#161F30]">{s}</option>)}
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-400 mb-2 uppercase tracking-wider">Password</label>
              <div className="relative">
                <input id="reg-password" type={showPassword ? 'text' : 'password'} required value={form.password}
                  onChange={set('password')} placeholder="Min. 8 characters" className={`${inputCls} pr-11`} />
                <button type="button" onClick={() => setShowPassword(p => !p)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-500 hover:text-slate-300">
                  {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </div>
            </div>

            <button id="reg-submit" type="submit" disabled={loading}
              className="w-full flex items-center justify-center gap-2 py-3 rounded-xl font-semibold text-sm
                bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500
                text-white transition-all duration-200 shadow-lg shadow-cyan-500/20 mt-2
                disabled:opacity-50 disabled:cursor-not-allowed">
              {loading ? <><Loader2 size={16} className="animate-spin" />Creating account…</> : 'Create Workspace Account'}
            </button>
          </form>

          <p className="text-center text-sm text-slate-500 mt-5">
            Already registered?{' '}
            <button onClick={onSwitchToLogin} className="text-cyan-400 hover:text-cyan-300 font-semibold transition-colors">
              Sign in
            </button>
          </p>
        </div>
        <p className="text-center text-xs text-slate-600 mt-4">🔒 Doctor-only system · Enterprise Clinical AI</p>
      </div>
    </div>
  );
};

export default RegisterView;
