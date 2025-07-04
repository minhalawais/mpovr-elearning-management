import React from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { ArrowDown } from 'lucide-react'

interface ScrollToBottomButtonProps {
  show: boolean
  onClick: () => void
}

export const ScrollToBottomButton: React.FC<ScrollToBottomButtonProps> = ({ show, onClick }) => {
  return (
    <AnimatePresence>
      {show && (
        <motion.button
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: 20 }}
          transition={{ duration: 0.2 }}
          onClick={onClick}
          className="fixed bottom-30 left-1/2 transform -translate-x-1/2 p-2 bg-indigo-600 text-white rounded-full shadow-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 z-10"        >
          <ArrowDown className="h-5 w-5" />
        </motion.button>
      )}
    </AnimatePresence>
  )
}

