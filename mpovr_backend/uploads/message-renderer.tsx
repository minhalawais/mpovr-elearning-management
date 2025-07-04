import React from 'react'
import { User, ShieldCheck, ExternalLink } from 'lucide-react'
import { format } from 'date-fns';

interface MessageProps {
  id: number
  sender: string
  time: string
  content: string
  type: string
  quizTitle?: string
  quizLink?: string
  assignmentTitle?: string
  dueDate?: string
  contentTitle?: string
  contentLink?: string
  role?: string
  sender_name?: string
  created_at?: string
}

interface MessageRendererProps {
  msg: MessageProps
  navigateToPage: (route: string) => void
}

// Trainees Avatar with softer design
const TraineeAvatar = () => (
  <div className="w-12 h-12 rounded-full 
    bg-gradient-to-br from-[#ede9fe] to-[#f5f3ff] 
    flex items-center justify-center 
    shadow-md border border-[#e0d7f9]">
    <User className="w-6 h-6 text-[#8b5cf6]/70" />
  </div>
)

// Trainers Avatar with modern gradient
const TrainerAvatar = () => (
  <div className="w-12 h-12 rounded-full 
    bg-gradient-to-br from-[#8b5cf6] to-[#a78bff] 
    flex items-center justify-center 
    shadow-md border border-[#7c3aed]/20">
    <ShieldCheck className="w-6 h-6 text-white" />
  </div>
)

export const MessageRenderer: React.FC<MessageRendererProps> = ({ msg, navigateToPage }) => {
  const isTrainer = msg.role === 'Trainer'
  const baseClasses = `flex ${isTrainer ? 'flex-row-reverse' : 'flex-row'} items-start max-w-[70%]`
  const messageClasses = `
    mx-2 relative overflow-hidden 
    ${isTrainer 
      ? 'bg-gradient-to-br from-[#8b5cf6] to-[#a78bff] text-white' 
      : 'bg-white border border-[#ede9fe]'
    } 
    rounded-2xl p-4 shadow-lg`

  const formattedDate = msg.created_at 
    ? format(new Date(msg.created_at), 'PPpp') 
    : '';

  const renderAdditionalContent = () => {
    switch (msg.type) {
      case 'quiz':
        return (
          <div className={`
            mt-3 p-3 
            ${isTrainer 
              ? 'bg-white/10 border-white/10' 
              : 'bg-[#ede9fe]/50 border border-[#ede9fe]'
            } 
            rounded-xl flex items-center justify-between`}>
            <div>
              <p className={`
                text-sm mb-1 font-medium 
                ${isTrainer ? 'text-purple-100' : 'text-[#8b5cf6]'}
              `}>
                Quiz: {msg.quizTitle}
              </p>
            </div>
            <button
              onClick={() => navigateToPage(msg.quizLink!)}
              className={`
                text-sm flex items-center gap-1
                ${isTrainer 
                  ? 'text-white bg-white/20 hover:bg-white/30' 
                  : 'text-[#8b5cf6] bg-[#8b5cf6]/10 hover:bg-[#8b5cf6]/20'
                }
                px-3 py-1.5 rounded-lg 
                transition-colors duration-300
                focus:outline-none focus:ring-2 
                ${isTrainer ? 'focus:ring-white/30' : 'focus:ring-[#8b5cf6]/30'}
              `}
            >
              Take Quiz
              <ExternalLink className="w-4 h-4" />
            </button>
          </div>
        )
      case 'assignment':
        return (
          <div className={`
            mt-3 p-3 
            ${isTrainer 
              ? 'bg-white/10 border-white/10' 
              : 'bg-[#ede9fe]/50 border border-[#ede9fe]'
            } 
            rounded-xl`}>
            <p className={`
              text-sm mb-1 font-medium 
              ${isTrainer ? 'text-purple-100' : 'text-[#8b5cf6]'}
            `}>
              Assignment: {msg.assignmentTitle}
            </p>
            <p className={`
              text-xs 
              ${isTrainer ? 'text-white/80' : 'text-[#8b5cf6]/70'}
            `}>
              Due: {msg.dueDate}
            </p>
          </div>
        )
      case 'content':
        return (
          <div className={`
            mt-3 p-3 
            ${isTrainer 
              ? 'bg-white/10 border-white/10' 
              : 'bg-[#ede9fe]/50 border border-[#ede9fe]'
            } 
            rounded-xl flex items-center justify-between`}>
            <p className={`
              text-sm font-medium 
              ${isTrainer ? 'text-purple-100' : 'text-[#8b5cf6]'}
            `}>
              New Content: {msg.contentTitle}
            </p>
            <button
              onClick={() => navigateToPage(msg.contentLink!)}
              className={`
                text-sm flex items-center gap-1
                ${isTrainer 
                  ? 'text-white bg-white/20 hover:bg-white/30' 
                  : 'text-[#8b5cf6] bg-[#8b5cf6]/10 hover:bg-[#8b5cf6]/20'
                }
                px-3 py-1.5 rounded-lg 
                transition-colors duration-300
                focus:outline-none focus:ring-2 
                ${isTrainer ? 'focus:ring-white/30' : 'focus:ring-[#8b5cf6]/30'}
              `}
            >
              View Content
              <ExternalLink className="w-4 h-4" />
            </button>
          </div>
        )
      default:
        return null
    }
  }

  return (
    <div className={`flex ${isTrainer ? 'justify-end' : 'justify-start'} mb-4`}>
      <div className={baseClasses}>
        {isTrainer ? <TrainerAvatar /> : <TraineeAvatar />}
        <div className={messageClasses}>
          <div className="flex justify-between items-center mb-2 gap-2 flex-wrap">
            <span className={`
              font-bold flex-grow min-w-0 truncate
              ${isTrainer ? 'text-white/90' : 'text-[#8b5cf6]'}
            `}>
              {msg.sender_name}
            </span>
            <span className={`
              text-xs flex-shrink-0
              ${isTrainer ? 'text-white/60' : 'text-[#8b5cf6]/60'}
            `}>
              {formattedDate}
            </span>
          </div>
          <p className={`
            text-sm 
            ${isTrainer ? 'text-white' : 'text-[#8b5cf6]'}
            mb-2
          `}>
            {msg.content}
          </p>
          {renderAdditionalContent()}
        </div>
      </div>
    </div>
  )
}
