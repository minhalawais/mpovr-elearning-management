import React from 'react'
import { ChevronRight, Home, Users, BookOpen, Briefcase, HelpCircle, MessageSquare, FileText, Settings, Shield, Clock, CreditCard, UserCheck, Laptop, Award, Bell } from 'lucide-react'
import mpovrLogo from '../../../images/mpovr_logo.png'

interface SitemapItem {
  name: string
  path: string
  icon: React.ReactNode
  children?: SitemapItem[]
}

const sitemapData: SitemapItem[] = [
  { name: 'How it works', path: '/how-it-works', icon: <Home className="w-5 h-5" /> },
  { name: 'Programs', path: '/programs', icon: <BookOpen className="w-5 h-5" /> },
  { name: 'FAQs', path: '/faqs', icon: <HelpCircle className="w-5 h-5" /> },
  { name: 'Sign Up/Sign In', path: '/auth', icon: <UserCheck className="w-5 h-5" /> },
  {
    name: 'Programs',
    path: '/programs',
    icon: <BookOpen className="w-5 h-5" />,
    children: [
      {
        name: 'Workday',
        path: '/programs/workday',
        icon: <ChevronRight className="w-4 h-4" />,
        children: [
          { name: 'Workday – Security', path: '/programs/workday/security', icon: <ChevronRight className="w-4 h-4" /> },
          { name: 'Workday – Integrations', path: '/programs/workday/integrations', icon: <ChevronRight className="w-4 h-4" /> },
          { name: 'Workday – HCM', path: '/programs/workday/hcm', icon: <ChevronRight className="w-4 h-4" /> },
          { name: 'Workday – Finance', path: '/programs/workday/finance', icon: <ChevronRight className="w-4 h-4" /> },
          { name: 'Workday – SCM', path: '/programs/workday/scm', icon: <ChevronRight className="w-4 h-4" /> },
          { name: 'Workday – Analytics', path: '/programs/workday/analytics', icon: <ChevronRight className="w-4 h-4" /> },
        ],
      },
      { name: 'SAP', path: '/programs/sap', icon: <ChevronRight className="w-4 h-4" /> },
      { name: 'Oracle', path: '/programs/oracle', icon: <ChevronRight className="w-4 h-4" /> },
    ],
  },
  {
    name: 'Learner Portal',
    path: '/learner',
    icon: <Users className="w-5 h-5" />,
    children: [
      { name: 'Pre-Selection', path: '/learner/pre-selection', icon: <ChevronRight className="w-4 h-4" /> },
      { name: 'Basic Profile', path: '/learner/basic-profile', icon: <ChevronRight className="w-4 h-4" /> },
      { name: 'Status', path: '/learner/status', icon: <ChevronRight className="w-4 h-4" /> },
      { name: 'Schedule call', path: '/learner/schedule-call', icon: <ChevronRight className="w-4 h-4" /> },
      { name: 'Additional Details', path: '/learner/additional-details', icon: <ChevronRight className="w-4 h-4" /> },
      { name: 'Payment', path: '/learner/payment', icon: <ChevronRight className="w-4 h-4" /> },
      { name: 'Agreement', path: '/learner/agreement', icon: <ChevronRight className="w-4 h-4" /> },
      { name: 'Dashboard', path: '/learner/dashboard', icon: <ChevronRight className="w-4 h-4" /> },
      { name: 'Program', path: '/learner/program', icon: <ChevronRight className="w-4 h-4" /> },
      { name: 'Grades', path: '/learner/grades', icon: <ChevronRight className="w-4 h-4" /> },
      { name: 'Messages', path: '/learner/messages', icon: <ChevronRight className="w-4 h-4" /> },
      { name: 'Support', path: '/learner/support', icon: <ChevronRight className="w-4 h-4" /> },
      { name: 'Profile', path: '/learner/profile', icon: <ChevronRight className="w-4 h-4" /> },
    ],
  },
  {
    name: 'Trainer Portal',
    path: '/trainer',
    icon: <Laptop className="w-5 h-5" />,
    children: [
      { name: 'Dashboard', path: '/trainer/dashboard', icon: <ChevronRight className="w-4 h-4" /> },
      { name: 'Current Batches', path: '/trainer/batches', icon: <ChevronRight className="w-4 h-4" /> },
      { name: 'Manage Sessions', path: '/trainer/sessions', icon: <ChevronRight className="w-4 h-4" /> },
      { name: 'Assessment', path: '/trainer/assessment', icon: <ChevronRight className="w-4 h-4" /> },
      { name: 'Learner Reports', path: '/trainer/reports', icon: <ChevronRight className="w-4 h-4" /> },
      { name: 'Notifications', path: '/trainer/notifications', icon: <ChevronRight className="w-4 h-4" /> },
    ],
  },
  {
    name: 'Admin Portal',
    path: '/admin',
    icon: <Settings className="w-5 h-5" />,
    children: [
      { name: 'Dashboard', path: '/admin/dashboard', icon: <ChevronRight className="w-4 h-4" /> },
      { name: 'Content Management', path: '/admin/content', icon: <ChevronRight className="w-4 h-4" /> },
      { name: 'Admin Management', path: '/admin/manage', icon: <ChevronRight className="w-4 h-4" /> },
      { name: 'Learner Management', path: '/admin/learners', icon: <ChevronRight className="w-4 h-4" /> },
      { name: 'Trainer Management', path: '/admin/trainers', icon: <ChevronRight className="w-4 h-4" /> },
      { name: 'Communication Approval', path: '/admin/communication', icon: <ChevronRight className="w-4 h-4" /> },
      { name: 'Workflow Configuration', path: '/admin/workflow', icon: <ChevronRight className="w-4 h-4" /> },
      { name: 'Analytics & Reporting', path: '/admin/analytics', icon: <ChevronRight className="w-4 h-4" /> },
    ],
  },
  { name: 'Enrolment', path: '/enrolment', icon: <UserCheck className="w-5 h-5" /> },
  { name: 'Payment', path: '/payment', icon: <CreditCard className="w-5 h-5" /> },
  { name: 'Training Agreement', path: '/agreement', icon: <FileText className="w-5 h-5" /> },
  { name: 'Program Selection', path: '/program-selection', icon: <BookOpen className="w-5 h-5" /> },
  { name: 'Account', path: '/account', icon: <Users className="w-5 h-5" /> },
  { name: 'Profile', path: '/profile', icon: <Users className="w-5 h-5" /> },
  { name: 'Settings', path: '/settings', icon: <Settings className="w-5 h-5" /> },
  { name: 'Billing', path: '/billing', icon: <CreditCard className="w-5 h-5" /> },
  { name: 'Support', path: '/support', icon: <HelpCircle className="w-5 h-5" /> },
  { name: 'FAQs', path: '/faqs', icon: <HelpCircle className="w-5 h-5" /> },
  { name: 'Contact Us', path: '/contact', icon: <MessageSquare className="w-5 h-5" /> },
  { name: 'Technical Support', path: '/tech-support', icon: <HelpCircle className="w-5 h-5" /> },
  { name: 'Legal', path: '/legal', icon: <Shield className="w-5 h-5" /> },
  { name: 'Privacy Policy', path: '/privacy', icon: <Shield className="w-5 h-5" /> },
  { name: 'Terms of Service', path: '/terms', icon: <FileText className="w-5 h-5" /> },
]

const SitemapItem: React.FC<{ item: SitemapItem; level: number }> = ({ item, level }) => {
  return (
    <div className={`ml-${level * 4}`}>
      <div className="flex items-center space-x-2 py-2 px-3 rounded-md hover:bg-[#edf6f9] transition-colors">
        {item.icon}
        <a href={item.path} className="text-[#3756C0] hover:text-[#E18400] transition-colors">{item.name}</a>
      </div>
      {item.children && (
        <div className="ml-4">
          {item.children.map((child, index) => (
            <SitemapItem key={index} item={child} level={level + 1} />
          ))}
        </div>
      )}
    </div>
  )
}

const Sitemap: React.FC = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-[#edf6f9] to-white py-16 px-4 sm:px-6 lg:px-8">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-12">
          <img src={mpovrLogo} alt="MPOVR Logo" className="mx-auto w-32 mb-4" />
          <h1 className="text-4xl font-bold text-[#8b5cf6] mb-4">MPOVR Web Portal Sitemap</h1>
          <p className="text-xl text-gray-600">Navigate through our comprehensive ERP training platform</p>
        </div>
        <div className="bg-white rounded-lg shadow-xl p-6 md:p-8">
          {sitemapData.map((item, index) => (
            <SitemapItem key={index} item={item} level={0} />
          ))}
        </div>
        <div className="mt-12 text-center">
          <a 
            href="/" 
            className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-[#8b5cf6] hover:bg-[#E18400] transition-colors duration-300 ease-in-out"
          >
            Back to Home
            <ChevronRight className="ml-2 w-5 h-5" />
          </a>
        </div>
      </div>
    </div>
  )
}

export default Sitemap

