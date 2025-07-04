import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { User, Mail, Phone, MapPin, Book, Briefcase, Calendar, Save, ArrowLeft, Plus, X, Loader2 } from 'lucide-react';
import Navbar from './navbar.tsx';

interface DegreeEntry {
  year: number;
  degree: string;
  institution: string;
}

interface JobEntry {
  years: string;
  company: string;
  position: string;
}

interface Profile {
  full_name: string;
  email: string;
  date_of_birth: string | null;
  phone_number: string | null;
  address: string | null;
  education_history: {
    degrees: DegreeEntry[];
  } | null;
  work_experience: {
    jobs: JobEntry[];
  } | null;
}

const EditProfile: React.FC = () => {
  const [profile, setProfile] = useState<Profile>({
    full_name: '',
    email: '',
    date_of_birth: null,
    phone_number: null,
    address: null,
    education_history: { degrees: [] },
    work_experience: { jobs: [] },
  });
  const [isSaving, setIsSaving] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await fetch('http://localhost:8000/profile', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          }
        });
        if (response.ok) {
          const data = await response.json();
          setProfile(data);
        }
      } catch (error) {
        console.error('Error fetching profile:', error);
      }
    };

    fetchProfile();
  }, []);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setProfile(prevProfile => ({
      ...prevProfile,
      [name]: value
    }));
  };

  const handleEducationChange = (index: number, field: keyof DegreeEntry, value: string) => {
    const newDegrees = [...(profile.education_history?.degrees || [])];
    newDegrees[index] = {
      ...newDegrees[index],
      [field]: field === 'year' ? parseInt(value) : value
    };
    setProfile(prev => ({
      ...prev,
      education_history: { degrees: newDegrees }
    }));
  };

  const handleWorkExperienceChange = (index: number, field: keyof JobEntry, value: string) => {
    const newJobs = [...(profile.work_experience?.jobs || [])];
    newJobs[index] = {
      ...newJobs[index],
      [field]: value
    };
    setProfile(prev => ({
      ...prev,
      work_experience: { jobs: newJobs }
    }));
  };

  const addEducation = () => {
    setProfile(prev => ({
      ...prev,
      education_history: {
        degrees: [...(prev.education_history?.degrees || []), { year: new Date().getFullYear(), degree: '', institution: '' }]
      }
    }));
  };

  const addWorkExperience = () => {
    setProfile(prev => ({
      ...prev,
      work_experience: {
        jobs: [...(prev.work_experience?.jobs || []), { years: '', position: '', company: '' }]
      }
    }));
  };

  const removeEducation = (index: number) => {
    setProfile(prev => ({
      ...prev,
      education_history: {
        degrees: prev.education_history?.degrees.filter((_, i) => i !== index) || []
      }
    }));
  };

  const removeWorkExperience = (index: number) => {
    setProfile(prev => ({
      ...prev,
      work_experience: {
        jobs: prev.work_experience?.jobs.filter((_, i) => i !== index) || []
      }
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSaving(true);
    try {
      const response = await fetch('http://localhost:8000/profile', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify(profile)
      });
      
      if (response.ok) {
        // Add a small delay to make the loading state visible
        await new Promise(resolve => setTimeout(resolve, 500));
        navigate('/profile');
      }
    } catch (error) {
      console.error('Error updating profile:', error);
      setIsSaving(false);
    }
  };

  const InputField = ({ 
    icon: Icon, 
    label, 
    name, 
    type = "text", 
    required = false 
  }: { 
    icon: React.ElementType, 
    label: string, 
    name: keyof Profile, 
    type?: string, 
    required?: boolean 
  }) => (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="mb-6"
    >
      <label htmlFor={name} className="block text-sm font-medium text-gray-600 mb-2">
        {label}
      </label>
      <div className="relative rounded-lg shadow-sm">
        <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
          <Icon className="h-5 w-5 text-purple-500" />
        </div>
        <input
          type={type}
          name={name}
          id={name}
          className="block w-full pl-12 pr-4 py-3 border-2 border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200 bg-white/50 backdrop-blur-sm"
          value={profile[name] || ''}
          onChange={handleInputChange}
          required={required}
          placeholder={`Enter your ${label.toLowerCase()}`}
          disabled={isSaving}
        />
      </div>
    </motion.div>
  );

  return (
    <>
      <Navbar />
      <div className="min-h-screen bg-gradient-to-b from-purple-50 to-white px-4 py-12 mt-10">
        <div className="max-w-3xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-2xl shadow-xl p-8 mb-8"
          >
            <div className="flex items-center justify-between mb-8">
              <div className="flex items-center space-x-4">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => navigate('/profile')}
                  className="p-2 rounded-full bg-purple-100 text-purple-600 hover:bg-purple-200 transition-colors"
                  disabled={isSaving}
                >
                  <ArrowLeft className="w-5 h-5" />
                </motion.button>
                <h1 className="text-3xl font-bold text-gray-800">Edit Profile</h1>
              </div>
            </div>

            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <InputField icon={User} label="Full Name" name="full_name" required />
                <InputField icon={Mail} label="Email" name="email" type="email" required />
                <InputField icon={Calendar} label="Date of Birth" name="date_of_birth" type="date" />
                <InputField icon={Phone} label="Phone Number" name="phone_number" type="tel" />
              </div>

              <InputField icon={MapPin} label="Address" name="address" />

              {/* Education History Section */}
              <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="space-y-4">
                <div className="flex items-center justify-between">
                  <label className="text-lg font-medium text-gray-700 flex items-center">
                    <Book className="h-5 w-5 text-purple-500 mr-2" />
                    Education History
                  </label>
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    type="button"
                    onClick={addEducation}
                    className="flex items-center space-x-2 px-4 py-2 rounded-lg bg-purple-100 text-purple-600 hover:bg-purple-200 transition-colors disabled:opacity-70 disabled:cursor-not-allowed"
                    disabled={isSaving}
                  >
                    <Plus className="w-4 h-4" />
                    <span>Add Education</span>
                  </motion.button>
                </div>
                
                {profile.education_history?.degrees.map((degree, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    className="bg-gray-50 p-4 rounded-lg relative"
                  >
                    <button
                      type="button"
                      onClick={() => removeEducation(index)}
                      className="absolute top-2 right-2 p-1 rounded-full hover:bg-gray-200 text-gray-500 disabled:opacity-70 disabled:cursor-not-allowed"
                      disabled={isSaving}
                    >
                      <X className="w-4 h-4" />
                    </button>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-600 mb-1">Year</label>
                        <input
                          type="number"
                          value={degree.year}
                          onChange={(e) => handleEducationChange(index, 'year', e.target.value)}
                          className="w-full p-2 border-2 border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent disabled:opacity-70 disabled:cursor-not-allowed"
                          disabled={isSaving}
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-600 mb-1">Degree</label>
                        <input
                          type="text"
                          value={degree.degree}
                          onChange={(e) => handleEducationChange(index, 'degree', e.target.value)}
                          className="w-full p-2 border-2 border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent disabled:opacity-70 disabled:cursor-not-allowed"
                          disabled={isSaving}
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-600 mb-1">Institution</label>
                        <input
                          type="text"
                          value={degree.institution}
                          onChange={(e) => handleEducationChange(index, 'institution', e.target.value)}
                          className="w-full p-2 border-2 border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent disabled:opacity-70 disabled:cursor-not-allowed"
                          disabled={isSaving}
                        />
                      </div>
                    </div>
                  </motion.div>
                ))}
              </motion.div>

              {/* Work Experience Section */}
              <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="space-y-4">
                <div className="flex items-center justify-between">
                  <label className="text-lg font-medium text-gray-700 flex items-center">
                    <Briefcase className="h-5 w-5 text-purple-500 mr-2" />
                    Work Experience
                  </label>
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    type="button"
                    onClick={addWorkExperience}
                    className="flex items-center space-x-2 px-4 py-2 rounded-lg bg-purple-100 text-purple-600 hover:bg-purple-200 transition-colors disabled:opacity-70 disabled:cursor-not-allowed"
                    disabled={isSaving}
                  >
                    <Plus className="w-4 h-4" />
                    <span>Add Experience</span>
                  </motion.button>
                </div>
                
                {profile.work_experience?.jobs.map((job, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    className="bg-gray-50 p-4 rounded-lg relative"
                  >
                    <button
                      type="button"
                      onClick={() => removeWorkExperience(index)}
                      className="absolute top-2 right-2 p-1 rounded-full hover:bg-gray-200 text-gray-500 disabled:opacity-70 disabled:cursor-not-allowed"
                      disabled={isSaving}
                    >
                      <X className="w-4 h-4" />
                    </button>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-600 mb-1">Years</label>
                        <input
                          type="text"
                          value={job.years}
                          onChange={(e) => handleWorkExperienceChange(index, 'years', e.target.value)}
                          placeholder="e.g., 2020-2024"
                          className="w-full p-2 border-2 border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent disabled:opacity-70 disabled:cursor-not-allowed"
                          disabled={isSaving}
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-600 mb-1">Company</label>
                        <input
                          type="text"
                          value={job.company}
                          onChange={(e) => handleWorkExperienceChange(index, 'company', e.target.value)}
                          className="w-full p-2 border-2 border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent disabled:opacity-70 disabled:cursor-not-allowed"
                          disabled={isSaving}
                        />
                      </div>
                    </div>
                  </motion.div>
                ))}
              </motion.div>

              <div className="flex justify-end space-x-4">
                <motion.button
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  type="button"
                  onClick={() => navigate('/profile')}
                  className="px-6 py-3 rounded-lg border-2 border-purple-500 text-purple-600 hover:bg-purple-50 transition-colors duration-300 disabled:opacity-70 disabled:cursor-not-allowed"
                  disabled={isSaving}
                >
                  Cancel
                </motion.button>
                <motion.button
                  whileHover={!isSaving ? { scale: 1.02 } : {}}
                  whileTap={!isSaving ? { scale: 0.98 } : {}}
                  type="submit"
                  disabled={isSaving}
                  className="px-6 py-3 rounded-lg bg-purple-600 text-white hover:bg-purple-700 transition-colors duration-300 flex items-center space-x-2 disabled:opacity-70 disabled:cursor-not-allowed"
                >
                  {isSaving ? (
                    <>
                      <Loader2 className="w-5 h-5 animate-spin" />
                      <span>Saving...</span>
                    </>
                  ) : (
                    <>
                      <Save className="w-5 h-5" />
                      <span>Save Changes</span>
                    </>
                  )}
                </motion.button>
              </div>
            </form>
          </motion.div>
        </div>
      </div>
    </>
  );
};

export default EditProfile;