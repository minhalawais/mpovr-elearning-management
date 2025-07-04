import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Plus, Minus, Save } from 'lucide-react';
import { enqueueSnackbar } from 'notistack';

interface Question {
  id: number;
  text: string;
  options: string[];
  correctOption: number;
}

interface QuizCreationModalProps {
  isOpen: boolean;
  onClose: () => void;
  initialQuizTitle: string;
  currentWeek: number;
}

export const QuizCreationModal: React.FC<QuizCreationModalProps> = ({ isOpen, onClose, initialQuizTitle, currentWeek }) => {
  const [quizTitle, setQuizTitle] = useState(initialQuizTitle);
  const [quizDescription, setQuizDescription] = useState('');
  const [quizStartDate, setQuizStartDate] = useState('');
  const [quizEndDate, setQuizEndDate] = useState('');
  const [questions, setQuestions] = useState<Question[]>([
    { id: 1, text: '', options: ['', '', '', ''], correctOption: 0 },
  ]);
  const [weekNumber, setWeekNumber] = useState(currentWeek);

  useEffect(() => {
    setQuizTitle(initialQuizTitle);
    setWeekNumber(currentWeek);
  }, [initialQuizTitle, currentWeek]);

  const addQuestion = () => {
    const newQuestion: Question = {
      id: questions.length + 1,
      text: '',
      options: ['', '', '', ''],
      correctOption: 0,
    };
    setQuestions([...questions, newQuestion]);
  };

  const removeQuestion = (id: number) => {
    if (questions.length > 1) {
      setQuestions(questions.filter(q => q.id !== id));
    }
  };

  const updateQuestion = (id: number, field: string, value: string | number) => {
    setQuestions(questions.map(q =>
      q.id === id ? { ...q, [field]: value } : q
    ));
  };

  const updateOption = (questionId: number, optionIndex: number, value: string) => {
    setQuestions(questions.map(q =>
      q.id === questionId
        ? { ...q, options: q.options.map((opt, idx) => idx === optionIndex ? value : opt) }
        : q
    ));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const quizData = {
      title: quizTitle,
      description: quizDescription,
      start_date: new Date(quizStartDate).toISOString(),
      end_date: new Date(quizEndDate).toISOString(),
      questions: questions.map(q => ({
        text: q.text,
        options: q.options,
        correct_option: q.correctOption
      })),
      week: weekNumber
    };

    try {
      const response = await fetch('http://127.0.0.1:8000/quizzes/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify(quizData)
      });

      if (response.ok) {
        const result = await response.json();
        console.log('Quiz created successfully:', result);
        enqueueSnackbar('Quiz created successfully', { variant: 'success' });
        setQuizTitle('');
        setQuizDescription('');
        setQuizStartDate('');
        setQuizEndDate('');
        setQuestions([{ id: 1, text: '', options: ['', '', '', ''], correctOption: 0 }]);
        onClose();
      } else {
        const errorData = await response.json();
        console.error('Failed to create quiz:', errorData);
        enqueueSnackbar(`Failed to create quiz: ${errorData.detail}`, { variant: 'error' });
      }
    } catch (error) {
      console.error('Error creating quiz:', error);
      enqueueSnackbar('Error creating quiz', { variant: 'error' });
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
              <h2 className="text-3xl font-extrabold text-purple-600 tracking-tight">Create a New Quiz</h2>
              <button 
                onClick={onClose} 
                className="text-purple-500 hover:text-purple-700 transition-all duration-300 hover:rotate-90"
              >
                <X className="w-8 h-8" strokeWidth={2.5} />
              </button>
            </div>
            <form onSubmit={handleSubmit} className="space-y-8">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label htmlFor="quizTitle" className="block text-sm font-medium text-purple-700 mb-2">
                    Quiz Title
                  </label>
                  <input
                    type="text"
                    id="quizTitle"
                    value={quizTitle}
                    onChange={(e) => setQuizTitle(e.target.value)}
                    className="w-full px-4 py-3 border-2 border-purple-200 rounded-xl focus:ring-4 focus:ring-purple-300 focus:border-purple-500 transition-all duration-300 bg-purple-50 text-purple-900"
                    required
                  />
                </div>
                <div>
                  <label htmlFor="quizDescription" className="block text-sm font-medium text-purple-700 mb-2">
                    Quiz Description
                  </label>
                  <textarea
                    id="quizDescription"
                    value={quizDescription}
                    onChange={(e) => setQuizDescription(e.target.value)}
                    className="w-full px-4 py-3 border-2 border-purple-200 rounded-xl focus:ring-4 focus:ring-purple-300 focus:border-purple-500 transition-all duration-300 bg-purple-50 text-purple-900"
                    rows={3}
                  />
                </div>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div>
                  <label htmlFor="quizStartDate" className="block text-sm font-medium text-purple-700 mb-2">
                    Start Date
                  </label>
                  <input
                    type="datetime-local"
                    id="quizStartDate"
                    value={quizStartDate}
                    onChange={(e) => setQuizStartDate(e.target.value)}
                    className="w-full px-4 py-3 border-2 border-purple-200 rounded-xl focus:ring-4 focus:ring-purple-300 focus:border-purple-500 transition-all duration-300 bg-purple-50 text-purple-900"
                    required
                  />
                </div>
                <div>
                  <label htmlFor="quizEndDate" className="block text-sm font-medium text-purple-700 mb-2">
                    End Date
                  </label>
                  <input
                    type="datetime-local"
                    id="quizEndDate"
                    value={quizEndDate}
                    onChange={(e) => setQuizEndDate(e.target.value)}
                    className="w-full px-4 py-3 border-2 border-purple-200 rounded-xl focus:ring-4 focus:ring-purple-300 focus:border-purple-500 transition-all duration-300 bg-purple-50 text-purple-900"
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
              </div>
              {questions.map((question, qIndex) => (
                <motion.div
                  key={question.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3, delay: qIndex * 0.1 }}
                  className="bg-purple-100 p-6 rounded-2xl shadow-lg border-2 border-purple-200"
                >
                  <div className="flex justify-between items-center mb-4">
                    <h3 className="text-xl font-semibold text-purple-800">Question {qIndex + 1}</h3>
                    <button
                      type="button"
                      onClick={() => removeQuestion(question.id)}
                      className="text-red-500 hover:text-red-700 transition-colors"
                    >
                      <Minus className="w-6 h-6" />
                    </button>
                  </div>
                  <input
                    type="text"
                    value={question.text}
                    onChange={(e) => updateQuestion(question.id, 'text', e.target.value)}
                    className="w-full px-4 py-3 border-2 border-purple-200 rounded-xl focus:ring-4 focus:ring-purple-300 focus:border-purple-500 transition-all duration-300 bg-white mb-4 text-purple-900"
                    placeholder="Enter question text"
                    required
                  />
                  {question.options.map((option, oIndex) => (
                    <div key={oIndex} className="flex items-center mb-3">
                      <input
                        type="radio"
                        id={`q${question.id}o${oIndex}`}
                        name={`q${question.id}correct`}
                        checked={question.correctOption === oIndex}
                        onChange={() => updateQuestion(question.id, 'correctOption', oIndex)}
                        className="mr-3 text-purple-600 focus:ring-purple-500 border-purple-300"
                      />
                      <input
                        type="text"
                        value={option}
                        onChange={(e) => updateOption(question.id, oIndex, e.target.value)}
                        className="flex-grow px-4 py-3 border-2 border-purple-200 rounded-xl focus:ring-4 focus:ring-purple-300 focus:border-purple-500 transition-all duration-300 bg-white text-purple-900"
                        placeholder={`Option ${oIndex + 1}`}
                        required
                      />
                    </div>
                  ))}
                </motion.div>
              ))}
              <div className="flex justify-between">
                <button
                  type="button"
                  onClick={addQuestion}
                  className="flex items-center px-6 py-3 border border-transparent text-sm font-medium rounded-xl text-purple-700 bg-purple-100 hover:bg-purple-200 focus:outline-none focus:ring-4 focus:ring-purple-300 transition-all duration-300"
                >
                  <Plus className="w-6 h-6 mr-2" />
                  Add Question
                </button>
                <button
                  type="submit"
                  className="flex items-center px-6 py-3 border border-transparent text-sm font-medium rounded-xl text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-4 focus:ring-purple-300 transition-all duration-300"
                >
                  <Save className="w-6 h-6 mr-2" />
                  Save Quiz
                </button>
              </div>
            </form>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

