import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { format } from 'date-fns';
import { Calendar, Clock, Edit, Users, CheckCircle, XCircle, BarChart2, ChevronRight } from 'lucide-react';
import Navbar from './navbar.tsx';

interface Quiz {
  id: number;
  title: string;
  description: string;
  start_date: string;
  end_date: string;
  total_trainees: number;
  completed_attempts: number;
  week: number;
}

interface TraineeAttempt {
  username: string;
  score: number;
  completed_at: string;
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

const QuizzesPage: React.FC = () => {
  const [quizzes, setQuizzes] = useState<Quiz[]>([]);
  const [selectedQuiz, setSelectedQuiz] = useState<Quiz | null>(null);
  const [traineeAttempts, setTraineeAttempts] = useState<TraineeAttempt[]>([]);
  const [isEditMode, setIsEditMode] = useState(false);
  const [editedQuiz, setEditedQuiz] = useState<Quiz | null>(null);
  const [currentWeek, setCurrentWeek] = useState(1);
  const [totalWeeks, setTotalWeeks] = useState(1);

  useEffect(() => {
    fetchQuizzes();
    fetchProgramDetails();
  }, []);

  const fetchQuizzes = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch('http://127.0.0.1:8000/quizzes', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      if (response.ok) {
        const data = await response.json();
        setQuizzes(data);
      } else {
        console.error('Failed to fetch quizzes');
      }
    } catch (error) {
      console.error('Error fetching quizzes:', error);
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

  const fetchTraineeAttempts = async (quizId: number) => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`http://127.0.0.1:8000/quiz/${quizId}/attempts`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      if (response.ok) {
        const data = await response.json();
        setTraineeAttempts(data);
      } else {
        console.error('Failed to fetch trainee attempts');
      }
    } catch (error) {
      console.error('Error fetching trainee attempts:', error);
    }
  };

  const handleQuizClick = (quiz: Quiz) => {
    setSelectedQuiz(quiz);
    fetchTraineeAttempts(quiz.id);
    setIsEditMode(false);
  };

  const handleEditClick = (quiz: Quiz) => {
    setSelectedQuiz(quiz);
    setEditedQuiz({ ...quiz });
    setIsEditMode(true);
  };

  const handleSaveEdit = async () => {
    if (!editedQuiz) return;

    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`http://127.0.0.1:8000/quiz/${editedQuiz.id}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(editedQuiz),
      });

      if (response.ok) {
        const updatedQuiz = await response.json();
        setQuizzes(quizzes.map(q => q.id === updatedQuiz.id ? updatedQuiz : q));
        setSelectedQuiz(updatedQuiz);
        setIsEditMode(false);
      } else {
        console.error('Failed to update quiz');
      }
    } catch (error) {
      console.error('Error updating quiz:', error);
    }
  };

  const filteredQuizzes = quizzes.filter(quiz => quiz.week === currentWeek);

  return (
    <>
      <Navbar />
      <div className="min-h-screen bg-gradient-to-br from-[#ede9fe] to-[#f5f3ff] py-12 px-4 sm:px-6 lg:px-8 mt-16">
        <div className="max-w-7xl mx-auto">
          <div className="flex justify-between items-center mb-10">
            <h1 className="text-4xl font-extrabold text-[#8b5cf6]">Quizzes Dashboard</h1>
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
                Create New Quiz
              </button>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Quizzes List */}
            <div className="lg:col-span-1 space-y-6">
              {filteredQuizzes.map((quiz) => (
                <motion.div
                  key={quiz.id}
                  className={`
                    bg-white rounded-xl shadow-lg overflow-hidden 
                    transform transition-all duration-300 
                    hover:shadow-2xl hover:-translate-y-2
                    ${selectedQuiz?.id === quiz.id ? 'border-2 border-[#8b5cf6]' : ''}
                  `}
                  whileHover={{ scale: 1.02 }}
                  onClick={() => handleQuizClick(quiz)}
                >
                  <div className="p-6">
                    <div className="flex justify-between items-start mb-4">
                      <h2 className="text-xl font-bold text-[#8b5cf6]">{quiz.title}</h2>
                      <motion.button
                        whileHover={{ scale: 1.1 }}
                        onClick={(e) => {
                          e.stopPropagation();
                          handleEditClick(quiz);
                        }}
                        className="text-[#8b5cf6] hover:bg-[#ede9fe] p-2 rounded-full transition-colors"
                      >
                        <Edit className="w-5 h-5" />
                      </motion.button>
                    </div>
                    <p className="text-gray-600 mb-4 line-clamp-2">{quiz.description}</p>
                    
                    <div className="flex justify-between items-center">
                      <div className="flex items-center text-sm text-gray-500">
                        <Users className="w-4 h-4 mr-2 text-[#8b5cf6]" />
                        <span>{quiz.completed_attempts} / {quiz.total_trainees}</span>
                      </div>
                      <div className="text-sm font-semibold text-[#8b5cf6]">
                        {Math.round((quiz.completed_attempts / quiz.total_trainees) * 100)}% Complete
                      </div>
                    </div>
                    <ProgressBar completed={quiz.completed_attempts} total={quiz.total_trainees} />
                  </div>
                </motion.div>
              ))}
            </div>

            {/* Quiz Details and Attempts */}
            <div className="lg:col-span-2">
              <AnimatePresence>
                {selectedQuiz ? (
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
                          Edit Quiz
                        </h2>
                        <div className="space-y-6">
                          <input
                            type="text"
                            value={editedQuiz?.title || ''}
                            onChange={(e) => setEditedQuiz({ ...editedQuiz!, title: e.target.value })}
                            className="w-full p-3 border-2 border-[#ede9fe] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#8b5cf6]"
                            placeholder="Quiz Title"
                          />
                          <textarea
                            value={editedQuiz?.description || ''}
                            onChange={(e) => setEditedQuiz({ ...editedQuiz!, description: e.target.value })}
                            className="w-full p-3 border-2 border-[#ede9fe] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#8b5cf6]"
                            placeholder="Quiz Description"
                            rows={4}
                          />
                          <div className="grid grid-cols-2 gap-4">
                            <div>
                              <label className="block text-sm font-medium text-gray-700 mb-1">Start Date</label>
                              <input
                                type="datetime-local"
                                value={format(new Date(editedQuiz?.start_date || ''), "yyyy-MM-dd'T'HH:mm")}
                                onChange={(e) => setEditedQuiz({ ...editedQuiz!, start_date: e.target.value })}
                                className="w-full p-3 border-2 border-[#ede9fe] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#8b5cf6]"
                              />
                            </div>
                            <div>
                              <label className="block text-sm font-medium text-gray-700 mb-1">End Date</label>
                              <input
                                type="datetime-local"
                                value={format(new Date(editedQuiz?.end_date || ''), "yyyy-MM-dd'T'HH:mm")}
                                onChange={(e) => setEditedQuiz({ ...editedQuiz!, end_date: e.target.value })}
                                className="w-full p-3 border-2 border-[#ede9fe] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#8b5cf6]"
                              />
                            </div>
                          </div>
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
                            <h2 className="text-3xl font-bold text-[#8b5cf6]">{selectedQuiz.title}</h2>
                            <p className="text-gray-600 mt-2">{selectedQuiz.description}</p>
                          </div>
                          <motion.button
                            whileHover={{ scale: 1.1 }}
                            onClick={() => handleEditClick(selectedQuiz)}
                            className="text-[#8b5cf6] hover:bg-[#ede9fe] p-2 rounded-full transition-colors"
                          >
                            <Edit className="w-6 h-6" />
                          </motion.button>
                        </div>

                        <div className="grid md:grid-cols-2 gap-6 mb-8 bg-[#ede9fe]/50 p-6 rounded-xl">
                          <div className="flex items-center">
                            <Calendar className="w-6 h-6 mr-3 text-[#8b5cf6]" />
                            <div>
                              <div className="text-sm text-gray-600">Start Date</div>
                              <div className="font-semibold">{format(new Date(selectedQuiz.start_date), 'MMM d, yyyy HH:mm')}</div>
                            </div>
                          </div>
                          <div className="flex items-center">
                            <Clock className="w-6 h-6 mr-3 text-[#8b5cf6]" />
                            <div>
                              <div className="text-sm text-gray-600">End Date</div>
                              <div className="font-semibold">{format(new Date(selectedQuiz.end_date), 'MMM d, yyyy HH:mm')}</div>
                            </div>
                          </div>
                        </div>

                        <div className="grid md:grid-cols-2 gap-6 mb-8">
                          <div className="bg-[#ede9fe]/50 p-4 rounded-xl flex items-center">
                            <Users className="w-6 h-6 mr-3 text-[#8b5cf6]" />
                            <div>
                              <div className="text-sm text-gray-600">Trainees</div>
                              <div className="font-semibold">{selectedQuiz.completed_attempts} / {selectedQuiz.total_trainees} Completed</div>
                            </div>
                          </div>
                          <div className="bg-[#ede9fe]/50 p-4 rounded-xl flex items-center">
                            <BarChart2 className="w-6 h-6 mr-3 text-[#8b5cf6]" />
                            <div>
                              <div className="text-sm text-gray-600">Completion Rate</div>
                              <div className="font-semibold">
                                {Math.round((selectedQuiz.completed_attempts / selectedQuiz.total_trainees) * 100)}%
                              </div>
                            </div>
                          </div>
                        </div>

                        <h3 className="text-2xl font-semibold mb-4 text-[#8b5cf6] flex items-center">
                          <CheckCircle className="w-6 h-6 mr-3 text-[#8b5cf6]" />
                          Trainee Attempts
                        </h3>
                        <div className="overflow-x-auto">
                          <table className="min-w-full bg-white border border-gray-200 rounded-lg overflow-hidden shadow-sm">
                          <thead className="bg-[#ede9fe]">
                              <tr>
                                <th className="py-3 px-4 text-left text-sm font-bold text-[#8b5cf6]">Trainee</th>
                                <th className="py-3 px-4 text-left text-sm font-bold text-[#8b5cf6]">Score</th>
                                <th className="py-3 px-4 text-left text-sm font-bold text-[#8b5cf6]">Completed At</th>
                                <th className="py-3 px-4 text-left text-sm font-bold text-[#8b5cf6]">Status</th>
                              </tr>
                            </thead>
                            <tbody>
                              {traineeAttempts.map((attempt, index) => (
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
                                      {attempt.username.charAt(0).toUpperCase()}
                                    </div>
                                    {attempt.username}
                                  </td>
                                  <td className="py-3 px-4 text-sm text-gray-800">
                                    <span 
                                      className={`
                                        px-3 py-1 rounded-full text-xs font-semibold
                                        ${attempt.score >= 90 ? 'bg-green-100 text-green-800' : 
                                          attempt.score >= 70 ? 'bg-yellow-100 text-yellow-800' : 
                                          'bg-red-100 text-red-800'}
                                      `}
                                    >
                                      {attempt.score}%
                                    </span>
                                  </td>
                                  <td className="py-3 px-4 text-sm text-gray-800">
                                    {format(new Date(attempt.completed_at), 'MMM d, yyyy HH:mm')}
                                  </td>
                                  <td className="py-3 px-4 text-sm text-gray-800">
                                    {attempt.score >= 70 ? (
                                      <div className="flex items-center text-green-600">
                                        <CheckCircle className="w-4 h-4 mr-2" />
                                        Passed
                                      </div>
                                    ) : (
                                      <div className="flex items-center text-red-600">
                                        <XCircle className="w-4 h-4 mr-2" />
                                        Failed
                                      </div>
                                    )}
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
                      <p className="text-xl text-gray-600">Select a quiz to view details</p>
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

export default QuizzesPage;

