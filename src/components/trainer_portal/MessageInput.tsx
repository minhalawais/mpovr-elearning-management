import React, { useState, useEffect } from 'react'
import { Send, Paperclip, Calendar, Clock, FileUp, Link, X } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

interface MessageInputProps {
  activeTab: string
  messageInput: string
  setMessageInput: (value: string) => void
  assignmentDescription: string
  setAssignmentDescription: (value: string) => void
  assignmentDueDate: string
  setAssignmentDueDate: (value: string) => void
  createAssignment: (assignmentData: FormData) => Promise<void>
  sendMessage: (message: any) => Promise<void>
  quizTitle: string
  setQuizTitle: (value: string) => void
  contentTitle: string
  setContentTitle: (value: string) => void
  contentDescription: string
  setContentDescription: (value: string) => void
  contentType: string
  setContentType: (value: string) => void
  contentUrl: string
  setContentUrl: (value: string) => void
  virtualSessionTitle: string
  setVirtualSessionTitle: (value: string) => void
  virtualSessionDate: string
  setVirtualSessionDate: (value: string) => void
  virtualSessionTime: string
  setVirtualSessionTime: (value: string) => void
  handleFileChange: (e: React.ChangeEvent<HTMLInputElement>) => void
  navigateToPage: (route: string) => void
  openQuizModal: (value: string) => void
  createContent: (contentData: FormData) => Promise<void>
  handleScheduleVirtualSession: (sessionData: any) => Promise<void>
  currentWeek: number
  discussionTitle: string
  setDiscussionTitle: (value: string) => void
  openDiscussionModal: (value: string) => void
}

export const MessageInput: React.FC<MessageInputProps> = ({
  activeTab,
  messageInput,
  setMessageInput,
  assignmentDescription,
  setAssignmentDescription,
  assignmentDueDate,
  setAssignmentDueDate,
  createAssignment,
  sendMessage,
  quizTitle,
  setQuizTitle,
  contentTitle,
  setContentTitle,
  contentDescription,
  setContentDescription,
  contentType,
  setContentType,
  contentUrl,
  setContentUrl,
  virtualSessionTitle,
  setVirtualSessionTitle,
  virtualSessionDate,
  setVirtualSessionDate,
  virtualSessionTime,
  setVirtualSessionTime,
  handleFileChange,
  navigateToPage,
  openQuizModal,
  createContent,
  handleScheduleVirtualSession,
  currentWeek,
  discussionTitle,
  setDiscussionTitle,
  openDiscussionModal
}) => {
  const [uploadedFile, setUploadedFile] = useState<File | null>(null)
  const [isMessageLoading, setIsMessageLoading] = useState(false)
  const [isAssignmentLoading, setIsAssignmentLoading] = useState(false)
  const [isContentLoading, setIsContentLoading] = useState(false)
  const [isVirtualSessionLoading, setIsVirtualSessionLoading] = useState(false)
  const [weekNumber, setWeekNumber] = useState(currentWeek);
  const [assignmentTitle, setAssignmentTitle] = useState("");
  const [attachments, setAttachments] = useState<File[]>([])
  const navigate = useNavigate()

  const handleSendMessage = () => {
    if (messageInput.trim() || attachments.length > 0) {
      const formData = new FormData();
      formData.append('content', messageInput);
      attachments.forEach((file, index) => {
        formData.append(`attachments`, file);
      });
      sendMessage(formData);
      setMessageInput('');
      setAttachments([]);
    }
  };


  const handleCreateAssignment = async () => {
    if (assignmentTitle && assignmentDescription && assignmentDueDate) {
      setIsAssignmentLoading(true)
      const formData = new FormData()
      formData.append('title', assignmentTitle)
      formData.append('description', assignmentDescription)
      formData.append('due_date', assignmentDueDate)
      formData.append('week', weekNumber.toString())
      if (uploadedFile) {
        formData.append('uploaded_content', uploadedFile)
      }
      try {
        console.log('Assignment FormData:', Object.fromEntries(formData));
        await createAssignment(formData)
        setAssignmentTitle('')
        setAssignmentDescription('')
        setAssignmentDueDate('')
        setUploadedFile(null)
      } catch (error) {
        console.error('Failed to create assignment:', error)
      } finally {
        setIsAssignmentLoading(false)
      }
    }
  }

  const handleCreateContent = async () => {
    if (contentTitle && contentDescription && contentType) {
      setIsContentLoading(true)
      const formData = new FormData()
      formData.append('title', contentTitle)
      formData.append('description', contentDescription)
      formData.append('content_type', contentType)
      formData.append('week', weekNumber.toString())
      if (contentType === 'url') {
        formData.append('content_url', contentUrl)
      } else if (uploadedFile) {
        formData.append('uploaded_content', uploadedFile)
      }
      try {
        console.log('Content FormData:', Object.fromEntries(formData));
        await createContent(formData)
        setContentTitle('')
        setContentDescription('')
        setContentType('video')
        setContentUrl('')
        setUploadedFile(null)
      } catch (error) {
        console.error('Failed to create content:', error)
      } finally {
        setIsContentLoading(false)
      }
    }
  }

  const handleScheduleSession = async () => {
    if (virtualSessionTitle && contentDescription && virtualSessionDate && virtualSessionTime) {
      setIsVirtualSessionLoading(true)
      try {
        const sessionData = {
          title: virtualSessionTitle,
          description: contentDescription,
          scheduled_datetime: `${virtualSessionDate}T${virtualSessionTime}`,
          duration_minutes: 60,
          week: weekNumber,
        }
        console.log('Virtual Session Data:', sessionData);
        await handleScheduleVirtualSession(sessionData)
        setVirtualSessionTitle('')
        setContentDescription('')
        setVirtualSessionDate('')
        setVirtualSessionTime('')
      } catch (error) {
        console.error('Failed to schedule virtual session:', error)
      } finally {
        setIsVirtualSessionLoading(false)
      }
    }
  }

  const handleContentFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setUploadedFile(e.target.files[0])
    }
  }

  const handleAttachmentChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const newAttachments = Array.from(e.target.files)
      setAttachments(prevAttachments => [...prevAttachments, ...newAttachments])
    }
  }

  const removeAttachment = (index: number) => {
    setAttachments(prevAttachments => prevAttachments.filter((_, i) => i !== index))
  }

  // Loading spinner component
  const LoadingSpinner = () => (
    <svg 
      className="animate-spin h-5 w-5 text-white" 
      xmlns="http://www.w3.org/2000/svg" 
      fill="none" 
      viewBox="0 0 24 24"
    >
      <circle 
        className="opacity-25" 
        cx="12" 
        cy="12" 
        r="10" 
        stroke="currentColor" 
        strokeWidth="4"
      ></circle>
      <path 
        className="opacity-75" 
        fill="currentColor" 
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
      ></path>
    </svg>
  )

  useEffect(() => {
    setWeekNumber(currentWeek);
  }, [currentWeek]);

  switch (activeTab) {
    case 'message':
      return (
        <div className="space-y-4 bg-white rounded-lg shadow-md p-4">
          <div className="flex items-center space-x-2">
            <input
              type="text"
              placeholder="Type your message..."
              value={messageInput}
              onChange={(e) => setMessageInput(e.target.value)}
              onKeyPress={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSendMessage();
                }
              }}
              className="flex-1 p-2 text-sm border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            />
            <label className="cursor-pointer">
              <Paperclip className="w-5 h-5 text-gray-400 hover:text-gray-600" />
              <input
                type="file"
                multiple
                onChange={handleAttachmentChange}
                className="hidden"
              />
            </label>
            <button 
              className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 flex items-center justify-center"
              onClick={handleSendMessage}
              disabled={isMessageLoading}
            >
              {isMessageLoading ? <LoadingSpinner /> : <Send className="w-4 h-4" />}
            </button>
          </div>
          {attachments.length > 0 && (
            <div className="mt-2 space-y-2">
              {attachments.map((file, index) => (
                <div key={index} className="flex items-center justify-between bg-gray-100 p-2 rounded-md">
                  <span className="text-sm truncate">{file.name}</span>
                  <button onClick={() => removeAttachment(index)} className="text-red-500 hover:text-red-700">
                    <X className="w-4 h-4" />
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      )
    case 'assignment':
      return (
        <div className="space-y-4 bg-white rounded-lg shadow-md p-4">
          <input
            type="text"
            placeholder="Assignment Title"
            value={assignmentTitle}
            onChange={(e) => setAssignmentTitle(e.target.value)}
            className="w-full p-2 text-sm border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
          />
          <textarea
            placeholder="Assignment Description"
            value={assignmentDescription}
            onChange={(e) => setAssignmentDescription(e.target.value)}
            className="w-full p-2 text-sm border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            rows={3}
          />
          <div className="flex items-center space-x-2">
            <Calendar className="w-5 h-5 text-gray-400" />
            <input
              type="datetime-local"
              value={assignmentDueDate}
              onChange={(e) => setAssignmentDueDate(e.target.value)}
              className="flex-1 p-2 text-sm border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            />
          </div>
          <div className="flex items-center space-x-2">
            <FileUp className="w-5 h-5 text-gray-400" />
            <input
              type="file"
              onChange={handleContentFileChange}
              className="flex-1 p-2 text-sm border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            />
          </div>
          <div className="flex items-center space-x-2">
            <input
              type="number"
              placeholder="Week Number"
              value={weekNumber}
              onChange={(e) => setWeekNumber(Number(e.target.value))}
              min={1}
              max={currentWeek}
              className="flex-1 p-2 text-sm border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            />
          </div>
          {uploadedFile && (
            <div className="text-sm text-gray-600">
              File uploaded: {uploadedFile.name}
            </div>
          )}
          <button 
            className="w-full px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 flex items-center justify-center"
            onClick={handleCreateAssignment}
            disabled={isAssignmentLoading}
          >
            {isAssignmentLoading ? <LoadingSpinner /> : 'Create Assignment'}
          </button>
        </div>
      )
    case 'quiz':
      return (
        <div className="space-y-4 bg-white rounded-lg shadow-md p-4">
          <input
            type="text"
            placeholder="Quiz Title"
            value={quizTitle}
            onChange={(e) => setQuizTitle(e.target.value)}
            className="w-full p-2 text-sm border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
          />
          <div className="flex items-center space-x-2">
            <input
              type="number"
              placeholder="Week Number"
              value={weekNumber}
              onChange={(e) => setWeekNumber(Number(e.target.value))}
              min={1}
              max={currentWeek}
              className="w-full p-2 text-sm border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            />
          </div>
          <button 
            onClick={() => openQuizModal(quizTitle)}
            className="w-full px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            Create Quiz
          </button>
        </div>
      )
    case 'content':
      return (
        <div className="space-y-4 bg-white rounded-lg shadow-md p-4">
          <input
            type="text"
            placeholder="Content Title"
            value={contentTitle}
            onChange={(e) => setContentTitle(e.target.value)}
            className="w-full p-2 text-sm border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
          />
          <textarea
            placeholder="Content Description"
            value={contentDescription}
            onChange={(e) => setContentDescription(e.target.value)}
            className="w-full p-2 text-sm border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            rows={3}
          />
          <select
            value={contentType}
            onChange={(e) => setContentType(e.target.value)}
            className="w-full p-2 text-sm border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
          >
            <option value="video">Video</option>
            <option value="document">Document</option>
            <option value="image">Image</option>
            <option value="url">URL</option>
          </select>
          {contentType === 'url' ? (
            <input
              type="url"
              placeholder="Content URL"
              value={contentUrl}
              onChange={(e) => setContentUrl(e.target.value)}
              className="w-full p-2 text-sm border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            />
          ) : (
            <input
              type="file"
              onChange={handleContentFileChange}
              className="w-full p-2 text-sm border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            />
          )}
          <div className="flex items-center space-x-2">
            <input
              type="number"
              placeholder="Week Number"
              value={weekNumber}
              onChange={(e) => setWeekNumber(Number(e.target.value))}
              min={1}
              max={currentWeek}
              className="w-full p-2 text-sm border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            />
          </div>
          {uploadedFile && contentType !== 'url' && (
            <div className="text-sm text-gray-600">
              File uploaded: {uploadedFile.name}
            </div>
          )}
          <button 
            className="w-full px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 flex items-center justify-center"
            onClick={handleCreateContent}
            disabled={isContentLoading}
          >
            {isContentLoading ? <LoadingSpinner /> : 'Upload Content'}
          </button>
        </div>
      )
    case 'virtual':
      return (
        <div className="space-y-4 bg-white rounded-lg shadow-md p-4">
          <input
            type="text"
            placeholder="Virtual Session Title"
            value={virtualSessionTitle}
            onChange={(e) => setVirtualSessionTitle(e.target.value)}
            className="w-full p-2 text-sm border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
          />
          <textarea
            placeholder="Session Description"
            value={contentDescription} 
            onChange={(e) => setContentDescription(e.target.value)}
            className="w-full p-2 text-sm border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            rows={3}
          />
          <div className="flex space-x-2">
            <div className="flex items-center space-x-2 flex-1">
              <Calendar className="w-5 h-5 text-gray-400" />
              <input
                type="date"
                value={virtualSessionDate}
                onChange={(e) => setVirtualSessionDate(e.target.value)}
                className="flex-1 p-2 text-sm border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              />
            </div>
            <div className="flex items-center space-x-2 flex-1">
              <Clock className="w-5 h-5 text-gray-400" />
              <input
                type="time"
                value={virtualSessionTime}
                onChange={(e) => setVirtualSessionTime(e.target.value)}
                className="flex-1 p-2 text-sm border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              />
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <input
              type="number"
              placeholder="Week Number"
              value={weekNumber}
              onChange={(e) => setWeekNumber(Number(e.target.value))}
              min={1}
              max={currentWeek}
              className="w-full p-2 text-sm border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            />
          </div>
          <button
            className="w-full px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 flex items-center justify-center"
            onClick={handleScheduleSession}
            disabled={isVirtualSessionLoading}
          >
            {isVirtualSessionLoading ? <LoadingSpinner /> : 'Schedule Virtual Session'}
          </button>
        </div>
      )
    case 'discussion':
      return (
        <div className="space-y-4 bg-white rounded-lg shadow-md p-4">
          <input
            type="text"
            placeholder="Discussion Title"
            value={discussionTitle}
            onChange={(e) => setDiscussionTitle(e.target.value)}
            className="w-full p-2 text-sm border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
          />
          <div className="flex items-center space-x-2">
            <input
              type="number"
              placeholder="Week Number"
              value={weekNumber}
              onChange={(e) => setWeekNumber(Number(e.target.value))}
              min={1}
              max={currentWeek}
              className="w-full p-2 text-sm border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            />
          </div>
          <button 
            onClick={() => openDiscussionModal(discussionTitle)}
            className="w-full px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            Create Discussion
          </button>
        </div>
      )
    default:
      return null
  }
}

