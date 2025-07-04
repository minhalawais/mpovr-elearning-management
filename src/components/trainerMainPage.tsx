import React, { useState, useRef, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { Bell, Search, X, ChevronDown, ChevronUp, Users, CheckCircle, Activity } from 'lucide-react'
import { SnackbarProvider, useSnackbar } from 'notistack'
import { ThemeProvider, createTheme } from '@mui/material/styles'
import mpovrLogo from '../images/mpovr_logo.png'
import { QuickAccessSection } from './trainer_portal/quickAccess.tsx'
import { MessageRenderer } from './trainer_portal/messageComponent.tsx'
import { MessageInput } from './trainer_portal/MessageInput.tsx'
import { ScrollToBottomButton } from './trainer_portal/scrollToBottom.tsx'
import { QuizCreationModal } from './trainer_portal/quizCreationPage.tsx'
import ContentModal from './trainer_portal/contentModal.tsx'
import { DiscussionModal } from './trainer_portal/discussionModal.tsx';
import { format, parseISO } from 'date-fns'
import Navbar from './trainer_portal/navbar.tsx'

interface TraineeInfo {
  unique_id: string
  enrollment_date: string
}

interface MessageProps {
  message_id: number;
  content: string;
  created_at: string;
  parent_id?: number;
  sender_id: number
  program_id: number
  updated_at: string
  sender_name: string
  role: string
  id?: number
  attachments?: string[]
  attachements_size?: number[]
}

interface GroupedMessages {
  [key: string]: MessageProps[]
}

const theme = createTheme({
  palette: {
    primary: {
      main: '#8b5cf6',
    },
    secondary: {
      main: '#a78bff',
    },
  },
})

function TrainerMainPageContent() {
  const [activeTab, setActiveTab] = useState('message')
  const [isQuickAccessOpen, setIsQuickAccessOpen] = useState(true)
  const [messageInput, setMessageInput] = useState("")
  const [assignmentDescription, setAssignmentDescription] = useState("")
  const [assignmentDueDate, setAssignmentDueDate] = useState("")
  const [quizTitle, setQuizTitle] = useState("")
  const [contentTitle, setContentTitle] = useState("")
  const [contentDescription, setContentDescription] = useState("")
  const [contentType, setContentType] = useState("video")
  const [contentUrl, setContentUrl] = useState("")
  const [contentFile, setContentFile] = useState<File | null>(null)
  const [virtualSessionTitle, setVirtualSessionTitle] = useState("")
  const [virtualSessionDate, setVirtualSessionDate] = useState("")
  const [virtualSessionTime, setVirtualSessionTime] = useState("")
  const [isSearchVisible, setIsSearchVisible] = useState(false)
  const [showScrollButton, setShowScrollButton] = useState(false)
  const [messages, setMessages] = useState<MessageProps[]>([])
  const [groupedMessages, setGroupedMessages] = useState<GroupedMessages>({})
  const [programTitle, setProgramTitle] = useState("")
  const [totalTrainees, setTotalTrainees] = useState(0)
  const [trainees, setTrainees] = useState<TraineeInfo[]>([])
  const [showTrainees, setShowTrainees] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [programStartDate, setProgramStartDate] = useState("")
  const [currentWeek, setCurrentWeek] = useState(1)
  const [upcomingEvents, setUpcomingEvents] = useState([])
  const conversationRef = useRef<HTMLDivElement>(null)
  const navigate = useNavigate()
  const socketRef = useRef<WebSocket | null>(null)
  const { enqueueSnackbar } = useSnackbar()
  const [isQuizModalOpen, setIsQuizModalOpen] = useState(false)
  const [modalContent, setModalContent] = useState<any>(null);
  const [modalType, setModalType] = useState<'quiz' | 'assignment' | 'content' | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isDiscussionModalOpen, setIsDiscussionModalOpen] = useState(false);
  const [discussionTitle, setDiscussionTitle] = useState("");
  const [replies, setReplies] = useState<{ [key: number]: MessageProps[] }>({})

  const openQuizModal = (quizTitle: string) => {
    console.log(quizTitle);
    setQuizTitle(quizTitle);
    setIsQuizModalOpen(true);
  };

  const closeQuizModal = () => {
    setIsQuizModalOpen(false);
  }

  const navigateToPage = (route: string) => {
    if (route === '/create-quiz') {
      navigate(route, { state: { programId: programTitle } });
    } else {
      navigate(route);
    }
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setContentFile(e.target.files[0])
    }
  }

  useEffect(() => {
    const handleScroll = () => {
      if (conversationRef.current) {
        const { scrollTop, scrollHeight, clientHeight } = conversationRef.current
        setShowScrollButton(scrollHeight - scrollTop > clientHeight + 100)
      }
    }

    const conversationElement = conversationRef.current
    if (conversationElement) {
      conversationElement.addEventListener('scroll', handleScroll)
    }

    return () => {
      if (conversationElement) {
        conversationElement.removeEventListener('scroll', handleScroll)
      }
    }
  }, [])

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      navigate('/login');
    } else {
      fetchMessages();
      initializeWebSocket();
      fetchProgramDetails();
      fetchUpcomingEvents();
    }

    return () => {
      if (socketRef.current) {
        socketRef.current.close();
      }
    };
  }, [navigate]);

  const fetchProgramDetails = async () => {
    try {
      const token = localStorage.getItem('access_token')
      const response = await fetch('http://127.0.0.1:8000/program_details', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      })
      if (response.ok) {
        const data = await response.json()
        setProgramTitle(data.program_title)
        setTotalTrainees(data.total_trainees)
        setTrainees(data.trainees)
        setProgramStartDate(data.start_date)
        
        // Calculate current week
        const startDate = new Date(data.start_date)
        const currentDate = new Date()
        const diffTime = Math.abs(currentDate.getTime() - startDate.getTime())
        const diffWeeks = Math.ceil(diffTime / (1000 * 60 * 60 * 24 * 7))
        setCurrentWeek(diffWeeks)

        enqueueSnackbar('Program details fetched successfully', { variant: 'success' })
      } else {
        enqueueSnackbar('Failed to fetch program details', { variant: 'error' })
      }
    } catch (error) {
      enqueueSnackbar('Error fetching program details', { variant: 'error' })
    }
  }

  const initializeWebSocket = () => {
    const token = localStorage.getItem('access_token')
    if (!token) {
      enqueueSnackbar('No access token found', { variant: 'error' })
      return
    }

    socketRef.current = new WebSocket(`ws://127.0.0.1:8000/ws/chat?token=${token}`)

    socketRef.current.onopen = () => {
      enqueueSnackbar('WebSocket connection established', { variant: 'success' })
    }

    socketRef.current.onmessage = (event) => {
      const newContent = JSON.parse(event.data);
      console.log('New content:', newContent);
      setMessages((prevMessages) => {
        if (!prevMessages.some(msg => msg.id === newContent.id)) {
          const updatedMessages = [...prevMessages, newContent];
          groupMessagesByDate(updatedMessages);
          console.log('Updated messages:', updatedMessages);
          return updatedMessages;
        }
        return prevMessages;
      });
    }

    socketRef.current.onerror = (error) => {
      enqueueSnackbar('WebSocket error', { variant: 'error' })
      console.error('WebSocket error:', error)
    }

    socketRef.current.onclose = () => {
      enqueueSnackbar('WebSocket connection closed', { variant: 'info' })
    }
  }

  const fetchMessages = async () => {
    try {
      const token = localStorage.getItem('access_token')
      if (!token) {
        enqueueSnackbar('No access token found', { variant: 'error' })
        return
      }

      const response = await fetch('http://127.0.0.1:8000/program_content', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      })

      if (response.ok) {
        const data = await response.json()
        if (Array.isArray(data)) {
          const sortedContent = data.sort((a, b) => 
            new Date(a.created_at).getTime() - new Date(b.created_at).getTime()
          )
          console.log('Sorted content:', sortedContent);
          setMessages(sortedContent)
          
          // Group replies
          const replyGroups: { [key: number]: MessageProps[] } = {}
          sortedContent.forEach(message => {
            if (message.parent_id) {
              if (!replyGroups[message.parent_id]) {
                replyGroups[message.parent_id] = []
              }
              replyGroups[message.parent_id].push(message)
            }
          })
          setReplies(replyGroups)
          
          groupMessagesByDate(sortedContent)
          enqueueSnackbar('Program content fetched successfully', { variant: 'success' })
        } else {
          enqueueSnackbar('Unexpected content format', { variant: 'warning' })
        }
      } else {
        const errorData = await response.json()
        enqueueSnackbar(`Error fetching program content: ${errorData.detail}`, { variant: 'error' })
      }
    } catch (error) {
      console.error('Error in fetchMessages:', error)
      enqueueSnackbar('Error in fetchMessages', { variant: 'error' })
    }
  }

  const groupMessagesByDate = (messages: MessageProps[]) => {
    const grouped = messages.reduce((acc, message) => {
      const date = format(new Date(message.created_at), 'yyyy-MM-dd')
      if (!acc[date]) {
        acc[date] = []
      }
      acc[date].push(message)
      return acc
    }, {} as GroupedMessages)
    setGroupedMessages(grouped)
  }

  const scrollToBottom = () => {
    if (conversationRef.current) {
      conversationRef.current.scrollTo({
        top: conversationRef.current.scrollHeight,
        behavior: 'smooth'
      });
    }
  };

  const sendMessage = async (formData: FormData) => {
    setIsLoading(true)
    try {
      const token = localStorage.getItem('access_token')
      if (!token) {
        enqueueSnackbar('No access token found', { variant: 'error' })
        return
      }
  
      const response = await fetch('http://127.0.0.1:8000/send_messages', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        body: formData,
      })
  
      if (response.ok) {
        setMessageInput('')
        enqueueSnackbar('Message sent successfully', { variant: 'success' })
      } else if (response.status === 401) {
        enqueueSnackbar('Unauthorized: Please log in again', { variant: 'error' })
      } else {
        const errorData = await response.json()
        enqueueSnackbar(`Failed to send message: ${errorData.detail}`, { variant: 'error' })
      }
    } catch (error) {
      console.error('Error sending message:', error)
      enqueueSnackbar('Error sending message', { variant: 'error' })
    } finally {
      setIsLoading(false)
    }
  }

  const createAssignment = async (assignmentData: FormData) => {
    setIsLoading(true)
    try {
      const token = localStorage.getItem('access_token');
      if (!token) {
        enqueueSnackbar('No access token found', { variant: 'error' })
        return;
      }

      console.log('Assignment data before sending:', Object.fromEntries(assignmentData));

      const response = await fetch('http://127.0.0.1:8000/assignments/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        body: assignmentData,
      });

      if (response.ok) {
        const newAssignment = await response.json();
        enqueueSnackbar('New assignment created successfully', { variant: 'success' })
      } else if (response.status === 401) {
        enqueueSnackbar('Unauthorized: Please log in again', { variant: 'error' })
      } else {
        const errorData = await response.json();
        enqueueSnackbar(`Failed to create assignment: ${errorData.detail}`, { variant: 'error' })
      }
    } catch (error) {
      console.error('Error creating assignment:', error)
      enqueueSnackbar('Error creating assignment', { variant: 'error' })
    } finally {
      setIsLoading(false)
    }
  };

  const createContent = async (contentData: FormData) => {
    setIsLoading(true)
    try {
      const token = localStorage.getItem('access_token');
      if (!token) {
        enqueueSnackbar('No access token found', { variant: 'error' })
        return;
      }

      console.log('Content data before sending:', Object.fromEntries(contentData));

      const response = await fetch('http://127.0.0.1:8000/content/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        body: contentData,
      });

      if (response.ok) {
        const newContent = await response.json();
        enqueueSnackbar('New content created successfully', { variant: 'success' })
      } else if (response.status === 401) {
        enqueueSnackbar('Unauthorized: Please log in again', { variant: 'error' })
      } else {
        const errorData = await response.json();
        enqueueSnackbar(`Failed to create content: ${errorData.detail}`, { variant: 'error' })
      }
    } catch (error) {
      console.error('Error creating content:', error)
      enqueueSnackbar('Error creating content', { variant: 'error' })
    } finally {
      setIsLoading(false)
    }
  };

  const handleScheduleVirtualSession = async (sessionData: any) => {
    try {
      const token = localStorage.getItem('access_token');
      if (!token) {
        enqueueSnackbar('No access token found', { variant: 'error' })
        return;
      }

      console.log('Virtual session data before sending:', sessionData);

      const response = await fetch("http://127.0.0.1:8000/virtual_sessions/create", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(sessionData),
      });

      if (response.ok) {
        const data = await response.json();
        enqueueSnackbar("Virtual session scheduled successfully", { variant: "success" });
      } else {
        const errorData = await response.json();
        enqueueSnackbar(`Failed to schedule virtual session: ${errorData.detail}`, { variant: "error" });
      }
    } catch (error) {
      console.error('Error scheduling virtual session:', error);
      enqueueSnackbar("Error scheduling virtual session", { variant: "error" });
    }
  };

  const toggleTraineesList = () => {
    setShowTrainees(!showTrainees)
  }

  const openContentModal = async (id: number, type: 'quiz' | 'assignment' | 'content') => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`http://127.0.0.1:8000/${type}/${id}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      if (response.ok) {
        const data = await response.json();
        setModalContent(data);
        setModalType(type);
        setIsModalOpen(true);
      } else {
        enqueueSnackbar(`Failed to fetch ${type} details`, { variant: 'error' });
      }
    } catch (error) {
      console.error(`Error fetching ${type} details:`, error);
      enqueueSnackbar(`Error fetching ${type} details`, { variant: 'error' });
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [groupedMessages]);

  const openDiscussionModal = (title: string) => {
    setDiscussionTitle(title);
    setIsDiscussionModalOpen(true);
  };

  const closeDiscussionModal = () => {
    setIsDiscussionModalOpen(false);
    setDiscussionTitle("");
  };

  useEffect(() => {
    fetchUpcomingEvents()
  }, [])

  const fetchUpcomingEvents = async () => {
    try {
      const token = localStorage.getItem('access_token')
      const response = await fetch('http://127.0.0.1:8000/upcoming_events', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      })
      if (response.ok) {
        const data = await response.json()
        setUpcomingEvents(data)
      } else {
        enqueueSnackbar('Failed to fetch upcoming events', { variant: 'error' })
      }
    } catch (error) {
      console.error('Error fetching upcoming events:', error)
      enqueueSnackbar('Error fetching upcoming events', { variant: 'error' })
    }
  }

  const handleReply = async (parentId: number, content: string) => {
    try {
      const token = localStorage.getItem('access_token')
      const response = await fetch('http://127.0.0.1:8000/reply_message', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ parent_id: parentId, content }),
      })

      if (response.ok) {
        const newReply = await response.json()
        setReplies(prevReplies => ({
          ...prevReplies,
          [parentId]: [...(prevReplies[parentId] || []), newReply],
        }))
        enqueueSnackbar('Reply sent successfully', { variant: 'success' })
      } else {
        enqueueSnackbar('Failed to send reply', { variant: 'error' })
      }
    } catch (error) {
      console.error('Error sending reply:', error)
      enqueueSnackbar('Error sending reply', { variant: 'error' })
    }
  }

  return (
    <div className="flex h-screen bg-gradient-to-br from-[#f5f3ff] to-[#ede9fe] overflow-hidden">
      <div className="flex-1 flex flex-col shadow-2xl bg-white">
        <Navbar />
        <div className="bg-gradient-to-r from-[#8b5cf6]/10 to-[#a78bff]/10 border-b border-gray-100 px-4 py-2 flex items-center justify-between mt-16">
          <div className="flex items-center space-x-4">
            <h2 className="text-lg font-bold text-gray-800 flex items-center">
              <Activity className="w-4 h-4 mr-1 text-[#8b5cf6]" />
              {programTitle}
            </h2>
            <div className="flex items-center space-x-1 text-xs">
              <Users className="h-3 w-3 text-[#8b5cf6]/70" />
              <span className="text-gray-600">
                Total Trainees: 
                <span className="font-semibold ml-1 text-[#8b5cf6]">{totalTrainees}</span>
              </span>
            </div>
            <div className="flex items-center space-x-1 text-xs">
              <span className="text-gray-600">
                Start Date: 
                <span className="font-semibold ml-1 text-[#8b5cf6]">{programStartDate}</span>
              </span>
            </div>
            <div className="flex items-center space-x-1 text-xs">
              <span className="text-gray-600">
                Current Week: 
                <span className="font-semibold ml-1 text-[#8b5cf6]">{currentWeek}</span>
              </span>
            </div>
          </div>
          <motion.button
            onClick={toggleTraineesList}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="flex items-center space-x-1 text-[#8b5cf6] hover:text-[#a78bff] transition-colors text-xs bg-[#8b5cf6]/10 px-2 py-1 rounded-full"
          >
            <span>View Trainees</span>
            {showTrainees ? <ChevronUp className="h-3 w-3" /> : <ChevronDown className="h-3 w-3" />}
          </motion.button>
        </div>

        <div className="flex flex-1 overflow-hidden">
          <div 
            className={`
              flex-1 flex flex-col bg-white/80 backdrop-blur-sm
              transition-all duration-300 ease-in-out
              ${isQuickAccessOpen ? 'w-[calc(100%-18rem)]' : 'w-full'}
            `}
          >
            <div className="p-2 border-b border-gray-100 flex items-center justify-end">
              {isSearchVisible ? (
                <div className="relative w-full max-w-md">
                  <input
                    type="text"
                    placeholder="Search trainees, messages..."
                    className="w-full pl-8 pr-4 py-1.5 text-sm bg-gray-50 border border-gray-200 rounded-full focus:ring-2 focus:ring-indigo-300 focus:border-transparent transition-all duration-300 ease-in-out"
                  />
                  <Search className="absolute left-2 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
                  <button
                    onClick={() => setIsSearchVisible(false)}
                    className="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-indigo-600 transition-colors"
                  >
                    <X className="h-4 w-4" />
                  </button>
                </div>
              ) : (
                <motion.button
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => setIsSearchVisible(true)}
                  className="p-1.5 bg-indigo-600 text-white rounded-full hover:bg-indigo-700 transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-300"
                >
                  <Search className="h-4 w-4" />
                </motion.button>
              )}
            </div>

            <div className="flex-1 p-6 overflow-y-auto hide-scrollbar relative" ref={conversationRef}>
              {Object.entries(groupedMessages).map(([date, messages]) => (
                <div key={date} className="mb-6">
                  <div className="flex justify-center mb-4">
                    <span className="bg-gray-200 text-gray-600 text-xs font-semibold px-3 py-1 rounded-full">
                      {format(new Date(date), 'MMMM d, yyyy')}
                    </span>
                  </div>
                  <div className="space-y-4">
                    {messages.map((msg) => (
                      <MessageRenderer key={msg.message_id} msg={msg} navigateToPage={navigateToPage} openContentModal={openContentModal} onReply={handleReply} replies={replies[msg.message_id] || []}/>
                    ))}
                  </div>
                </div>
              ))}
              <ScrollToBottomButton show={showScrollButton} onClick={scrollToBottom} />
            </div>

            <div className="border-t border-gray-100/50 p-4 bg-white/50 backdrop-blur-sm">
              <div className="flex mb-4 space-x-2 overflow-x-auto">
                {['message', 'assignment', 'quiz', 'content', 'virtual', 'discussion'].map((tab) => (
                  <button
                    key={tab}
                    className={`px-4 py-2 rounded-full text-sm capitalize whitespace-nowrap transition-all ${
                      activeTab === tab 
                        ? 'bg-indigo-600 text-white' 
                        : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                    }`}
                    onClick={() => setActiveTab(tab)}
                  >
                    {tab === 'virtual' ? 'Virtual Session' : tab}
                  </button>
                ))}
              </div>
              <MessageInput
                activeTab={activeTab}
                messageInput={messageInput}
                setMessageInput={setMessageInput}
                assignmentDescription={assignmentDescription}
                setAssignmentDescription={setAssignmentDescription}
                assignmentDueDate={assignmentDueDate}
                setAssignmentDueDate={setAssignmentDueDate}
                quizTitle={quizTitle}
                setQuizTitle={setQuizTitle}
                contentTitle={contentTitle}
                setContentTitle={setContentTitle}
                contentDescription={contentDescription}
                setContentDescription={setContentDescription}
                contentType={contentType}
                setContentType={setContentType}
                contentUrl={contentUrl}
                setContentUrl={setContentUrl}
                virtualSessionTitle={virtualSessionTitle}
                setVirtualSessionTitle={setVirtualSessionTitle}
                virtualSessionDate={virtualSessionDate}
                setVirtualSessionDate={setVirtualSessionDate}
                virtualSessionTime={virtualSessionTime}
                setVirtualSessionTime={setVirtualSessionTime}
                handleFileChange={handleFileChange}
                navigateToPage={navigateToPage}
                sendMessage={sendMessage}
                createAssignment={createAssignment}
                createContent={createContent}
                openQuizModal={openQuizModal}
                handleScheduleVirtualSession={handleScheduleVirtualSession}
                currentWeek={currentWeek}
                discussionTitle={discussionTitle}
                setDiscussionTitle={setDiscussionTitle}
                openDiscussionModal={openDiscussionModal}
                handleReply={handleReply}
              />
            </div>
          </div>

          <QuickAccessSection 
            isQuickAccessOpen={isQuickAccessOpen}
            setIsQuickAccessOpen={setIsQuickAccessOpen}
            navigateToPage={navigateToPage}
            upcomingEvents={upcomingEvents}
          />
        </div>
        
        <AnimatePresence>
          {showTrainees && (
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center z-50"
            >
              <motion.div 
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0.9, opacity: 0 }}
                className="bg-white rounded-3xl p-6 w-[500px] max-h-[80vh] overflow-y-auto shadow-2xl"
              >
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-xl font-bold text-[#8b5cf6] flex items-center">
                    <Users className="w-6 h-6 mr-2" />
                    Trainees
                  </h3>
                  <motion.button
                    whileHover={{ rotate: 90 }}
                    onClick={toggleTraineesList}
                    className="text-gray-500 hover:text-[#8b5cf6]"
                  >
                    <X className="w-6 h-6" />
                  </motion.button>
                </div>
                <div className="space-y-3">
                  {trainees.map((trainee, index) => (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: index * 0.1 }}
                      className="bg-[#f5f3ff] p-3 rounded-xl flex items-center justify-between hover:bg-[#ede9fe] transition-colors"
                    >
                      <div>
                        <span className="font-semibold text-[#8b5cf6]">{trainee.unique_id}</span>
                        <p className="text-xs text-gray-500 mt-1">
                          Enrolled: {format(parseISO(trainee.enrollment_date), 'MMMM d, yyyy')}
                        </p>
                      </div>
                      <CheckCircle className="w-5 h-5 text-[#8b5cf6]/70" />
                    </motion.div>
                  ))}
                </div>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>
        <QuizCreationModal
          isOpen={isQuizModalOpen}
          onClose={closeQuizModal}
          initialQuizTitle={quizTitle}
          currentWeek={currentWeek}
        />
        <ContentModal
          isOpen={isModalOpen}
          onClose={() => setIsModalOpen(false)}
          content={modalContent}
          type={modalType!}
        />
        <DiscussionModal
          isOpen={isDiscussionModalOpen}
          onClose={closeDiscussionModal}
          initialDiscussionTitle={discussionTitle}
          currentWeek={currentWeek}
        />
      </div>
    </div>
  )
}

export default function TrainerMainPage() {
  return (
    <ThemeProvider theme={theme}>
      <SnackbarProvider maxSnack={3}>
        <TrainerMainPageContent />
      </SnackbarProvider>
    </ThemeProvider>
  )
}

