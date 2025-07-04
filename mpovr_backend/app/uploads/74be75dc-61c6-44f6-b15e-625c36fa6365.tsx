import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { format } from 'date-fns';
import { Calendar, Clock, Edit, Users, CheckCircle, XCircle, BarChart2, ChevronRight, Video, Upload } from 'lucide-react';
import Navbar from './navbar.tsx';

interface VirtualSession {
  id: number;
  title: string;
  description: string;
  scheduled_datetime: string;
  duration_minutes: number;
  meeting_link: string;
  created_at: string;
  total_trainees: number;
  attended_count: number;
  recording_url?: string;
  week: number;
}

interface TraineeAttendance {
  username: string;
  joined_at: string;
  left_at: string;
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

const VirtualSessionPage: React.FC = () => {
  const [sessions, setSessions] = useState<VirtualSession[]>([]);
  const [selectedSession, setSelectedSession] = useState<VirtualSession | null>(null);
  const [traineeAttendance, setTraineeAttendance] = useState<TraineeAttendance[]>([]);
  const [isEditMode, setIsEditMode] = useState(false);
  const [editedSession, setEditedSession] = useState<VirtualSession | null>(null);
  const [recordingFile, setRecordingFile] = useState<File | null>(null);
  const [currentWeek, setCurrentWeek] = useState(1);
  const [totalWeeks, setTotalWeeks] = useState(1);

  useEffect(() => {
    fetchSessions();
    fetchProgramDetails();
  }, []);

  const fetchSessions = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch('http://127.0.0.1:8000/virtual_sessions', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      if (response.ok) {
        const data = await response.json();
        setSessions(data);
      } else {
        console.error('Failed to fetch virtual sessions');
      }
    } catch (error) {
      console.error('Error fetching virtual sessions:', error);
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

  const fetchTraineeAttendance = async (sessionId: number) => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`http://127.0.0.1:8000/virtual_session/${sessionId}/attendance`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      if (response.ok) {
        const data = await response.json();
        setTraineeAttendance(data);
      } else {
        console.error('Failed to fetch trainee attendance');
      }
    } catch (error) {
      console.error('Error fetching trainee attendance:', error);
    }
  };

  const handleSessionClick = (session: VirtualSession) => {
    setSelectedSession(session);
    fetchTraineeAttendance(session.id);
    setIsEditMode(false);
  };

  const handleEditClick = (session: VirtualSession) => {
    setSelectedSession(session);
    setEditedSession({ ...session });
    setIsEditMode(true);
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setRecordingFile(event.target.files[0]);
    }
  };

  const handleSaveEdit = async () => {
    if (!editedSession) return;

    const formData = new FormData();
    formData.append('title', editedSession.title);
    formData.append('description', editedSession.description);
    formData.append('scheduled_datetime', editedSession.scheduled_datetime);
    formData.append('duration_minutes', String(editedSession.duration_minutes));
    formData.append('week', String(editedSession.week));
    if (recordingFile) {
      formData.append('recording', recordingFile);
    }

    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`http://127.0.0.1:8000/virtual_session/${editedSession.id}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        body: formData,
      });

      if (response.ok) {
        const updatedSession = await response.json();
        setSessions(sessions.map(s => s.id === updatedSession.id ? updatedSession : s));
        setSelectedSession(updatedSession);
        setIsEditMode(false);
        setRecordingFile(null);
      } else {
        console.error('Failed to update virtual session');
      }
    } catch (error) {
      console.error('Error updating virtual session:', error);
    }
  };

  const filteredSessions = sessions.filter(session => session.week === currentWeek);

  return (
    <>
      <Navbar />
      <div className="min-h-screen bg-gradient-to-br from-[#ede9fe] to-[#f5f3ff] py-12 px-4 sm:px-6 lg:px-8 mt-16">
        <div className="max-w-7xl mx-auto">
          <div className="flex justify-between items-center mb-10">
            <h1 className="text-4xl font-extrabold text-[#8b5cf6]">Virtual Sessions Dashboard</h1>
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
                Schedule New Session
              </button>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Session List */}
            <div className="lg:col-span-1 space-y-6">
            {filteredSessions.map((session) => (
              <motion.div
                  key={session.id}
                  className={`
                  bg-white rounded-xl shadow-lg overflow-hidden 
                  transform transition-all duration-300 
                  hover:shadow-2xl hover:-translate-y-2
                  ${selectedSession?.id === session.id ? 'border-2 border-[#8b5cf6]' : 'border-2 border-transparent'}
                  `}
                  whileHover={{ scale: 1.02 }}
                  onClick={() => handleSessionClick(session)}
              >
                  <div className="p-6">
                  <div className="flex justify-between items-start mb-4">
                      <h2 className="text-xl font-bold text-[#8b5cf6]">{session.title}</h2>
                      <motion.button
                      whileHover={{ scale: 1.1 }}
                      onClick={(e) => {
                          e.stopPropagation();
                          handleEditClick(session);
                      }}
                      className="text-[#8b5cf6] hover:bg-[#ede9fe] p-2 rounded-full transition-colors"
                      >
                      <Edit className="w-5 h-5" />
                      </motion.button>
                  </div>
                  <p className="text-gray-600 mb-4 line-clamp-2">{session.description}</p>
                  
                  <div className="flex justify-between items-center">
                      <div className="flex items-center text-sm text-gray-500">
                      <Users className="w-4 h-4 mr-2 text-[#8b5cf6]" />
                      <span>{session.attended_count} / {session.total_trainees}</span>
                      </div>
                      <div className="text-sm font-semibold text-[#8b5cf6]">
                      {Math.round((session.attended_count / session.total_trainees) * 100)}% Attended
                      </div>
                  </div>
                  <ProgressBar completed={session.attended_count} total={session.total_trainees} />
                  </div>
              </motion.div>
              ))}
            </div>

            {/* Session Details and Attendance */}
            <div className="lg:col-span-2">
              <AnimatePresence>
                {selectedSession ? (
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
                          Edit Virtual Session
                        </h2>
                        <div className="space-y-6">
                          <div>
                            <label htmlFor="edit-title" className="block text-sm font-medium text-gray-700 mb-1">Title</label>
                            <input
                              type="text"
                              id="edit-title"
                              value={editedSession?.title || ''}
                              onChange={(e) => setEditedSession({ ...editedSession!, title: e.target.value })}
                              className="w-full p-3 border-2 border-[#ede9fe] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#8b5cf6]"
                            />
                          </div>
                          <div>
                            <label htmlFor="edit-description" className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                            <textarea
                              id="edit-description"
                              value={editedSession?.description || ''}
                              onChange={(e) => setEditedSession({ ...editedSession!, description: e.target.value })}
                              className="w-full p-3 border-2 border-[#ede9fe] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#8b5cf6]"
                              rows={4}
                            />
                          </div>
                          <div>
                            <label htmlFor="edit-datetime" className="block text-sm font-medium text-gray-700 mb-1">Date and Time</label>
                            <input
                              type="datetime-local"
                              id="edit-datetime"
                              value={editedSession?.scheduled_datetime.slice(0, 16) || ''}
                              onChange={(e) => setEditedSession({ ...editedSession!, scheduled_datetime: e.target.value })}
                              className="w-full p-3 border-2 border-[#ede9fe] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#8b5cf6]"
                            />
                          </div>
                          <div>
                            <label htmlFor="edit-duration" className="block text-sm font-medium text-gray-700 mb-1">Duration (minutes)</label>
                            <input
                              type="number"
                              id="edit-duration"
                              value={editedSession?.duration_minutes || ''}
                              onChange={(e) => setEditedSession({ ...editedSession!, duration_minutes: parseInt(e.target.value) })}
                              className="w-full p-3 border-2 border-[#ede9fe] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#8b5cf6]"
                            />
                          </div>
                          <div>
                            <label htmlFor="edit-recording" className="block text-sm font-medium text-gray-700 mb-1">Upload Recording</label>
                            <input
                              type="file"
                              id="edit-recording"
                              onChange={handleFileChange}
                              accept="video/*"
                              className="w-full p-3 border-2 border-[#ede9fe] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#8b5cf6]"
                            />
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
                            <h2 className="text-3xl font-bold text-[#8b5cf6]">{selectedSession.title}</h2>
                            <p className="text-gray-600 mt-2">{selectedSession.description}</p>
                          </div>
                          <motion.button
                            whileHover={{ scale: 1.1 }}
                            onClick={() => handleEditClick(selectedSession)}
                            className="text-[#8b5cf6] hover:bg-[#ede9fe] p-2 rounded-full transition-colors"
                          >
                            <Edit className="w-6 h-6" />
                          </motion.button>
                        </div>

                        <div className="grid md:grid-cols-2 gap-6 mb-8 bg-[#ede9fe]/50 p-6 rounded-xl">
                          <div className="flex items-center">
                            <Calendar className="w-6 h-6 mr-3 text-[#8b5cf6]" />
                            <div>
                              <div className="text-sm text-gray-600">Scheduled Date</div>
                              <div className="font-semibold">{format(new Date(selectedSession.scheduled_datetime), 'MMM d, yyyy')}</div>
                            </div>
                          </div>
                          <div className="flex items-center">
                            <Clock className="w-6 h-6 mr-3 text-[#8b5cf6]" />
                            <div>
                              <div className="text-sm text-gray-600">Scheduled Time</div>
                              <div className="font-semibold">{format(new Date(selectedSession.scheduled_datetime), 'HH:mm')}</div>
                            </div>
                          </div>
                          <div className="flex items-center">
                            <Users className="w-6 h-6 mr-3 text-[#8b5cf6]" />
                            <div>
                              <div className="text-sm text-gray-600">Attendance</div>
                              <div className="font-semibold">{selectedSession.attended_count} / {selectedSession.total_trainees} Attended</div>
                            </div>
                          </div>
                          <div className="flex items-center">
                            <Video className="w-6 h-6 mr-3 text-[#8b5cf6]" />
                            <div>
                              <div className="text-sm text-gray-600">Duration</div>
                              <div className="font-semibold">{selectedSession.duration_minutes} minutes</div>
                            </div>
                          </div>
                        </div>

                        <div className="mb-8">
                          <div className="bg-[#ede9fe]/50 p-4 rounded-xl flex items-center">
                            <BarChart2 className="w-6 h-6 mr-3 text-[#8b5cf6]" />
                            <div>
                              <div className="text-sm text-gray-600">Attendance Rate</div>
                              <div className="font-semibold">
                                {Math.round((selectedSession.attended_count / selectedSession.total_trainees) * 100)}%
                              </div>
                            </div>
                          </div>
                        </div>

                        <div className="mb-8 space-y-4">
                        <button
                          className="w-full bg-[#8b5cf6] text-white px-6 py-3 rounded-lg hover:bg-opacity-90 transition-colors flex items-center justify-center"
                          onClick={(e) => {
                              e.stopPropagation();
                              window.open(selectedSession.meeting_link, '_blank');
                          }}
                          >                          
                          <Video className="w-4 h-4 mr-2" />
                            Join Virtual Session
                          </button>
                          {selectedSession.recording_url && (
                            <button className="w-full bg-white border-2 border-[#8b5cf6] text-[#8b5cf6] px-6 py-3 rounded-lg hover:bg-[#ede9fe] transition-colors flex items-center justify-center">
                              <Video className="w-4 h-4 mr-2" />
                              View Recording
                            </button>
                          )}
                        </div>

                        <h3 className="text-2xl font-semibold mb-4 text-[#8b5cf6] flex items-center">
                          <CheckCircle className="w-6 h-6 mr-3 text-[#8b5cf6]" />
                          Trainee Attendance
                        </h3>
                        <div className="overflow-x-auto">
                          <table className="min-w-full bg-white border border-gray-200 rounded-lg overflow-hidden shadow-sm">
                            <thead className="bg-[#ede9fe]">
                              <tr>
                                <th className="py-3 px-4 text-left text-sm font-bold text-[#8b5cf6]">Trainee</th>
                                <th className="py-3 px-4 text-left text-sm font-bold text-[#8b5cf6]">Joined At</th>
                                <th className="py-3 px-4 text-left text-sm font-bold text-[#8b5cf6]">Left At</th>
                                <th className="py-3 px-4 text-left text-sm font-bold text-[#8b5cf6]">Duration</th>
                              </tr>
                            </thead>
                            <tbody>
                              {traineeAttendance.map((attendance, index) => (
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
                                      {attendance.username.charAt(0).toUpperCase()}
                                    </div>
                                    {attendance.username}
                                  </td>
                                  <td className="py-3 px-4 text-sm text-gray-800">
                                    {format(new Date(attendance.joined_at), 'HH:mm:ss')}
                                  </td>
                                  <td className="py-3 px-4 text-sm text-gray-800">
                                    {attendance.left_at ? format(new Date(attendance.left_at), 'HH:mm:ss') : 'N/A'}
                                  </td>
                                  <td className="py-3 px-4 text-sm text-gray-800">
                                    {attendance.left_at 
                                      ? `${Math.round((new Date(attendance.left_at).getTime() - new Date(attendance.joined_at).getTime()) / 60000)} min`
                                      : 'N/A'
                                    }
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
                      <Video className="w-16 h-16 mx-auto text-[#8b5cf6] mb-4" />
                      <p className="text-xl text-gray-600">Select a virtual session to view details</p>
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

export default VirtualSessionPage;

