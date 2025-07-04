import React from 'react'
import { HelpCircle, FileText, BookOpen, Video, PanelLeft, PanelRight, Calendar } from 'lucide-react'

interface UpcomingEvent {
  id: number
  title: string
  type: 'quiz' | 'assignment' | 'virtual_session'
  datetime: string
}

interface QuickAccessSectionProps {
  isQuickAccessOpen: boolean
  setIsQuickAccessOpen: (isOpen: boolean) => void
  navigateToPage: (route: string) => void
  upcomingEvents: UpcomingEvent[]
}

export const QuickAccessSection: React.FC<QuickAccessSectionProps> = ({ 
  isQuickAccessOpen, 
  setIsQuickAccessOpen, 
  navigateToPage,
  upcomingEvents
}) => (
  <div className={`
    bg-white shadow-2xl border-l border-purple-100
    transition-all duration-300 ease-in-out
    ${isQuickAccessOpen ? 'w-80' : 'w-0 overflow-hidden'}
    h-full relative
  `}>
    <div className="absolute left-0 top-1/2 transform -translate-y-1/2 -translate-x-full z-10">
      <button 
        onClick={() => setIsQuickAccessOpen(!isQuickAccessOpen)}
        className="
          bg-[#8b5cf6] text-white p-2.5 
          rounded-l-lg hover:bg-[#7c3aed] 
          transition-colors shadow-lg
          flex items-center justify-center
          focus:outline-none focus:ring-2 focus:ring-purple-300
        "
        aria-label={isQuickAccessOpen ? "Close Quick Access" : "Open Quick Access"}
      >
        {isQuickAccessOpen ? <PanelLeft className="h-5 w-5" /> : <PanelRight className="h-5 w-5" />}
      </button>
    </div>
    {isQuickAccessOpen && (
      <div className="p-6 space-y-6 overflow-y-auto h-full">
        <h3 className="text-2xl font-bold text-[#8b5cf6] tracking-tight">Quick Access</h3>
        
        <div className="grid grid-cols-2 gap-4">
          {[
            { icon: HelpCircle, color: 'purple', label: 'Quizzes', route: '/quizzes' },
            { icon: FileText, color: 'purple', label: 'Assignments', route: '/assignments' },
            { icon: BookOpen, color: 'purple', label: 'Content', route: '/content' },
            { icon: Video, color: 'purple', label: 'Virtual Sessions', route: '/virtual-sessions' }
          ].map(({ icon: Icon, color, label, route }) => (
            <div 
              key={label}
              onClick={() => navigateToPage(route)}
              className={`
                bg-[#ede9fe] hover:bg-purple-100
                p-4 rounded-2xl cursor-pointer 
                flex flex-col items-center space-y-2 
                transition-all duration-300 
                transform hover:-translate-y-1 
                shadow-md hover:shadow-xl group
              `}
            >
              <Icon className="h-7 w-7 text-[#8b5cf6] group-hover:scale-110 transition-transform" />
              <span className="text-sm font-medium text-[#8b5cf6]">{label}</span>
            </div>
          ))}
        </div>

        <div className="space-y-3 bg-[#ede9fe] p-4 rounded-xl">
          <div className="flex justify-between items-center">
            <h4 className="text-lg font-semibold text-[#8b5cf6]">Upcoming</h4>
            <button 
              className="text-[#8b5cf6] hover:text-purple-800 text-sm font-medium"
              onClick={() => navigateToPage('/schedule')}
            >
              View All
            </button>
          </div>
          <div className="space-y-3">
            {upcomingEvents.map((event) => (
              <div key={event.id} className="bg-white p-3.5 rounded-lg shadow-sm border border-purple-50">
                <div className="flex justify-between items-center">
                  <div>
                    <p className="text-sm font-semibold text-gray-800">{event.title}</p>
                    <p className="text-xs text-gray-500">{new Date(event.datetime).toLocaleString()}</p>
                  </div>
                  {event.type === 'virtual_session' && (
                    <button 
                      onClick={() => navigateToPage(`/virtual-sessions/${event.id}`)}
                      className="text-xs bg-[#8b5cf6] text-white px-2 py-1 rounded hover:bg-[#7c3aed] transition-colors"
                    >
                      Join
                    </button>
                  )}
                  {(event.type === 'quiz' || event.type === 'assignment') && (
                    <button 
                      onClick={() => navigateToPage(`/${event.type}s/${event.id}`)}
                      className="text-xs bg-[#8b5cf6] text-white px-2 py-1 rounded hover:bg-[#7c3aed] transition-colors"
                    >
                      View
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    )}
  </div>
)

