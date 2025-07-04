import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { format } from 'date-fns';
import { Calendar, Clock, Edit, Users, CheckCircle, XCircle, BarChart2, ChevronRight, FileText, Download, Video, Image, Link } from 'lucide-react';
import Navbar from './navbar.tsx';

interface Content {
  id: number;
  title: string;
  description: string;
  content_type: 'video' | 'image' | 'document' | 'url';
  created_at: string;
  total_trainees: number;
  viewed_count: number;
  url: string;
  file_path: string;
  week: number;
}

interface TraineeView {
  username: string;
  viewed_at: string;
}

const ProgressBar = ({ completed, total }: { completed: number, total: number }) => {
  const percentage = Math.round((completed / total) * 100);
  return (
    <div className="w-full bg-gray-200 rounded-full h-2.5 mt-2">
      <div 
        className="bg-[#8b5cf6] h-2.5 rounded-full" 
        style={{ width: `${percentage}%` }}
      ></div>
    </div>
  );
};

const ContentPage: React.FC = () => {
  const [contents, setContents] = useState<Content[]>([]);
  const [selectedContent, setSelectedContent] = useState<Content | null>(null);
  const [traineeViews, setTraineeViews] = useState<TraineeView[]>([]);
  const [isEditMode, setIsEditMode] = useState(false);
  const [editedContent, setEditedContent] = useState<Content | null>(null);
  const [file, setFile] = useState<File | null>(null);
  const [currentWeek, setCurrentWeek] = useState(1);
  const [totalWeeks, setTotalWeeks] = useState(1);

  useEffect(() => {
    fetchContents();
    fetchProgramDetails();
  }, []);

  const fetchContents = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch('http://127.0.0.1:8000/contents', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      if (response.ok) {
        const data = await response.json();
        setContents(data);
      } else {
        console.error('Failed to fetch contents');
      }
    } catch (error) {
      console.error('Error fetching contents:', error);
    }
  };

  const fetchProgramDetails = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch('http://127.0.0.1:8000/program_details', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      if (response.ok) {
        const data = await response.json();
        const startDate = new Date(data.start_date);
        const currentDate = new Date();
        const diffTime = Math.abs(currentDate.getTime() - startDate.getTime());
        const diffWeeks = Math.ceil(diffTime / (1000 * 60 * 60 * 24 * 7));
        setCurrentWeek(diffWeeks);
        setTotalWeeks(data.total_weeks || diffWeeks);
      } else {
        console.error('Failed to fetch program details');
      }
    } catch (error) {
      console.error('Error fetching program details:', error);
    }
  };

  const fetchTraineeViews = async (contentId: number) => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`http://127.0.0.1:8000/content/${contentId}/views`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      if (response.ok) {
        const data = await response.json();
        setTraineeViews(data);
      } else {
        console.error('Failed to fetch trainee views');
      }
    } catch (error) {
      console.error('Error fetching trainee views:', error);
    }
  };

  const handleContentClick = (content: Content) => {
    setSelectedContent(content);
    fetchTraineeViews(content.id);
    setIsEditMode(false);
  };

  const handleEditClick = (content: Content) => {
    setSelectedContent(content);
    setEditedContent({ ...content });
    setIsEditMode(true);
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setFile(event.target.files[0]);
    }
  };

  const handleSaveEdit = async () => {
    if (!editedContent) return;

    const formData = new FormData();
    formData.append('title', editedContent.title);
    formData.append('description', editedContent.description);
    formData.append('content_type', editedContent.content_type);
    formData.append('week', String(editedContent.week)); // Added week to formData
    if (editedContent.content_type === 'url') {
      formData.append('url', editedContent.url);
    }
    if (file) {
      formData.append('file', file);
    }

    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`http://127.0.0.1:8000/content/${editedContent.id}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        body: formData,
      });

      if (response.ok) {
        const updatedContent = await response.json();
        setContents(contents.map(c => c.id === updatedContent.id ? updatedContent : c));
        setSelectedContent(updatedContent);
        setIsEditMode(false);
        setFile(null);
      } else {
        console.error('Failed to update content');
      }
    } catch (error) {
      console.error('Error updating content:', error);
    }
  };

  const getContentTypeIcon = (type: string) => {
    switch (type) {
      case 'video':
        return <Video className="w-6 h-6" />;
      case 'image':
        return <Image className="w-6 h-6" />;
      case 'document':
        return <FileText className="w-6 h-6" />;
      case 'url':
        return <Link className="w-6 h-6" />;
      default:
        return <FileText className="w-6 h-6" />;
    }
  };

  const filteredContents = contents.filter(content => content.week === currentWeek);

  return (
    <>
      <Navbar />
      <div className="min-h-screen bg-gradient-to-br from-[#ede9fe] to-[#f5f3ff] py-12 px-4 sm:px-6 lg:px-8 mt-16">
        <div className="max-w-7xl mx-auto">
          <div className="flex justify-between items-center mb-10">
            <h1 className="text-4xl font-extrabold text-[#8b5cf6]">Content Dashboard</h1>
            <div className="flex items-center space-x-4">
              <select
                value={currentWeek}
                onChange={(e) => setCurrentWeek(Number(e.target.value))}
                className="bg-white border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[#8b5cf6]"
              >
                {Array.from({ length: totalWeeks }, (_, i) => i + 1).map((week) => (
                  <option key={week} value={week}>Week {week}</option>
                ))}
              </select>
              <button className="bg-[#8b5cf6] text-white px-4 py-2 rounded-lg hover:bg-opacity-90 transition-colors">
                Add New Content
              </button>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Content List */}
            <div className="lg:col-span-1 space-y-6">
              {filteredContents.map((content) => (
                <motion.div
                  key={content.id}
                  className={`
                    bg-white rounded-xl shadow-lg overflow-hidden 
                    transform transition-all duration-300 
                    hover:shadow-2xl hover:-translate-y-2
                    ${selectedContent?.id === content.id ? 'border-2 border-[#8b5cf6]' : ''}
                  `}
                  whileHover={{ scale: 1.02 }}
                  onClick={() => handleContentClick(content)}
                >
                  <div className="p-6">
                    <div className="flex justify-between items-start mb-4">
                      <h2 className="text-xl font-bold text-[#8b5cf6]">{content.title}</h2>
                      <motion.button
                        whileHover={{ scale: 1.1 }}
                        onClick={(e) => {
                          e.stopPropagation();
                          handleEditClick(content);
                        }}
                        className="text-[#8b5cf6] hover:bg-[#ede9fe] p-2 rounded-full transition-colors"
                      >
                        <Edit className="w-5 h-5" />
                      </motion.button>
                    </div>
                    <p className="text-gray-600 mb-4 line-clamp-2">{content.description}</p>
                    
                    <div className="flex justify-between items-center">
                      <div className="flex items-center text-sm text-gray-500">
                        <Users className="w-4 h-4 mr-2 text-[#8b5cf6]" />
                        <span>{content.viewed_count} / {content.total_trainees}</span>
                      </div>
                      <div className="text-sm font-semibold text-[#8b5cf6]">
                        {Math.round((content.viewed_count / content.total_trainees) * 100)}% Viewed
                      </div>
                    </div>
                    <ProgressBar completed={content.viewed_count} total={content.total_trainees} />
                  </div>
                </motion.div>
              ))}
            </div>

            {/* Content Details and Views */}
            <div className="lg:col-span-2">
              <AnimatePresence>
                {selectedContent ? (
                  <motion.div
                    initial={{ opacity: 0, x: 50 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: 50 }}
                    className="bg-white rounded-xl shadow-lg p-8"
                  >
                    {isEditMode ? (
                      <div>
                        <h2 className="text-3xl font-bold mb-6 text-[#8b5cf6] flex items-center">
                          <Edit className="w-8 h-8 mr-3 text-[#8b5cf6]" />
                          Edit Content
                        </h2>
                        <div className="space-y-6">
                          <div>
                            <label htmlFor="edit-title" className="block text-sm font-medium text-gray-700 mb-1">Title</label>
                            <input
                              type="text"
                              id="edit-title"
                              value={editedContent?.title || ''}
                              onChange={(e) => setEditedContent({ ...editedContent!, title: e.target.value })}
                              className="w-full p-3 border-2 border-[#ede9fe] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#8b5cf6]"
                            />
                          </div>
                          <div>
                            <label htmlFor="edit-description" className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                            <textarea
                              id="edit-description"
                              value={editedContent?.description || ''}
                              onChange={(e) => setEditedContent({ ...editedContent!, description: e.target.value })}
                              className="w-full p-3 border-2 border-[#ede9fe] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#8b5cf6]"
                              rows={4}
                            />
                          </div>
                          <div>
                            <label htmlFor="edit-content-type" className="block text-sm font-medium text-gray-700 mb-1">Content Type</label>
                            <select
                              id="edit-content-type"
                              value={editedContent?.content_type}
                              onChange={(e) => setEditedContent({ ...editedContent!, content_type: e.target.value as Content['content_type'] })}
                              className="w-full p-3 border-2 border-[#ede9fe] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#8b5cf6]"
                            >
                              <option value="video">Video</option>
                              <option value="image">Image</option>
                              <option value="document">Document</option>
                              <option value="url">URL</option>
                            </select>
                          </div>
                          {editedContent?.content_type === 'url' && (
                            <div>
                              <label htmlFor="edit-url" className="block text-sm font-medium text-gray-700 mb-1">URL</label>
                              <input
                                type="text"
                                id="edit-url"
                                value={editedContent?.url || ''}
                                onChange={(e) => setEditedContent({ ...editedContent!, url: e.target.value })}
                                className="w-full p-3 border-2 border-[#ede9fe] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#8b5cf6]"
                              />
                            </div>
                          )}
                          <div>
                            <label htmlFor="edit-file" className="block text-sm font-medium text-gray-700 mb-1">File</label>
                            <input
                              type="file"
                              id="edit-file"
                              onChange={handleFileChange}
                              className="w-full p-3 border-2 border-[#ede9fe] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#8b5cf6]"
                            />
                          </div>
                          {editedContent?.file_path && (
                            <div>
                              <label className="block text-sm font-medium text-gray-700 mb-1">Current File</label>
                              <p className="text-sm text-gray-500">{editedContent.file_path}</p>
                            </div>
                          )}
                          <div className="flex space-x-4">
                            <button
                              onClick={handleSaveEdit}
                              className="flex-1 bg-[#8b5cf6] text-white px-6 py-3 rounded-lg hover:bg-opacity-90 transition-colors"
                            >
                              Save Changes
                            </button>
                            <button
                              onClick={() => setIsEditMode(false)}
                              className="flex-1 bg-gray-200 text-gray-700 px-6 py-3 rounded-lg hover:bg-gray-300 transition-colors"
                            >
                              Cancel
                            </button>
                          </div>
                        </div>
                      </div>
                    ) : (
                      <div>
                        <div className="flex justify-between items-start mb-6">
                          <div>
                            <h2 className="text-3xl font-bold text-[#8b5cf6]">{selectedContent.title}</h2>
                            <p className="text-gray-600 mt-2">{selectedContent.description}</p>
                          </div>
                          <motion.button
                            whileHover={{ scale: 1.1 }}
                            onClick={() => handleEditClick(selectedContent)}
                            className="text-[#8b5cf6] hover:bg-[#ede9fe] p-2 rounded-full transition-colors"
                          >
                            <Edit className="w-6 h-6" />
                          </motion.button>
                        </div>

                        <div className="grid md:grid-cols-2 gap-6 mb-8 bg-[#ede9fe]/50 p-6 rounded-xl">
                          <div className="flex items-center">
                            <Calendar className="w-6 h-6 mr-3 text-[#8b5cf6]" />
                            <div>
                              <div className="text-sm text-gray-600">Created At</div>
                              <div className="font-semibold">{format(new Date(selectedContent.created_at), 'MMM d, yyyy HH:mm')}</div>
                            </div>
                          </div>
                          <div className="flex items-center">
                            <Users className="w-6 h-6 mr-3 text-[#8b5cf6]" />
                            <div>
                              <div className="text-sm text-gray-600">Views</div>
                              <div className="font-semibold">{selectedContent.viewed_count} / {selectedContent.total_trainees} Viewed</div>
                            </div>
                          </div>
                        </div>

                        <div className="mb-8">
                          <div className="bg-[#ede9fe]/50 p-4 rounded-xl flex items-center">
                            <BarChart2 className="w-6 h-6 mr-3 text-[#8b5cf6]" />
                            <div>
                              <div className="text-sm text-gray-600">View Rate</div>
                              <div className="font-semibold">
                                {Math.round((selectedContent.viewed_count / selectedContent.total_trainees) * 100)}%
                              </div>
                            </div>
                          </div>
                        </div>

                        <div className="mb-8">
                          <button className="bg-[#8b5cf6] text-white px-6 py-3 rounded-lg hover:bg-opacity-90 transition-colors">
                            {selectedContent.content_type === 'url' ? (
                              <a href={selectedContent.url} target="_blank" rel="noopener noreferrer" className="flex items-center">
                                <Link className="w-4 h-4 mr-2" />
                                View Content
                              </a>
                            ) : (
                              <a href={selectedContent.file_path} target="_blank" rel="noopener noreferrer" className="flex items-center">
                                <FileText className="w-4 h-4 mr-2" />
                                View File
                              </a>
                            )}
                          </button>
                        </div>

                        <h3 className="text-2xl font-semibold mb-4 text-[#8b5cf6] flex items-center">
                          <CheckCircle className="w-6 h-6 mr-3 text-[#8b5cf6]" />
                          Trainee Views
                        </h3>
                        <div className="overflow-x-auto">
                          <table className="min-w-full bg-white border border-gray-200 rounded-lg overflow-hidden shadow-sm">
                            <thead className="bg-[#ede9fe]">
                              <tr>
                                <th className="py-3 px-4 text-left text-sm font-bold text-[#8b5cf6]">Trainee</th>
                                <th className="py-3 px-4 text-left text-sm font-bold text-[#8b5cf6]">Viewed At</th>
                              </tr>
                            </thead>
                            <tbody>
                              {traineeViews.map((view, index) => (
                                <tr 
                                  key={index} 
                                  className={`
                                    ${index % 2 === 0 ? 'bg-gray-50' : 'bg-white'} 
                                    hover:bg-[#ede9fe]/50 
                                    transition-colors
                                  `}
                                >
                                  <td className="py-3 px-4 text-sm text-gray-800 flex items-center">
                                    <div className="w-8 h-8 bg-[#8b5cf6]/20 rounded-full flex items-center justify-center mr-3">
                                      {view.username.charAt(0).toUpperCase()}
                                    </div>
                                    {view.username}
                                  </td>
                                  <td className="py-3 px-4 text-sm text-gray-800">
                                    {format(new Date(view.viewed_at), 'MMM d, yyyy HH:mm')}
                                  </td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                      </div>
                    )}
                  </motion.div>
                ) : (
                  <div className="flex items-center justify-center h-full bg-white rounded-xl shadow-lg p-8">
                    <div className="text-center">
                      <BarChart2 className="w-16 h-16 mx-auto text-[#8b5cf6] mb-4" />
                      <p className="text-xl text-gray-600">Select a content item to view details</p>
                    </div>
                  </div>
                )}
              </AnimatePresence>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default ContentPage;

