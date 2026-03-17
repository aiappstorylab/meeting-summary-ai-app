import React, { useState } from 'react';
import { Upload as UploadIcon, Loader2 } from 'lucide-react';
import axios from 'axios';

const Upload = ({ onUploadSuccess }) => {
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState('');

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    setLoading(true);
    setStatus('음성을 텍스트로 변환하고 업무를 추출하는 중입니다...');

    try {
      const response = await axios.post('http://localhost:8000/upload', formData);
      onUploadSuccess(response.data);
      setStatus('처리 완료!');
    } catch (error) {
      console.error('Upload failed:', error);
      setStatus('처리에 실패했습니다. 서버 상태와 API 키를 확인해 주세요.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center p-12 glass-morphism border-dashed border-2 border-primary-500/50 hover:border-primary-500 transition-all duration-300">
      {!loading ? (
        <label className="cursor-pointer flex flex-col items-center">
          <UploadIcon className="w-16 h-16 text-primary-400 mb-4 animate-bounce" />
          <span className="text-xl font-semibold text-white mb-2">회의 음성 파일 업로드</span>
          <span className="text-sm text-slate-400">mp3, wav 파일을 선택하세요</span>
          <input type="file" className="hidden" accept="audio/*" onChange={handleFileChange} />
        </label>
      ) : (
        <div className="flex flex-col items-center">
          <Loader2 className="w-16 h-16 text-primary-400 mb-4 animate-spin" />
          <span className="text-lg font-medium text-white">{status}</span>
        </div>
      )}
    </div>
  );
};

export default Upload;
