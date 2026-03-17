import React, { useState } from 'react';
import Upload from './components/Upload';
import Dashboard from './components/Dashboard';
import { Cpu, Zap } from 'lucide-react';

function App() {
  const [meetingData, setMeetingData] = useState(null);

  return (
    <div className="min-h-screen bg-[#0f172a] text-slate-200 p-4 md:p-8 font-inter">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <header className="flex flex-col md:flex-row md:items-center justify-between mb-12 gap-4">
          <div>
            <h1 className="text-4xl font-extrabold text-white tracking-tight flex items-center">
              Meeting <span className="text-primary-400 mx-2">Agent</span>
              <Zap className="text-yellow-400 fill-yellow-400" />
            </h1>
            <p className="text-slate-400 mt-2">음성 회의록 분석 및 노션 업무 자동 할당 시스템</p>
          </div>
          <div className="flex items-center space-x-2 bg-slate-800/50 px-4 py-2 rounded-full border border-slate-700">
            <Cpu className="w-4 h-4 text-primary-400" />
            <span className="text-xs font-medium">GPT-4o mini & Whisper Hybrid Beta</span>
          </div>
        </header>

        {/* Main Content */}
        <main className="space-y-12">
          {!meetingData ? (
            <div className="animate-in fade-in duration-1000">
              <Upload onUploadSuccess={setMeetingData} />
              
              <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
                <FeatureCard 
                  title="로컬 STT 변환" 
                  description="faster-whisper를 사용해 유출 걱정 없이 로컬에서 고품질 전사를 수행합니다."
                />
                <FeatureCard 
                  title="AI 업무 추출" 
                  description="회의 맥락을 분석해 담당자, 마감일, 구체적 지시사항을 자동으로 분류합니다."
                />
                <FeatureCard 
                  title="노션 동기화" 
                  description="추출된 Action Item을 즉시 노션 칸반 보드에 생성하여 협업을 가속화합니다."
                />
              </div>
            </div>
          ) : (
            <div className="relative">
              <button 
                onClick={() => setMeetingData(null)}
                className="absolute -top-12 right-0 text-sm text-primary-400 hover:text-white transition-colors"
              >
                ← 다시 업로드하기
              </button>
              <Dashboard meetingData={meetingData} />
            </div>
          )}
        </main>

        {/* Footer */}
        <footer className="mt-20 pt-8 border-t border-slate-800 text-center text-slate-500 text-sm">
          &copy; 2024 AI Meeting Secretary Agent. All rights reserved.
        </footer>
      </div>
    </div>
  );
}

function FeatureCard({ title, description }) {
  return (
    <div className="p-6 rounded-2xl bg-slate-800/30 border border-slate-700/50 hover:bg-slate-800/50 transition-colors">
      <h3 className="text-white font-semibold mb-2">{title}</h3>
      <p className="text-slate-400 text-xs leading-relaxed">{description}</p>
    </div>
  );
}

export default App;
