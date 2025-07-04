'use client'

import React, { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { User, Mail, Briefcase, GraduationCap, Globe, Phone, Calendar, ChevronDown } from 'lucide-react'
import Navbar from './landingPageComponents/navbar.tsx'

const BasicProfileForm: React.FC = () => {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    dateOfBirth: '',
    highestEducation: '',
    workExperience: '',
    currentRole: '',
    desiredProgram: '',
    englishProficiency: '',
  })

  const [errors, setErrors] = useState<{ [key: string]: string }>({})

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData(prevData => ({
      ...prevData,
      [name]: value
    }))
    if (errors[name]) {
      setErrors(prevErrors => ({
        ...prevErrors,
        [name]: ''
      }))
    }
  }

  const validateForm = () => {
    const newErrors: { [key: string]: string } = {}
    if (!formData.firstName.trim()) newErrors.firstName = 'First name is required'
    if (!formData.lastName.trim()) newErrors.lastName = 'Last name is required'
    if (!formData.email.trim()) newErrors.email = 'Email is required'
    else if (!/\S+@\S+\.\S+/.test(formData.email)) newErrors.email = 'Email is invalid'
    if (!formData.phone.trim()) newErrors.phone = 'Phone number is required'
    if (!formData.dateOfBirth) newErrors.dateOfBirth = 'Date of birth is required'
    if (!formData.highestEducation) newErrors.highestEducation = 'Highest education is required'
    if (!formData.workExperience) newErrors.workExperience = 'Work experience is required'
    if (!formData.currentRole.trim()) newErrors.currentRole = 'Current role is required'
    if (!formData.desiredProgram) newErrors.desiredProgram = 'Desired program is required'
    if (!formData.englishProficiency) newErrors.englishProficiency = 'English proficiency is required'
    return newErrors
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    const formErrors = validateForm()
    if (Object.keys(formErrors).length > 0) {
      setErrors(formErrors)
    } else {
      console.log('Form submitted:', formData)
      alert('Application submitted successfully! We will contact you soon.')
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
          The First Step towards Career Reskilling
        </motion.h1>
        <motion.p 
          className="text-xl text-center text-gray-600 mb-12 max-w-3xl mx-auto leading-relaxed"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          Take the first step towards your dream career in tech. Fill out this quick form and let's explore how we can help you achieve your goals.
        </motion.p>

        <motion.form
          onSubmit={handleSubmit}
          className="bg-white rounded-2xl p-8 shadow-lg border border-gray-200 max-w-4xl mx-auto"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
        >
          <div className="grid md:grid-cols-2 gap-8">
            <FormField
              label="First Name"
              name="firstName"
              type="text"
              value={formData.firstName}
              onChange={handleChange}
              error={errors.firstName}
              icon={<User size={18} />}
              placeholder="John"
            />
            <FormField
              label="Last Name"
              name="lastName"
              type="text"
              value={formData.lastName}
              onChange={handleChange}
              error={errors.lastName}
              icon={<User size={18} />}
              placeholder="Doe"
            />
            <FormField
              label="Email"
              name="email"
              type="email"
              value={formData.email}
              onChange={handleChange}
              error={errors.email}
              icon={<Mail size={18} />}
              placeholder="john.doe@example.com"
            />
            <FormField
              label="Phone"
              name="phone"
              type="tel"
              value={formData.phone}
              onChange={handleChange}
              error={errors.phone}
              icon={<Phone size={18} />}
              placeholder="+1 (555) 123-4567"
            />
            <FormField
              label="Date of Birth"
              name="dateOfBirth"
              type="date"
              value={formData.dateOfBirth}
              onChange={handleChange}
              error={errors.dateOfBirth}
              icon={<Calendar size={18} />}
            />
            <FormSelect
              label="Highest Education"
              name="highestEducation"
              value={formData.highestEducation}
              onChange={handleChange}
              error={errors.highestEducation}
              icon={<GraduationCap size={18} />}
              options={[
                { value: "", label: "Select education" },
                { value: "high_school", label: "High School" },
                { value: "bachelors", label: "Bachelor's Degree" },
                { value: "masters", label: "Master's Degree" },
                { value: "phd", label: "Ph.D." },
              ]}
            />
            <FormSelect
              label="Work Experience"
              name="workExperience"
              value={formData.workExperience}
              onChange={handleChange}
              error={errors.workExperience}
              icon={<Briefcase size={18} />}
              options={[
                { value: "", label: "Select experience" },
                { value: "0-2", label: "0-2 years" },
                { value: "3-5", label: "3-5 years" },
                { value: "6-10", label: "6-10 years" },
                { value: "10+", label: "10+ years" },
              ]}
            />
            <FormField
              label="Current Role"
              name="currentRole"
              type="text"
              value={formData.currentRole}
              onChange={handleChange}
              error={errors.currentRole}
              icon={<Briefcase size={18} />}
              placeholder="e.g. Software Developer"
            />
            <FormSelect
              label="Desired Program"
              name="desiredProgram"
              value={formData.desiredProgram}
              onChange={handleChange}
              error={errors.desiredProgram}
              icon={<GraduationCap size={18} />}
              options={[
                { value: "", label: "Select program" },
                { value: "web_development", label: "Web Development" },
                { value: "data_science", label: "Data Science" },
                { value: "cloud_computing", label: "Cloud Computing" },
                { value: "cybersecurity", label: "Cybersecurity" },
                { value: "ai_ml", label: "AI & Machine Learning" },
              ]}
            />
            <FormSelect
              label="English Proficiency"
              name="englishProficiency"
              value={formData.englishProficiency}
              onChange={handleChange}
              error={errors.englishProficiency}
              icon={<Globe size={18} />}
              options={[
                { value: "", label: "Select proficiency" },
                { value: "beginner", label: "Beginner" },
                { value: "intermediate", label: "Intermediate" },
                { value: "advanced", label: "Advanced" },
                { value: "native", label: "Native" },
              ]}
            />
          </div>
          <motion.button
            type="submit"
            className="mt-12 w-full px-8 py-4 bg-[#8b5cf6] text-white rounded-lg font-semibold text-lg hover:bg-[#7c3aed] transition-all duration-300 shadow-lg shadow-[#8b5cf6]/30 flex items-center justify-center space-x-2 group"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <span>Submit Application</span>
            <ChevronDown className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </motion.button>
        </motion.form>
      </div>
    </div>
  )
}

interface FormFieldProps {
  label: string
  name: string
  type: string
  value: string
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void
  error?: string
  icon: React.ReactNode
  placeholder?: string
}

const FormField: React.FC<FormFieldProps> = ({ label, name, type, value, onChange, error, icon, placeholder }) => (
  <div>
    <label htmlFor={name} className="block text-sm font-medium text-gray-600 mb-1">{label}</label>
    <div className="relative">
      <div className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400">
        {icon}
      </div>
      <input
        type={type}
        id={name}
        name={name}
        value={value}
        onChange={onChange}
        className="bg-gray-50 text-gray-800 rounded-md px-3 py-2 pl-10 w-full focus:outline-none focus:ring-2 focus:ring-[#8b5cf6] border border-gray-300"
        placeholder={placeholder}
      />
    </div>
    {error && <p className="text-red-500 text-xs mt-1">{error}</p>}
  </div>
)

interface FormSelectProps {
  label: string
  name: string
  value: string
  onChange: (e: React.ChangeEvent<HTMLSelectElement>) => void
  error?: string
  icon: React.ReactNode
  options: { value: string; label: string }[]
}

const FormSelect: React.FC<FormSelectProps> = ({ label, name, value, onChange, error, icon, options }) => (
  <div>
    <label htmlFor={name} className="block text-sm font-medium text-gray-600 mb-1">{label}</label>
    <div className="relative">
      <div className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400">
        {icon}
      </div>
      <select
        id={name}
        name={name}
        value={value}
        onChange={onChange}
        className="bg-gray-50 text-gray-800 rounded-md px-3 py-2 pl-10 pr-10 w-full focus:outline-none focus:ring-2 focus:ring-[#8b5cf6] border border-gray-300 appearance-none"
      >
        {options.map((option) => (
          <option key={option.value} value={option.value}>{option.label}</option>
        ))}
      </select>
      <div className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 pointer-events-none">
        <ChevronDown size={18} />
      </div>
    </div>
    {error && <p className="text-red-500 text-xs mt-1">{error}</p>}
  </div>
)

export default BasicProfileForm

