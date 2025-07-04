'use client'

import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Mail, Phone, MapPin, Send } from 'lucide-react'
import Navbar from './landingPageComponents/navbar.tsx'

const ContactPage: React.FC = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    subject: '',
    message: ''
  })

  const [errors, setErrors] = useState<{ [key: string]: string }>({})

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setFormData(prevData => ({
      ...prevData,
      [name]: value
    }))
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prevErrors => ({
        ...prevErrors,
        [name]: ''
      }))
    }
  }

  const validateForm = () => {
    const newErrors: { [key: string]: string } = {}
    if (!formData.name.trim()) newErrors.name = 'Name is required'
    if (!formData.email.trim()) newErrors.email = 'Email is required'
    else if (!/\S+@\S+\.\S+/.test(formData.email)) newErrors.email = 'Email is invalid'
    if (!formData.subject.trim()) newErrors.subject = 'Subject is required'
    if (!formData.message.trim()) newErrors.message = 'Message is required'
    return newErrors
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    const formErrors = validateForm()
    if (Object.keys(formErrors).length > 0) {
      setErrors(formErrors)
    } else {
      // Here you would typically send the form data to your backend
      console.log('Form submitted:', formData)
      alert('Message sent successfully! We will get back to you soon.')
      // Reset form after successful submission
      setFormData({ name: '', email: '', subject: '', message: '' })
    }
  }
  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);
  return (
    <div className="min-h-screen bg-gradient-to-b from-[#edf6f9] to-white relative overflow-hidden">
      <div className="absolute top-0 left-0 right-0 h-96 bg-gradient-to-b from-[#8b5cf6]/10 to-transparent"></div>
      <Navbar />
      
      <div className="container mx-auto px-4 py-24 relative z-10">
        <motion.h1 
          className="text-4xl md:text-5xl font-bold text-center mb-4 text-gray-800"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          Get in <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#8b5cf6] to-[#6366f1] MontserratFont">Touch</span>
        </motion.h1>
        <motion.p 
          className="text-xl text-center text-gray-600 mb-12 max-w-3xl mx-auto leading-relaxed"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          Have questions about our programs or need more information? We're here to help!
        </motion.p>

        <div className="grid md:grid-cols-2 gap-8 max-w-6xl mx-auto">
          <motion.div
            className="bg-white rounded-2xl p-8 shadow-lg border border-gray-200"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
          >
            <h2 className="text-2xl font-bold mb-6 text-gray-800">Contact Information</h2>
            <div className="space-y-4">
              <div className="flex items-center">
                <Mail className="w-6 h-6 text-[#8b5cf6] mr-4" />
                <span className="text-gray-600">info@mpovr.com</span>
              </div>
              <div className="flex items-center">
                <Phone className="w-6 h-6 text-[#8b5cf6] mr-4" />
                <span className="text-gray-600">+1 (555) 123-4567</span>
              </div>
              <div className="flex items-center">
                <MapPin className="w-6 h-6 text-[#8b5cf6] mr-4" />
                <span className="text-gray-600">123 Tech Street, San Francisco, CA 94105</span>
              </div>
            </div>

            <h2 className="text-2xl font-bold mt-12 mb-6 text-gray-800">Our Location</h2>
            <div className="w-full h-64 bg-gray-100 rounded-lg overflow-hidden">
              {/* Replace this div with an actual map component */}
              <div className="w-full h-full flex items-center justify-center text-gray-400">
                Map Component Here
              </div>
            </div>
          </motion.div>

          <motion.div
            className="bg-white rounded-2xl p-8 shadow-lg border border-gray-200"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
          >
            <h2 className="text-2xl font-bold mb-6 text-gray-800">Send Us a Message</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label htmlFor="name" className="block text-sm font-medium text-gray-600 mb-1">Name</label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  className="bg-gray-50 text-gray-800 rounded-md px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-[#8b5cf6] border border-gray-300"
                  placeholder="Your Name"
                />
                {errors.name && <p className="text-red-500 text-xs mt-1">{errors.name}</p>}
              </div>
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-600 mb-1">Email</label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  className="bg-gray-50 text-gray-800 rounded-md px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-[#8b5cf6] border border-gray-300"
                  placeholder="your@email.com"
                />
                {errors.email && <p className="text-red-500 text-xs mt-1">{errors.email}</p>}
              </div>
              <div>
                <label htmlFor="subject" className="block text-sm font-medium text-gray-600 mb-1">Subject</label>
                <input
                  type="text"
                  id="subject"
                  name="subject"
                  value={formData.subject}
                  onChange={handleChange}
                  className="bg-gray-50 text-gray-800 rounded-md px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-[#8b5cf6] border border-gray-300"
                  placeholder="Message Subject"
                />
                {errors.subject && <p className="text-red-500 text-xs mt-1">{errors.subject}</p>}
              </div>
              <div>
                <label htmlFor="message" className="block text-sm font-medium text-gray-600 mb-1">Message</label>
                <textarea
                  id="message"
                  name="message"
                  value={formData.message}
                  onChange={handleChange}
                  rows={4}
                  className="bg-gray-50 text-gray-800 rounded-md px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-[#8b5cf6] border border-gray-300"
                  placeholder="Your message here..."
                ></textarea>
                {errors.message && <p className="text-red-500 text-xs mt-1">{errors.message}</p>}
              </div>
              <motion.button
                type="submit"
                className="w-full px-6 py-3 bg-[#8b5cf6] text-white rounded-lg font-semibold text-lg hover:bg-[#7c3aed] transition-all duration-300 shadow-lg shadow-[#8b5cf6]/30 flex items-center justify-center space-x-2 group"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <span>Send Message</span>
                <Send className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </motion.button>
            </form>
          </motion.div>
        </div>
      </div>
    </div>
  )
}

export default ContactPage

