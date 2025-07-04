import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { format } from 'date-fns';
import { Calendar, Clock, Edit, Users, CheckCircle, XCircle, BarChart2, ChevronRight, FileText, Download } from 'lucide-react';
import Navbar from './navbar.tsx';

interface Assignment {
  id: number;
  title: string;
  description: string;
  due_date: string;
  total_trainees: number;
  submitted_count: number;
  week: number;
}

interface TraineeSubmission {
  username: string;
  submitted_at: string;
  file_path: string;
  grade: number | null;
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

const AssignmentsPage: React.FC = () => {
  const [assignments, setAssignments] = useState<Assignment[]>([]);
  const [selectedAssignment, setSelectedAssignment] = useState<Assignment | null>(null);
  const [traineeSubmissions, setTraineeSubmissions] = useState<TraineeSubmission[]>([]);
  const [isEditMode, setIsEditMode] = useState(false);
  const [editedAssignment, setEditedAssignment] = useState<Assignment | null>(null);
  const [currentWeek, setCurrentWeek] = useState(1);
  const [totalWeeks, setTotalWeeks] = useState(1);

  useEffect(() => {
    fetchAssignments();
    fetchProgramDetails();
  }, []);

  const fetchAssignments = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch('http://127.0.0.1:8000/assignments', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      if (response.ok) {
        const data = await response.json();
        setAssignments(data);
      } else {
        console.error('Failed to fetch assignments');
      }
    } catch (error) {
      console.error('Error fetching assignments:', error);
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

  const fetchTraineeSubmissions = async (assignmentId: number) => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`http://127.0.0.1:8000/assignment/${assignmentId}/submissions`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      if (response.ok) {
        const data = await response.json();
        setTraineeSubmissions(data);
      } else {
        console.error('Failed to fetch trainee submissions');
      }
    } catch (error) {
      console.error('Error fetching trainee submissions:', error);
    }
  };

  const handleAssignmentClick = (assignment: Assignment) => {
    setSelectedAssignment(assignment);
    fetchTraineeSubmissions(assignment.id);
    setIsEditMode(false);
  };

  const handleEditClick = (assignment: Assignment) => {
    setSelectedAssignment(assignment);
    setEditedAssignment({ ...assignment });
    setIsEditMode(true);
  };

  const handleSaveEdit = async () => {
    if (!editedAssignment) return;

    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`http://127.0.0.1:8000/assignment/${editedAssignment.id}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(editedAssignment),
      });

      if (response.ok) {
        const updatedAssignment = await response.json();
        setAssignments(assignments.map(a => a.id === updatedAssignment.id ? updatedAssignment : a));
        setSelectedAssignment(updatedAssignment);
        setIsEditMode(false);
      } else {
        console.error('Failed to update assignment');
      }
    } catch (error) {
      console.error('Error updating assignment:', error);
    }
  };

  const filteredAssignments = assignments.filter(assignment => assignment.week === currentWeek);

  return (
    <>
      <Navbar />
      <div className="min-h-screen bg-gradient-to-br from-[#ede9fe] to-[#f5f3ff] py-12 px-4 sm:px-6 lg:px-8 mt-16">
        <div className="max-w-7xl mx-auto">
          <div className="flex justify-between items-center mb-10">
            <h1 className="text-4xl font-extrabold text-[#8b5cf6]">Assignments Dashboard</h1>
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
                Create New Assignment
              </button>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Assignments List */}
            <div className="lg:col-span-1 space-y-6">
              {filteredAssignments.map((assignment) => (
                <motion.div
                  key={assignment.id}
                  className={`
                    bg-white rounded-xl shadow-lg overflow-hidden 
                    transform transition-all duration-300 
                    hover:shadow-2xl hover:-translate-y-2
                    ${selectedAssignment?.id === assignment.id ? 'border-2 border-[#8b5cf6]' : ''}
                  `}
                  whileHover={{ scale: 1.02 }}
                  onClick={() => handleAssignmentClick(assignment)}
                >
                  <div className="p-6">
                    <div className="flex justify-between items-start mb-4">
                      <h2 className="text-xl font-bold text-[#8b5cf6]">{assignment.title}</h2>
                      <motion.button
                        whileHover={{ scale: 1.1 }}
                        onClick={(e) => {
                          e.stopPropagation();
                          handleEditClick(assignment);
                        }}
                        className="text-[#8b5cf6] hover:bg-[#ede9fe] p-2 rounded-full transition-colors"
                      >
                        <Edit className="w-5 h-5" />
                      </motion.button>
                    </div>
                    <p className="text-gray-600 mb-4 line-clamp-2">{assignment.description}</p>
                    
                    <div className="flex justify-between items-center">
                      <div className="flex items-center text-sm text-gray-500">
                        <Users className="w-4 h-4 mr-2 text-[#8b5cf6]" />
                        <span>{assignment.submitted_count} / {assignment.total_trainees}</span>
                      </div>
                      <div className="text-sm font-semibold text-[#8b5cf6]">
                        {Math.round((assignment.submitted_count / assignment.total_trainees) * 100)}% Submitted
                      </div>
                    </div>
                    <ProgressBar completed={assignment.submitted_count} total={assignment.total_trainees} />
                  </div>
                </motion.div>
              ))}
            </div>

            {/* Assignment Details and Submissions */}
            <div className="lg:col-span-2">
              <AnimatePresence>
                {selectedAssignment ? (
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
                          Edit Assignment
                        </h2>
                        <div className="space-y-6">
                          <input
                            type="text"
                            value={editedAssignment?.title || ''}
                            onChange={(e) => setEditedAssignment({ ...editedAssignment!, title: e.target.value })}
                            className="w-full p-3 border-2 border-[#ede9fe] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#8b5cf6]"
                            placeholder="Assignment Title"
                          />
                          <textarea
                            value={editedAssignment?.description || ''}
                            onChange={(e) => setEditedAssignment({ ...editedAssignment!, description: e.target.value })}
                            className="w-full p-3 border-2 border-[#ede9fe] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#8b5cf6]"
                            placeholder="Assignment Description"
                            rows={4}
                          />
                          <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">Due Date</label>
                            <input
                              type="datetime-local"
                              value={format(new Date(editedAssignment?.due_date || ''), "yyyy-MM-dd'T'HH:mm")}
                              onChange={(e) => setEditedAssignment({ ...editedAssignment!, due_date: e.target.value })}
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
                            <h2 className="text-3xl font-bold text-[#8b5cf6]">{selectedAssignment.title}</h2>
                            <p className="text-gray-600 mt-2">{selectedAssignment.description}</p>
                          </div>
                          <motion.button
                            whileHover={{ scale: 1.1 }}
                            onClick={() => handleEditClick(selectedAssignment)}
                            className="text-[#8b5cf6] hover:bg-[#ede9fe] p-2 rounded-full transition-colors"
                          >
                            <Edit className="w-6 h-6" />
                          </motion.button>
                        </div>

                        <div className="grid md:grid-cols-2 gap-6 mb-8 bg-[#ede9fe]/50 p-6 rounded-xl">
                          <div className="flex items-center">
                            <Calendar className="w-6 h-6 mr-3 text-[#8b5cf6]" />
                            <div>
                              <div className="text-sm text-gray-600">Due Date</div>
                              <div className="font-semibold">{format(new Date(selectedAssignment.due_date), 'MMM d, yyyy HH:mm')}</div>
                            </div>
                          </div>
                          <div className="flex items-center">
                            <Users className="w-6 h-6 mr-3 text-[#8b5cf6]" />
                            <div>
                              <div className="text-sm text-gray-600">Submissions</div>
                              <div className="font-semibold">{selectedAssignment.submitted_count} / {selectedAssignment.total_trainees} Submitted</div>
                            </div>
                          </div>
                        </div>

                        <div className="mb-8">
                          <div className="bg-[#ede9fe]/50 p-4 rounded-xl flex items-center">
                            <BarChart2 className="w-6 h-6 mr-3 text-[#8b5cf6]" />
                            <div>
                              <div className="text-sm text-gray-600">Submission Rate</div>
                              <div className="font-semibold">
                                {Math.round((selectedAssignment.submitted_count / selectedAssignment.total_trainees) * 100)}%
                              </div>
                            </div>
                          </div>
                        </div>

                        <h3 className="text-2xl font-semibold mb-4 text-[#8b5cf6] flex items-center">
                          <CheckCircle className="w-6 h-6 mr-3 text-[#8b5cf6]" />
                          Trainee Submissions
                        </h3>
                        <div className="overflow-x-auto">
                          <table className="min-w-full bg-white border border-gray-200 rounded-lg overflow-hidden shadow-sm">
                            <thead className="bg-[#ede9fe]">
                              <tr>
                                <th className="py-3 px-4 text-left text-sm font-bold text-[#8b5cf6]">Trainee</th>
                                <th className="py-3 px-4 text-left text-sm font-bold text-[#8b5cf6]">Submitted At</th>
                                <th className="py-3 px-4 text-left text-sm font-bold text-[#8b5cf6]">File</th>
                                <th className="py-3 px-4 text-left text-sm font-bold text-[#8b5cf6]">Grade</th>
                                <th className="py-3 px-4 text-left text-sm font-bold text-[#8b5cf6]">Action</th>
                              </tr>
                            </thead>
                            <tbody>
                              {traineeSubmissions.map((submission, index) => (
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
                                      {submission.username.charAt(0).toUpperCase()}
                                    </div>
                                    {submission.username}
                                  </td>
                                  <td className="py-3 px-4 text-sm text-gray-800">
                                    {format(new Date(submission.submitted_at), 'MMM d, yyyy HH:mm')}
                                  </td>
                                  <td className="py-3 px-4 text-sm text-gray-800">
                                    <a
                                      href={submission.file_path}
                                      target="_blank"
                                      rel="noopener noreferrer"
                                      className="text-[#8b5cf6] hover:text-[#7c3aed] flex items-center"
                                    >
                                      <FileText className="w-4 h-4 mr-1" />
                                      View File
                                    </a>
                                  </td>
                                  <td className="py-3 px-4 text-sm text-gray-800">
                                    {submission.grade !== null ? (
                                      <span 
                                        className={`
                                          px-3 py-1 rounded-full text-xs font-semibold
                                          ${submission.grade >= 90 ? 'bg-green-100 text-green-800' : 
                                            submission.grade >= 70 ? 'bg-yellow-100 text-yellow-800' : 
                                            'bg-red-100 text-red-800'}
                                        `}
                                      >
                                        {submission.grade}%
                                      </span>
                                    ) : (
                                      <span className="text-gray-500">Not graded</span>
                                    )}
                                  </td>
                                  <td className="py-3 px-4 text-sm text-gray-800">
                                    <button
                                      onClick={() => {/* Implement grading functionality */}}
                                      className="text-[#8b5cf6] hover:text-[#7c3aed] font-medium"
                                    >
                                      {submission.grade !== null ? 'Edit Grade' : 'Grade'}
                                    </button>
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
                      <p className="text-xl text-gray-600">Select an assignment to view details</p>
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

export default AssignmentsPage;

