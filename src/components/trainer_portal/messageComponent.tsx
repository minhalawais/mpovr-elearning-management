import React, { useState } from 'react'
import { User, ShieldCheck, ExternalLink, Calendar, FileText, Video, Bell, MessageSquare, Reply, Paperclip, Download, Loader2 } from 'lucide-react'
import { format } from 'date-fns'

interface MessageProps {
  id: number
  type: string
  title?: string
  content?: string
  description?: string
  due_date?: string
  scheduled_datetime?: string
  created_at: string
  sender_id: string
  role: string
  link?: string
  week?: number
  replies?: MessageProps[]
  attachments?: string[]
  attachments_size?: number[]
}

interface MessageRendererProps {
  msg: MessageProps
  navigateToPage: (route: string) => void
  openContentModal: (id: number, type: 'quiz' | 'assignment' | 'content' | 'discussion') => void
  onReply: (parentId: number, content: string) => void
  baseApiUrl?: string
}

const TraineeAvatar = () => (
  <div className="w-10 h-10 rounded-full 
    bg-gradient-to-br from-[#f0e6ff] to-[#f5f3ff] 
    flex items-center justify-center 
    shadow-md border border-[#e0d7f9]/50">
    <User className="w-5 h-5 text-[#8b5cf6]/80" />
  </div>
)

const TrainerAvatar = () => (
  <div className="w-10 h-10 rounded-full 
    bg-gradient-to-br from-[#8b5cf6] to-[#a78bff] 
    flex items-center justify-center 
    shadow-md border border-[#7c3aed]/10">
    <ShieldCheck className="w-5 h-5 text-white/90" />
  </div>
)

const getFileIcon = (filename: string) => {
  const extension = filename.split('.').pop()?.toLowerCase()
  const iconClasses = "w-4 h-4"
  
  switch(extension) {
    case 'pdf':
      return <FileText className={iconClasses} />
    case 'mp4':
    case 'mov':
    case 'avi':
      return <Video className={iconClasses} />
    default:
      return <Paperclip className={iconClasses} />
  }
}

const getTypeIcon = (type: string, isTrainer: boolean) => {
  const iconClasses = "w-4 h-4 mr-2"
  const iconColor = isTrainer ? "text-white" : "text-[#8b5cf6]"

  switch (type) {
    case 'quiz': return <FileText className={`${iconClasses} ${iconColor}`} />
    case 'assignment': return <Calendar className={`${iconClasses} ${iconColor}`} />
    case 'content': return <ExternalLink className={`${iconClasses} ${iconColor}`} />
    case 'virtual_session': return <Video className={`${iconClasses} ${iconColor}`} />
    case 'discussion': return <MessageSquare className={`${iconClasses} ${iconColor}`} />
    default: return null
  }
}

const getTypeLabel = (type: string) => {
  switch (type) {
    case 'quiz': return 'New Quiz'
    case 'assignment': return 'New Assignment'
    case 'content': return 'New Content'
    case 'virtual_session': return 'New Virtual Session'
    case 'discussion': return 'New Discussion'
    default: return 'New Message'
  }
}

const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

export const MessageRenderer: React.FC<MessageRendererProps> = ({ 
  msg, 
  navigateToPage, 
  openContentModal, 
  onReply,
  baseApiUrl = 'http://127.0.0.1:8000'
}) => {
  const [isReplying, setIsReplying] = useState(false)
  const [replyContent, setReplyContent] = useState('')
  const [hoveredAttachment, setHoveredAttachment] = useState<number | null>(null)
  const [downloadingFile, setDownloadingFile] = useState<string | null>(null)
  const [downloadError, setDownloadError] = useState<string | null>(null)
  const isTrainer = msg.role === 'trainer'

  const baseClasses = `flex ${isTrainer ? 'flex-row-reverse' : 'flex-row'} items-start w-full`
  const messageClasses = `
    mx-2 relative overflow-hidden 
    ${isTrainer 
      ? 'bg-gradient-to-br from-[#8b5cf6] to-[#a78bff] text-white' 
      : 'bg-[#f9f5ff] border border-[#ede9fe]'
    } 
    rounded-2xl p-4 shadow-lg max-w-md w-[500px]`

  const formattedTime = msg.created_at 
    ? format(new Date(msg.created_at), 'h:mm a') 
    : ''

  const handleContentClick = () => {
    if (msg.type === 'quiz' || msg.type === 'assignment' || msg.type === 'content' || msg.type === 'discussion') {
      openContentModal(msg.id, msg.type)
    } else if (msg.type === 'virtual_session' && msg.link) {
      window.open(msg.link, '_blank')
    }
  }

  const handleReply = () => {
    if (replyContent.trim()) {
      onReply(msg.id, replyContent)
      setReplyContent('')
      setIsReplying(false)
    }
  }

  const handleDownload = async (attachment: string,filename: string) => {
    try {
      setDownloadingFile(filename)
      setDownloadError(null)

      if (!filename) {
        throw new Error('Filename is required')
      }

      const downloadUrl = `${baseApiUrl}/${attachment}`

      // Check if file exists
      const checkResponse = await fetch(downloadUrl, {
        method: 'HEAD',
        credentials: 'include',
      })

      if (!checkResponse.ok) {
        throw new Error(`File not found (${checkResponse.status})`)
      }

      // Get file size from headers
      const fileSize = checkResponse.headers.get('content-length')
      const maxSize = 100 * 1024 * 1024 // 100MB limit
      if (fileSize && parseInt(fileSize) > maxSize) {
        throw new Error('File size exceeds 100MB limit')
      }

      // Download file
      const response = await fetch(downloadUrl, {
        credentials: 'include',
      })

      if (!response.ok) {
        throw new Error(`Download failed (${response.status})`)
      }

      const contentDisposition = response.headers.get('content-disposition')
      const serverFilename = contentDisposition
        ? contentDisposition.split('filename=')[1]?.replace(/["']/g, '')
        : filename

      const blob = await response.blob()
      const objectUrl = window.URL.createObjectURL(blob)
      const downloadElement = document.createElement('a')
      
      downloadElement.href = objectUrl
      downloadElement.download = serverFilename || filename
      
      document.body.appendChild(downloadElement)
      downloadElement.click()
      
      // Cleanup
      document.body.removeChild(downloadElement)
      window.URL.revokeObjectURL(objectUrl)
      setDownloadingFile(null)
    } catch (error) {
      console.error('Download failed:', error)
      setDownloadError(error.message)
      setTimeout(() => setDownloadError(null), 5000) // Clear error after 5 seconds
    } finally {
      setDownloadingFile(null)
    }
  }

  const renderAttachments = () => {
    if (!msg.attachments || msg.attachments.length === 0) return null

    return (
      <div className="mt-4 space-y-2">
        <div className="text-xs font-medium mb-2 flex items-center">
          <Paperclip className="w-3 h-3 mr-1" />
          <span>{msg.attachments.length} Attachment{msg.attachments.length !== 1 ? 's' : ''}</span>
        </div>
        <div className="grid grid-cols-1 gap-2">
          {msg.attachments.map((attachment, index) => {
            const filename = attachment.split('/').pop() || ''
            const isHovered = hoveredAttachment === index
            const isDownloading = downloadingFile === filename
            const fileSize = msg.attachments_size && msg.attachments_size[index] ? formatFileSize(msg.attachments_size[index]) : 'Unknown size'

            return (
              <div
                key={index}
                onMouseEnter={() => setHoveredAttachment(index)}
                onMouseLeave={() => setHoveredAttachment(null)}
                className={`
                  relative group rounded-lg transition-all duration-200
                  ${isTrainer 
                    ? 'bg-white/10 hover:bg-white/20' 
                    : 'bg-white hover:bg-[#f5f3ff] border border-[#ede9fe]'
                  }
                  p-3
                `}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3 flex-grow min-w-0">
                    <div className={`
                      p-2 rounded-md
                      ${isTrainer 
                        ? 'bg-white/20' 
                        : 'bg-[#8b5cf6]/10'
                      }
                    `}>
                      {getFileIcon(filename)}
                    </div>
                    <div className="flex-grow min-w-0">
                      <p className={`
                        text-sm font-medium truncate
                        ${isTrainer ? 'text-white' : 'text-gray-700'}
                      `}>
                        {filename}
                      </p>
                      <p className={`
                        text-xs
                        ${isTrainer ? 'text-white/60' : 'text-gray-500'}
                      `}>
                        {fileSize}
                      </p>
                      {downloadError && downloadError.includes(filename) && (
                        <p className="text-xs text-red-500 mt-1">
                          {downloadError}
                        </p>
                      )}
                    </div>
                  </div>
                  
                  <button
                    onClick={() => handleDownload(attachment, filename)}
                    disabled={isDownloading}
                    className={`
                      p-2 rounded-md transition-all duration-200
                      ${isTrainer 
                        ? 'bg-white/20 hover:bg-white/30' 
                        : 'bg-[#8b5cf6]/10 hover:bg-[#8b5cf6]/20'
                      }
                      ${isDownloading ? 'opacity-50 cursor-not-allowed' : ''}
                    `}
                  >
                    {isDownloading ? (
                      <Loader2 className={`
                        w-4 h-4 animate-spin
                        ${isTrainer ? 'text-white' : 'text-[#8b5cf6]'}
                      `} />
                    ) : (
                      <Download className={`
                        w-4 h-4
                        ${isTrainer ? 'text-white' : 'text-[#8b5cf6]'}
                      `} />
                    )}
                  </button>
                </div>
                
                <div className={`
                  absolute bottom-0 left-0 w-full h-0.5 transition-all duration-200
                  ${isHovered 
                    ? isTrainer 
                      ? 'bg-white/30' 
                      : 'bg-[#8b5cf6]/30'
                    : 'bg-transparent'
                  }
                `} />
              </div>
            )
          })}
        </div>
      </div>
    )
  }

  const renderContent = () => {
    switch (msg.type) {
      case 'message':
        return (
          <>
            <p className="text-sm">{msg.content}</p>
            {renderAttachments()}
          </>
        )
      case 'quiz':
      case 'assignment':
      case 'content':
      case 'virtual_session':
      case 'discussion':
        return (
          <div className="mt-2">
            <div className="flex items-center mb-2">
              {getTypeIcon(msg.type, isTrainer)}
              <p className="text-sm font-semibold flex-grow">
                {getTypeLabel(msg.type)}: {msg.title}
              </p>
              {msg.week && (
                <span className={`text-xs px-2 py-1 rounded-full ${
                  isTrainer ? 'bg-white/20 text-white' : 'bg-[#8b5cf6]/10 text-[#8b5cf6]'
                }`}>
                  Week {msg.week}
                </span>
              )}
            </div>
            
            <p className="text-xs opacity-80 mb-2">{msg.description}</p>
            
            {msg.type === 'assignment' && msg.due_date && (
              <div className="flex items-center text-xs opacity-80 mb-2">
                <Calendar className={`w-3 h-3 mr-1 ${isTrainer ? 'text-white/70' : 'text-[#8b5cf6]/70'}`} />
                Due: {format(new Date(msg.due_date), 'MMM d, yyyy')}
              </div>
            )}
            
            {msg.type === 'virtual_session' && msg.scheduled_datetime && (
              <div className="flex items-center text-xs opacity-80 mb-2">
                <Calendar className={`w-3 h-3 mr-1 ${isTrainer ? 'text-white/70' : 'text-[#8b5cf6]/70'}`} />
                {format(new Date(msg.scheduled_datetime), 'MMM d, yyyy h:mm a')}
              </div>
            )}
            
            <button
              onClick={handleContentClick}
              className={`
                mt-2 text-xs font-medium rounded-md transition-all duration-300
                ${isTrainer 
                  ? 'bg-white/20 hover:bg-white/30 text-white' 
                  : 'bg-[#8b5cf6]/10 hover:bg-[#8b5cf6]/20 text-[#8b5cf6]'
                }
                px-3 py-1.5
              `}
            >
              {msg.type === 'virtual_session' ? 'Join Session' : `View ${msg.type.charAt(0).toUpperCase() + msg.type.slice(1)}`}
            </button>
            {renderAttachments()}
          </div>
        )
      default:
        return null
    }
  }

  return (
<div className={`flex ${isTrainer ? 'justify-end' : 'justify-start'} mb-6 w-full`}>
      <div className={`${baseClasses} w-full max-w-2xl`}>
        {isTrainer ? <TrainerAvatar /> : <TraineeAvatar />}
        <div className={messageClasses}>
          <div className="flex justify-between items-center mb-3">
            <span className="text-sm font-semibold">
              {isTrainer ? 'Trainer' : `Trainee ${msg.sender_name}`}
            </span>
            <span className="text-xs opacity-75">{formattedTime}</span>
          </div>
          {renderContent()}
          <div className="mt-2 flex justify-end">
            <button
              onClick={() => setIsReplying(!isReplying)}
              className={`
                text-xs font-medium rounded-md transition-all duration-300
                ${isTrainer 
                  ? 'bg-white/20 hover:bg-white/30 text-white' 
                  : 'bg-[#8b5cf6]/10 hover:bg-[#8b5cf6]/20 text-[#8b5cf6]'
                }
                px-2 py-1 flex items-center
              `}
            >
              <Reply className="w-3 h-3 mr-1" />
              Reply
            </button>
          </div>
          
          {isReplying && (
            <div className="mt-2">
              <textarea
                value={replyContent}
                onChange={(e) => setReplyContent(e.target.value)}
                className={`
                  w-full p-2 text-sm rounded-md resize-none
                  border border-gray-300 
                  focus:ring-2 focus:ring-[#8b5cf6] focus:border-transparent
                  placeholder-gray-400
                  ${isTrainer ? 'bg-white/90' : 'bg-white'}
                `}
                rows={3}
                placeholder="Type your reply..."
              />
              <div className="mt-2 flex justify-end space-x-2">
                <button
                  onClick={() => setIsReplying(false)}
                  className={`
                    px-3 py-1 text-sm font-medium rounded-md
                    transition-all duration-200
                    ${isTrainer
                      ? 'bg-white/20 hover:bg-white/30 text-white'
                      : 'bg-gray-100 hover:bg-gray-200 text-gray-600'
                    }
                  `}
                >
                  Cancel
                </button>
                <button
                  onClick={handleReply}
                  disabled={!replyContent.trim()}
                  className={`
                    px-3 py-1 text-sm font-medium text-white rounded-md
                    transition-all duration-200
                    ${replyContent.trim()
                      ? 'bg-[#8b5cf6] hover:bg-[#7c3aed]'
                      : 'bg-[#8b5cf6]/50 cursor-not-allowed'
                    }
                  `}
                >
                  Send Reply
                </button>
              </div>
            </div>
          )}

          {msg.replies && msg.replies.length > 0 && (
            <div className="mt-4 space-y-3">
              <div className="text-xs font-medium flex items-center">
                <MessageSquare className="w-3 h-3 mr-1" />
                <span>{msg.replies.length} Repl{msg.replies.length === 1 ? 'y' : 'ies'}</span>
              </div>
              <div className="space-y-2">
                {msg.replies.map((reply, index) => (
                  <div
                    key={reply.id}
                    className={`
                      p-3 rounded-lg text-sm
                      ${isTrainer
                        ? 'bg-white/10'
                        : 'bg-white border border-[#ede9fe]'
                      }
                    `}
                  >
                    <div className="flex justify-between items-center mb-1">
                      <span className="font-medium">
                        {reply.role === 'trainer' ? 'Trainer' : `Trainee ${reply.sender_id}`}
                      </span>
                      <span className="text-xs opacity-75">
                        {format(new Date(reply.created_at), 'h:mm a')}
                      </span>
                    </div>
                    <p className="text-sm">{reply.content}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

