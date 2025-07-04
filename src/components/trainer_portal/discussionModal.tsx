import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Plus, Save } from 'lucide-react';
import { enqueueSnackbar } from 'notistack';

interface DiscussionModalProps {
  isOpen: boolean;
  onClose: () => void;
  initialDiscussionTitle: string;
  currentWeek: number;
}

export const DiscussionModal: React.FC<DiscussionModalProps> = ({ isOpen, onClose, initialDiscussionTitle, currentWeek }) => {
  const [discussionTitle, setDiscussionTitle] = useState(initialDiscussionTitle);
  const [discussionDescription, setDiscussionDescription] = useState('');
  const [weekNumber, setWeekNumber] = useState(currentWeek);
  const [file, setFile] = useState<File | null>(null);

  useEffect(() => {
    setDiscussionTitle(initialDiscussionTitle);
    setWeekNumber(currentWeek);
  }, [initialDiscussionTitle, currentWeek]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('title', discussionTitle);
    formData.append('description', discussionDescription);
    formData.append('week', weekNumber.toString());
    if (file) {
      formData.append('uploaded_file', file);
    }

    try {
      const response = await fetch('http://127.0.0.1:8000/discussions/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: formData
      });

      if (response.ok) {
        const result = await response.json();
        console.log('Discussion created successfully:', result);
        enqueueSnackbar('Discussion created successfully', { variant: 'success' });
        setDiscussionTitle('');
        setDiscussionDescription('');
        setFile(null);
        onClose();
      } else {
        const errorData = await response.json();
        console.error('Failed to create discussion:', errorData);
        enqueueSnackbar(`Failed to create discussion: ${errorData.detail}`, { variant: 'error' });
      }
    } catch (error) {
      console.error('Error creating discussion:', error);
      enqueueSnackbar('Error creating discussion', { variant: 'error' });
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 bg-purple-600 bg-opacity-50 backdrop-blur-sm flex items-center justify-center z-50 p-4"
        >
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.9, opacity: 0 }}
            className="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-4xl max-h-[90vh] overflow-y-auto scrollbar-hide"
            style={{
              backgroundImage: 'linear-gradient(to bottom right, #ede9fe, white)',
              boxShadow: '0 25px 50px -12px rgba(139, 92, 246, 0.25)'
            }}
          >
            <div className="flex justify-between items-center mb-8">
              <h2 className="text-3xl font-extrabold text-purple-600 tracking-tight">Create a New Discussion</h2>
              <button 
                onClick={onClose} 
                className="text-purple-500 hover:text-purple-700 transition-all duration-300 hover:rotate-90"
              >
                <X className="w-8 h-8" strokeWidth={2.5} />
              </button>
            </div>
            <form onSubmit={handleSubmit} className="space-y-8">
              <div>
                <label htmlFor="discussionTitle" className="block text-sm font-medium text-purple-700 mb-2">
                  Discussion Title
                </label>
                <input
                  type="text"
                  id="discussionTitle"
                  value={discussionTitle}
                  onChange={(e) => setDiscussionTitle(e.target.value)}
                  className="w-full px-4 py-3 border-2 border-purple-200 rounded-xl focus:ring-4 focus:ring-purple-300 focus:border-purple-500 transition-all duration-300 bg-purple-50 text-purple-900"
                  required
                />
              </div>
              <div>
                <label htmlFor="discussionDescription" className="block text-sm font-medium text-purple-700 mb-2">
                  Discussion Description
                </label>
                <textarea
                  id="discussionDescription"
                  value={discussionDescription}
                  onChange={(e) => setDiscussionDescription(e.target.value)}
                  className="w-full px-4 py-3 border-2 border-purple-200 rounded-xl focus:ring-4 focus:ring-purple-300 focus:border-purple-500 transition-all duration-300 bg-purple-50 text-purple-900"
                  rows={5}
                  required
                />
              </div>
              <div>
                <label htmlFor="weekNumber" className="block text-sm font-medium text-purple-700 mb-2">
                  Week Number
                </label>
                <input
                  type="number"
                  id="weekNumber"
                  value={weekNumber}
                  onChange={(e) => setWeekNumber(Number(e.target.value))}
                  min={1}
                  max={currentWeek}
                  className="w-full px-4 py-3 border-2 border-purple-200 rounded-xl focus:ring-4 focus:ring-purple-300 focus:border-purple-500 transition-all duration-300 bg-purple-50 text-purple-900"
                  required
                />
              </div>
              <div>
                <label htmlFor="file" className="block text-sm font-medium text-purple-700 mb-2">
                  Upload File (optional)
                </label>
                <input
                  type="file"
                  id="file"
                  onChange={handleFileChange}
                  className="w-full px-4 py-3 border-2 border-purple-200 rounded-xl focus:ring-4 focus:ring-purple-300 focus:border-purple-500 transition-all duration-300 bg-purple-50 text-purple-900"
                />
              </div>
              <button
                type="submit"
                className="w-full flex items-center justify-center px-6 py-3 border border-transparent text-base font-medium rounded-xl text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-4 focus:ring-purple-300 transition-all duration-300"
              >
                <Save className="w-5 h-5 mr-2" />
                Create Discussion
              </button>
            </form>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

