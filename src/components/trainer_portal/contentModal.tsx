import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, FileText, Calendar, Users, CheckCircle, MessageSquare } from 'lucide-react';

interface ContentModalProps {
  isOpen: boolean;
  onClose: () => void;
  content: any;
  type: 'quiz' | 'assignment' | 'content' | 'discussion';
}

const ContentModal: React.FC<ContentModalProps> = ({ isOpen, onClose, content, type }) => {
  if (!isOpen) return null;

  // Determine icon and color based on type
  const typeConfig = {
    'quiz': { 
      icon: <FileText className="text-purple-600" size={24} />,
      bgColor: 'bg-purple-50'
    },
    'assignment': { 
      icon: <CheckCircle className="text-purple-600" size={24} />,
      bgColor: 'bg-purple-50'
    },
    'content': { 
      icon: <FileText className="text-purple-600" size={24} />,
      bgColor: 'bg-purple-50'
    },
    'discussion': { 
      icon: <MessageSquare className="text-purple-600" size={24} />,
      bgColor: 'bg-purple-50'
    }
  };

  const { icon, bgColor } = typeConfig[type];

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50 p-4"
        onClick={onClose}
      >
        <motion.div
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          exit={{ scale: 0.9, opacity: 0 }}
          className={`${bgColor} rounded-2xl shadow-2xl border border-purple-100 w-full max-w-lg transform transition-all`}
          onClick={(e) => e.stopPropagation()}
        >
          <div className="p-6">
            <div className="flex justify-between items-center mb-4">
              <div className="flex items-center space-x-3">
                {icon}
                <h2 className="text-2xl font-bold text-gray-800">{content.title || content.description}</h2>
              </div>
              <button 
                onClick={onClose} 
                className="text-gray-500 hover:text-purple-600 transition-colors rounded-full hover:bg-purple-100 p-2"
              >
                <X size={24} />
              </button>
            </div>

            <div className="space-y-4 text-gray-700">
              {type === 'quiz' && (
                <>
                  <DetailRow 
                    icon={<FileText size={20} className="text-purple-500" />} 
                    label="Description" 
                    value={content.description} 
                  />
                  <DetailRow 
                    icon={<Calendar size={20} className="text-purple-500" />} 
                    label="Start Date" 
                    value={new Date(content.start_date).toLocaleString()} 
                  />
                  <DetailRow 
                    icon={<Calendar size={20} className="text-purple-500" />} 
                    label="End Date" 
                    value={new Date(content.end_date).toLocaleString()} 
                  />
                  <DetailRow 
                    icon={<Users size={20} className="text-purple-500" />} 
                    label="Total Trainees" 
                    value={content.total_trainees} 
                  />
                  <DetailRow 
                    icon={<CheckCircle size={20} className="text-purple-500" />} 
                    label="Completed Attempts" 
                    value={content.completed_attempts} 
                  />
                </>
              )}
              {type === 'assignment' && (
                <>
                  <DetailRow 
                    icon={<FileText size={20} className="text-purple-500" />} 
                    label="Description" 
                    value={content.description} 
                  />
                  <DetailRow 
                    icon={<Calendar size={20} className="text-purple-500" />} 
                    label="Due Date" 
                    value={new Date(content.due_date).toLocaleString()} 
                  />
                  <DetailRow 
                    icon={<Users size={20} className="text-purple-500" />} 
                    label="Total Trainees" 
                    value={content.total_trainees} 
                  />
                  <DetailRow 
                    icon={<CheckCircle size={20} className="text-purple-500" />} 
                    label="Submitted Count" 
                    value={content.submitted_count} 
                  />
                </>
              )}
              {type === 'content' && (
                <>
                  <DetailRow 
                    icon={<FileText size={20} className="text-purple-500" />} 
                    label="Description" 
                    value={content.description} 
                  />
                  <DetailRow 
                    icon={<FileText size={20} className="text-purple-500" />} 
                    label="Content Type" 
                    value={content.content_type} 
                  />
                  {content.file_path && (
                    <div className="flex items-center space-x-3 text-purple-600 hover:text-purple-800 transition-colors">
                      <FileText size={20} />
                      <a 
                        href={content.file_path} 
                        target="_blank" 
                        rel="noopener noreferrer" 
                        className="underline"
                      >
                        View File
                      </a>
                    </div>
                  )}
                </>
              )}
              {type === 'discussion' && (
                <>
                  <DetailRow 
                    icon={<MessageSquare size={20} className="text-purple-500" />} 
                    label="Description" 
                    value={content.description} 
                  />
                  <DetailRow 
                    icon={<Calendar size={20} className="text-purple-500" />} 
                    label="Created At" 
                    value={new Date(content.created_at).toLocaleString()} 
                  />
                  <DetailRow 
                    icon={<Users size={20} className="text-purple-500" />} 
                    label="Total Responses" 
                    value={content.total_responses} 
                  />
                </>
              )}
            </div>
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
};

// Utility component for consistent detail row rendering
const DetailRow = ({ icon, label, value }) => (
  <div className="flex items-center space-x-3 bg-white bg-opacity-70 p-3 rounded-lg shadow-sm">
    {icon}
    <div>
      <p className="text-xs text-gray-500 font-medium">{label}</p>
      <p className="text-sm text-gray-800">{value}</p>
    </div>
  </div>
);

export default ContentModal;

