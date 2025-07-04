import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { ChevronDown, ChevronUp, CheckCircle, Circle, Calendar, Clock, FileText, Video, Book, PenTool, Presentation, HelpCircle, Users } from 'lucide-react'
import Navbar from './landingPageComponents/navbar.tsx'
interface Task {
  id: string
  title: string
  type: 'virtual_session' | 'video' | 'reading' | 'assignment' | 'practicum' | 'presentation' | 'quiz' | 'custom'
  dueDate: string
  uploadDate: string
  status: 'pending' | 'completed'
}

interface Week {
  number: number
  startDate: string
  endDate: string
  agenda: string
  tasks: Task[]
}

const mockWeeks: Week[] = [
  {
    number: 1,
    startDate: '2024-09-30',
    endDate: '2024-10-06',
    agenda: 'Introduction to Workday HCM and Core Concepts',
    tasks: [
      { id: '1-1', title: 'Welcome Webinar', type: 'virtual_session', dueDate: '2024-10-01', uploadDate: '2024-09-30', status: 'pending' },
      { id: '1-2', title: 'Read Workday HCM Overview', type: 'reading', dueDate: '2024-10-03', uploadDate: '2024-09-30', status: 'pending' },
      { id: '1-3', title: 'Watch Workday HCM Introduction Video', type: 'video', dueDate: '2024-10-04', uploadDate: '2024-09-30', status: 'pending' },
      { id: '1-4', title: 'Complete HCM Basics Quiz', type: 'quiz', dueDate: '2024-10-06', uploadDate: '2024-10-01', status: 'pending' },
    ]
  },
  {
    number: 2,
    startDate: '2024-10-07',
    endDate: '2024-10-13',
    agenda: 'Workday HCM Architecture and Data Model',
    tasks: [
      { id: '2-1', title: 'Read Workday HCM Architecture Guide', type: 'reading', dueDate: '2024-10-10', uploadDate: '2024-10-07', status: 'pending' },
      { id: '2-2', title: 'Watch Data Model Explanation Video', type: 'video', dueDate: '2024-10-11', uploadDate: '2024-10-07', status: 'pending' },
      { id: '2-3', title: 'Complete Data Model Exercise', type: 'assignment', dueDate: '2024-10-13', uploadDate: '2024-10-07', status: 'pending' },
    ]
  },
  {
    number: 3,
    startDate: '2024-10-14',
    endDate: '2024-10-20',
    agenda: 'Employee Lifecycle Management in Workday',
    tasks: [
      { id: '3-1', title: 'Read Employee Lifecycle Documentation', type: 'reading', dueDate: '2024-10-16', uploadDate: '2024-10-14', status: 'pending' },
      { id: '3-2', title: 'Attend Hiring Process Webinar', type: 'virtual_session', dueDate: '2024-10-17', uploadDate: '2024-10-14', status: 'pending' },
      { id: '3-3', title: 'Complete Onboarding Simulation', type: 'practicum', dueDate: '2024-10-20', uploadDate: '2024-10-14', status: 'pending' },
    ]
  },
  {
    number: 4,
    startDate: '2024-10-21',
    endDate: '2024-10-27',
    agenda: 'Compensation and Benefits in Workday HCM',
    tasks: [
      { id: '4-1', title: 'Read Compensation Management Guide', type: 'reading', dueDate: '2024-10-23', uploadDate: '2024-10-21', status: 'pending' },
      { id: '4-2', title: 'Watch Benefits Administration Video', type: 'video', dueDate: '2024-10-24', uploadDate: '2024-10-21', status: 'pending' },
      { id: '4-3', title: 'Complete Compensation Planning Exercise', type: 'assignment', dueDate: '2024-10-27', uploadDate: '2024-10-21', status: 'pending' },
    ]
  },
  {
    number: 5,
    startDate: '2024-10-28',
    endDate: '2024-11-03',
    agenda: 'Talent Management and Performance',
    tasks: [
      { id: '5-1', title: 'Read Talent Management Whitepaper', type: 'reading', dueDate: '2024-10-30', uploadDate: '2024-10-28', status: 'pending' },
      { id: '5-2', title: 'Attend Performance Review Webinar', type: 'virtual_session', dueDate: '2024-10-31', uploadDate: '2024-10-28', status: 'pending' },
      { id: '5-3', title: 'Complete Goal Setting Practicum', type: 'practicum', dueDate: '2024-11-03', uploadDate: '2024-10-28', status: 'pending' },
    ]
  },
  {
    number: 6,
    startDate: '2024-11-04',
    endDate: '2024-11-10',
    agenda: 'Workday Reporting and Analytics',
    tasks: [
      { id: '6-1', title: 'Read Workday Report Design Guide', type: 'reading', dueDate: '2024-11-06', uploadDate: '2024-11-04', status: 'pending' },
      { id: '6-2', title: 'Watch Advanced Analytics Tutorial', type: 'video', dueDate: '2024-11-07', uploadDate: '2024-11-04', status: 'pending' },
      { id: '6-3', title: 'Create Custom HCM Dashboard', type: 'assignment', dueDate: '2024-11-10', uploadDate: '2024-11-04', status: 'pending' },
    ]
  },
  {
    number: 7,
    startDate: '2024-11-11',
    endDate: '2024-11-17',
    agenda: 'Security and Compliance in Workday HCM',
    tasks: [
      { id: '7-1', title: 'Read Workday Security Whitepaper', type: 'reading', dueDate: '2024-11-13', uploadDate: '2024-11-11', status: 'pending' },
      { id: '7-2', title: 'Attend Compliance Webinar', type: 'virtual_session', dueDate: '2024-11-14', uploadDate: '2024-11-11', status: 'pending' },
      { id: '7-3', title: 'Complete Security Configuration Exercise', type: 'assignment', dueDate: '2024-11-17', uploadDate: '2024-11-11', status: 'pending' },
    ]
  },
  {
    number: 8,
    startDate: '2024-11-18',
    endDate: '2024-11-24',
    agenda: 'Workday Integration and APIs',
    tasks: [
      { id: '8-1', title: 'Read Integration Cloud Connect Guide', type: 'reading', dueDate: '2024-11-20', uploadDate: '2024-11-18', status: 'pending' },
      { id: '8-2', title: 'Watch API Usage Tutorial', type: 'video', dueDate: '2024-11-21', uploadDate: '2024-11-18', status: 'pending' },
      { id: '8-3', title: 'Develop Simple Integration Scenario', type: 'practicum', dueDate: '2024-11-24', uploadDate: '2024-11-18', status: 'pending' },
    ]
  },
  {
    number: 9,
    startDate: '2024-11-25',
    endDate: '2024-12-01',
    agenda: 'Workday Mobile and User Experience',
    tasks: [
      { id: '9-1', title: 'Read Mobile App Documentation', type: 'reading', dueDate: '2024-11-27', uploadDate: '2024-11-25', status: 'pending' },
      { id: '9-2', title: 'Attend UX Design Principles Webinar', type: 'virtual_session', dueDate: '2024-11-28', uploadDate: '2024-11-25', status: 'pending' },
      { id: '9-3', title: 'Complete Mobile App Usability Test', type: 'assignment', dueDate: '2024-12-01', uploadDate: '2024-11-25', status: 'pending' },
    ]
  },
  {
    number: 10,
    startDate: '2024-12-02',
    endDate: '2024-12-08',
    agenda: 'Workday HCM Administration and Configuration',
    tasks: [
      { id: '10-1', title: 'Read System Admin Guide', type: 'reading', dueDate: '2024-12-04', uploadDate: '2024-12-02', status: 'pending' },
      { id: '10-2', title: 'Watch Configuration Best Practices Video', type: 'video', dueDate: '2024-12-05', uploadDate: '2024-12-02', status: 'pending' },
      { id: '10-3', title: 'Perform System Configuration Exercise', type: 'practicum', dueDate: '2024-12-08', uploadDate: '2024-12-02', status: 'pending' },
    ]
  },
  {
    number: 11,
    startDate: '2024-12-09',
    endDate: '2024-12-15',
    agenda: 'Workday HCM Implementation Best Practices',
    tasks: [
      { id: '11-1', title: 'Read Implementation Methodology Guide', type: 'reading', dueDate: '2024-12-11', uploadDate: '2024-12-09', status: 'pending' },
      { id: '11-2', title: 'Attend Project Management Webinar', type: 'virtual_session', dueDate: '2024-12-12', uploadDate: '2024-12-09', status: 'pending' },
      { id: '11-3', title: 'Develop Implementation Plan Draft', type: 'assignment', dueDate: '2024-12-15', uploadDate: '2024-12-09', status: 'pending' },
    ]
  },
  {
    number: 12,
    startDate: '2024-12-16',
    endDate: '2024-12-22',
    agenda: 'Course Wrap-up and Certification Preparation',
    tasks: [
      { id: '12-1', title: 'Review All Course Materials', type: 'reading', dueDate: '2024-12-18', uploadDate: '2024-12-16', status: 'pending' },
      { id: '12-2', title: 'Attend Certification Prep Webinar', type: 'virtual_session', dueDate: '2024-12-19', uploadDate: '2024-12-16', status: 'pending' },
      { id: '12-3', title: 'Complete Practice Certification Exam', type: 'quiz', dueDate: '2024-12-21', uploadDate: '2024-12-16', status: 'pending' },
      { id: '12-4', title: 'Submit Course Feedback Survey', type: 'assignment', dueDate: '2024-12-22', uploadDate: '2024-12-16', status: 'pending' },
    ]
  },
]

const TaskIcon = ({ type }: { type: Task['type'] }) => {
  switch (type) {
    case 'virtual_session': return <Users className="w-5 h-5 text-blue-500" />
    case 'video': return <Video className="w-5 h-5 text-red-500" />
    case 'reading': return <Book className="w-5 h-5 text-green-500" />
    case 'assignment': return <PenTool className="w-5 h-5 text-yellow-500" />
    case 'practicum': return <FileText className="w-5 h-5 text-purple-500" />
    case 'presentation': return <Presentation className="w-5 h-5 text-indigo-500" />
    case 'quiz': return <HelpCircle className="w-5 h-5 text-orange-500" />
    default: return <Circle className="w-5 h-5 text-gray-500" />
  }
}

const ProgramTimeline: React.FC = () => {
  const [expandedWeeks, setExpandedWeeks] = useState<Set<number>>(new Set(mockWeeks.map(week => week.number)))
  const [completedTasks, setCompletedTasks] = useState<Set<string>>(new Set())

  const toggleWeek = (weekNumber: number) => {
    setExpandedWeeks(prev => {
      const newSet = new Set(prev)
      if (newSet.has(weekNumber)) {
        newSet.delete(weekNumber)
      } else {
        newSet.add(weekNumber)
      }
      return newSet
    })
  }

  const toggleTaskCompletion = (taskId: string) => {
    setCompletedTasks(prev => {
      const newSet = new Set(prev)
      if (newSet.has(taskId)) {
        newSet.delete(taskId)
      } else {
        newSet.add(taskId)
      }
      return newSet
    })
  }

  return (
    <div className="w-full p-6 bg-white rounded-xl shadow-lg mt-20">
      <Navbar />
      <h1 className="text-3xl font-bold text-gray-800 mb-2">Workday HCM</h1>
      <h2 className="text-xl text-gray-600 mb-6">Batch 2024FA-WD101</h2>
      {mockWeeks.map((week) => (
        <motion.div
          key={week.number}
          className="mb-4 border border-gray-200 rounded-lg overflow-hidden"
          initial={false}
        >
          <motion.button
            className="w-full p-4 flex items-center justify-between bg-gradient-to-r from-[#8b5cf6] to-[#6366f1] text-white"
            onClick={() => toggleWeek(week.number)}
          >
            <span className="text-lg font-semibold">Week {week.number}</span>
            {expandedWeeks.has(week.number) ? <ChevronUp /> : <ChevronDown />}
          </motion.button>
          <AnimatePresence initial={false}>
            {expandedWeeks.has(week.number) && (
              <motion.div
                initial="collapsed"
                animate="open"
                exit="collapsed"
                variants={{
                  open: { opacity: 1, height: "auto" },
                  collapsed: { opacity: 0, height: 0 }
                }}
                transition={{ duration: 0.8, ease: [0.04, 0.62, 0.23, 0.98] }}
              >
                <div className="p-4 bg-[#eeebfe]">
                  <p className="text-gray-700 mb-2">
                    <Calendar className="inline-block mr-2" />
                    {week.startDate} - {week.endDate}
                  </p>
                  <p className="text-gray-800 font-medium mb-4">{week.agenda}</p>
                  <div className="space-y-3">
                    {week.tasks.map((task) => (
                      <motion.div
                        key={task.id}
                        className="flex items-center justify-between p-3 bg-white rounded-lg shadow"
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                      >
                        <div className="flex items-center space-x-3">
                          <TaskIcon type={task.type} />
                          <span className="text-gray-800">{task.title}</span>
                          <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded-full">{task.type}</span>
                        </div>
                        <div className="flex items-center space-x-4">
                          <span className="text-sm text-gray-500">
                            <Clock className="inline-block mr-1 w-4 h-4" />
                            Due: {task.dueDate}
                          </span>
                          <button
                            onClick={() => toggleTaskCompletion(task.id)}
                            className="focus:outline-none"
                          >
                            {completedTasks.has(task.id) ? (
                              <CheckCircle className="w-6 h-6 text-green-500" />
                            ) : (
                              <Circle className="w-6 h-6 text-gray-300" />
                            )}
                          </button>
                        </div>
                      </motion.div>
                    ))}
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>
      ))}
    </div>
  )
}

export default ProgramTimeline

