import React from 'react';
import { CheckCircle, User, Calendar, ExternalLink } from 'lucide-react';

const Dashboard = ({ meetingData }) => {
  if (!meetingData) return null;

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <div className="glass-morphism p-6">
        <h2 className="text-2xl font-bold text-white mb-4 flex items-center">
          <span className="w-2 h-8 premium-gradient rounded-full mr-3"></span>
          회의록 원문
        </h2>
        <div className="bg-slate-900/50 rounded-lg p-4 max-h-60 overflow-y-auto border border-slate-700">
          <p className="text-slate-300 leading-relaxed whitespace-pre-wrap">
            {meetingData.raw_text}
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {meetingData.tasks.map((task, index) => (
          <div key={index} className="glass-morphism p-6 hover:scale-[1.02] transition-transform duration-300 border-l-4 border-l-primary-500">
            <div className="flex justify-between items-start mb-4">
              <h3 className="text-lg font-bold text-white">{task.title}</h3>
              <CheckCircle className="text-green-400 w-5 h-5" />
            </div>
            
            <p className="text-slate-400 text-sm mb-4">
              {task.content}
            </p>

            <div className="flex flex-wrap gap-4 mt-auto">
              <div className="flex items-center text-xs text-slate-300 bg-slate-800 px-2 py-1 rounded">
                <User className="w-3 h-3 mr-1" />
                {task.assignee}
              </div>
              <div className="flex items-center text-xs text-slate-300 bg-slate-800 px-2 py-1 rounded">
                <Calendar className="w-3 h-3 mr-1" />
                {task.deadline}
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="flex justify-center">
        <button 
          onClick={() => window.open(`https://www.notion.so`, '_blank')}
          className="flex items-center px-6 py-3 rounded-full premium-gradient text-white font-bold hover:shadow-[0_0_20px_rgba(168,85,247,0.5)] transition-all duration-300"
        >
          Notion에서 확인하기 <ExternalLink className="ml-2 w-4 h-4" />
        </button>
      </div>
    </div>
  );
};

export default Dashboard;
