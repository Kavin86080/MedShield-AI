import React, { useEffect, useState, useRef } from 'react';
import {
  Upload, Send, FileText, Loader2, AlertCircle, Bot,
  User, ChevronLeft, BarChart3, BookOpen, Shield,
  CheckCircle2, ClipboardList, Sparkles, File, X
} from 'lucide-react';
import { consultationAPI, ragAPI } from '../services/api';
import { Consultation, UploadedDocument, AIConversation, GeneratedReport } from '../types';

interface Props {
  consultationId: number;
  onBack: () => void;
}

type TabId = 'chat' | 'documents' | 'reports';

const ConfidenceBadge: React.FC<{ score?: number | null }> = ({ score }) => {
  if (score == null) return null;
  const pct = Math.round(score * 100);
  const color = pct >= 70 ? 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20'
    : pct >= 40 ? 'text-amber-400 bg-amber-500/10 border-amber-500/20'
    : 'text-red-400 bg-red-500/10 border-red-500/20';
  return (
    <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs border font-semibold ${color}`}>
      <BarChart3 size={9} /> {pct}% confidence
    </span>
  );
};

const EvidenceAccordion: React.FC<{ evidence?: any[]; citations?: any[] }> = ({ evidence, citations }) => {
  const [open, setOpen] = useState(false);
  const hasEvidence = (evidence && evidence.length > 0) || (citations && citations.length > 0);
  if (!hasEvidence) return null;

  return (
    <div className="mt-2">
      <button onClick={() => setOpen(p => !p)}
        className="flex items-center gap-1.5 text-xs text-slate-500 hover:text-slate-300 transition-colors">
        <BookOpen size={11} />
        {open ? 'Hide' : 'Show'} evidence & citations ({(evidence?.length ?? 0) + (citations?.length ?? 0)})
      </button>
      {open && (
        <div className="mt-2 space-y-1.5">
          {evidence?.slice(0, 3).map((ev, i) => (
            <div key={i} className="px-3 py-2 bg-cyan-600/5 border border-cyan-500/10 rounded-lg text-xs text-slate-400">
              <p className="font-semibold text-cyan-400 mb-0.5">Evidence {i + 1}</p>
              <p className="line-clamp-3">{typeof ev === 'string' ? ev : JSON.stringify(ev)}</p>
            </div>
          ))}
          {citations?.slice(0, 3).map((ct, i) => (
            <div key={i} className="px-3 py-2 bg-violet-600/5 border border-violet-500/10 rounded-lg text-xs text-slate-400">
              <p className="font-semibold text-violet-400 mb-0.5">Citation {i + 1}</p>
              <p className="line-clamp-2">{typeof ct === 'string' ? ct : JSON.stringify(ct)}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

const ConsultationDetailView: React.FC<Props> = ({ consultationId, onBack }) => {
  const [consultation, setConsultation] = useState<Consultation | null>(null);
  const [documents, setDocuments] = useState<UploadedDocument[]>([]);
  const [messages, setMessages] = useState<AIConversation[]>([]);
  const [reports, setReports] = useState<GeneratedReport[]>([]);
  const [activeTab, setActiveTab] = useState<TabId>('chat');
  const [question, setQuestion] = useState('');
  const [chatLoading, setChatLoading] = useState(false);
  const [uploadLoading, setUploadLoading] = useState(false);
  const [reportLoading, setReportLoading] = useState(false);
  const [pageLoading, setPageLoading] = useState(true);
  const [error, setError] = useState('');
  const [dragOver, setDragOver] = useState(false);
  const chatEndRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    Promise.all([
      consultationAPI.getDetails(consultationId),
      ragAPI.getDocuments(consultationId),
      ragAPI.getChatHistory(consultationId),
      ragAPI.getReports(consultationId),
    ])
      .then(([c, docs, chats, rpts]) => {
        setConsultation(c);
        setDocuments(docs);
        setMessages(chats);
        setReports(rpts);
      })
      .catch(() => setError('Failed to load consultation workspace.'))
      .finally(() => setPageLoading(false));
  }, [consultationId]);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, chatLoading]);

  const handleFileUpload = async (file: File) => {
    setUploadLoading(true);
    setError('');
    try {
      const doc = await ragAPI.uploadDocument(consultationId, file);
      setDocuments(p => [...p, doc]);
      setActiveTab('chat');
    } catch (err: any) {
      setError(err.response?.data?.detail ?? 'Failed to upload document.');
    } finally {
      setUploadLoading(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files[0];
    if (file) handleFileUpload(file);
  };

  const handleChat = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim() || chatLoading) return;
    const q = question.trim();
    setQuestion('');
    setChatLoading(true);
    setError('');
    try {
      const msg = await ragAPI.chat(consultationId, q);
      setMessages(p => [...p, msg]);
    } catch (err: any) {
      setError(err.response?.data?.detail ?? 'Failed to get AI response.');
    } finally {
      setChatLoading(false);
    }
  };

  const handleGenerateReport = async () => {
    setReportLoading(true);
    setError('');
    try {
      const report = await ragAPI.generateReport(consultationId, { report_type: 'clinical_summary' });
      setReports(p => [report, ...p]);
      setActiveTab('reports');
    } catch (err: any) {
      setError(err.response?.data?.detail ?? 'Failed to generate report.');
    } finally {
      setReportLoading(false);
    }
  };

  const tabs: { id: TabId; label: string; icon: React.ElementType; count?: number }[] = [
    { id: 'chat',      label: 'AI Chat',    icon: Bot,         count: messages.length },
    { id: 'documents', label: 'Documents',  icon: FileText,    count: documents.length },
    { id: 'reports',   label: 'Reports',    icon: ClipboardList, count: reports.length },
  ];

  if (pageLoading) return (
    <div className="flex items-center justify-center h-full gap-3 text-slate-500">
      <Loader2 size={22} className="animate-spin" />
      <span>Loading workspace…</span>
    </div>
  );

  return (
    <div className="flex flex-col h-full">
      {/* Workspace header */}
      <div className="flex items-center gap-4 px-5 py-3.5 border-b border-white/5 bg-[#161F30] flex-shrink-0">
        <button onClick={onBack} className="flex items-center gap-1.5 text-sm text-slate-400 hover:text-white transition-colors">
          <ChevronLeft size={16} />
          Back
        </button>
        <div className="w-px h-5 bg-white/10" />
        <div className="flex-1 min-w-0">
          <p className="text-sm font-bold text-white truncate">{consultation?.patient_name ?? '—'}</p>
          <p className="text-xs text-slate-500">{consultation?.patient_age} y/o · {consultation?.patient_gender}</p>
        </div>
        <div className="flex items-center gap-2 flex-shrink-0">
          <span className={`flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold border ${
            consultation?.status === 'active'
              ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
              : 'bg-slate-500/10 text-slate-400 border-slate-500/20'
          }`}>
            {consultation?.status === 'active' ? <Shield size={9} /> : <CheckCircle2 size={9} />}
            {consultation?.status ?? 'active'}
          </span>
          <button
            onClick={handleGenerateReport}
            disabled={reportLoading || documents.length === 0}
            className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-xl bg-gradient-to-r from-violet-600 to-purple-600
              hover:from-violet-500 hover:to-purple-500 text-white text-xs font-semibold transition-all
              disabled:opacity-40 disabled:cursor-not-allowed shadow-lg shadow-violet-500/20"
          >
            {reportLoading ? <Loader2 size={12} className="animate-spin" /> : <Sparkles size={12} />}
            Generate Report
          </button>
        </div>
      </div>

      {/* Error bar */}
      {error && (
        <div className="flex items-center gap-3 px-5 py-2 bg-red-500/10 border-b border-red-500/20 flex-shrink-0">
          <AlertCircle size={14} className="text-red-400 flex-shrink-0" />
          <p className="text-xs text-red-300 flex-1">{error}</p>
          <button onClick={() => setError('')}><X size={14} className="text-red-400" /></button>
        </div>
      )}

      {/* Tabs */}
      <div className="flex items-center gap-1 px-5 py-2 border-b border-white/5 bg-[#0B0F19] flex-shrink-0">
        {tabs.map(tab => {
          const Icon = tab.icon;
          return (
            <button key={tab.id} onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                activeTab === tab.id
                  ? 'bg-cyan-600/20 text-cyan-400 border border-cyan-500/20'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-white/5'
              }`}>
              <Icon size={13} />
              {tab.label}
              {(tab.count ?? 0) > 0 && (
                <span className="px-1.5 py-0.5 rounded-full bg-white/10 text-slate-400 text-[10px]">{tab.count}</span>
              )}
            </button>
          );
        })}
      </div>

      {/* Tab content */}
      <div className="flex-1 overflow-hidden">

        {/* ── AI CHAT TAB ── */}
        {activeTab === 'chat' && (
          <div className="flex flex-col h-full">
            {/* Messages */}
            <div className="flex-1 overflow-y-auto px-4 py-4 space-y-4">
              {messages.length === 0 && !chatLoading && (
                <div className="flex flex-col items-center justify-center h-full text-slate-500 gap-3">
                  <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-cyan-600/20 to-blue-600/20 border border-cyan-500/10 flex items-center justify-center">
                    <Bot size={28} className="text-cyan-500" />
                  </div>
                  <div className="text-center">
                    <p className="text-sm font-semibold text-slate-300">Clinical AI Assistant</p>
                    <p className="text-xs mt-1">
                      {documents.length === 0
                        ? 'Upload patient documents first, then ask clinical questions.'
                        : `${documents.length} document(s) loaded. Ask any clinical question.`}
                    </p>
                  </div>
                </div>
              )}

              {messages.map(msg => (
                <div key={msg.id} className="space-y-1.5">
                  {/* Doctor question */}
                  <div className="flex items-start gap-3 justify-end">
                    <div className="max-w-[75%] bg-gradient-to-br from-cyan-600/20 to-blue-600/20 border border-cyan-500/15 rounded-2xl rounded-tr-sm px-4 py-3">
                      <p className="text-sm text-slate-200">{msg.question}</p>
                    </div>
                    <div className="w-7 h-7 rounded-full bg-cyan-600/20 border border-cyan-500/20 flex items-center justify-center flex-shrink-0">
                      <User size={13} className="text-cyan-400" />
                    </div>
                  </div>

                  {/* AI answer */}
                  <div className="flex items-start gap-3">
                    <div className="w-7 h-7 rounded-full bg-violet-600/20 border border-violet-500/20 flex items-center justify-center flex-shrink-0">
                      <Bot size={13} className="text-violet-400" />
                    </div>
                    <div className="max-w-[80%] bg-[#161F30] border border-white/8 rounded-2xl rounded-tl-sm px-4 py-3">
                      <div className="flex items-center gap-2 mb-2">
                        <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider">Clinical AI</span>
                        <ConfidenceBadge score={msg.confidence_score} />
                      </div>
                      <p className="text-sm text-slate-200 whitespace-pre-wrap leading-relaxed">{msg.answer}</p>
                      <EvidenceAccordion evidence={msg.evidence} citations={msg.citations} />
                    </div>
                  </div>
                </div>
              ))}

              {chatLoading && (
                <div className="flex items-start gap-3">
                  <div className="w-7 h-7 rounded-full bg-violet-600/20 border border-violet-500/20 flex items-center justify-center">
                    <Bot size={13} className="text-violet-400" />
                  </div>
                  <div className="bg-[#161F30] border border-white/8 rounded-2xl rounded-tl-sm px-4 py-3">
                    <div className="flex items-center gap-2">
                      <Loader2 size={13} className="animate-spin text-violet-400" />
                      <span className="text-xs text-slate-500">Analyzing clinical data…</span>
                    </div>
                  </div>
                </div>
              )}
              <div ref={chatEndRef} />
            </div>

            {/* Input */}
            <form onSubmit={handleChat} className="flex items-end gap-3 px-4 py-3 border-t border-white/5 bg-[#0B0F19] flex-shrink-0">
              <textarea
                value={question}
                onChange={e => setQuestion(e.target.value)}
                onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleChat(e as any); } }}
                placeholder="Ask a clinical question… (Enter to send, Shift+Enter for new line)"
                rows={2}
                className="flex-1 px-4 py-2.5 bg-[#161F30] border border-white/10 rounded-xl text-sm text-white placeholder-slate-500
                  focus:outline-none focus:border-cyan-500/40 focus:ring-1 focus:ring-cyan-500/10 transition-all resize-none"
              />
              <button
                type="submit"
                disabled={!question.trim() || chatLoading}
                className="flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-600 to-blue-600
                  hover:from-cyan-500 hover:to-blue-500 text-white transition-all flex-shrink-0
                  disabled:opacity-40 disabled:cursor-not-allowed shadow-lg shadow-cyan-500/20"
              >
                <Send size={15} />
              </button>
            </form>
          </div>
        )}

        {/* ── DOCUMENTS TAB ── */}
        {activeTab === 'documents' && (
          <div className="h-full overflow-y-auto p-4 space-y-4">
            {/* Drop zone */}
            <div
              onDragOver={e => { e.preventDefault(); setDragOver(true); }}
              onDragLeave={() => setDragOver(false)}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
              className={`relative border-2 border-dashed rounded-2xl p-8 text-center cursor-pointer transition-all ${
                dragOver
                  ? 'border-cyan-500/60 bg-cyan-500/5'
                  : 'border-white/10 hover:border-white/20 hover:bg-white/2'
              }`}
            >
              <input
                ref={fileInputRef}
                type="file"
                className="hidden"
                onChange={e => { const f = e.target.files?.[0]; if (f) handleFileUpload(f); }}
                accept=".pdf,.docx,.xlsx,.png,.jpg,.jpeg,.tiff,.bmp"
              />
              {uploadLoading ? (
                <div className="flex flex-col items-center gap-3">
                  <Loader2 size={28} className="animate-spin text-cyan-400" />
                  <p className="text-sm text-slate-400">Processing and indexing document…</p>
                </div>
              ) : (
                <div className="flex flex-col items-center gap-3">
                  <div className="w-12 h-12 rounded-xl bg-white/5 flex items-center justify-center">
                    <Upload size={22} className="text-slate-400" />
                  </div>
                  <div>
                    <p className="text-sm font-semibold text-slate-300">Drop files here or click to upload</p>
                    <p className="text-xs text-slate-500 mt-1">PDF, DOCX, XLSX, PNG, JPG, TIFF supported</p>
                  </div>
                </div>
              )}
            </div>

            {/* Uploaded files list */}
            {documents.length > 0 ? (
              <div className="space-y-2">
                <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider px-1">
                  Uploaded Files ({documents.length})
                </p>
                {documents.map(doc => (
                  <div key={doc.id} className="flex items-center gap-3 px-4 py-3 bg-[#161F30] border border-white/5 rounded-xl">
                    <div className="w-9 h-9 rounded-lg bg-cyan-600/10 border border-cyan-500/15 flex items-center justify-center flex-shrink-0">
                      <File size={16} className="text-cyan-400" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-semibold text-white truncate">{doc.filename}</p>
                      <p className="text-xs text-slate-500 uppercase">{doc.file_type} · {new Date(doc.created_at).toLocaleDateString()}</p>
                    </div>
                    <CheckCircle2 size={15} className="text-emerald-400 flex-shrink-0" />
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-center text-sm text-slate-600 py-4">No files uploaded yet.</p>
            )}
          </div>
        )}

        {/* ── REPORTS TAB ── */}
        {activeTab === 'reports' && (
          <div className="h-full overflow-y-auto p-4 space-y-4">
            {reports.length === 0 ? (
              <div className="flex flex-col items-center justify-center py-20 text-slate-500 gap-3">
                <ClipboardList size={36} className="text-slate-700" />
                <div className="text-center">
                  <p className="text-sm font-semibold text-slate-400">No reports generated yet</p>
                  <p className="text-xs mt-1">Use "Generate Report" after uploading clinical documents.</p>
                </div>
              </div>
            ) : (
              reports.map(report => (
                <div key={report.id} className="bg-[#161F30] border border-white/5 rounded-2xl overflow-hidden">
                  <div className="flex items-center gap-3 px-4 py-3 border-b border-white/5">
                    <div className="w-8 h-8 rounded-lg bg-violet-600/15 border border-violet-500/15 flex items-center justify-center">
                      <Sparkles size={14} className="text-violet-400" />
                    </div>
                    <div className="flex-1">
                      <p className="text-sm font-semibold text-white capitalize">{report.report_type.replace('_', ' ')}</p>
                      <p className="text-xs text-slate-500">{new Date(report.created_at).toLocaleString()}</p>
                    </div>
                  </div>
                  <div className="px-4 py-4">
                    <pre className="text-sm text-slate-300 whitespace-pre-wrap leading-relaxed font-sans">{report.content}</pre>
                  </div>
                </div>
              ))
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default ConsultationDetailView;
